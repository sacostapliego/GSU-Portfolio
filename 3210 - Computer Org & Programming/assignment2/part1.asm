;Student: Steven Acosta-Pliego
;Class: CSC3210
;Assignment#: 2
;Description:Implements the following expression in assembly, EDX = (val3 + val4) - (val2 - val1) - (5/3) * 7

.386
.model flat, stdcall
.stack 4096

ExitProcess PROTO, dwExitCode:DWORD

.data
val1 WORD 120h      ;288 decimal
val2 WORD 39h       ;57 decimal
val3 WORD 20h       ;32 decimal
val4 WORD 27h       ;39 decimal

.code
main PROC

;(val3 + val4)
    movzx eax, val3
    movzx ebx, val4
    add eax, ebx

;(val2 - val1)
    movzx ecx, val2
    movzx edx, val1
    sub ecx, edx

;(val3 + val4) - (val2 - val1)
    sub eax, ecx

;move result to ecx to prepare division
    mov ecx, eax

;(5/3) - Chapter 7 Signed Integer Division
    mov eax, 0
    mov eax, 5
    cwd
    mov bx, 3
    idiv ebx

; * (7)
    mov ebx, 7
    imul eax, ebx

;(val3 + val4) - (val2 - val1) - (5/3) * 7
    sub ecx, eax

;Result is stored in edx register
    mov edx, ecx

    Invoke ExitProcess, 0
main ENDP
END main