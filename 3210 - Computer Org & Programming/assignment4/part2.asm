;Student Name: Steven Acosta-Pliego
;Class: CSC3210
;Assignment#: 4
;Description: Finds the largest item in an array and returns it.

.386
.model flat, stdcall
.stack 4096

ExitProcess PROTO, dwExitCode:DWORD

.data
Array DWORD 10, 34, 2, 56, 67, -1, 9, 45, 0, 11
ArraySize = ($ - Array) / TYPE array

.code
function1 PROC                      ;function 
    mov eax, DWORD PTR [esi]        ;first element
    add esi, ebx                    ;move to next element

L1:
    cmp ecx, 1      ;if there are more than one element
    jle next        ;if there are no more, end the loop

    mov edx, DWORD PTR [esi]    ;load current element into edx
    cmp edx, eax                ;compare current with largest so far
    jle L2                      ;if current <= largest, jump to second loop
    mov eax, edx                ;if current > largest, upadte eax

L2:
    add esi, ebx                ;move to next element
    dec ecx                     ;decreamnt how many loops left
    jmp L1                      ;repeat

next:   
    ret                         ;return from preocedutre

function1 ENDP

main PROC
    mov esi, OFFSET array       ;address of the array
    mov ecx, ArraySize          ;number of elements
    mov ebx, TYPE array         ;size of each element 

    call function1              ;calls function


    Invoke ExitProcess, 0
main ENDP
END main