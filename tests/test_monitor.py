from collections import namedtuple

import pytest

import monitor

def test_filesystem_usage(monkeypatch):
    """
    it invokes `shutils` to report correct filesystem usage
    """
    import shutil
    MockUsage = namedtuple('MockUsage', ['total', 'used','free'])
    monkeypatch.setattr(
            shutil,
            'disk_usage',
            lambda x: MockUsage(25000, 10000, 4000)
            )
    usage = monitor.filesystem_usage('/tmp')
    assert usage.total == 25000
    assert usage.used == 10000
    assert usage.free == 4000
    assert usage.percent_used == pytest.approx(0.4)

def test_disk_usage_per_directory():
    got = monitor.disk_usage_per_directory('tests/test-dir')
    expected = [
            monitor.DirectoryDiskUsage('tests/test-dir', 1, 10),
            monitor.DirectoryDiskUsage('tests/test-dir/test-dir2', 1, 10),
            monitor.DirectoryDiskUsage('tests/test-dir/test-dir3', 0, 0),
            ]


    for expected_item in expected:
        matches = list(filter(lambda x: x.name == expected_item.name, got))
        assert len(matches) == 1
        assert matches[0].file_count == expected_item.file_count
        assert matches[0].total_bytes == pytest.approx(expected_item.total_bytes)





