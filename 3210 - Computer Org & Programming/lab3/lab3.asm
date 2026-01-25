.386
.model flat,stdcall
.stack 4096
ExitProcess proto,dwExitCode:dword

.code
main proc

	mov al, 245
	mov bl, 41
	mov cl, 11
	mov dl, 215

	sub al, dl
	add al, cl
	sub al, bl
	
	invoke ExitProcess,0
main endp
end main