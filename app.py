import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from database_setup import *

initialize_db()

def generate_student_to_department_ratio():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT department, COUNT(*) FROM students
        GROUP BY department
    """)
    department_data = cursor.fetchall()
    conn.close()

    departments = [data[0] for data in department_data]
    student_counts = [data[1] for data in department_data]

    fig = go.Figure(data=[go.Pie(labels=departments, values=student_counts, hole=0.3)])
    fig.update_layout(title="Student to Department Ratio")
    st.plotly_chart(fig)

def generate_faculty_to_department_ratio():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT department, COUNT(*) FROM faculty
        GROUP BY department
    """)
    department_data = cursor.fetchall()
    conn.close()

    departments = [data[0] for data in department_data]
    faculty_counts = [data[1] for data in department_data]

    fig = go.Figure(data=[go.Pie(labels=departments, values=faculty_counts, hole=0.3)])
    fig.update_layout(title="Faculty to Department Ratio")
    st.plotly_chart(fig)

def generate_gender_ratio():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT gender, COUNT(*) FROM students
        GROUP BY gender
    """)
    gender_data = cursor.fetchall()
    conn.close()

    genders = [data[0] for data in gender_data]
    gender_counts = [data[1] for data in gender_data]

    fig = go.Figure(data=[go.Pie(labels=genders, values=gender_counts, hole=0.3)])
    fig.update_layout(title="Girl to Boy Ratio")
    st.plotly_chart(fig)

if "user" not in st.session_state:
    st.session_state.user = "Normal"

def authenticate_admin(username, password):
    admin_username = "admin"
    admin_password = "admin"
    if username == admin_username and password == admin_password:
        return True
    return False

def admin_login():
    st.subheader("Admin Login")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if authenticate_admin(username, password):
            st.session_state.user = "admin"
            st.rerun()
        else:
            st.error("Invalid credentials. Please try again.")
    
def main():
    st.title("University Database Management System")

    admin_menu = ["Home", "Student", "Faculty", "View Data", "Search"]
    normal_menu = ["Home", "View Data", "Search", "Admin"]

    if "menu" not in st.session_state:
        st.session_state.menu = normal_menu

    if st.session_state.user == "admin":
        if st.sidebar.button("Logout"):
            st.session_state.user = "Normal"
            st.rerun()

        st.session_state.menu = admin_menu
        
    else:
        st.session_state.menu = normal_menu

    choice = st.sidebar.selectbox("Choose an Option", st.session_state.menu)

    if choice == "Home":
        st.subheader("Welcome to the University Management System")
        st.write("""Use this app to manage students, faculty, and departments.""")

        st.write("### Student to Department Ratio")
        if has_data("students"):
            generate_student_to_department_ratio()
        else:
            st.warning("No student data found to display the Student to Department Ratio.")

        st.write("### Faculty to Department Ratio")
        if has_data("faculty"):
            generate_faculty_to_department_ratio()
        else:
            st.warning("No faculty data found to display the Faculty to Department Ratio.")

        st.write("### Girl to Boy Ratio")
        if has_data("students"):
            generate_gender_ratio()
        else:
            st.warning("No student data found to display the Girl to Boy Ratio.")

    if choice == "Student":
        add_tab, remove_tab, update_tab = st.tabs(["Add Student", "Remove Student", "Update Student"])

        with add_tab:
            st.subheader("Add a New Student")
            with st.form("student_form"):
                prn = st.number_input("PRN", value=None, min_value=0)
                name = st.text_input("Name").strip().title()
                age = st.number_input("Age", min_value=18, max_value=100)
                address = st.text_area("Address").strip()
                phone = st.text_input("Phone").strip()
                email = st.text_input("Email (Optional)").strip()
                department = st.selectbox("Department", ["Computer Engineering", "Information Technology", "Mechanical Engineering", "Electrical Engineering", "Chemical Engineering", "Petrochemical Engineering"])
                gender = st.selectbox("Gender", ["Male", "Female", "Other"])
                duration = st.number_input("Course Duration (Years)", min_value=4)
                starting_year = st.number_input("Starting Year (Year)", value=2024)
                submitted = st.form_submit_button("Add Student", help="Adds student data to the database")
                if submitted:
                    if check_duplicate_prn(prn):
                        st.error("Student with this PRN already exists!")
                    else:
                        add_record("students", (prn, name, age, address, phone, email, department, gender, starting_year, duration))
                        st.success(f"Student '{name}' added successfully!")

        with remove_tab:
            st.subheader("Remove a Student")
            with st.form("remove_student_form"):
                prn = st.number_input("Enter PRN of Student to Remove", value=None, min_value=0)
                submitted = st.form_submit_button("Remove Student", help="Removes a student record from the database")
                if submitted:
                    conn = create_connection()
                    cursor = conn.cursor()
                    cursor.execute("SELECT COUNT(*) FROM students WHERE prn = ?", (prn,))
                    exists = cursor.fetchone()[0]
                    if exists:
                        cursor.execute("DELETE FROM students WHERE prn = ?", (prn,))
                        conn.commit()
                        st.success(f"Student with PRN '{prn}' removed successfully!")
                    else:
                        st.error(f"No student found with PRN '{prn}'")
                    conn.close()

        with update_tab:
            st.subheader("Update a Student Record")

            if "student_prn" not in st.session_state:
                st.session_state.student_prn = None
            if "student_record" not in st.session_state:
                st.session_state.student_record = None
            if "student_selected_attributes" not in st.session_state:
                st.session_state.student_selected_attributes = []

            prn = st.number_input("Enter PRN of Student to Update", value=st.session_state.student_prn or None, min_value=0)

            if st.button("Check Record"):
                if prn is None:
                    st.warning("Please enter a valid PRN")
                else:
                    conn = create_connection()
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM students WHERE prn = ?", (prn,))
                    record = cursor.fetchone()

                    if record:
                        st.session_state.student_prn = prn
                        st.session_state.student_record = record
                        st.success("Record found!")
                    else:
                        st.session_state.student_prn = None
                        st.session_state.student_record = None
                        st.error(f"No student found with PRN '{prn}'")
                    conn.close()

            if st.session_state.student_record:
                record = st.session_state.student_record
                st.write("### Current Data")
                headers = ["PRN", "Name", "Age", "Address", "Phone", "Email", "Department", "Gender", "Starting Year", "Duration"]
                df = pd.DataFrame([record], columns=headers)
                df["PRN"] = df["PRN"].astype(str)
                df["Starting Year"] = df["Starting Year"].astype(str)
                st.dataframe(df, hide_index=True)

                st.write("### Select Attributes to Update")
                attributes = ["Name", "Age", "Address", "Phone", "Email", "Department", "Gender", "Starting Year", "Duration"]
                selected_attributes = st.multiselect(
                    "Attributes",
                    attributes,
                    default=st.session_state.student_selected_attributes,
                )

                update_data = {}

                if "Name" in selected_attributes:
                    update_data["name"] = st.text_input("New Name", record[1]).strip().title()
                if "Age" in selected_attributes:
                    update_data["age"] = st.number_input("New Age", value=record[2], min_value=18, max_value=100)
                if "Address" in selected_attributes:
                    update_data["address"] = st.text_area("New Address", record[3]).strip()
                if "Phone" in selected_attributes:
                    update_data["phone"] = st.text_input("New Phone", record[4]).strip()
                if "Email" in selected_attributes:
                    update_data["email"] = st.text_input("New Email", record[5]).strip()
                if "Department" in selected_attributes:
                    update_data["department"] = st.selectbox("Department", ["Computer Engineering", "Information Technology", "Mechanical Engineering", "Electrical Engineering", "Chemical Engineering", "Petrochemical Engineering"])

                if "Gender" in selected_attributes:
                    update_data["gender"] = st.selectbox("New Gender", ["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(record[7]))
                if "Starting Year" in selected_attributes:
                    update_data["starting_year"] = st.number_input("New Starting Year (Year)", value=record[8])
                if "Duration" in selected_attributes:
                    update_data["duration"] = st.number_input("New Course Duration (Years)", value=record[9], min_value=4)

                if st.button("Update Student Record"):
                    if update_data:
                        conn = create_connection()
                        cursor = conn.cursor()
                        set_clause = ", ".join([f"{key} = ?" for key in update_data.keys()])
                        values = list(update_data.values()) + [prn]
                        cursor.execute(f"UPDATE students SET {set_clause} WHERE prn = ?", values)
                        conn.commit()
                        conn.close()
                        st.success(f"Student record with PRN '{prn}' updated successfully!")
                        st.session_state.student_prn = None
                        st.session_state.student_record = None
                        st.session_state.student_selected_attributes = []
                    else:
                        st.warning("No attributes selected for update.")

    elif choice == "Faculty":
        add_tab, remove_tab, update_tab = st.tabs(["Add Faculty", "Remove Faculty", "Update Faculty"])

        with add_tab:
            st.subheader("Add a New Faculty")
            with st.form("faculty_form"):
                name = st.text_input("Name").strip().title()
                experience = st.number_input("Experience (Years)", min_value=0)
                education = st.text_input("Education").strip().title()
                department = st.selectbox("Department", ["Computer Engineering", "Information Technology", "Mechanical Engineering", "Electrical Engineering", "Chemical Engineering", "Petrochemical Engineering"])
                submitted = st.form_submit_button("Add Faculty", help="Adds faculty data to the database")
                if submitted:
                    if check_duplicate_faculty_name(name):
                        st.error("Faculty with this name already exists!")
                    else:
                        add_record("faculty", (name, experience, education, department))
                        st.success(f"Faculty '{name}' added successfully!")

        with remove_tab:
            st.subheader("Remove a Faculty")
            with st.form("remove_faculty_form"):
                name = st.text_input("Enter Faculty Name to Remove").strip().title()
                submitted = st.form_submit_button("Remove Faculty", help="Removes a faculty record from the database")
                if submitted:
                    conn = create_connection()
                    cursor = conn.cursor()
                    cursor.execute("SELECT COUNT(*) FROM faculty WHERE name = ?", (name,))
                    exists = cursor.fetchone()[0]
                    if exists:
                        cursor.execute("DELETE FROM faculty WHERE name = ?", (name,))
                        conn.commit()
                        st.success(f"Faculty '{name}' removed successfully!")
                    else:
                        st.error(f"No faculty found with name '{name}'")
                    conn.close()

        with update_tab:
            st.subheader("Update a Faculty Record")

            if "faculty_name" not in st.session_state:
                st.session_state.faculty_name = None
            if "faculty_record" not in st.session_state:
                st.session_state.faculty_record = None
            if "faculty_selected_attributes" not in st.session_state:
                st.session_state.faculty_selected_attributes = []

            faculty_name = st.text_input("Enter Faculty Name to Update", value=st.session_state.faculty_name or "").strip().title()

            if st.button("Check Record"):
                if not faculty_name:
                    st.warning("Please enter a valid Faculty Name")
                else:
                    conn = create_connection()
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM faculty WHERE name = ?", (faculty_name,))
                    faculty_record = cursor.fetchone()

                    if faculty_record:
                        st.session_state.faculty_name = faculty_name
                        st.session_state.faculty_record = faculty_record
                        st.success("Record found!")
                    else:
                        st.session_state.faculty_name = None
                        st.session_state.faculty_record = None
                        st.error(f"No faculty found with name '{faculty_name}'")
                    conn.close()

            if st.session_state.faculty_record:
                faculty_record = st.session_state.faculty_record
                st.write("### Current Data")
                headers = ["Name", "Experience", "Education", "Department"]
                df = pd.DataFrame([faculty_record], columns=headers)
                st.dataframe(df, hide_index=True)

                st.write("### Select Attributes to Update")
                attributes = ["Name", "Experience", "Education", "Department"]
                selected_attributes = st.multiselect(
                    "Attributes",
                    attributes,
                    default=st.session_state.faculty_selected_attributes,
                )

                update_data = {}

                if "Name" in selected_attributes:
                    update_data["name"] = st.text_input("New Name", faculty_record[0]).strip().title()
                if "Experience" in selected_attributes:
                    update_data["experience"] = st.number_input("New Experience (Years)", value=faculty_record[1], min_value=0)
                if "Education" in selected_attributes:
                    update_data["education"] = st.text_input("New Education", faculty_record[2]).strip().title()
                if "Department" in selected_attributes:
                    update_data["department"] = st.text_input("New Department", faculty_record[3]).strip().title()

                if st.button("Update Faculty Record"):
                    if update_data:
                        conn = create_connection()
                        cursor = conn.cursor()
                        set_clause = ", ".join([f"{key} = ?" for key in update_data.keys()])
                        values = list(update_data.values()) + [faculty_name]
                        cursor.execute(f"UPDATE faculty SET {set_clause} WHERE name = ?", values)
                        conn.commit()
                        conn.close()
                        st.success(f"Faculty record with name '{faculty_name}' updated successfully!")
                        st.session_state.faculty_name = None
                        st.session_state.faculty_record = None
                        st.session_state.faculty_selected_attributes = []
                    else:
                        st.warning("No attributes selected for update.")

    elif choice == "View Data":
        st.subheader("View Records")
        table = st.selectbox("Select Table", ["Students", "Faculty", "Departments"])
        
        if table == "Departments":
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute(""" 
                SELECT 
                    s.department AS Department,
                    COUNT(DISTINCT s.prn) AS Students,
                    COUNT(DISTINCT f.name) AS Faculty
                FROM students s
                LEFT JOIN faculty f ON s.department = f.department
                GROUP BY s.department
            """)
            records = cursor.fetchall()
            conn.close()
            headers = ["Department", "Number of Students", "Number of Faculty"]
        else:
            records = fetch_records(table)
            headers = (
                ["PRN", "Name", "Age", "Address", "Phone", "Email", "Department", "Gender", "Starting Year", "Duration"]
                if table == "Students"
                else ["Name", "Experience (Years)", "Education", "Department"]
            )

        if records:
            df = pd.DataFrame(records, columns=headers)

            if table == "Students":
                df["PRN"] = df["PRN"].astype(str)
                df["Starting Year"] = df["Starting Year"].astype(str)
               
            st.write(f"**{table.capitalize()} Records**")
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.warning(f"No {table} data found.")

    elif choice == "Search":
        st.subheader("Search Across All Tables")
        relation = st.selectbox("Select Table", ["Students", "Faculty", "Departments"])
        keyword = st.text_input("Enter keyword to search").strip()

        if st.button("Search", help="Submits the current query"):
            if not keyword:
                st.warning("Please enter a keyword.")
            else:
                conn = create_connection()
                cursor = conn.cursor()

                query = ""
                params = ()
                headers = []

                if relation == "Students":
                    cursor.execute("PRAGMA table_info(students)")
                    columns = [row[1] for row in cursor.fetchall()]
                    headers = ["PRN", "Name", "Age", "Address", "Phone", "Email", "Department", "Gender", "Starting Year", "Duration"]

                    if keyword.lower() in ["male", "female"]:
                        conditions = "LOWER(gender) = ?"
                        params = (keyword.lower(),)
                    else:
                        conditions = " OR ".join([f"LOWER({col}) LIKE ?" for col in columns])
                        params = tuple([f"%{keyword.lower()}%"] * len(columns))

                    query = f"SELECT * FROM students WHERE {conditions}"

                elif relation == "Faculty":
                    cursor.execute("PRAGMA table_info(faculty)")
                    columns = [row[1] for row in cursor.fetchall()]
                    headers = ["Name", "Experience (Years)", "Education", "Department"]

                    conditions = " OR ".join([f"LOWER({col}) LIKE ?" for col in columns])
                    query = f"SELECT * FROM faculty WHERE {conditions}"
                    params = tuple([f"%{keyword.lower()}%"] * len(columns))

                elif relation == "Departments":
                    query = """
                        SELECT s.department AS Department,
                            COUNT(DISTINCT s.prn) AS Students,
                            COUNT(DISTINCT f.name) AS Faculty
                        FROM students s
                        LEFT JOIN faculty f ON f.department = s.department
                        WHERE LOWER(s.department) LIKE ?
                        GROUP BY s.department
                    """
                    params = (f"%{keyword.lower()}%",)
                    headers = ["Department", "Number of Students", "Number of Faculty"]

                cursor.execute(query, params)
                records = cursor.fetchall()
                conn.close()

                if records:
                    df = pd.DataFrame(records, columns=headers)
                    if relation == "Students":
                        df["PRN"] = df["PRN"].astype(str)
                        if "Starting Year" in df.columns:
                            df["Starting Year"] = df["Starting Year"].astype(str)

                    st.write(f"**Search Results for {relation}**")
                    st.dataframe(df, use_container_width=True, hide_index=True)
                else:
                    st.warning("No records found.")

    elif choice == "Admin":
        admin_login()
    
if __name__ == "__main__":
    main()