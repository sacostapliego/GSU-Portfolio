;Student: Steven Acosta-Pliego
;Class: CSC3210
;Assignment#: 3
;Description: This program takes the string, and swaps it into the string shown in the instructions, using xchg and a loop

.386
.model flat, stdcall
.stack 4096

ExitProcess PROTO, dwExitCode:DWORD

.data
inputStr BYTE "A", "B", "C", "D", "E", "F", "G", "H"
.code
main PROC

    ;pointers
    mov esi, OFFSET inputStr    
    mov edi, OFFSET inputStr

    ;counter
    mov ecx, 2 ;loop counter                      

;loop
L1: 
    ;moves two characters into higher and lower halves of ax register
    mov al, [esi+0]             
    mov ah, [esi+1]

    ;moves two characters into higher and lower halves of bx register
    mov bl, [edi+6]
    mov bh, [edi+7]

    ;swaps ax and bx
    xchg ax, bx

    ;moves esi to the top
    mov [esi], ax

    ;moves edi to the bottom
    mov [edi+6], bx
    
    ;increments by 2
    add esi, 2 

    ;decrements by 2
    sub edi, 2

    ;end loop after 2 loops
    loop L1

    invoke ExitProcess, 0    ; Exit program

main ENDP
END main
