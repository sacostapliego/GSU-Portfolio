package src;
import java.sql.*;
import java.util.ArrayList;

public class SMS {
    
    // main program to print students with their enrolled courses from data in the MYSql 'SMS2' database
	
    public static void main(String[] args) {
        String url = "jdbc:mysql://localhost:3306/sms2";
        String user = "root";
        String password = "password";
		// 'Reports()' method could have multiple report types
        Reports("enrollment", url, user, password);   
    }
    
    public static void Reports(String reportName, String url, String user, String password) {
        ArrayList<Student> students = new ArrayList<>();
        
		if(reportName.toLowerCase().equals("enrollment")) {
            String sqlcommand = "SELECT student_id, firstname, lastname, classify, major "+ 
                                "FROM students " +
                                "ORDER BY student_id; ";
                                
            try (Connection myConn = DriverManager.getConnection(url, user, password)) {
                Statement myStmt = myConn.createStatement();
                ResultSet myRS = myStmt.executeQuery(sqlcommand);
                
                while (myRS.next()) {
                    Student temp = new Student();
					
					// use 'temp' to store studentID, firstname, lastname, classification, major, and the 
					// associated 'enrolled courses' using methods in the 'Student.java' object
                    // add the temp 'student' to the ArrayList (students) command: 'students.add(temp);'
                    temp.setStudent_id(myRS.getInt("student_id"));
                    temp.setFname(myRS.getString("firstname"));
                    temp.setLname(myRS.getString("lastname"));
                    temp.setClassify(myRS.getString("classify"));
                    temp.setMajor(myRS.getString("major"));	

                    temp.setEnrolled_courses();

                    students.add(temp);
                }
                myConn.close();
            
            } catch (Exception e) {
                System.out.println("ERROR " + e.getLocalizedMessage());
            } finally {
            }
			
			// calling the helper method, 'PrintEnrollments(students)' to print a student and 
			// all their enrolled courses.
			
			// STUDY THE CODE IN "PrintEnrollments()" method. 
            PrintEnrollments(students);
			
        } else {
            System.out.println("\n\n****ERROR**** Invalid report requested\n\n");
        }
    }
    
    public static void PrintEnrollments(ArrayList<Student> myStudents) {
		
		// * * * * * * * * * * * * change to your name here...
        System.out.println("\n\n\nStudent Enrollment Report by Steven Acosta-Pliego\n");
        System.out.println("ID   CLASS\t MAJOR\t NAME\t\t\tEnrollments");
        for(Student s:myStudents) {
			
			// print the student information formatted in the instructions with using
			// the methods from 'Student.java' object. Use the "\t" for tab
			
            System.out.printf("%d   %s\t %s\t%s\t\t",
                    s.getStudent_id(),
                    s.getClassify(),
                    s.getMajor(),
                    s.getFname() + " " + s.getLname()
            );           
		    // I am giving you the setup data structure to iterate over each student's enrollments using 
			// a second Arraylist and loading if first with 's.getEnrolled_courses()' method
			
            ArrayList<Enrollments> e1 = new ArrayList<>();
            e1.addAll(s.getEnrolled_courses());
            
            // print the first enrollment with a proper tab space
            boolean first = true;
            int counter = 1;
			for( Enrollments eStudent:e1 ) {
				
				// print the enrolled courses formatted in the instructions with using
				// the methods from 'Enrollments.java' object. Use the "\t" for tab spacing
				if (first) {
                System.out.printf( "%d) %s %d HRS:%d %s\n",
                        counter,
                        eStudent.getDeptID(),
                        eStudent.getCourseID(),
                        eStudent.getCourseHours(),
                        eStudent.getCourseName()
                );
                first = false;
                } else {
                    System.out.printf( "\t\t\t\t\t\t%d) %s %d HRS:%d %s\n",
                    counter,
                    eStudent.getDeptID(),
                    eStudent.getCourseID(),
                    eStudent.getCourseHours(),
                    eStudent.getCourseName()
                    );
                };
                counter++;
            }
            System.out.println("\t\t\t\t\t\t-----------------------------------------");
        }
    }
} 