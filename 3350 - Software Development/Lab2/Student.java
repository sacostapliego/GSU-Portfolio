/*
    Starter code
*/
public abstract class Student
{
    private int ID;
    private String lastName;
    protected double tuition;
	protected String classification;
	
    public Student(int pID, String pName)
    {
		// set the 'ID' and 'lastname', DO NOT assign values\
        this.ID = pID;
        this.lastName = pName;

    }
    public void setId(int idNum)
    {
        // write your code here
        this.ID = idNum;
    }
    public void setLastName(String pName)
    {
        // write your code here
        this.lastName = pName;
    }
    public int getId()
    {
        // write your code here
        return ID;
    }
    public String getLastName()
    {
        // write your code here
        return lastName;
    }
    public double getTuition()
    {
        // write your code here
        return tuition;
    }
    public String getClassification()
    {
        // write your code here
        return classification;
    }
	// no concrete code for abstract methods
    public abstract void setTuition();
	public abstract void setClassification();
}
