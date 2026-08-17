"""Verifies the concourse role installs and configures web + worker correctly."""

import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


def test_concourse_user_and_group(host):
    group = host.group("concourse")
    assert group.exists
    assert group.gid == 14500

    user = host.user("concourse")
    assert user.exists
    assert user.uid == 14500
    assert user.gid == 14500
    assert user.shell == "/bin/false"


def test_concourse_binary_installed(host):
    binary = host.file("/opt/concourse/bin/concourse")
    assert binary.exists
    assert binary.user == "concourse"
    assert binary.group == "concourse"
    assert oct(binary.mode) == "0o750"


def test_etc_dir(host):
    etc_dir = host.file("/opt/concourse/etc")
    assert etc_dir.is_directory
    assert etc_dir.user == "concourse"
    assert etc_dir.group == "concourse"
    assert oct(etc_dir.mode) == "0o750"


def test_web_launcher_script(host):
    launcher = host.file("/opt/concourse/bin/concourse-web")
    assert launcher.exists
    assert launcher.user == "concourse"
    assert oct(launcher.mode) == "0o700"
    assert "concourse web" in launcher.content_string
    assert "--session-signing-key" in launcher.content_string
    assert "--tsa-authorized-keys" in launcher.content_string


def test_worker_launcher_script(host):
    launcher = host.file("/opt/concourse/bin/concourse-worker")
    assert launcher.exists
    assert launcher.user == "concourse"
    assert oct(launcher.mode) == "0o700"
    assert "concourse worker" in launcher.content_string
    assert '--tsa-host "127.0.0.1"' in launcher.content_string
    assert "--work-dir" in launcher.content_string


def test_worker_land_and_retire_scripts(host):
    for script in ("concourse-land-worker", "concourse-retire-worker"):
        f = host.file(f"/opt/concourse/bin/{script}")
        assert f.exists
        assert oct(f.mode) == "0o700"


def test_web_secret_files(host):
    for filename in (
        "host_key",
        "session_signing_key",
        "authorized_worker_keys",
    ):
        f = host.file(f"/opt/concourse/etc/{filename}")
        assert f.exists
        assert f.user == "concourse"
        assert oct(f.mode) == "0o400"


def test_worker_secret_files(host):
    for filename in ("host_key.pub", "worker_key"):
        f = host.file(f"/opt/concourse/etc/{filename}")
        assert f.exists
        assert f.user == "concourse"
        assert oct(f.mode) == "0o400"


def test_worker_work_dir(host):
    work_dir = host.file("/opt/concourse/work")
    assert work_dir.is_directory
    assert work_dir.user == "concourse"
    assert oct(work_dir.mode) == "0o750"
