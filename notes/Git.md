# Git
<!-- GFM-TOC -->
* [Git](#git)
    * [Centralized and Distributed](#centralized-and-distributed)
    * [Central Server](#central-server)
    * [Workflow](#workflow)
    * [Branch Implementation](#branch-implementation)
    * [Conflicts](#conflicts)
    * [Fast forward](#fast-forward)
    * [Stashing](#stashing)
    * [SSH Transport Setup](#ssh-transport-setup)
    * [.gitignore File](#gitignore-file)
    * [Git Command Overview](#git-command-overview)
    * [References](#references)
<!-- GFM-TOC -->


## Centralized and Distributed

Git is a distributed version control system, while SVN is centralized.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/image-20191208200656794.png"/> </div><br>

In centralized version control, only the central server has a copy of the code. In distributed version control, everyone has a complete copy of the code on their own computer.

Centralized version control has reliability risks: if the central server goes down, no one can work.

Centralized version control requires a network connection. If the network is too slow, committing a file can become unbearably slow. Distributed version control can work without a network connection.

Distributed version control can create and merge branches very quickly, while in centralized version control creating a branch is equivalent to copying the entire codebase.

## Central Server

The central server is used to exchange each user's changes. Work can continue without it, but a central server can stay online 24 hours a day, making it more convenient to exchange changes.

GitHub is a central server.

## Workflow

After creating a new repository, the current directory becomes the working tree. It contains a hidden .git directory, which is Git's repository.

A Git repository has a staging area called Stage and the final History repository. History stores all branch information, and a HEAD pointer points to the current branch.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/image-20191208195941661.png"/> </div><br>

- git add files adds file changes to the staging area.
- git commit commits staged changes to the current branch; after the commit, the staging area is cleared.
- git reset -- files overwrites the staging area with changes from the current branch, undoing the most recent git add files.
- git checkout -- files overwrites the working directory with staged changes, undoing local modifications.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/image-20191208200014395.png"/> </div><br>

You can skip the staging area and check changes out directly from a branch, or commit changes directly to a branch.

- git commit -a directly stages all file modifications and commits them.
- git checkout HEAD -- files checks out the latest committed version and can be used for rollback.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/image-20191208200543923.png"/> </div><br>

## Branch Implementation

Pointers connect each commit into a timeline, and the HEAD pointer points to the current branch pointer.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/image-20191208203219927.png"/> </div><br>

Creating a new branch creates a new pointer to the last node in the timeline and makes HEAD point to the new branch, meaning the new branch becomes the current branch.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/image-20191208203142527.png"/> </div><br>

Each commit only moves the current branch pointer forward; other branch pointers do not move.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/image-20191208203112400.png"/> </div><br>

Merging branches also only requires changing pointers.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/image-20191208203010540.png"/> </div><br>

## Conflicts

When two branches both modify the same line in the same file, a conflict occurs during branch merge.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/image-20191208203034705.png"/> </div><br>

Git uses \<\<\<\<\<\<\<, =======, and \>\>\>\>\>\>\> to mark content from different branches. To resolve the conflict, edit the conflicting parts from the different branches so they become consistent.

```
<<<<<<< HEAD
Creating a new branch is quick & simple.
=======
Creating a new branch is quick AND simple.
>>>>>>> feature1
```

## Fast forward

A "fast-forward merge" directly moves the master branch to point to the merged branch. In this mode, branch information is lost, so the branch history no longer shows that branch information.

Use the --no-ff parameter during merge to disable Fast forward mode, and add the -m parameter to create a new commit during the merge.

```
$ git merge --no-ff -m "merge with no-ff" dev
```

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/image-20191208203639712.png"/> </div><br>

## Stashing

After working on one branch, if the changes have not been committed and you switch branches, the new changes can also be seen on the other branch. This is because all branches share the same working tree.

Use git stash to stash the current branch changes. At this point, all modifications in the current working tree are saved on a stack, meaning the working tree is clean and has no uncommitted changes. You can then safely switch to another branch.

```
$ git stash
Saved working directory and index state \ "WIP on master: 049d078 added the index file"
HEAD is now at 049d078 added the index file (To restore them type "git stash apply")
```

This feature can be used for bug-fix branches. If you are developing on the dev branch and a bug on master needs to be fixed, but the work on dev is not finished and should not be committed yet, use git stash to stash the uncommitted changes on dev before creating and switching to the bug branch.

## SSH Transport Setup

Transmission between a Git repository and the GitHub central repository is encrypted through SSH.

If there is no .ssh directory under the working tree, or if that directory does not contain id_rsa and id_rsa.pub, create an SSH Key with the following command:

```
$ ssh-keygen -t rsa -C "youremail@example.com"
```

Then copy the contents of the public key id_rsa.pub into SSH Keys under GitHub "Account settings".

## .gitignore File

Ignore the following files:

- Files automatically generated by the operating system, such as thumbnails;
- Intermediate files generated by compilation, such as .class files produced by Java compilation;
- Personal sensitive information, such as configuration files that store passwords.

You do not need to write everything yourself; you can search at [https://github.com/github/gitignore](https://github.com/github/gitignore).

## Git Command Overview

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/7a29acce-f243-4914-9f00-f2988c528412.jpg" width=""> </div><br>

A more detailed reference: http://www.cheat-sheets.org/saved-copy/git-cheat-sheet.pdf

## References

- [Git - The Simple Guide](http://rogerdudler.github.io/git-guide/index.zh.html)
- [A Visual Git Guide](http://marklodato.github.io/visual-git-guide/index-zh-cn.html)
- [Liao Xuefeng: Git Tutorial](https://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000)
- [Learn Git Branching](https://learngitbranching.js.org/)
