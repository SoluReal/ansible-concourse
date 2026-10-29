"""Verifies concourse_binary_src replaces the archive's binary."""

import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


def test_local_binary_replaces_archive_binary(host):
    binary = host.file("/opt/concourse/bin/concourse")
    assert binary.exists
    assert binary.user == "concourse"
    assert binary.group == "concourse"
    assert oct(binary.mode) == "0o750"
    assert host.check_output("/opt/concourse/bin/concourse -v") == "0.0.0-dev"
