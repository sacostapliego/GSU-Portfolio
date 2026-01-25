;Student: Steven Acosta-Pliego
;Class: CSC3210
;Assignment#: 3
;Description: Finds the sum of the qVal value, dividing them into 4 words and finding the sum.

.386
.model flat, stdcall
.stack 4096

ExitProcess PROTO, dwExitCode:DWORD

.data
;64-bit
qVal QWORD 0506030704080102h

.code
main PROC
    ;1st word (05060)
    mov ax, WORD PTR qVal

    ;2nd word (0307) + ax
    add ax, WORD PTR qVal+2

    ;3rd word (0408) + ax
    add ax, WORD PTR qVal+4

    ;4th word (0102) + ax
    add ax, WORD PTR qVal+6
    
    ;fill the rest with 0s to show the answer
    movzx eax, ax

    invoke ExitProcess, 0    ; Exit program

main ENDP
END main
