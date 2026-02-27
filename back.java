import java.io.*;
import java.sql.*;
import javax.servlet.*;
import javax.servlet.http.*;

public class JobFinderServlet extends HttpServlet {

    // Database Connection Details
    String jdbcURL = "jdbc:mysql://localhost:3306/CampusJobFinder";
    String dbUser = "root";
    String dbPassword = "root"; // change if needed

    protected void doPost(HttpServletRequest request,
                          HttpServletResponse response)
                          throws ServletException, IOException {

        response.setContentType("text/html");
        PrintWriter out = response.getWriter();

        // Get form values
        String name = request.getParameter("name");
        String gender = request.getParameter("gender");
        String timing = request.getParameter("timing");
        String jobType = request.getParameter("jobType");
        String safety = request.getParameter("safety");

        Connection conn = null;

        try {

            // Load Driver
            Class.forName("com.mysql.cj.jdbc.Driver");

            // Connect Database
            conn = DriverManager.getConnection(
                    jdbcURL, dbUser, dbPassword);

            /* ==========================
               STORE STUDENT SEARCH
            ========================== */

            String insertStudent =
                "INSERT INTO students(name,gender,college_timing,preferred_job,safety_preference) VALUES(?,?,?,?,?)";

            PreparedStatement ps1 =
                    conn.prepareStatement(insertStudent);

            ps1.setString(1, name);
            ps1.setString(2, gender);
            ps1.setString(3, timing);
            ps1.setString(4, jobType);
            ps1.setString(5, safety);

            ps1.executeUpdate();


            /* ==========================
               FETCH MATCHING JOBS
            ========================== */

            String query =
              "SELECT * FROM jobs WHERE job_type=? OR timing=?";

            PreparedStatement ps2 =
                    conn.prepareStatement(query);

            ps2.setString(1, jobType);
            ps2.setString(2, timing);

            ResultSet rs = ps2.executeQuery();

            /* ==========================
               OUTPUT PAGE
            ========================== */

            out.println("<html>");
            out.println("<head>");
            out.println("<title>Matched Jobs</title>");
            out.println("</head>");
            out.println("<body style='font-family:Poppins;'>");

            out.println("<h2>Hello " + name + " 👋</h2>");
            out.println("<h3>Recommended Jobs For You</h3>");

            while(rs.next()) {

                out.println("<div style='border:1px solid #ccc;"
                        + "padding:15px;margin:10px;"
                        + "border-radius:8px;'>");

                out.println("<h3>"
                        + rs.getString("job_title")
                        + "</h3>");

                out.println("<p><b>Location:</b> "
                        + rs.getString("location") + "</p>");

                out.println("<p><b>Timing:</b> "
                        + rs.getString("timing") + "</p>");

                out.println("<p><b>Salary:</b> ₹"
                        + rs.getInt("pay_min")
                        + " - ₹"
                        + rs.getInt("pay_max")
                        + "</p>");

                out.println("<p><b>Safety:</b> "
                        + rs.getString("safety") + "</p>");

                out.println("</div>");
            }

            out.println("<br><a href='index.html'>⬅ Search Again</a>");
            out.println("</body></html>");

            conn.close();

        } catch(Exception e) {
            out.println("<h3>Error: "+e.getMessage()+"</h3>");
        }
    }
}