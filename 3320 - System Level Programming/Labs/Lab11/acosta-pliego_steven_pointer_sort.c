#include <stdio.h>

#define N 10

void bubbleSort(int *arr, int n) {  //pointer is an integer, size of an array
    int *p, *p_next, temp;          //declare pointers
    for (int i = 0; i < n - 1; i++) {   //for loop
        for (p = arr; p < arr + n - 1 - i; p++) {   //nested for loop, beginning o f the array until p reaches arr + n - 1 - i
            p_next = p + 1; //element after p is p_next
            if (*p > *p_next) {     //if p is larger than p_next
                //switch
                temp = *p;     
                *p = *p_next;
                *p_next = temp;
            }
        }
    }
}

int main() {
    int num_array[N];
    int largest, smallest;

    //loop for user input, N = 10 times
    for (int i = 0; i < N; i++) {
        printf("Please Enter Number %d: ", i + 1);
        scanf("%d", &num_array[i]);
    }

    //bubble sorting with implementation of pointers
    bubbleSort(num_array, N);

    //print array, using loops, and bracket from example output
    printf("[");
    for (int i = 0; i < N; i++) {
        printf("%d", num_array[i]);
        if (i < N - 1) printf(", ");
    }
    printf("]\n\n");

    //Finds the largest and smallest array using pointers
    largest = smallest = *num_array;
    for (int *p = num_array; p < num_array + N; p++) {
        if (*p > largest) largest = *p;
        if (*p < smallest) smallest = *p;
    }

    //prints the smaller and largerst number
    printf("Largest: %d\n", largest);
    printf("Smallest: %d\n", smallest);

    return 0;
}
