.386
.model flat, stdcall
.stack 4096

ExitProcess PROTO, dwExitCode:DWORD

.data
	arrayB WORD 1,2,3,4

.code
main PROC
	mov eax, 0

   Invoke ExitProcess, 0
main ENDP
END main