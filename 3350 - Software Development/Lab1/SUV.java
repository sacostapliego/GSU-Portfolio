public class SUV extends Automobile 
{
	private int numpass;
	private double cargospc;
	
	public SUV(String mk, String md, int y, int nw, int np, double c) 
	{
		// call the constructor
		super(mk, md, y, nw);

		// add numpass and cargospc
		numpass = np;
		cargospc = c;
	}
	
	@Override
	public void getinfo() 
	{
		super.getinfo();

		// Passangers + Cargo space
		System.out.println("Passengers: " + numpass);
		System.out.println("Cargo Space: " + cargospc);
	}
}