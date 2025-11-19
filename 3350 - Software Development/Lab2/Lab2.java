/*
starter code
*/

public class Lab2
{
    public static void main(String[] args)
    {
        Student students[] = new Student[2];
        int i;
        students[0] = new UndergraduateStudent(111, "Lambert");
        students[1] = new UndergraduateStudent(122, "Lembeck");
		System.out.println("\n\n\n\nUndergraduate Students:");
		
        for(i = 0; i < students.length; ++i) 
		{
			System.out.println("Student ID: " +
			                    students[i].getId() + ", Name: " +
			                    students[i].getLastName() + ", Tuition: " +
			                    students[i].getTuition() + " per year, " +
			                    "Student Class is: " + students[i].getClassification());
		}
		// NOTE: output for first UndergraduateStudent should be:
		// "Student ID: 111, Name: Lambert, Tuition: 4000 per year, Student Class is: Undergraduate"
		

		// REUSE the students[] array and create two GraduateStudent objects
		// Initialize with ID and lastname values
		// Print the two graduates with identical "for loop"
		// use very similar code as above...
		System.out.println("\n\n\nGraduate Students:");
		students[0] = new GraduateStudent(222, "Charlie Brown");
		students[1] = new GraduateStudent(333, "Shaggy");
		for(i = 0; i < students.length; ++i) 
		{
			System.out.println("Student ID: " +
			                    students[i].getId() + ", Name: " +
			                    students[i].getLastName() + ", Tuition: " +
			                    students[i].getTuition() + " per year, " +
			                    "Student Class is: " + students[i].getClassification());
		}
		
		System.out.println("\n\n\nProgrammer is: Steven Acosta-Pliego\n\n\n\n");
    }
}
