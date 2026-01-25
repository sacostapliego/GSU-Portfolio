.386
.model flat, stdcall
.stack 4096

ExitProcess PROTO, dwExitCode:DWORD

.data
val1 SWORD 23
val2 SWORD -35
val3 SDWORD 4

.code
main PROC
    mov eax, val1
    add eax, val2

    Invoke ExitProcess, 0
main ENDP
END main