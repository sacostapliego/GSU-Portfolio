#include <stdio.h>
#include <string.h>

#define MAX_STUDENTS 100
#define SUBJECT_COUNT 5 //set to five from example output
#define NAME_LENGTH 50

//Create new structure 
typedef struct {
    int id;
    char name[NAME_LENGTH];
    float grades[SUBJECT_COUNT];
    float average;
} Student;

//functions used in program
void addStudents(Student students[], int *count);
void calculateAverage(Student *student);
void displayStudents(const Student students[], int count);

int main() {
    Student students[MAX_STUDENTS];
    int studentCount = 0;
    int choice;

    do {
        //print greeting message + user options
        printf("\n=== Student Grade Management System ===\n");
        printf("1. Add Students\n");
        printf("2. Display All Students\n");
        printf("3. Exit\n");
        printf("Enter your choice: ");

        //executes a function based on the user choice
        scanf("%d", &choice);
        switch (choice) {
            case 1:
                addStudents(students, &studentCount);
                break;
            case 2:
                displayStudents(students, studentCount);
                break;
            case 3:
                printf("Exiting the program. Goodbye!\n");
                break;
            default:
                printf("Invalid choice. Please try again.\n");
        }
    //loops, until '3' is picked
    } while (choice != 3);

    return 0;
}

//add students
void addStudents(Student students[], int *count) {
    int numStudents;
    printf("Enter the number of students to add: ");
    scanf("%d", &numStudents);

    //loops for however many students
    for (int i = 0; i < numStudents; i++) {
        printf("\nEnter details for student %d:\n", *count + 1);

        printf("ID: ");
        scanf("%d", &students[*count].id); //id:number

        printf("Name: ");
        scanf("%s", students[*count].name); //name:string

        for (int j = 0; j < SUBJECT_COUNT; j++) {       //loops until subject count is reached
            printf("Grade for subject %d: ", j + 1);    
            scanf("%f", &students[*count].grades[j]);   //scans for floats
        }

        calculateAverage(&students[*count]);            //calculate function
        (*count)++;                 //up the count
    }

    printf("\nStudent data added successfully!\n"); //
}

void calculateAverage(Student *student) {
    //inti sum
    float sum = 0.0;
    for (int i = 0; i < SUBJECT_COUNT; i++) {
        sum += student->grades[i];
    }
    student->average = sum / SUBJECT_COUNT; //pointer
}

//diplay student function
void displayStudents(const Student students[], int count) {
    //base case
    if (count == 0) {
        printf("No students to display.\n");
        return;
    }
    \
    //presents student informatoin
    printf("\n=== Student Information ===\n");
    //table like structure
    printf("%-5s %-20s %-10s %-10s %-10s %-10s %-10s %-10s %-10s\n",
           "ID", "Name", "Grade1", "Grade2", "Grade3", "Grade4", "Grade5", "Average");

    for (int i = 0; i < count; i++) {
        //prints the id and student name using copying the template above
        printf("%-5d %-20s ", students[i].id, students[i].name);
        for (int j = 0; j < SUBJECT_COUNT; j++) {
            //prints the student grades, spaced out -10
            printf("%-10.2f ", students[i].grades[j]);
        }
        //prints average at the end
        printf("%-10.2f\n", students[i].average);
    }
}
