#include <stdio.h>
#include <math.h>   //for the sqrt() function

int main() 
{
    //All varibles that are used in the equations (m, h, t, v, e) and g = 9.8 m/s^2
    double mass, height, time, velocity, kinetic;
    double gravity = 9.8;
    printf("Enter the mass of the object in kilograms: ");
    //use lf for longer floating values
    scanf("%lf", &mass);
    printf("Enter the height of the drop in meters: ");
    scanf("%lf", &height);

    //time equaiton from instructions
    time = sqrt(2 * (height/gravity));

    //velocity equation from instructions
    velocity = (gravity * time);

    //kinetic energy equation from instructions
    kinetic = ((0.5) * mass * (velocity * velocity));

    //%.2lf, prints out the floating values only to two decimal places, as instructions show.
    printf("The time taken by an object weighing %.2lf to reach the ground when dropped from a height of %.2lf meters is %.2lf seconds.\n", mass, height, time);
    printf("The velocity of the object when it hits the ground = %.2lf m/s.\n", velocity);
    printf("The kinetic energy at the moment of impact with the ground is %.2lf Joules.\n", kinetic);

    return 0;
}