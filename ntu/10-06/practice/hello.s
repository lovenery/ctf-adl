global _start

section .text:

_start:
	call main
	db 'Hello World', 00

main:
	xor rax, rax
	xor rdi, rdi
	xor rdx, rdx
	xor rcx, rcx
	mov rax, 1 ; rax = sys_write
	mov rdi, 1  ; stdout
	mov rsi, [rsp] ; buffer
	mov rdx, 12  ; len(buffer)
	syscall
	mov rax, 60 ; rax = sys_exit
	mov rdi, 0
	syscall
