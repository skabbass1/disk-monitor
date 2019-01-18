# Task Description

You are a software engineer at a company where employees make heavy use of a Network File Sytem(NFS) mount to share all sorts of  documents. The NFS mount has limited space available. Employees dont regularly cleanup old unused files. As a result, the filesystem often runs out of space causing a lot of issues for the business.

Your task is to write a file system  monitoring script. The purpose of this script is to watch a single  directory for space usage and alert (via email for example) when the available space within the associated file system goes below a specified threshold.

The  script should take in a directoy path as `input` and return a summary of the the total space available on the associated file system, the total space used in the associated file system and the total space consumed by the directory path given as input above. Additionally, your script should also provide information on the largest disk space consumers within the directory path provided above.

The script should be able to run standalone via the command line and should expose methods which can be exposed programatically from another application to request disk usage of a desired path on the file system

