import os
import shutil
from collections import namedtuple

FileSystemUsage = namedtuple(
        'FileSystemUsage',
        ['total', 'used', 'free', 'percent_used']
        )

DirectoryDiskUsage = namedtuple(
        'DirectoryDiskUsage',
        ['name', 'file_count','total_bytes' ]
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

