;Student: Steven Acosta-Pliego
;Class: CSC3210
;Assignment#: 2
;Description:Implements the following expressions in assembly
;z0 = x + 130
;z1 = y - x + z0
;z2 = r + x - z1

.386
.model flat, stdcall
.stack 4096

ExitProcess PROTO, dwExitCode:DWORD

.data
    x WORD 10           ;16-bit
    y WORD 15           ;16-bit 
    r WORD 4            ;16-bit
    z DWORD 3 DUP(?)    ;uninitialized

.code
main PROC   
    ;x + 130
    movzx eax, x       ;ax = x
    add eax, 130     ;ax = x + 130
    mov [z], eax     ;Store in first item (z0)

    ;y - x + z0
    movzx eax, y       ;ax = y
    movzx ebx, x       ;bx = x
    sub eax, ebx      ;ax = y - x  
    add eax, [z]     ;ax = y + z0
    mov [z+4], eax   ;Store in second item (z1)

    ;r + x - z1
    movzx eax, r       ;ax = r
    movzx ebx, x       ;bx = x
    add eax, ebx      ;ax = r + x
    sub eax, [z+4]   ;ax = r + x - z1
    mov [z+8], eax   ;Store in third item (z2)

    Invoke ExitProcess, 0
main ENDP
END main