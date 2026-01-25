.386
.model flat, stdcall
.stack 4096

ExitProcess PROTO, dwExitCode:DWORD

.data
;declare variables here
var1 DWORD 100
var2 DWORD 200
var3 DWORD 50
var4 DWORD ?    ;empty 32 bit


.code
main PROC
    mov eax, var1
    imul eax, var2  ;eax = var1 * var2

    mov edx, 0
    mov ebx, var3 
    imul ebx, 5     ;ebx = var3 * 5

    idiv ebx        ;eax = var4 = (var1 * var2) / (var3 * 5)

    mov var4, eax   ;store result

    Invoke ExitProcess, 0
main ENDP
END main