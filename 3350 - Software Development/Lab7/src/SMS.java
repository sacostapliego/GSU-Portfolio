package src;
import java.sql.*;
import java.util.ArrayList;

public class SMS {
    public static void main(String[] args) {
        String url = "jdbc:mysql://localhost:3306/sms2";
        String user = "root";
        String password = "BlueJay9.";
        //Reports("enrollment", url, user, password);
        Reports("department", url, user, password);  
    }
    
    public static void Reports(String reportName, String url, String user, String password) {
        ArrayList<Student> students = new ArrayList<>();
     
        String sqlcommand = "SELECT student_id, firstname, lastname, classify, major "+ 
	        					"FROM students ORDER BY student_id; ";
        
	        try (Connection myConn = DriverManager.getConnection(url, user, password)) {
	            Statement myStmt = myConn.createStatement();
	            ResultSet myRS = myStmt.executeQuery(sqlcommand);

	            while (myRS.next()) {
	                Student temp = new Student();
	                temp.setStudent_id(myRS.getInt(1));
	                temp.setFname(myRS.getString(2));
	                temp.setLname(myRS.getString(3));
	                temp.setClassify(myRS.getString(4));
	                temp.setMajor(myRS.getString(5));
	                temp.setEnrolled_courses();
	                students.add(temp);
	            }
	            myConn.close();
	        } catch (Exception e) {
	            System.out.println("ERROR " + e.getLocalizedMessage());
	        } finally {

	        }

        if(reportName.toLowerCase().equals("enrollment")) {
			
			/*************** MOVE this block above the 'if(reportName.tolowerCase().equals("enrollment"))' */
			/* code will be used by both if and 'else if' blocks
			/*************STARTE HERE***/

			/*************END HERE***/
			
            PrintEnrollments(students);
			
        } else if(reportName.toLowerCase().equals("department")) {
			
            ArrayList<Department> departments = new ArrayList<>(); 
			
            String sqlcmd = "SELECT dept_id, dept_name, building "+ 
                            "FROM department ORDER BY dept_id; ";
			
			/************* CREATE a new 'try-catch-finally' block for processing the data from the */
			/************* select statement. You will need to do the while loop, create a "temp" */
			/************* variable of type 'Department' to load all values, then add to ArrayList */
			/************* from above 'departments' */	

            try (Connection myConn = DriverManager.getConnection(url, user, password)) {
                Statement myStmt = myConn.createStatement();
                ResultSet myRS = myStmt.executeQuery(sqlcmd);

                while (myRS.next()) {
                    Department temp = new Department();
                    temp.setDept_id(myRS.getString("dept_id"));
                    temp.setDept_name(myRS.getString("dept_name"));
                    temp.setLocation(myRS.getString("building"));
                    departments.add(temp);
                }
                myConn.close();
            } catch (Exception e) {
                System.out.println("ERROR " + e.getLocalizedMessage());
            }
            finally {

            }
            
            PrintDepartments(students, departments);
        } else {
            System.out.println("\n\n****ERROR**** Invalid report requested\n\n");
        }
    }
    
    public static void PrintEnrollments(ArrayList<Student> myStudents) {
        System.out.println("\n\n\nStudent Enrollment Report by Steven Acosta-Pliego\n");
        System.out.println("ID   CLASS\t MAJOR\t NAME\t\t\tEnrollments");
        for(Student s:myStudents) {
            System.out.println(s.getStudent_id()+"   "+s.getClassify()+"\t "+s.getMajor()+"\t "+s.getFname()+
                    " "+s.getLname());
           
            ArrayList<Enrollments> e1 = new ArrayList<>();
            e1.addAll(s.getEnrolled_courses());
            for( Enrollments eStudent:e1 ) {
                System.out.println("\t\t\t\t\t\t"+
                        (e1.indexOf(eStudent)+1)+") "+ eStudent.getDeptID()+"-"+eStudent.getCourseID()
                        +", HRS:"+eStudent.getCourseHours()
                        +", "+eStudent.getCourseName());
            }
            System.out.println("\t\t\t\t\t\t-----------------------------------------");
        }
    }
    
    public static void PrintDepartments(ArrayList<Student> myStudents, ArrayList<Department> myDepts) {
		/*************  change my name to your name */
        System.out.println("\n\n\nDepartment with Student Majors Report by Steven Acosta-Pliego\n");
        System.out.printf("%-8s %-12s %-36s %-10s\n","Major","Location","Department","Students");
        System.out.printf("%-8s %-12s %-36s %-32s\n","-----","--------","----------","-----------------------------------------");
        
        for(Department d:myDepts) {
            System.out.printf("%-8s %-12s %-37s",d.getDept_id(),d.getLocation(),d.getDept_name());
            
            boolean bNotFirst = false;
            for(Student s:myStudents ) {
				/*************  use if( d.getDept_id().equals(s.getMajor() )) */
                /*************  use another if - else test on 'bNotFirst' to trigger printing on same line */
				/*************  as the department data or move to next line and print.*/
				/*************  HOW I GOT THE FIRST LINE department data to print FIRST student information: */
				/*************  example: if(!bNotFirst) print on same line as department data, then set */
				/*************  bNotFirst to true, else print on line by itself */
                if (d.getDept_id().equals(s.getMajor())) {
                    if (!bNotFirst) {
                        System.out.println(s.getFname() + " " + s.getLname() + "   \t" + s.getClassify());
                        bNotFirst = true;
                    } else {
                        System.out.printf("%-58s %s %s\n", " ", s.getFname(), s.getLname() +"   \t" + s.getClassify());
                    }
                }
            }
            System.out.printf("%-58s %32s\n"," ","-----------------------------------------");
        }
    }
} 