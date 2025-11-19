import java.sql.*;

public class Payroll {

	public Payroll() {

	}

	public StringBuilder getPayByMonth(int empID, Connection myConn) {
		StringBuilder SB_output = new StringBuilder("");

		// command to get the payroll (copy from GetEmployeesPayroll.java)
		String sqlcommand = "SELECT p.empid, p.pay_date, p.earnings, p.fed_tax, " +
                "p.fed_med,p.fed_SS,p.state_tax,p.retire_401k,p.health_care  " +
                "FROM payroll p " +
                "WHERE p.empid = " + empID + " " +
                "ORDER BY p.pay_date;";


		try {
            Statement myStmt = myConn.createStatement();

            SB_output.append("\tEMP ID\tPAY DATE\tGROSS\tFederal\tFedMed\tFedSS\tState\t401K\tHealthCare\n");
            ResultSet myRS1 = myStmt.executeQuery(sqlcommand);
            while (myRS1.next()) {
                SB_output.append("\t" + myRS1.getString("p.empid") + "\t");
                SB_output.append(myRS1.getDate("p.pay_date") + "\t" + myRS1.getDouble("p.earnings") + "\t");
                SB_output.append(myRS1.getDouble("p.fed_tax") + "\t" + myRS1.getDouble("p.fed_med") + "\t");
                SB_output.append(myRS1.getDouble("p.fed_SS") + "\t" + myRS1.getDouble("p.state_tax") + "\t");
                SB_output.append(myRS1.getDouble("p.retire_401K") + "\t" + myRS1.getDouble("p.health_care")+"\n" );
            }
            System.out.println(SB_output.toString());
            SB_output.setLength( 0 );
        } catch (SQLException e) {
            System.out.println("ERROR " + e.getLocalizedMessage());
        }
		return (SB_output);
	}

}
