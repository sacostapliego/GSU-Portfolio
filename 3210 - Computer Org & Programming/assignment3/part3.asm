;Student: Steven Acosta-Pliego
;Class: CSC3210
;Assignment#: 3
;Description: This progam translates the C program to assembly

.386
.model flat, stdcall
.stack 4096

ExitProcess PROTO, dwExitCode:DWORD

.data
    var1 DWORD 10
    var2 DWORD 11
    var3 DWORD 12

.code
main PROC
;load values into registers
    mov eax, var1
    mov ebx, var2
    mov ecx, var3

;(var1 > var2) OR (var3 < var2)
    ;(var1 > var2)
    cmp eax, ebx            ;compare var1 and var2
    jg condTrue             ;jump to CondTrue function if greater

    ;(var3 < var2)
    cmp ecx, ebx            ;compare var3 and var2
    jl condTrue             ;jump to CondTru if less

;else:
    sub eax, 1d             ;var1--
    sub ebx, 1d             ;var2--
    sub ecx, 1d             ;var3--
    jmp updateValues        ;jump to update values

condTrue:
    ;If case
    add eax, ecx            ;var1 = var2 + var3 (eax = eax + ecx)
    add eax, 1d             ;var2++
    add eax, 1d             ;var3++

updateValues:
    ;update values
    mov var1, eax           ;Update var1
    mov var2, ebx           ;Update var2
    mov var3, ecx           ;Update var3

    invoke ExitProcess, 0       ; Exit program

main ENDP
END main
