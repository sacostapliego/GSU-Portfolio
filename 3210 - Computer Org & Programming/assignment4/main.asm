.386
.model flat, stdcall
.stack 4096

ExitProcess PROTO, dwExitCode:DWORD

.data
Array DWORD 10, 34, 2, 56, 67, -1, 9, 45, 0, 11
arrayLength DWORD 10  ; Number of elements in the array

.code
main PROC
    ; Pass parameters to findLargest function
    lea esi, Array       ; Load the address of the array into ESI
    mov ecx, arrayLength ; Load the length of the array into ECX
    mov edx, TYPE Array  ; Load the type (size of each element) of the array into EDX

    ; Call findLargest function
    call findLargest

    ; EAX now contains the largest item in the array
    ; Program end
    Invoke ExitProcess, 0
main ENDP

; Function to find the largest item in an array
findLargest PROC
    ; Input: 
    ; ESI - initial address of the array
    ; ECX - length of the array
    ; EDX - type/size of array elements (DWORD here, 4 bytes)
    
    mov eax, [esi]       ; Initialize EAX with the first element of the array (largest so far)
    add esi, edx         ; Move to the next element in the array
    dec ecx              ; Reduce count by 1, as we've already processed the first element

findLoop:
    cmp ecx, 0           ; Check if we have processed all elements
    je endLoop           ; If count is zero, end loop

    mov ebx, [esi]       ; Load the current element into EBX
    cmp eax, ebx         ; Compare EAX (current largest) with EBX (current element)
    jge skipUpdate       ; If EAX >= EBX, skip updating the largest value

    mov eax, ebx         ; Update EAX to the new largest value

skipUpdate:
    add esi, edx         ; Move to the next element in the array
    dec ecx              ; Decrease the counter
    jmp findLoop         ; Repeat the loop

endLoop:
    ret                  ; Return with EAX holding the largest value
findLargest ENDP

END main