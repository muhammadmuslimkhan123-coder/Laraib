import streamlit as st
import sqlite3
import pandas as pd
from datetime import date
from urllib.parse import quote

# Government Girls High School Sial
# Web app created by Masooma Batool
# Python application using Streamlit; no hand-written HTML/CSS/JavaScript.

st.set_page_config(
    page_title="Govt Girls High School Sial",
    page_icon="🏫",
    layout="wide"
)

SCHOOL_NAME = "Government Girls High School Sial"
CREATOR = "Masooma Batool"
DB_FILE = "school.db"

# A general school-building photo search link is used because a verified photo
# specifically of this school could not be confirmed. Replace with the school's
# own photo when available.
SCHOOL_PHOTO = (
    "https://images.unsplash.com/photo-1580582932707-520aed937b7b"
    "?auto=format&fit=crop&w=1600&q=85"
)

CLASSES = [f"{grade}{section}" for grade in range(6, 11) for section in "ABC"]

# Demo teacher names and assignments: confirm/replace with actual school records.
TEACHERS = [
    ("Ayesha Malik", "English", "6A"),
    ("Sana Iqbal", "Mathematics", "6B"),
    ("Nadia Aslam", "Science", "6C"),
    ("Hina Rauf", "Urdu", "7A"),
    ("Farah Khalid", "Pakistan Studies", "7B"),
    ("Samina Noor", "Islamiyat", "7C"),
    ("Mehwish Akram", "Mathematics", "8A"),
    ("Rabia Shah", "English", "8B"),
    ("Kiran Bibi", "Science", "8C"),
    ("Uzma Yousaf", "Urdu", "9A"),
    ("Sadia Ahmed", "Biology", "9B"),
    ("Nimra Javed", "Chemistry", "9C"),
    ("Shazia Parveen", "Physics", "10A"),
    ("Bushra Amin", "Mathematics", "10B"),
    ("Saira Bano", "English", "10C"),
    ("Mariam Asghar", "Computer Science", "6A"),
    ("Lubna Tariq", "General Science", "7A"),
    ("Sehrish Fatima", "Islamiyat", "8A"),
    ("Ambreen Yaqoob", "Urdu", "9A"),
    ("Noreen Akhtar", "Pakistan Studies", "10A"),
]

def get_connection():
    return sqlite3.connect(DB_FILE, check_same_thread=False)

def initialize_database():
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                roll_no TEXT NOT NULL UNIQUE,
                class_section TEXT NOT NULL,
                guardian TEXT,
                phone TEXT
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_roll TEXT NOT NULL,
                attendance_date TEXT NOT NULL,
                status TEXT NOT NULL,
                UNIQUE(student_roll, attendance_date)
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS marks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_roll TEXT NOT NULL,
                subject TEXT NOT NULL,
                exam TEXT NOT NULL,
                obtained REAL NOT NULL,
                total REAL NOT NULL
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS notices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                details TEXT NOT NULL,
                notice_date TEXT NOT NULL
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT,
                quantity INTEGER NOT NULL DEFAULT 1
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS fees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_roll TEXT NOT NULL,
                month TEXT NOT NULL,
                amount REAL NOT NULL,
                status TEXT NOT NULL
            )
        """)
        conn.commit()

initialize_database()

# Uses Streamlit's built-in theme; no custom HTML/CSS is written.

with st.sidebar:
    st.title("🏫 School Portal")
    st.caption("Red & White Theme")
    page = st.radio(
        "Navigation",
        [
            "1. Home Dashboard",
            "2. Student Registration",
            "3. Students Records",
            "4. Classes & Sections",
            "5. Teacher Management",
            "6. Principal Dashboard",
            "7. Student Attendance",
            "8. Teacher Attendance",
            "9. Exams & Results",
            "10. Homework & Study Material",
            "11. Timetable",
            "12. School Facilities",
            "13. Notices & Announcements",
            "14. Parent Portal",
            "15. Student ID Card",
            "16. Staff Management",
            "17. Library Management",
            "18. Reports & Analytics",
        ],
    )
    st.divider()
    st.write("**Created by:** Masooma Batool")

def load_df(query, params=()):
    with get_connection() as conn:
        return pd.read_sql_query(query, conn, params=params)

def student_options():
    df = load_df("SELECT roll_no, name, class_section FROM students ORDER BY class_section, name")
    return df

st.title("Government Girls High School Sial")
st.caption("School Management Web Application | Created by Masooma Batool")

# Feature 1: Home dashboard
if page == "1. Home Dashboard":
    st.image(SCHOOL_PHOTO, use_container_width=True, caption="School-building illustration/photo (not verified as this exact school)")
    st.subheader("Welcome to Government Girls High School Sial")
    st.write(
        "A central portal for student records, classes, teachers, attendance, "
        "examinations, notices and school resources."
    )
    students = load_df("SELECT * FROM students")
    teachers_df = pd.DataFrame(TEACHERS, columns=["Teacher Name", "Subject", "Assigned Class"])
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Registered Students", len(students))
    c2.metric("Teachers (demo list)", len(teachers_df))
    c3.metric("Class Sections", len(CLASSES))
    c4.metric("Classrooms (configured)", 18)
    st.info("Teacher names and assignments are sample data. Please verify them before real school use.")
    st.markdown("### School information")
    st.write("Principal: Lubaba Batool (as provided for this project)")
    st.write("Main gates: 2 | Classrooms: 18 | Sections: 6A–10C")

# Feature 2: Student registration
elif page == "2. Student Registration":
    st.header("Student Registration")
    with st.form("student_form", clear_on_submit=True):
        name = st.text_input("Student full name")
        roll_no = st.text_input("Roll number / student ID")
        class_section = st.selectbox("Class and section", CLASSES)
        guardian = st.text_input("Parent / guardian name")
        phone = st.text_input("Parent / guardian contact (optional)")
        submitted = st.form_submit_button("Register Student")
        if submitted:
            if not name.strip() or not roll_no.strip():
                st.error("Student name and roll number are required.")
            else:
                try:
                    with get_connection() as conn:
                        conn.execute(
                            "INSERT INTO students(name, roll_no, class_section, guardian, phone) VALUES (?, ?, ?, ?, ?)",
                            (name.strip(), roll_no.strip(), class_section, guardian.strip(), phone.strip())
                        )
                    st.success("Student registered successfully.")
                except sqlite3.IntegrityError:
                    st.error("This roll number already exists. Please use a unique roll number.")

# Feature 3: Students records
elif page == "3. Students Records":
    st.header("Student Records")
    df = load_df("SELECT id, name, roll_no, class_section, guardian, phone FROM students ORDER BY class_section, name")
    search = st.text_input("Search by name or roll number")
    if search:
        df = df[df["name"].str.contains(search, case=False, na=False) |
                df["roll_no"].str.contains(search, case=False, na=False)]
    st.dataframe(df, use_container_width=True, hide_index=True)
    if not df.empty:
        roll_to_delete = st.selectbox("Select roll number to delete", [""] + df["roll_no"].tolist())
        if st.button("Delete selected student"):
            if roll_to_delete:
                with get_connection() as conn:
                    conn.execute("DELETE FROM students WHERE roll_no = ?", (roll_to_delete,))
                st.success("Student record deleted. Refresh the page to update the list.")
                st.rerun()

# Feature 4: Classes and sections
elif page == "4. Classes & Sections":
    st.header("Classes & Sections")
    class_df = pd.DataFrame({
        "Class / Section": CLASSES,
        "Classroom": [f"Room {i+1:02d}" for i in range(len(CLASSES))]
    })
    st.dataframe(class_df, use_container_width=True, hide_index=True)
    st.write("Configured classrooms: 18 (Room 01 to Room 18).")
    st.write("There are 15 sections: 6A, 6B, 6C through 10A, 10B, 10C.")

# Feature 5: Teacher management
elif page == "5. Teacher Management":
    st.header("Teacher Management")
    st.warning("These 20 teacher names and class assignments are fictional examples for the project, not verified school staff.")
    teachers_df = pd.DataFrame(TEACHERS, columns=["Teacher Name", "Subject", "Assigned Class"])
    st.dataframe(teachers_df, use_container_width=True, hide_index=True)
    st.download_button(
        "Download teacher list (CSV)",
        teachers_df.to_csv(index=False).encode("utf-8"),
        "sample_teachers.csv",
        "text/csv"
    )

# Feature 6: Principal dashboard
elif page == "6. Principal Dashboard":
    st.header("Principal Dashboard")
    st.write("Principal: Lubaba Batool")
    st.write("School: Government Girls High School Sial")
    students_count = load_df("SELECT COUNT(*) AS n FROM students")["n"][0]
    attendance_count = load_df("SELECT COUNT(*) AS n FROM attendance")["n"][0]
    marks_count = load_df("SELECT COUNT(*) AS n FROM marks")["n"][0]
    a, b, c = st.columns(3)
    a.metric("Students", int(students_count))
    b.metric("Attendance entries", int(attendance_count))
    c.metric("Result entries", int(marks_count))
    st.info("Use the Reports & Analytics page for exported records.")

# Feature 7: Student attendance
elif page == "7. Student Attendance":
    st.header("Student Attendance")
    students = student_options()
    if students.empty:
        st.info("Register students first.")
    else:
        choice = st.selectbox(
            "Student",
            students.to_dict("records"),
            format_func=lambda x: f'{x["roll_no"]} — {x["name"]} ({x["class_section"]})'
        )
        att_date = st.date_input("Attendance date", value=date.today())
        status = st.selectbox("Status", ["Present", "Absent", "Leave"])
        if st.button("Save student attendance"):
            with get_connection() as conn:
                conn.execute("""
                    INSERT INTO attendance(student_roll, attendance_date, status)
                    VALUES (?, ?, ?)
                    ON CONFLICT(student_roll, attendance_date)
                    DO UPDATE SET status=excluded.status
                """, (choice["roll_no"], att_date.isoformat(), status))
            st.success("Attendance saved.")
    st.subheader("Attendance register")
    st.dataframe(load_df("""
        SELECT a.attendance_date, a.student_roll, s.name, s.class_section, a.status
        FROM attendance a LEFT JOIN students s ON a.student_roll=s.roll_no
        ORDER BY a.attendance_date DESC
    """), use_container_width=True, hide_index=True)

# Feature 8: Teacher attendance
elif page == "8. Teacher Attendance":
    st.header("Teacher Attendance")
    st.caption("Demo teacher names; verify the real staff list before use.")
    teacher_names = [row[0] for row in TEACHERS]
    with st.form("teacher_attendance_form"):
        teacher = st.selectbox("Teacher", teacher_names)
        att_date = st.date_input("Date", value=date.today(), key="teacher_att_date")
        status = st.selectbox("Attendance", ["Present", "Absent", "Leave"], key="teacher_att_status")
        save = st.form_submit_button("Save teacher attendance")
        if save:
            st.session_state.setdefault("teacher_attendance", [])
            st.session_state["teacher_attendance"].append(
                {"Date": att_date.isoformat(), "Teacher": teacher, "Status": status}
            )
            st.success("Teacher attendance saved for this session.")
    st.dataframe(pd.DataFrame(st.session_state.get("teacher_attendance", [])), use_container_width=True)

# Feature 9: Exams and results
elif page == "9. Exams & Results":
    st.header("Exams & Results")
    students = student_options()
    if students.empty:
        st.info("Register students before entering marks.")
    else:
        with st.form("marks_form"):
            choice = st.selectbox(
                "Student",
                students.to_dict("records"),
                format_func=lambda x: f'{x["roll_no"]} — {x["name"]} ({x["class_section"]})'
            )
            exam = st.selectbox("Exam", ["Monthly Test", "Midterm", "Final Exam", "Class Test"])
            subject = st.selectbox("Subject", ["English", "Urdu", "Mathematics", "Science", "Islamiyat", "Pakistan Studies", "Biology", "Chemistry", "Physics", "Computer Science"])
            total = st.number_input("Total marks", min_value=1.0, value=100.0)
            obtained = st.number_input("Obtained marks", min_value=0.0, value=0.0)
            save_marks = st.form_submit_button("Save marks")
            if save_marks:
                if obtained > total:
                    st.error("Obtained marks cannot exceed total marks.")
                else:
                    with get_connection() as conn:
                        conn.execute(
                            "INSERT INTO marks(student_roll, subject, exam, obtained, total) VALUES (?, ?, ?, ?, ?)",
                            (choice["roll_no"], subject, exam, obtained, total)
                        )
                    st.success("Marks saved.")
    result_df = load_df("""
        SELECT m.student_roll, s.name, s.class_section, m.exam, m.subject,
               m.obtained, m.total,
               ROUND((m.obtained * 100.0) / m.total, 2) AS percentage
        FROM marks m LEFT JOIN students s ON m.student_roll=s.roll_no
        ORDER BY m.exam, s.class_section, s.name
    """)
    st.dataframe(result_df, use_container_width=True, hide_index=True)

# Feature 10: Homework and study material
elif page == "10. Homework & Study Material":
    st.header("Homework & Study Material")
    st.write("This section can be used to publish homework, notes, syllabi and past papers.")
    st.link_button("Search educational study material", "https://www.google.com/search?q=Punjab+textbook+board+class+6+to+10+books")
    uploaded = st.file_uploader("Upload notes / syllabus / past paper", type=["pdf", "docx", "txt", "png", "jpg"])
    if uploaded:
        st.download_button("Download uploaded file", uploaded.getvalue(), uploaded.name)

# Feature 11: Timetable
elif page == "11. Timetable":
    st.header("Timetable")
    timetable = pd.DataFrame([
        ("08:00–08:40", "Period 1", "English"),
        ("08:40–09:20", "Period 2", "Mathematics"),
        ("09:20–10:00", "Period 3", "Science"),
        ("10:00–10:20", "Break", "Break"),
        ("10:20–11:00", "Period 4", "Urdu"),
        ("11:00–11:40", "Period 5", "Islamiyat"),
        ("11:40–12:20", "Period 6", "Pakistan Studies"),
    ], columns=["Time", "Period", "Sample Subject"])
    selected_class = st.selectbox("Select class", CLASSES)
    st.subheader(f"Sample timetable — {selected_class}")
    st.dataframe(timetable, use_container_width=True, hide_index=True)
    st.caption("This is an example timetable. Replace it with the school's approved timetable.")

# Feature 12: School facilities
elif page == "12. School Facilities":
    st.header("School Facilities")
    facilities = pd.DataFrame([
        ("Classrooms", 18, "Room 01–18"),
        ("Main gates", 2, "Gate 1 and Gate 2"),
        ("Library", "To confirm", "Update according to actual school facilities"),
        ("Science lab", "To confirm", "Update according to actual school facilities"),
        ("Computer lab", "To confirm", "Update according to actual school facilities"),
        ("Playground", "To confirm", "Update according to actual school facilities"),
        ("Staff room", "To confirm", "Update according to actual school facilities"),
    ], columns=["Facility", "Quantity / Status", "Details"])
    st.dataframe(facilities, use_container_width=True, hide_index=True)
    st.caption("Only the 18 classrooms and 2 gates were specified for this project; other facilities need confirmation.")

# Feature 13: Notices and announcements
elif page == "13. Notices & Announcements":
    st.header("Notices & Announcements")
    with st.form("notice_form", clear_on_submit=True):
        title = st.text_input("Notice title")
        details = st.text_area("Notice details")
        notice_date = st.date_input("Notice date", value=date.today())
        save_notice = st.form_submit_button("Publish notice")
        if save_notice:
            if title.strip() and details.strip():
                with get_connection() as conn:
                    conn.execute(
                        "INSERT INTO notices(title, details, notice_date) VALUES (?, ?, ?)",
                        (title.strip(), details.strip(), notice_date.isoformat())
                    )
                st.success("Notice published.")
            else:
                st.error("Enter both a title and details.")
    notices = load_df("SELECT title, details, notice_date FROM notices ORDER BY notice_date DESC")
    if notices.empty:
        st.info("No notices have been published yet.")
    for _, row in notices.iterrows():
        with st.expander(f'{row["title"]} — {row["notice_date"]}'):
            st.write(row["details"])

# Feature 14: Parent portal
elif page == "14. Parent Portal":
    st.header("Parent Portal")
    st.info("Demo lookup only. A real parent portal needs secure login and verified parent-to-student links.")
    roll = st.text_input("Enter student's roll number")
    if st.button("View student record"):
        student = load_df("SELECT name, roll_no, class_section, guardian FROM students WHERE roll_no=?", (roll.strip(),))
        if student.empty:
            st.warning("No student found with that roll number.")
        else:
            st.dataframe(student, use_container_width=True, hide_index=True)
            st.subheader("Attendance")
            st.dataframe(load_df("SELECT attendance_date, status FROM attendance WHERE student_roll=? ORDER BY attendance_date DESC", (roll.strip(),)), use_container_width=True, hide_index=True)
            st.subheader("Results")
            st.dataframe(load_df("SELECT exam, subject, obtained, total FROM marks WHERE student_roll=?", (roll.strip(),)), use_container_width=True, hide_index=True)

# Feature 15: Student ID card
elif page == "15. Student ID Card":
    st.header("Student ID Card Generator")
    students = student_options()
    if students.empty:
        st.info("Register a student first.")
    else:
        roll = st.selectbox("Choose student roll number", students["roll_no"].tolist())
        student = load_df("SELECT name, roll_no, class_section, guardian FROM students WHERE roll_no=?", (roll,))
        if not student.empty:
            row = student.iloc[0]
            st.markdown("---")
            st.subheader(SCHOOL_NAME)
            st.write("**STUDENT ID CARD**")
            st.write(f"**Name:** {row['name']}")
            st.write(f"**Roll No.:** {row['roll_no']}")
            st.write(f"**Class:** {row['class_section']}")
            st.write(f"**Guardian:** {row['guardian']}")
            st.write(f"**Issued by:** {CREATOR}")
            st.markdown("---")
            st.download_button("Download ID details (CSV)", student.to_csv(index=False).encode("utf-8"), f"id_{roll}.csv", "text/csv")

# Feature 16: Staff management
elif page == "16. Staff Management":
    st.header("Non-Teaching Staff Management")
    staff = pd.DataFrame([
        ("Head Clerk", "Office records and reports"),
        ("Junior Clerk", "Data entry and student files"),
        ("Librarian", "Book issue and return"),
        ("Lab Assistant", "Laboratory assistance (if applicable)"),
        ("Peon 1", "Office assistance"),
        ("Peon 2", "Classroom and office assistance"),
        ("Security Staff", "Gate monitoring"),
        ("Cleaning Staff", "Cleanliness"),
    ], columns=["Role", "Sample Duty"])
    st.warning("These are suggested roles and duties, not a verified list of current employees.")
    st.dataframe(staff, use_container_width=True, hide_index=True)

# Feature 17: Library management
elif page == "17. Library Management":
    st.header("Library Management")
    with st.form("book_form", clear_on_submit=True):
        title = st.text_input("Book title")
        author = st.text_input("Author")
        quantity = st.number_input("Available copies", min_value=0, value=1, step=1)
        add_book = st.form_submit_button("Add book")
        if add_book:
            if title.strip():
                with get_connection() as conn:
                    conn.execute("INSERT INTO books(title, author, quantity) VALUES (?, ?, ?)", (title.strip(), author.strip(), int(quantity)))
                st.success("Book added.")
            else:
                st.error("Book title is required.")
    books_df = load_df("SELECT title, author, quantity FROM books ORDER BY title")
    st.dataframe(books_df, use_container_width=True, hide_index=True)

# Feature 18: Reports and analytics
elif page == "18. Reports & Analytics":
    st.header("Reports & Analytics")
    students = load_df("SELECT name, roll_no, class_section, guardian, phone FROM students ORDER BY class_section, name")
    attendance = load_df("SELECT student_roll, attendance_date, status FROM attendance ORDER BY attendance_date DESC")
    marks = load_df("SELECT student_roll, subject, exam, obtained, total FROM marks ORDER BY exam")
    a, b, c = st.columns(3)
    a.metric("Students", len(students))
    b.metric("Attendance records", len(attendance))
    c.metric("Marks records", len(marks))
    st.subheader("Students by class")
    if not students.empty:
        counts = students.groupby("class_section").size().reindex(CLASSES, fill_value=0).rename("Students")
        st.bar_chart(counts)
    st.subheader("Download reports")
    st.download_button("Download students CSV", students.to_csv(index=False).encode("utf-8"), "students_report.csv", "text/csv")
    st.download_button("Download attendance CSV", attendance.to_csv(index=False).encode("utf-8"), "attendance_report.csv", "text/csv")
    st.download_button("Download results CSV", marks.to_csv(index=False).encode("utf-8"), "results_report.csv", "text/csv")

st.divider()
st.caption(f"{SCHOOL_NAME} | Web App Created by {CREATOR} | Demo project — verify school details before official use.")
