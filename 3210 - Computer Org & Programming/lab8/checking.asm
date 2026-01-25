.386
.model flat, stdcall
.stack 4096

ExitProcess PROTO, dwExitCode:DWORD

.data
    dVal DWORD ?

.code
main PROC
    mov dVal,12345678h
    mov ax, WORD PTR dVal+2
    add ax,3
    mov WORD PTR dVal,ax
    mov eax,dVal

    Invoke ExitProcess, 0
main ENDP
END main
