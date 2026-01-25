.386
.model flat, stdcall
.stack 4096

ExitProcess PROTO, dwExitCode:DWORD

.data
Array WORD 10, 2, 23, 45, 21, 11
MAXIMUM WORD ?

.code
main PROC
    mov esi, OFFSET Array   ;pointer
    mov ecx, 5              ;counter
    mov ax, [esi+0]         ;ax = 10 first item
    mov MAXIMUM, ax         ;assume first item is maximum

L1:                         ;beginning of loop
    mov bx, [esi+2]         ;next item move to bx
    cmp ax, bx              ;compare item in ax, and bx
    jl If_Block             ;if ax < bx, move to if statement block
    jmp next                ;if false, skip to next/end of loop

    If_Block:           
    mov ax, bx              ;if true, moves bx to ax for further comparison
    mov MAXIMUM, bx         ;also moves bx to maximum

    next:
    add esi, 2              ;increment by 2, since data type is WORD
    loop L1                 ;loops

    Invoke ExitProcess, 0
main ENDP
END main