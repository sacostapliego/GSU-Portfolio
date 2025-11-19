public class GraduateStudent extends Student
{
    public static final double GRAD_TUITION = 6000;
	public static final String GRAD_CLASSIFY = "Graduate";
    public GraduateStudent(int pID, String pName)
    {
		// initialze super class, Student.java for 'pID' and 'Student' values
        super(pID, pName);
        // initialze the Student.java's 'tuition' and 'classification' values
        setTuition();
        setClassification();
    }
    public void setTuition()
    {
        tuition = GRAD_TUITION;
    }
    public void setClassification()
    {
        classification = GRAD_CLASSIFY;
    }
}
