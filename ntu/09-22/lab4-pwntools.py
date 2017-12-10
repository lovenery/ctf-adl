from pwn import *

host, port = "csie.ctf.tw", 10123
r = remote(host, port)

left = 1
right = 50000000

while(True):
    r.recvuntil('input number =')
    r.sendline( str(int( (left+right)/2 )) )
    l = r.recvline().strip()
    print("Debug v=", str(int( (left+right)/2 )), l)

    if l == "It's too small":
        left = int( (left+right)/2 )
    elif l == "It's too big":
        right = int( (left+right)/2 )
    else:
        print(str(int( (left+right)/2 )))
        break

r.interactive()
