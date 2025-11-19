public class Lab1 
{
    public static void main( String[] args )
    {
        Automobile a = new Automobile("Porsche", "911 ST", 2025, 4);
        SUV s = new SUV("Subaru", "Outback", 2025, 4, 5, 6.7 );

        a.getinfo();
        
        s.getinfo();
    }
}
