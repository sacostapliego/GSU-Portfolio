.386
.model flat, stdcall
.stack 4096

ExitProcess PROTO, dwExitCode:DWORD

.data
array DWORD 10, 11, 13, 18, 21, 23, 24, 17, 45
ArraySize = ($ - Array) / TYPE array
sum DWORD 0

.code
main PROC
    mov eax, 0              ;sum
    mov esi, 0              ;index
    mov ecx, ArraySize

L1:                         ;outer loop/for
    cmp ecx, 0              ;current_size > 0
    jle next                ;if current_size <= 0, then exit

    mov esi, 0              ;reset index

L2:                         ;innter loop/while
    cmp esi, ecx            ;if index < current_size
    jge L4                  ;exit if index >= current_size

    mov edx, array[esi*4]   ;put array[index] to edx 
    test edx, 1             ;check if even
    jnz L3                  ;if odd, skip to index += 1

    add eax, edx            ; add even number to eax/sum

L3:
    inc esi                 ;index += 1
    jmp L2                  ;repeat inner loop/while

L4:
    dec ecx                 ;decrement current_size
    jmp l1                  ;repeat outer loop/for

next:
    mov sum, eax            ;moves eax resgiser(holding the values), to sum

    Invoke ExitProcess, 0
main ENDP
END main