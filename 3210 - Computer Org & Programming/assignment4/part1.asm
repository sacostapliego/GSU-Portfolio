;Student Name: Steven Acosta-Pliego
;Class: CSC3210
;Assignment#: 4
;Implements the psuedo code in the instructions and translates it

.386
.model flat, stdcall
.stack 4096

ExitProcess PROTO, dwExitCode:DWORD

.data
sum SDWORD 0
var1 SDWORD 3d
var2 SDWORD 3d
var3 SDWORD 0d

.code
main PROC
mov esi, 0d      ;i
mov edi, 12d     ;j
mov eax, var1
mov ebx, var2
mov ecx, var3

    L1:
    cmp esi, edi    ;checking i < j
    jge next        ;if i >= j, move to end program

    cmp eax, ecx    ;var1 = var1 - i
    jle L3          ;jump to else, if var1 <= var3
    
    sub eax, esi    ;var1 = var1 - i
    jmp L4

    L3:
    add ecx, esi    ;var3 = var3 + 1

    L4:
    mov edx, eax
    add edx, ebx
    add edx, ecx
    mov sum, edx    ;sum = var1 + var2 + var3

    dec edi         ;j = j - 1
    inc esi         ;i++
    jmp L1

    next:

    Invoke ExitProcess, 0
main ENDP
END main
