#include <stdio.h>
#include <string.h>

#define MAX_LENGTH 100 //could be anything, setting 100 just for this lab

//two functions used to reverse the string
void reverseString(char *str);
void swap(char *left, char *right);

int main() {
    char str[MAX_LENGTH];

    //user input
    printf("Enter a string: ");
    //stores in str, reads up to max_length
    fgets(str, MAX_LENGTH, stdin);

    //trims the string for the example output for lab instructions
    str[strcspn(str, "\n")] = '\0';

    //prints orginal string
    printf("Original string: %s\n", str);

    //performs reverse function
    reverseString(str);

    //prints reversed string
    printf("Reversed string: %s\n", str);

    //exit
    return 0;
}

//pointer
void reverseString(char *str) {
    //length of string
    int length = strlen(str);
    //loop from beginng to the midpoint
    for (int i = 0; i < length / 2; i++) {
        //swap position from i and from the end
        swap(&str[i], &str[length - i - 1]);
    }
}

//swaps the two pointers (left and right) values that they point to
void swap(char *left, char *right) {
    //copies the value poitned left to a temp value
    char temp = *left;
    //copies the value pointed right to left
    *left = *right;
    //copies the value pointed at right to temp
    *right = temp;
}
