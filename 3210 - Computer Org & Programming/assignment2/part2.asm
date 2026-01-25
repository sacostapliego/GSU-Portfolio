;Student: Steven Acosta-Pliego
;Class: CSC3210
;Assignment#: 2
;Description:Implements the following expression in assembly, ECX = -(val3 + val1) + (-val4 - val2) + 3

.386
.model flat, stdcall
.stack 4096

ExitProcess PROTO, dwExitCode:DWORD

.data
    val1 BYTE 12    ;8-bit
    val2 WORD 9     ;16-bit
    val3 DWORD 2    ;32-bit
    val4 BYTE 20    ;8-bit

.code
main PROC   
    mov eax, val3       ;eax = val3
    movzx ebx, val1     ;ebx = val1 - same size
    add eax, ebx        ;eax = val3 + val1
    neg eax             ;eax = -(val3 + val1)

    movzx ebx, val4     ;ebx = val4
    neg ebx             ;ebx = -val4
    movsx edx, val2     ;edx = val2
    sub ebx, edx        ;ebx = (-val4 - val2)

    add eax, ebx        ;eax = -(val3 + val1) + (-val4 - val2)
    add eax, 3          ;eax = -(val3 + val1) + (-val4 - val2) + 3

    ;save result in ecx register
    mov ecx, eax        ;ecx = -(val3 + val1) + (-val4 - val2) + 3

    Invoke ExitProcess, 0
main ENDP
END main