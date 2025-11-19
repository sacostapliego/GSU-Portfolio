package src;
import java.sql.*;
import java.util.ArrayList;

public class Student {
	
	private int student_id;
	private String fname, lname, classify, major;
	private ArrayList<Enrollments> enrolled_courses  = new ArrayList<>();

	public int getStudent_id() {
		return this.student_id;
	}

	public void setStudent_id(int student_id) {
		this.student_id = student_id;
	}

	public String getFname() {
		return this.fname;
	}

	public void setFname(String fname) {
		this.fname = fname;
	}

	public String getLname() {
		return this.lname;
	}

	public void setLname(String lname) {
		this.lname = lname;
	}

	public String getClassify() {
		return this.classify;
	}

	public void setClassify(String classify) {
		this.classify = classify;
	}

	public String getMajor() {
		return this.major;
	}

	public void setMajor(String major) {
		this.major = major;
	}

	public ArrayList<Enrollments> getEnrolled_courses() {
		return this.enrolled_courses;
	}

	public void setEnrolled_courses() {
		String url = "jdbc:mysql://localhost:3306/sms2";
        String user = "root";
        String password = "password";
		String sqlcommand = "SELECT ce.dept_id, ce.course_id, c.course_name, c.hours " +
						"FROM current_enrollments ce " +
						"JOIN course c ON c.course_id = ce.course_id " +
						"WHERE ce.student_id = " + getStudent_id() +"; ";

        try (Connection myConn = DriverManager.getConnection(url, user, password)) {
            Statement myStmt = myConn.createStatement();
            ResultSet myRS = myStmt.executeQuery(sqlcommand);
            
			
            while (myRS.next()) {
				Enrollments temp = new Enrollments();
                temp.addCourse(myRS.getString(1),myRS.getInt(2),myRS.getString(3),myRS.getInt(4));
				enrolled_courses.add(temp);
			}  
			myConn.close();       
        } catch (Exception e) {
            System.out.println("ERROR " + e.getLocalizedMessage());
        } finally {
		}
	}
	
		
	public Student()
	{
		// all values handled individually
	}
}
