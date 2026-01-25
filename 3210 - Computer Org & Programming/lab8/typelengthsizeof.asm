.386
.model flat, stdcall
.stack 4096

ExitProcess PROTO, dwExitCode:DWORD

.data
    myBytes BYTE 10h,20,30h,40h
    myWords WORD 3 DUP(?), 2000h
    myString BYTE "ABCDE"

.code
main PROC
    mov eax, TYPE myBytes
    mov eax, LENGTHOF myBytes
    mov eax, SIZEOF myBytes
    mov eax, TYPE myWords
    mov eax, LENGTHOF myWords
    mov eax, SIZEOF myWords
    mov eax, SIZEOF myString
    
    Invoke ExitProcess, 0
main ENDP
END main