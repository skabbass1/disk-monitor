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






