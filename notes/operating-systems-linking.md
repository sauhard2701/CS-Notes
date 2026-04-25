# Operating Systems - Linking
<!-- GFM-TOC -->
* [Operating Systems - Linking](#operating-systems---linking)
    * [Compilation System](#compilation-system)
    * [Static Linking](#static-linking)
    * [Object Files](#object-files)
    * [Dynamic Linking](#dynamic-linking)
<!-- GFM-TOC -->


## Compilation System


The following is a `hello.c` program:

```c
#include <stdio.h>

int main()
{
    printf("hello, world\n");
    return 0;
}
```

On Unix systems, the compiler converts the source file into an object file.

```bash
gcc -o hello hello.c
```

The process is roughly as follows:

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/b396d726-b75f-4a32-89a2-03a7b6e19f6f.jpg" width="800"/> </div><br>

- Preprocessing phase: handles preprocessing directives that start with `#`.
- Compilation phase: translates the code into an assembly file.
- Assembly phase: translates the assembly file into a relocatable object file.
- Linking phase: combines relocatable object files with separately precompiled object files such as `printf.o` to produce the final executable object file.

## Static Linking

A static linker takes a set of relocatable object files as input and produces a fully linked executable object file as output. The linker mainly performs two tasks:

- Symbol resolution: each symbol corresponds to a function, global variable, or static variable. Symbol resolution associates each symbol reference with a symbol definition.
- Relocation: the linker associates each symbol definition with a memory location, then modifies all references to those symbols so they point to that memory location.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/47d98583-8bb0-45cc-812d-47eefa0a4a40.jpg"/> </div><br>

## Object Files

- Executable object file: can be executed directly in memory.
- Relocatable object file: can be combined with other relocatable object files during linking to create an executable object file.
- Shared object file: a special type of relocatable object file that can be dynamically loaded into memory and linked at runtime.

## Dynamic Linking

Static libraries have two problems:

- When a static library is updated, the entire program must be relinked.
- For standard library functions such as `printf`, including code in every program wastes a large amount of resources.

Shared libraries are designed to solve these two problems with static libraries. On Linux systems they usually use the `.so` suffix; on Windows systems they are called DLLs. They have the following characteristics:

- In a given file system, a library has only one file. All executable object files that reference the library share this file; it is not copied into the executables that reference it.
- In memory, one copy of a shared library's `.text` section, the compiled machine code, can be shared by different running processes.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/76dc7769-1aac-4888-9bea-064f1caa8e77.jpg"/> </div><br>
