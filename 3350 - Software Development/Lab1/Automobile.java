public class Automobile 
{
    private String make;
    private String model;
    private int year;
    private int numWheels;

    public Automobile(String mk, String md, int y, int nw)
    {
        make = mk;
        model = md;
        year = y;
        numWheels = nw;
    }

    public void getinfo()
    {
        // print 'The programmer is: <your name>'
       System.out.println("The programmer is: Steven Acosta-Pliego");

		// print the 'Make: ' 'Model: ' 'Year: ' and 'Number of Wheels: '
        System.out.println("Make: " + make);
        System.out.println("Model: " + model);
        System.out.println("Year: " + year);
        System.out.println("Number of Wheels: " + numWheels);

    }
}