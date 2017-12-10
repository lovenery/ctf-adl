# Lab 1

```shell
strings lab1-strings
strings lab1-strings | grep FLAG
```

# Lab 2

```shell
chmod u+x lab2-strace
strace ./lab2-strace 
strace -s 36 ./lab2-strace # 預設只有顯示32個字元
```

# Lab3

## using xxd

```shell
./lab3-patching
vim -b ./lab3-patching # binary mode
:%!xxd
/c876 # `c876 03` 改成 `3333 02`
:%!xxd -r
:wq
./lab3-patching
```

## using gdb

```shell
./lab3-patching
Value = 0x376c8
Go patching the value to 0x00023333

gdb lab3-patching

gdb-peda$ find 0x376c8
Searching for '0x376c8' in: None ranges
Found 1 results, display max 1 items:
lab3-patching : 0x601048 --> 0x376c8

gdb-peda$ break main
Breakpoint 1 at 0x4005ba

gdb-peda$ run

gdb-peda$ set *0x601048=0x23333
gdb-peda$ x/x 0x601048
0x601048 <value>:	0x0000000000023333
gdb-peda$ c
Continuing.
Value = 0x23333
FLAG{oa11TH80wfMEs6ZflBhGF4btUcS1Ds9y}[Inferior 1 (process 19516) exited normally]
```
