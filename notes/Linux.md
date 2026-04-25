# Linux
<!-- GFM-TOC -->
* [Linux](#linux)
    * [Preface](#preface)
    * [1. Common Operations and Concepts](#1-common-operations-and-concepts)
        * [Shortcuts](#shortcuts)
        * [Help](#help)
        * [Shutdown](#shutdown)
        * [PATH](#path)
        * [sudo](#sudo)
        * [Package Managers](#package-managers)
        * [Distributions](#distributions)
        * [VIM Three Modes](#vim-three-modes)
        * [GNU](#gnu)
        * [Open Source Licenses](#open-source-licenses)
    * [2. Disks](#2-disks)
        * [Disk Interfaces](#disk-interfaces)
        * [Disk File Names](#disk-file-names)
    * [3. Partitions](#3-partitions)
        * [Partition Table](#partition-table)
        * [Boot-Time Checker](#boot-time-checker)
    * [4. File Systems](#4-file-systems)
        * [Partitions and File Systems](#partitions-and-file-systems)
        * [Components](#components)
        * [File Reading](#file-reading)
        * [Disk Fragmentation](#disk-fragmentation)
        * [block](#block)
        * [inode](#inode)
        * [Directories](#directories)
        * [Logs](#logs)
        * [Mounting](#mounting)
        * [Directory Layout](#directory-layout)
    * [5. Files](#5-files)
        * [File Attributes](#file-attributes)
        * [Basic File and Directory Operations](#basic-file-and-directory-operations)
        * [Modify Permissions](#modify-permissions)
        * [Default Permissions](#default-permissions)
        * [Directory Permissions](#directory-permissions)
        * [Links](#links)
        * [Read File Contents](#read-file-contents)
        * [Command and File Search](#command-and-file-search)
    * [6. Compression and Archiving](#6-compression-and-archiving)
        * [Compressed File Names](#compressed-file-names)
        * [Compression Commands](#compression-commands)
        * [Archiving](#archiving)
    * [7. Bash](#7-bash)
        * [Features](#features)
        * [Variable Operations](#variable-operations)
        * [Command Search Order](#command-search-order)
        * [Data Stream Redirection](#data-stream-redirection)
    * [8. Pipeline Commands](#8-pipeline-commands)
        * [Extraction Commands](#extraction-commands)
        * [Sorting Commands](#sorting-commands)
        * [Bidirectional Output Redirection](#bidirectional-output-redirection)
        * [Character Conversion Commands](#character-conversion-commands)
        * [Partition Commands](#partition-commands)
    * [9. Regular Expressions](#9-regular-expressions)
        * [grep](#grep)
        * [printf](#printf)
        * [awk](#awk)
    * [10. Process Management](#10-process-management)
        * [View Processes](#view-processes)
        * [Process States](#process-states)
        * [SIGCHLD](#sigchld)
        * [wait()](#wait)
        * [waitpid()](#waitpid)
        * [Orphan Processes](#orphan-processes)
        * [Zombie Processes](#zombie-processes)
    * [References](#references)
<!-- GFM-TOC -->


## Preface

To make the material easier to follow, this article starts with common operations and concepts. Although the content has been simplified as much as possible, it still covers quite a lot. In interviews, Linux knowledge is usually less important than topics such as networking and operating systems, so focus on the key principles and commands. The most important points are:

- Be able to use commands such as cat, grep, and cut for basic operations;
- File-system principles, concepts such as inode and block, and data recovery;
- Hard links and symbolic links;
- Process management, including zombie processes, orphan processes, and SIGCHLD.

## 1. Common Operations and Concepts

### Shortcuts

- Tab: complete command and file names;
- Ctrl+C: interrupt the running program;
- Ctrl+D: end keyboard input (End Of File, EOF).

### Help

#### 1. --help

Shows the basic usage and options for a command.

#### 2. man

man is short for manual. It displays detailed information about a command.

When running `man date`, DATE(1) appears. The number indicates the command type. Common numbers and their meanings are:

| Code | Type |
| :--: | -- |
| 1 | Commands or executable files that users can run in the shell |
| 5 | Configuration files |
| 8 | Administrative commands for system administrators |

#### 3. info

info is similar to man, but it divides documentation into pages and supports navigation between them.

#### 4. doc

/usr/share/doc stores the full documentation set for installed software.

### Shutdown

#### 1. who

Before shutting down, use the who command to check whether other users are online.

#### 2. sync

To speed up disk reads and writes, file data in memory is not synchronized to disk immediately. Therefore, run sync before shutting down.

#### 3. shutdown

```html
## shutdown [-krhc] time [message]
-k: do not shut down; only send a warning message to all online users
-r: stop system services and then reboot
-h: stop system services and then shut down immediately
-c: cancel an in-progress shutdown
```

### PATH

Executable file paths can be declared in the PATH environment variable, separated by colons.

```html
/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/home/dmtsai/.local/bin:/home/dmtsai/bin
```

### sudo

sudo allows regular users to run commands that require root privileges, but only users listed in /etc/sudoers can use it.

### Package Managers

RPM and DPKG are the two most common package management systems:

- RPM stands for Redhat Package Manager. It was first developed and implemented by Red Hat, then adopted by GNU open-source operating systems and became a standard software package format for many Linux systems. YUM is based on RPM and provides dependency management and software upgrade features.
- DPKG is the DEB package management system used by Debian-based operating systems. Its full name is Debian Package, and its functionality is similar to RPM.

### Distributions

A Linux distribution is an integrated release of the Linux kernel and various applications.

| Package Manager | Commercial Distribution | Community Distribution |
| :--: | :--: | :--: |
| RPM | Red Hat | Fedora / CentOS |
| DPKG | Ubuntu | Debian |

### VIM Three Modes

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/image-20191209002818626.png"/> </div><br>



- Command mode: VIM's default mode, used to move the cursor and view content;
- Insert mode: entered after pressing keys such as "i"; used to edit text;
- Bottom-line mode: entered after pressing ":"; used for operations such as saving and quitting.

In bottom-line mode, the following commands are used to leave or save a file.

| Command | Action |
| :--: | :--: |
| :w | Write to disk |
| :w! | Force a write to disk when the file is read-only. Whether the write succeeds depends on the user's permissions for the file |
| :q | Quit |
| :q! | Force quit without saving |
| :wq | Write to disk and quit |
| :wq!| Force write to disk and quit |

### GNU

The GNU Project aims to create a completely free operating system called GNU, with its software released under the GPL. GPL stands for GNU General Public License and includes the following freedoms:

- The freedom to run the program for any purpose;
- The freedom to redistribute copies;
- The freedom to improve the program and publicly release those improvements.

### Open Source Licenses

- [Choose an open source license](https://choosealicense.com/)
- [How to choose an open-source license?](http://www.ruanyifeng.com/blog/2011/05/how_to_choose_free_software_licenses.html)

## 2. Disks

### Disk Interfaces

#### 1. IDE

IDE (ATA) stands for Advanced Technology Attachment. Its maximum interface speed is 133MB/s. Because parallel cables have poor interference resistance and take up considerable space inside a computer, which hurts cooling, IDE has gradually been replaced by SATA.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/924914c0-660c-4e4a-bbc0-1df1146e7516.jpg" width="400"/> </div><br>

#### 2. SATA

SATA stands for Serial ATA, an ATA interface that uses serial transmission. It has strong interference resistance, has much lower cable length requirements than ATA, and supports features such as hot swapping. SATA-II has an interface speed of 300MB/s, while the SATA-III standard can reach 600MB/s. SATA data cables are also much thinner than ATA cables, improving airflow inside the case and making cable management easier.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/f9f2a16b-4843-44d1-9759-c745772e9bcf.jpg" width=""/> </div><br>

#### 3. SCSI

SCSI stands for Small Computer System Interface. SCSI disks are widely used in workstations, personal computers, and servers, and often use more advanced technologies such as 15000rpm platters. They also use less CPU during data transfer, but they are more expensive than ATA and SATA disks of the same capacity.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/f0574025-c514-49f5-a591-6d6a71f271f7.jpg" width=""/> </div><br>

#### 4. SAS

SAS (Serial Attached SCSI) is a newer generation of SCSI technology. Like SATA disks, it uses serial technology to achieve higher transfer speeds, up to 6Gb/s. It also improves internal system space by reducing cable size.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/6729baa0-57d7-4817-b3aa-518cbccf824c.jpg" width=""/> </div><br>

### Disk File Names

In Linux, every hardware device is treated as a file, including disks. Disks are named according to their interface type. Common disk file names are:

- IDE disks: /dev/hd[a-d]
- SATA/SCSI/SAS disks: /dev/sd[a-p]

The number after the file name depends on the order in which the system detects the disks, not on the slot into which the disk is inserted.

## 3. Partitions

### Partition Table

Disk partition tables mainly have two formats: the older, more limited MBR partition table and the newer, less restrictive GPT partition table.

#### 1. MBR

In MBR, the first sector is the most important. It contains the master boot record (MBR) and the partition table. The master boot record occupies 446 bytes, and the partition table occupies 64 bytes.

The partition table is only 64 bytes, so it can store at most 4 partitions. These 4 partitions can be primary partitions or extended partitions. There can be only one extended partition. It uses other sectors to record additional partition tables, so more partitions can be created through the extended partition. These are called logical partitions.

Linux also treats partitions as files. Partition files are named as disk file name + number, such as /dev/sda1. Note that logical partition numbers start from 5.

#### 2. GPT

Sectors are the smallest storage units on a disk. Older disks usually have 512-byte sectors, while newer disks support 4K sectors. To remain compatible with all disks, GPT defines sectors using Logical Block Addressing (LBA), whose default size is 512 bytes.

The first GPT block records the master boot record (MBR), followed by 33 blocks that record partition information. The last 33 blocks are used to back up partition information. The first of these 33 blocks is the GPT header, which records the position and size of the partition table itself and the position of the backup partition. It also stores the partition table checksum (CRC32), which the operating system can use to verify whether GPT is correct. If an error occurs, the backup partition information can be used for recovery.

GPT has no concept of extended partitions; all partitions are primary partitions. Each LBA can describe 4 partitions, so GPT can define 4 * 32 = 128 partitions in total.

MBR does not support disks larger than 2.2 TB, while GPT supports up to 2<sup>33</sup> TB = 8 ZB.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/GUID_Partition_Table_Scheme.svg.png" width="400"/> </div><br>

### Boot-Time Checker

#### 1. BIOS

BIOS (Basic Input/Output System) is firmware, which is software embedded in hardware. The BIOS program is stored in read-only memory whose contents are not lost after power is removed.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/50831a6f-2777-46ea-a571-29f23c85cc21.jpg"/> </div><br>

BIOS is the first program a computer runs at startup. It knows which disks are bootable and reads the master boot record (MBR) in the first sector of the disk. The MBR then executes the boot loader inside it, and the boot loader loads the operating system's kernel files.

The boot loader in the MBR provides these functions: menu selection, kernel loading, and handoff to another boot loader. The handoff feature can implement multi-boot. Install another operating system's boot loader in the boot sector of another partition, and at startup the menu can either boot the current operating system or hand off to another boot loader to start another operating system.

In the following figure, the boot loader in the MBR of the first sector provides two menu entries: M1 and M2. M1 points to Windows, while M2 points to the boot sector of another partition, which contains another boot loader and provides a menu entry pointing to Linux.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/f900f266-a323-42b2-bc43-218fdb8811a8.jpg" width="600"/> </div><br>

When installing multi-boot, it is best to install Windows first and then Linux. Windows installation overwrites the MBR, while Linux can choose to install its boot loader in the MBR or in the boot sector of another partition, and it can configure the boot loader menu.

#### 2. UEFI

BIOS cannot read GPT partition tables, but UEFI can.

## 4. File Systems

### Partitions and File Systems

Formatting a partition creates a file system on it. A partition is usually formatted with only one file system, but technologies such as disk arrays can make one partition contain multiple file systems.

### Components

The main components are:

- inode: each file occupies one inode, which records the file's attributes and the block numbers where its contents are stored;
- block: stores file contents. Large files occupy multiple blocks.

Other components include:

- superblock: records overall file-system information, including the total, used, and remaining counts of inodes and blocks, as well as the file-system format and related information;
- block bitmap: records whether each block is in use.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/BSD_disk.png" width="800"/> </div><br>

### File Reading

In the Ext2 file system, when reading a file's contents, the system first finds all blocks containing the file's contents from the inode, then reads the contents of those blocks.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/12a65cc6-20e0-4706-9fe6-3ba49413d7f6.png" width="500px"> </div><br>

In the FAT file system, there are no inodes. Each block stores the number of the next block.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/5b718e86-7102-4bb6-8ca5-d1dd791530c5.png" width="500px"> </div><br>

### Disk Fragmentation

Disk fragmentation means the blocks containing a file are too scattered, causing the disk head to move too far and reducing disk read/write performance.

### block

The Ext2 file system supports block sizes of 1K, 2K, and 4K. Different block sizes limit the maximum size of a single file and of the file system.

| Size | 1KB | 2KB | 4KB |
| :---: | :---: | :---: | :---: |
| Maximum single file | 16GB | 256GB | 2TB |
| Maximum file system | 2TB | 8TB | 16TB |

A block can be used by only one file, so any unused portion is wasted. Therefore, if many small files need to be stored, it is better to use a smaller block size.

### inode

An inode contains the following information:

- Permissions (read/write/execute);
- Owner and group;
- Size;
- Creation or status change time (ctime);
- Last access time (atime);
- Last modification time (mtime);
- Flags defining file characteristics, such as SetUID;
- Pointers to the file's actual contents.

Inodes have the following characteristics:

- Each inode has a fixed size of 128 bytes (newer ext4 and xfs can be configured to 256 bytes);
- Each file occupies only one inode.

The inode records the block numbers where file contents are stored, but each block is small, and a large file may easily require hundreds of thousands of blocks. Because an inode has limited space, it cannot directly reference that many block numbers. Therefore, indirect, double-indirect, and triple-indirect references are introduced. Indirect references let the inode point to reference blocks, which then record reference information.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/inode_with_signatures.jpg" width="600"/> </div><br>

### Directories

When a directory is created, one inode and at least one block are allocated. The block records the inode numbers and file names of all files in the directory.

The file's inode itself does not record the file name; the file name is recorded in the directory. Therefore, operations such as adding files, deleting files, and renaming files depend on write permission for the directory.

### Logs

If power is suddenly lost, the file system may become inconsistent. For example, the block bitmap may have been modified before the data was actually written into the block.

The ext3/ext4 file systems introduce journaling, which can use logs to repair the file system.

### Mounting

Mounting uses a directory as the entry point to a file system. After entering that directory, the file-system data can be read.

### Directory Layout

To keep directory structures consistent across Linux distributions, the Filesystem Hierarchy Standard (FHS) defines the Linux directory layout. The three most basic directories are:

- / (root)
- /usr (unix software resource): all default system software is installed in this directory;
- /var (variable): stores data files generated while the system or programs are running.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/linux-filesystem.png" width=""/> </div><br>

## 5. Files

### File Attributes

Users are divided into three categories: file owner, group, and others. Different permissions can be assigned to each category.

When using ls to inspect a file, file information is displayed, such as `drwxr-xr-x 3 root root 17 May 6 00:14 .config`. This information means:

- drwxr-xr-x: file type and permissions. The first character is the file type, and the next 9 characters are the file permissions
- 3: link count
- root: file owner
- root: group
- 17: file size
- May 6 00:14: last modification time
- .config: file name

Common file types and their meanings:

- d: directory
- -: file
- l: link file

In the 9-character file permission field, every 3 characters form a group, for a total of 3 groups. The groups represent permissions for the file owner, group, and others. The 3 characters in each group are r, w, and x permissions, meaning readable, writable, and executable.

There are three file times:

- modification time (mtime): updated when file contents change;
- status time (ctime): updated when file status, such as permissions or attributes, changes;
- access time (atime): updated when the file is read.

### Basic File and Directory Operations

#### 1. ls

List information about files or directories. Directory information is the files contained in the directory.

```html
## ls [-aAdfFhilnrRSt] file|dir
-a: list all files
-d: list only the directory itself
-l: list in long format, including file attributes, permissions, and other data
```

#### 2. cd

Change the current directory.

```
cd [relative path or absolute path]
```

#### 3. mkdir

Create a directory.

```
## mkdir [-mp] directory_name
-m: configure directory permissions
-p: create directories recursively
```

#### 4. rmdir

Remove a directory. The directory must be empty.

```html
rmdir [-p] directory_name
-p: remove directories recursively
```

#### 5. touch

Update file times or create a new file.

```html
## touch [-acdmt] filename
-a: update atime
-c: update ctime; do not create a new file if it does not exist
-m: update mtime
-d: specify an update date instead of the current date; --date="date or time" can also be used
-t: specify an update time instead of the current time, in the format [YYYYMMDDhhmm]
```

#### 6. cp

Copy files. If there is more than one source file, the destination must be a directory.

```html
cp [-adfilprsu] source destination
-a: equivalent to -dr --preserve=all
-d: if the source file is a link file, copy the link file attributes instead of the file itself
-i: if the target file already exists, ask before overwriting it
-p: copy file attributes along with the file
-r: copy recursively
-u: update destination only when destination is older than source, or when destination does not exist
--preserve=all: in addition to the permission-related parameters of -p, also copy SELinux attributes, links, xattr, and so on
```

#### 7. rm

Remove files.

```html
## rm [-fir] file or directory
-r: remove recursively
```

#### 8. mv

Move files.

```html
## mv [-fiu] source destination
## mv [options] source1 source2 source3 .... directory
-f: force; if the target file already exists, overwrite it without asking
```

### Modify Permissions

A group of permissions can be represented with a number. The 3 permission bits are treated as bits in a binary number. From left to right, their weights are 4, 2, and 1, so the numeric values are r: 4, w: 2, and x: 1.

```html
## chmod [-R] xyz dirname/filename
```

Example: change the permissions of the .bashrc file to -rwxr-xr--.

```html
## chmod 754 .bashrc
```

Permissions can also be set using symbols.

```html
## chmod [ugoa]  [+-=] [rwx] dirname/filename
- u: owner
- g: group
- o: others
- a: all users
- +: add permission
- -: remove permission
- =: set permission
```

Example: add write permission for all users on the .bashrc file.

```html
## chmod a+w .bashrc
```

### Default Permissions

- Default file permissions: files do not have execute permission by default, so the default is 666, or -rw-rw-rw-.
- Default directory permissions: directories must be enterable, meaning they must have execute permission, so the default is 777, or drwxrwxrwx.

Default permissions can be set or viewed through umask, usually represented as a mask. For example, 002 means write permission (value 2) is removed from other users, so the default permissions for new files are -rw-rw-r--.

### Directory Permissions

File names are not stored inside file contents; they are stored in the directory containing the file. Therefore, having write permission on a file does not allow the file name to be modified.

A directory stores a file list, so directory permissions are permissions on that file list. The r permission on a directory means the file list can be read. The w permission means the file list can be modified, including adding files, deleting files, and renaming files. The x permission allows the directory to become the working directory. The x permission is the basis for r and w permissions; without the ability to make a directory the working directory, the file list cannot be read or modified.

### Links

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/1e46fd03-0cda-4d60-9b1c-0c256edaf6b2.png" width="450px"> </div><br>


```html
## ln [-sf] source_filename dist_filename
-s: the default is a hard link; add -s to create a symbolic link
-f: if the target file exists, remove it first
```

#### 1. Hard Links

Create an entry in the directory that records the file name and inode number. This inode is the source file's inode.

Deleting any one entry does not remove the file as long as the reference count is not 0.

Hard links have these restrictions: they cannot cross file systems, and they cannot link to directories.

```html
## ln /etc/crontab .
## ll -i /etc/crontab crontab
34474855 -rw-r--r--. 2 root root 451 Jun 10 2014 crontab
34474855 -rw-r--r--. 2 root root 451 Jun 10 2014 /etc/crontab
```

#### 2. Symbolic Links

A symbolic link file stores the absolute path of the source file. When it is read, it resolves to the source file. It can be understood like a Windows shortcut.

When the source file is deleted, the link file can no longer be opened.

Because a symbolic link records a path, symbolic links can be created for directories.

```html
## ll -i /etc/crontab /root/crontab2
34474855 -rw-r--r--. 2 root root 451 Jun 10 2014 /etc/crontab
53745909 lrwxrwxrwx. 1 root root 12 Jun 23 22:31 /root/crontab2 -> /etc/crontab
```

### Read File Contents

#### 1. cat

Get file contents.

```html
## cat [-AbEnTv] filename
-n: print line numbers, including for blank lines; -b does not number blank lines
```

#### 2. tac

tac is the reverse of cat. It prints starting from the last line.

#### 3. more

Unlike cat, more lets you view file contents one page at a time, making it more suitable for large files.

#### 4. less

less is similar to more, but it adds backward paging.

#### 5. head

Get the first few lines of a file.

```html
## head [-n number] filename
-n: followed by a number indicating how many lines to display
```

#### 6. tail

tail is the reverse of head. It gets the last few lines.

#### 7. od

Display binary files as characters or hexadecimal values.

### Command and File Search

#### 1. which

Search for commands.

```html
## which [-a] command
-a: list all matching commands instead of only the first one
```

#### 2. whereis

Search for files. It is faster because it searches only a few specific directories.

```html
## whereis [-bmsu] dirname/filename
```

#### 3. locate

Search for files using keywords or regular expressions.

locate searches using the /var/lib/mlocate/ database. The database is stored in memory and updated once per day, so locate cannot find newly created files. Use updatedb to update the database immediately.

```html
## locate [-ir] keyword
-r: regular expression
```

#### 4. find

Search for files using file attributes and permissions.

```html
## find [basedir] [option]
example: find . -name "shadow*"
```

**1. Time-related options**  

```html
-mtime  n: list files whose contents were modified exactly n days ago
-mtime +n: list files whose contents were modified more than n days ago, excluding day n itself
-mtime -n: list files whose contents were modified within n days, including day n itself
-newer file: list files newer than file
```

The time ranges indicated by +4, 4, and -4 are as follows:

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/658fc5e7-79c0-4247-9445-d69bf194c539.png" width=""/> </div><br>

**2. Options related to file owner and group**  

```html
-uid n
-gid n
-user name
-group name
-nouser: search for files whose owner does not exist in /etc/passwd
-nogroup: search for files whose group does not exist in /etc/group
```

**3. Options related to file permissions and names**  

```html
-name filename
-size [+-]SIZE: search for files larger (+) or smaller (-) than SIZE. SIZE units include c for bytes and k for 1024 bytes. To find files larger than 50KB, use -size +50k
-type TYPE
-perm mode: search for files whose permissions equal mode
-perm -mode: search for files whose permissions include mode
-perm /mode: search for files whose permissions include any bit in mode
```

## 6. Compression and Archiving

### Compressed File Names

Linux has many compressed file name extensions. Common ones are:

| Extension | Compression Program |
| -- | -- |
| \*.Z | compress |
|\*.zip |  zip |
|\*.gz  | gzip|
|\*.bz2 |  bzip2 |
|\*.xz  | xz |
|\*.tar |  Data archived by tar, without compression |
|\*.tar.gz | tar archive compressed with gzip |
|\*.tar.bz2 | tar archive compressed with bzip2 |
|\*.tar.xz | tar archive compressed with xz |

### Compression Commands

#### 1. gzip

gzip is the most widely used compression command on Linux. It can decompress files compressed with compress, zip, and gzip.

After gzip compression, the source file no longer exists.

There are 9 different compression levels.

zcat, zmore, and zless can be used to read compressed file contents.

```html
$ gzip [-cdtv#] filename
-c: output compressed data to the screen
-d: decompress
-t: check whether the compressed file has errors
-v: show information such as compression ratio
-#: # is a number indicating the compression level. Higher numbers mean higher compression ratios. The default is 6
```

#### 2. bzip2

Provides a higher compression ratio than gzip.

Viewing commands: bzcat, bzmore, bzless, and bzgrep.

```html
$ bzip2 [-cdkzv#] filename
-k: keep the source file
```

#### 3. xz

Provides a better compression ratio than bzip2.

gzip, bzip2, and xz provide progressively better compression ratios. Note that the higher the compression ratio, the longer compression takes.

Viewing commands: xzcat, xzmore, xzless, and xzgrep.

```html
$ xz [-dtlkc#] filename
```

### Archiving

Compression commands can compress only one file, while archiving packages multiple files into one large file. tar can be used not only for archiving but also with gzip, bzip2, or xz to compress the archive.

```html
$ tar [-z|-j|-J] [cv] [-f new tar file] filename...       ==archive and compress
$ tar [-z|-j|-J] [tv] [-f existing tar file]              ==view
$ tar [-z|-j|-J] [xv] [-f existing tar file] [-C dir]     ==extract
-z: use gzip;
-j: use bzip2;
-J: use xz;
-c: create a new archive;
-t: view which files are inside the archive;
-x: extract or decompress;
-v: show file names being processed during compression/extraction;
-f: filename: file to process;
-C dir: extract into a specific directory.
```

| Usage | Command |
| :---: | --- |
| Archive and compress | tar -jcv -f filename.tar.bz2 file-or-directory-to-compress |
| View | tar -jtv -f filename.tar.bz2 |
| Extract | tar -jxv -f filename.tar.bz2 -C target-directory |

## 7. Bash

You can request kernel services through a shell. Bash is one type of shell.

### Features

- Command history: records commands that have been used
- Command and file completion: shortcut key: tab
- Command aliases: for example, ll is an alias for ls -al
- shell scripts
- Wildcards: for example, ls -l /usr/bin/X\* lists all files under /usr/bin whose names start with X

### Variable Operations

Use = directly to assign a value to a variable.

To access a variable, add \$ before the variable name, or use the \${} form.

Use the echo command to output a variable.

```bash
$ x=abc
$ echo $x
$ echo ${x}
```

If the variable value contains spaces, use double quotes or single quotes.

- Special characters inside double quotes keep their original behavior. For example, if x="lang is \$LANG", then x is lang is zh_TW.UTF-8;
- Special characters inside single quotes are treated as literal characters. For example, if x='lang is \$LANG', then x is lang is \$LANG.

You can assign the result of a command to a variable using \`command\` or \$(command). For example, version=\$(uname -r) gives version the value 4.15.0-22-generic.

Use the export command to convert a custom variable into an environment variable. Environment variables can be used in child processes, which are child Bash processes created by the current Bash.

Bash variables can be declared as arrays or integers. Note that numeric types do not include floating-point numbers. If no declaration is made, the default type is string. Variables are declared with the declare command:

```html
$ declare [-aixr] variable
-a: define as an array
-i: define as an integer
-x: define as an environment variable
-r: define as readonly
```

Use [ ] to index an array:

```bash
$ array[1]=a
$ array[2]=b
$ echo ${array[1]}
```

### Command Search Order

- Execute the command using an absolute or relative path, such as /bin/ls or ./ls;
- Find and execute the command through an alias;
- Execute a Bash built-in command;
- Find and execute the first matching command in the search paths specified by the \$PATH variable.

### Data Stream Redirection

Redirection means using files in place of standard input, standard output, and standard error output.

| Stream | Code | Operator |
| :---: | :---: | :---:|
| Standard input (stdin)  | 0 | \< or \<\< |
| Standard output (stdout) | 1 | &gt; or \>\> |
| Standard error output (stderr) | 2 | 2\> or 2\>\> |

A single arrow redirects by overwriting, while a double arrow redirects by appending.

Unneeded standard output and standard error output can be redirected to /dev/null, which is like throwing them away.

To redirect both standard output and standard error output to one file, convert one output stream to the other. For example, 2\>&1 converts standard error output to standard output.

```bash
$ find /home -name .bashrc > list 2>&1
```

## 8. Pipeline Commands

A pipeline uses the standard output of one command as the standard input of another. Use pipelines when data must pass through multiple processing steps before producing the desired result.

Use | between commands to separate pipeline commands.

```bash
$ ls -al /etc | less
```

### Extraction Commands

cut splits data and extracts the desired part.

Splitting is performed line by line.

```html
$ cut
-d: delimiter
-f: after splitting with -d, use -f n to extract the nth field
-c: extract ranges by character
```

Example 1: last displays login information; extract the user names.

```html
$ last
root pts/1 192.168.201.101 Sat Feb 7 12:35 still logged in
root pts/1 192.168.201.101 Fri Feb 6 12:13 - 18:46 (06:33)
root pts/1 192.168.201.254 Thu Feb 5 22:37 - 23:53 (01:16)

$ last | cut -d ' ' -f 1
```

Example 2: from the output of export, extract all characters after the 12th character.

```html
$ export
declare -x HISTCONTROL="ignoredups"
declare -x HISTSIZE="1000"
declare -x HOME="/home/dmtsai"
declare -x HOSTNAME="study.centos.vbird"
.....(others omitted).....

$ export | cut -c 12-
```

### Sorting Commands

**sort**   is used for sorting.

```html
$ sort [-fbMnrtuk] [file or stdin]
-f: ignore case
-b: ignore leading spaces
-M: sort by month names, such as JAN and DEC
-n: sort numerically
-r: reverse sort
-u: equivalent to unique; duplicate content appears only once
-t: delimiter; default is tab
-k: specify the sort field
```

Example: /etc/passwd is separated by colons; sort by the third column.

```html
$ cat /etc/passwd | sort -t ':' -k 3
root:x:0:0:root:/root:/bin/bash
dmtsai:x:1000:1000:dmtsai:/home/dmtsai:/bin/bash
alex:x:1001:1002::/home/alex:/bin/bash
arod:x:1002:1003::/home/arod:/bin/bash
```

**uniq**   keeps only one copy of duplicate data.

```html
$ uniq [-ic]
-i: ignore case
-c: count occurrences
```

Example: get the total login count for each user.

```html
$ last | cut -d ' ' -f 1 | sort | uniq -c
1
6 (unknown
47 dmtsai
4 reboot
7 root
1 wtmp
```

### Bidirectional Output Redirection

Output redirection redirects output to a file, while   **tee**   not only does that but also keeps the output on the screen. In other words, with tee, one output is sent to both a file and the screen.

```html
$ tee [-a] file
```

### Character Conversion Commands

**tr**   deletes characters from a line or replaces characters.

```html
$ tr [-ds] SET1 ...
-d: delete the string SET1 from the line
```

Example: convert all lowercase letters in the output of last to uppercase.

```html
$ last | tr '[a-z]' '[A-Z]'
```

   **col**   converts tab characters to spaces.

```html
$ col [-xb]
-x: convert tabs to equivalent spaces
```

**expand**   converts tabs to a specified number of spaces. The default is 8.

```html
$ expand [-t] file
-t: number of spaces to convert each tab into
```

**join**   merges lines that have matching data.

```html
$ join [-ti12] file1 file2
-t: delimiter; default is space
-i: ignore case differences
-1: comparison field used by the first file
-2: comparison field used by the second file
```

**paste**   directly pastes two lines together.

```html
$ paste [-d] file1 file2
-d: delimiter; default is tab
```

### Partition Commands

**split**   splits one file into multiple files.

```html
$ split [-bl] file PREFIX
-b: split by size; units such as b, k, and m can be added
-l: split by line count
- PREFIX: prefix name for the split files
```

## 9. Regular Expressions

### grep

g/re/p (globally search a regular expression and print) globally searches using a regular expression and prints matching lines.

```html
$ grep [-acinv] [--color=auto] search_string filename
-c: count the number of matching lines
-i: ignore case
-n: output line numbers
-v: invert the match, showing lines that do not contain search_string
--color=auto: display matched keywords in color
```

Example: extract lines containing the string the. Note that --color=auto is enabled by default, so the string the is displayed in color on Linux.

```html
$ grep -n 'the' regular_express.txt
8:I can't finish the test.
12:the symbol '*' is represented as start.
15:You are the best is mean you are the no. 1.
16:The world Happy is the same with "glad".
18:google is the best tools for search keyword
```

Example: the regular expression a{m,n} matches the character a from m to n times. Here, { and } must be escaped because they have special meaning in the shell.

```html
$ grep -n 'a\{2,5\}' regular_express.txt
```

### printf

Used for formatted output. It is not a pipeline command, so data passed to printf should use the $( ) form.

```html
$ printf '%10s %5i %5i %5i %8.2f \n' $(cat printf.txt)
    DmTsai    80    60    92    77.33
     VBird    75    55    80    70.00
       Ken    60    90    70    73.33
```

### awk

awk was created by Alfred Aho, Peter Weinberger, and Brian Kernighan. Its name comes from the first letters of these three founders' names.

awk processes one line at a time. Its smallest processing unit is a field. Fields are named as \$n, where n is the field number starting from 1. \$0 represents the entire line.

Example: extract the user names and IP addresses of the last five logged-in users. First use last -n 5 to get all information about the last five logged-in users. The user name and IP address are in columns 1 and 3, so \$1 and \$3 can extract these two fields, and print can output them.

```html
$ last -n 5
dmtsai pts/0 192.168.1.100 Tue Jul 14 17:32 still logged in
dmtsai pts/0 192.168.1.100 Thu Jul 9 23:36 - 02:58 (03:22)
dmtsai pts/0 192.168.1.100 Thu Jul 9 17:23 - 23:36 (06:12)
dmtsai pts/0 192.168.1.100 Thu Jul 9 08:02 - 08:17 (00:14)
dmtsai tty1 Fri May 29 11:55 - 12:11 (00:15)
```

```html
$ last -n 5 | awk '{print $1 "\t" $3}'
dmtsai   192.168.1.100
dmtsai   192.168.1.100
dmtsai   192.168.1.100
dmtsai   192.168.1.100
dmtsai   Fri
```

Matching can be based on conditions on fields, such as matching rows where a field is smaller than a certain value.

```html
$ awk 'condition type 1 {action 1} condition type 2 {action 2} ...' filename
```

Example: the third field in /etc/passwd is UID. Process rows whose UID is less than 10.

```text
$ cat /etc/passwd | awk 'BEGIN {FS=":"} $3 < 10 {print $1 "\t " $3}'
root 0
bin 1
daemon 2
```

awk variables:

| Variable Name | Meaning |
| :--: | -- |
| NF | Total number of fields in each line |
| NR | Current line number being processed |
| FS | Current delimiter; default is space |

Example: display the line number being processed and the number of fields in each line.

```html
$ last -n 5 | awk '{print $1 "\t lines: " NR "\t columns: " NF}'
dmtsai lines: 1 columns: 10
dmtsai lines: 2 columns: 10
dmtsai lines: 3 columns: 10
dmtsai lines: 4 columns: 10
dmtsai lines: 5 columns: 9
```

## 10. Process Management

### View Processes

#### 1. ps

View process information at a specific point in time.

Example: view your own processes.

```sh
## ps -l
```

Example: view all system processes.

```sh
## ps aux
```

Example: view a specific process.

```sh
## ps aux | grep threadx
```

#### 2. pstree

View the process tree.

Example: view all process trees.

```sh
## pstree -A
```

#### 3. top

Display process information in real time.

Example: refresh every two seconds.

```sh
## top -d 2
```

#### 4. netstat

View the process occupying a port.

Example: view the process for a specific port.

```sh
## netstat -anp | grep port
```

### Process States

| State | Description |
| :---: | --- |
| R | running or runnable (on run queue)<br>The process is running or runnable and is currently in the run queue.|
| D | uninterruptible sleep (usually I/O)<br>Uninterruptible blocking, usually I/O blocking. |
| S | interruptible sleep (waiting for an event to complete) <br> Interruptible blocking; the process is waiting for an event to complete.|
| Z | zombie (terminated but not reaped by its parent)<br>Zombie; the process has terminated but its parent has not yet collected its information.|
| T | stopped (either by a job control signal or because it is being traced) <br> Stopped; the process can be stopped by a job-control signal or because it is being traced.|
<br>

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/2bab4127-3e7d-48cc-914e-436be859fb05.png" width="490px"/> </div><br>

### SIGCHLD

When a child process changes its state (stops, continues, or exits), two things happen in the parent process:

- It receives the SIGCHLD signal;
- A waitpid() or wait() call returns.

The SIGCHLD signal sent by the child process contains information about the child, such as process ID, process state, and CPU time used.

When a child process exits, its process descriptor is not released immediately. This allows the parent process to obtain information about the child through wait() and waitpid().

<div align="center"> <!-- <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/flow.png" width=""/> --> </div><br>

### wait()

```c
pid_t wait(int *status)
```

When the parent process calls wait(), it blocks until it receives a SIGCHLD signal indicating that a child process has exited. Then wait() destroys the child process and returns.

On success, it returns the process ID of the collected child process. If the calling process has no children, the call fails, returns -1, and sets errno to ECHILD.

The status parameter stores status information from the collected child process when it exits. If you do not care how the child died and only want to reap it, set this parameter to NULL.

### waitpid()

```c
pid_t waitpid(pid_t pid, int *status, int options)
```

It works exactly like wait(), but adds two user-controllable parameters: pid and options.

The pid parameter specifies a child process ID, meaning it cares only about the SIGCHLD signal from that child process. If pid=-1, it behaves like wait() and cares about SIGCHLD signals from all child processes.

The options parameter mainly includes WNOHANG and WUNTRACED. WNOHANG makes waitpid() non-blocking, meaning it returns immediately and the parent process can continue executing other tasks.

### Orphan Processes

If a parent process exits while one or more of its child processes are still running, those child processes become orphan processes.

Orphan processes are adopted by the init process (process ID 1), and init collects their status.

Because orphan processes are adopted by init, they do not harm the system.

### Zombie Processes

A child process's process descriptor is not released when the child exits. It is released only after the parent obtains the child process information through wait() or waitpid(). If the child exits but the parent does not call wait() or waitpid(), the child process descriptor remains in the system. Such a process is called a zombie process.

Zombie processes appear with state Z (zombie) in the ps command.

The system has a limited number of process IDs. If many zombie processes are created, the system may be unable to create new processes because no process IDs are available.

To eliminate a large number of zombie processes, kill their parent process. The zombie processes then become orphan processes and are adopted by init, which releases all resources occupied by the zombie processes and terminates them.

## References

- Bird Brother. Bird Brother's Linux Private Kitchen: Basic Edition, Third Edition[J]. 2009.
- [Package management on Linux](https://www.ibm.com/developerworks/cn/linux/l-cn-rpmdpkg/index.html)
- [Linux daemon processes, zombie processes, and orphan processes](http://liubigbin.github.io/2016/03/11/Linux-%E4%B9%8B%E5%AE%88%E6%8A%A4%E8%BF%9B%E7%A8%8B%E3%80%81%E5%83%B5%E6%AD%BB%E8%BF%9B%E7%A8%8B%E4%B8%8E%E5%AD%A4%E5%84%BF%E8%BF%9B%E7%A8%8B/)
- [What is the difference between a symbolic link and a hard link?](https://stackoverflow.com/questions/185899/what-is-the-difference-between-a-symbolic-link-and-a-hard-link)
- [Linux process states](https://idea.popcount.org/2012-12-11-linux-process-states/)
- [GUID Partition Table](https://en.wikipedia.org/wiki/GUID_Partition_Table)
- [Detailed explanation of wait and waitpid](https://blog.csdn.net/kevinhg/article/details/7001719)
- [Introduction to IDE, SATA, SCSI, SAS, FC, and SSD disk types](https://blog.csdn.net/tianlesoftware/article/details/6009110)
- [Akai IB-301S SCSI Interface for S2800,S3000](http://www.mpchunter.com/s3000/akai-ib-301s-scsi-interface-for-s2800s3000/)
- [Parallel ATA](https://en.wikipedia.org/wiki/Parallel_ATA)
- [ADATA XPG SX900 256GB SATA 3 SSD Review – Expanded Capacity and SandForce Driven Speed](http://www.thessdreview.com/our-reviews/adata-xpg-sx900-256gb-sata-3-ssd-review-expanded-capacity-and-sandforce-driven-speed/4/)
- [Decoding UCS Invicta – Part 1](https://blogs.cisco.com/datacenter/decoding-ucs-invicta-part-1)
- [Hard disk drive](https://zh.wikipedia.org/wiki/%E7%A1%AC%E7%9B%98)
- [Difference between SAS and SATA](http://www.differencebetween.info/difference-between-sas-and-sata)
- [BIOS](https://zh.wikipedia.org/wiki/BIOS)
- [File system design case studies](https://www.cs.rutgers.edu/\~pxk/416/notes/13-fs-studies.html)
- [Programming Project #4](https://classes.soe.ucsc.edu/cmps111/Fall08/proj4.shtml)
- [FILE SYSTEM DESIGN](http://web.cs.ucla.edu/classes/fall14/cs111/scribe/11a/index.html)
