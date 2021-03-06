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
    """
    it recursively traverses directories to report disk usage
    """
    got = monitor.disk_usage_per_directory('tests/test-dir')
    expected = [
            monitor.DirectoryDiskUsage('tests/test-dir', 1, 10),
            monitor.DirectoryDiskUsage('tests/test-dir/test-dir2', 1, 150),
            monitor.DirectoryDiskUsage('tests/test-dir/test-dir3', 0, 0),
            ]


    for expected_item in expected:
        matches = list(filter(lambda x: x.name == expected_item.name, got))
        assert len(matches) == 1
        assert matches[0].file_count == expected_item.file_count
        assert matches[0].total_bytes == pytest.approx(expected_item.total_bytes)

def test_top_n_percent_disk_space_consumers():
    """
    it returns the largest n percent of disk space consumers
    """
    directories = monitor.disk_usage_per_directory('tests/test-dir')
    got = monitor.top_n_percent_disk_space_consumers(directories, 0.5)
    assert len(got) == 1
    assert got[0].name == 'tests/test-dir/test-dir2'
    assert got[0].file_count == 1
    assert got[0].total_bytes == pytest.approx(150)

def test_top_n_disk_space_consumers():
    """
    it returns the largest n number of disk space consumers
    """
    directories = monitor.disk_usage_per_directory('tests/test-dir')
    expected = [
            monitor.DirectoryDiskUsage('tests/test-dir/test-dir2', 1, 150),
            monitor.DirectoryDiskUsage('tests/test-dir', 1, 10),
            ]
    got = monitor.top_n_disk_space_consumers(directories, 2)
    assert got == expected


def test_summarize_usage():
    """
    it summarizes directory usage correctly
    """
    summary = monitor.summarize_usage('tests/test-dir')
    assert summary.total_directory_space == '160 Bytes'
    assert summary.total_directory_files == 2
    assert summary.top_space_consumers == [
            monitor.DirectoryDiskUsage('tests/test-dir/test-dir2', 1, '150 Bytes'),
            monitor.DirectoryDiskUsage('tests/test-dir', 1, '10 Bytes'),
            ]

@pytest.mark.parametrize("bytes, expected", [
    (150, '150 Bytes'),
    (1024, '1.0 KB'),
    (102432454, '102.4 MB'),
    (102432454435, '102.4 GB'),
    (102432454437865, '102.4 TB'),
    ])
def test_humanize_bytes(bytes, expected):
    "it converts bytes to human readable units"
    got = monitor._humanize_bytes(bytes)
    assert got == expected




