import os
import shutil
from collections import namedtuple
from functools import reduce

FileSystemUsage = namedtuple(
        'FileSystemUsage',
        ['total', 'used', 'free', 'percent_used']
        )

DirectoryDiskUsage = namedtuple(
        'DirectoryDiskUsage',
        ['name', 'file_count','total_bytes' ]
        )


Summary = namedtuple(
        'Summary',
        [
            'total_file_system',
            'total_file_system_used',
            'total_directory_space',
            'total_directory_files',
            'top_space_consumers',
            ]
        )

def summarize_usage(path):
    file_system = filesystem_usage(path)
    per_directory = disk_usage_per_directory(path)
    total_directory_space = reduce(lambda x, y: x + y.total_bytes, per_directory, 0)
    total_directory_files = reduce(lambda x, y: x + y.file_count, per_directory, 0)
    top_n_consumers = top_n_disk_space_consumers(per_directory, 20)
    return Summary(
            file_system.total,
            file_system.used,
            total_directory_space,
            total_directory_files,
            top_n_consumers
            )


def filesystem_usage(path):
    usage =  shutil.disk_usage(path)
    return FileSystemUsage(
            usage.total,
            usage.used,
            usage.free,
            usage.used / usage.total
            )

def disk_usage_per_directory(path):
    d = []
    for root, dirs, files in os.walk(path):
        total_bytes = sum(os.path.getsize(os.path.join(root, name)) for name in files)
        d.append(DirectoryDiskUsage(root, len(files), total_bytes ))
    return d

def top_n_percent_disk_space_consumers(directory_disk_usage, top_n_percent):
    n  = int(len(directory_disk_usage) * top_n_percent)
    return _first_n_items(directory_disk_usage, n)

def top_n_disk_space_consumers(directory_disk_usage, n):
    return _first_n_items(directory_disk_usage, n)

def _first_n_items(l, n):
    s = sorted(l, key=lambda x: x.total_bytes, reverse=True)
    return s[:n]

