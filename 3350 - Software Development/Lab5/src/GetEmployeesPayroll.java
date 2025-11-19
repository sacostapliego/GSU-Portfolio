import java.sql.*;
import java.util.Scanner;

public class GetEmployeesPayroll {
    public static void main(String[] args) {
        String url = "jdbc:mysql://localhost:3306/employeeData";
        String user = "root";
        String password = "password";
        StringBuilder output = new StringBuilder("");
        String sqlcommand = "SELECT e.Fname, e.Lname, e.email, jt.job_title, e.empid " +
                "FROM employees e  " +
                "JOIN employee_job_titles ejt ON e.empid = ejt.empid " +
                "JOIN job_titles jt ON ejt.job_title_id = jt.job_title_id  " +
                "ORDER BY e.empid ; ";

        try (Connection myConn = DriverManager.getConnection(url, user, password)) {
            Statement myStmt = myConn.createStatement();

            output.append("\nEMPLOYEE PAYROLL REPORT by Steven Acosta-Pliego\n");
            ResultSet myRS = myStmt.executeQuery(sqlcommand);
            while (myRS.next()) {
                output.append("Name= " + myRS.getString("e.Fname") + " " + myRS.getString("e.Fname") + "\t");
                output.append("Title=" + myRS.getString("jt.job_title") + "     " + myRS.getString("e.email") + "\n");
                System.out.print(output.toString());
                output.setLength(0);
                
				/* instead of calling the method 'getPayroll()' use the following code 
                 * once you have created the Payroll.java class. Notice the parameters to the 
				 * method 'getPayByMonth...' in your new Payroll.java class.
                 */

                 
				 /* CODE: */
                 Payroll p1 = new Payroll();
                 output.append(p1.getPayByMonth(myRS.getInt("e.empid"), myConn)); 
            }
            myConn.close();
        } catch (Exception e) {
            System.out.println("ERROR " + e.getLocalizedMessage());
        } finally {
        }
        System.out.println("\nPress Enter to clear console screen...\n");
        Scanner myScann = new Scanner(System.in);
        String str = myScann.nextLine() ;
        System.out.print("\033[H\033[2J");  
        System.out.flush();  
        
    }
    /* This method needs to be moved into its own class called Payroll.java 
     * Use an empty default constructor, no need to have private instance variables. 
     * 
     * Pass the "myRS.getInt("e.empid")" and "myConn" into the method called
     * 'getPayByMonth()' It must return a StringBuilder object.
     * 
     * 
     * DELETE THIS METHOD 'getPayByMonth(..' code BEFORE YOU TURN IN THIS JAVA FILE. */
}

