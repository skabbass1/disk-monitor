import os
import shutil
from collections import namedtuple
from functools import reduce

from tabulate import tabulate

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
    top_n_consumers = [
            DirectoryDiskUsage(x.name, x.file_count, _humanize_bytes(x.total_bytes))
                for x in top_n_consumers
            ]
    return Summary(
            _humanize_bytes(file_system.total),
            _humanize_bytes(file_system.used),
            _humanize_bytes(total_directory_space),
            total_directory_files,
            top_n_consumers
            )

def tabulate_usage_summary(summary):
    summary_table = tabulate(
            [
                [
                    summary.total_file_system,
                    summary.total_file_system_used,
                    summary.total_directory_space,
                    summary.total_directory_files,
                ]
            ],
            headers=['File System Total', 'File System Used', 'Directory Space Used', 'Directory File Count']
            )
    top_n_consumers_rows = [[x.name, x.total_bytes, x.file_count] for x in summary.top_space_consumers]
    top_n_consumers_table = tabulate(top_n_consumers_rows, headers=['Directory Path', 'Directory Space Used', 'Directory File Count'])
    return summary_table, top_n_consumers_table

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
    s = list(filter(lambda x: x.total_bytes > 0, s))
    return s[:n]

def _humanize_bytes(b):
    base = 1e3
    bounds = [
        ('KB', 1e6),
        ('MB',1e9),
        ('GB',1e12),
        ('TB',1e15),
        ('PB',1e18),
        ('EB',1e21),
        ('ZB',1e24),
        ('YB',1e27),
    ]

    if b < 1e3:
        return f'{b} Bytes'

    for unit, bound in bounds:
        if b <= bound:
            return f'{b / (bound / base):.1f} {unit}'
    return f'{b} Bytes'

