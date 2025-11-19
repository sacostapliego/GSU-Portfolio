#include <stdio.h>
#include <math.h>

// Function prototypes for each operation
double addition(double left, double right);         //"+"
double subtraction(double left, double right);      //"-"
double multiplication(double left, double right);   //"*"
double division(double left, double right);         //"/"
double power(double left, double right);            //"**"
double floordivision(double left, double right);   //"//"

int main() {
    char operator[3]; // Left Value, Opperand, Right Value (3)
    double left, right;
    
    //loop
    while (1) {

    printf("Please enter an expression:\n");
    printf(":> ");
    
        //Makes sure the expression is in the form of LHS, operator, RHS
        if (scanf("%lf %2s %lf", &left, operator, &right) != 3) {
            printf("Invalid input format.\n");
            return 1;
        }

        double result;
        if (operator[0] == '+') {
            result = addition(left, right);
        } else if (operator[0] == '-') {
            result = subtraction(left, right);
        } else if (operator[0] == '*' && operator[1] == '\0') { //operator[1] used to diff. the * and **
            result = multiplication(left, right);
        } else if (operator[0] == '/' && operator[1] == '\0') { //operator[1] used to diff. the / and //
            result = division(left, right);
            //since power has two opperators **
        } else if (operator[0] == '*' && operator[1] == '*') {
            result = power(left, right);
            //since floor has two opperators **
        } else if (operator[0] == '/' && operator[1] == '/') {
            result = floordivision(left, right);
        } else {
            printf("Invalid operator. (%s)\n", operator);
            return 1;
        }

        //prints the result
        printf("%.2lf %s %.2lf = %.2lf\n\n", left, operator, right, result);
    }

    return 0;
}

//Functions as used above
double addition(double left, double right) {
    return left + right;
}

double subtraction(double left, double right) {
    return left - right;
}

double multiplication(double left, double right) {
    return left * right;
}

double division(double left, double right) {
    return left / right;
}

double power(double left, double right) {
    return pow(left, right);
}

double floordivision(double left, double right) {
    return floor(left / right);
}
