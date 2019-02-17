import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_directories(host):
    dirs = [
        "/etc/prometheus",
        "/etc/prometheus/conf.d",
        "/etc/prometheus/rules",
        "/etc/prometheus/file_sd",
        "/var/lib/prometheus/data",
        "/usr/lib/prometheus",
    ]
    files = [
        "/lib/systemd/system/prometheus.service",
        "/etc/prometheus/prometheus.yml"
    ]
    links = [
        "/usr/bin/prometheus",
        "/usr/bin/promtool",
        "/etc/prometheus/console_libraries",
        "/etc/prometheus/consoles"
    ]
    no_files = [
        "/usr/lib/prometheus/prometheus.yml"
    ]
    for directory in dirs:
        d = host.file(directory)
        assert d.exists
        assert d.is_directory
    for file in files:
        f = host.file(file)
        assert f.exists
        assert f.is_file
    for lnk in links:
        f = host.file(lnk)
        assert f.exists
        assert f.is_symlink
    for file in no_files:
        f = host.file(file)
        assert not f.exists


def test_service(host):
    s = host.service("prometheus")
    assert s.is_enabled
    assert s.is_running


def test_socket(host):
    assert host.socket("tcp://0.0.0.0:9000").is_listening
