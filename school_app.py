import streamlit as st
import pandas as pd
import sqlite3
import re

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="School Management System",
    page_icon="🏫",
    layout="centered"
)

# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_connection():
    return sqlite3.connect("school.db")

conn = get_connection()
cursor = conn.cursor()

# =========================================================
# CREATE TABLE
# =========================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Age INTEGER NOT NULL,
    Standard INTEGER NOT NULL,
    Contact TEXT NOT NULL
)
""")

conn.commit()

# =========================================================
# TITLE
# =========================================================

st.title("🏫 School Management System")
st.write("Manage student records easily")

# =========================================================
# SIDEBAR MENU
# =========================================================

menu = st.sidebar.selectbox(
    "Select Option",
    [
        "New Admission",
        "View Students",
        "Search Student",
        "Update Student",
        "Delete Student"
    ]
)

# =========================================================
# NEW ADMISSION
# =========================================================

if menu == "New Admission":

    st.header("📝 New Student Admission")

    name = st.text_input("Enter Student Name")

    age = st.number_input(
        "Enter Age",
        min_value=5,
        max_value=18,
        step=1
    )

    standard = st.selectbox(
        "Select Standard",
        list(range(1, 13))
    )

    contact = st.text_input(
        "Enter Guardian Contact Number"
    )

    if st.button("Register Student"):

        pattern = r'^[6-9]\d{9}$'

        # VALIDATIONS

        if not name.strip():

            st.error("Student name cannot be empty")

        elif not all(i.isalpha() for i in name.split()):

            st.error("Only alphabets are allowed in name")

        elif not re.match(pattern, contact):

            st.error(
                "Invalid contact number. Must start from 6-9 and contain 10 digits"
            )

        else:

            # INSERT DATA INTO DATABASE

            cursor.execute("""
            INSERT INTO students(Name, Age, Standard, Contact)
            VALUES (?, ?, ?, ?)
            """, (name.title(), age, standard, contact))

            conn.commit()

            st.success("✅ Student Registered Successfully")

# =========================================================
# VIEW STUDENTS
# =========================================================

elif menu == "View Students":

    st.header("📋 All Student Records")

    df = pd.read_sql_query(
        "SELECT * FROM students",
        conn
    )

    if not df.empty:

        st.dataframe(
            df,
            use_container_width=True
        )

    else:

        st.warning("No student records found")

# =========================================================
# SEARCH STUDENT
# =========================================================

elif menu == "Search Student":

    st.header("🔍 Search Student By ID")

    search_id = st.number_input(
        "Enter Student ID",
        min_value=1,
        step=1
    )

    if st.button("Search"):

        cursor.execute("""
        SELECT * FROM students
        WHERE ID = ?
        """, (search_id,))

        student = cursor.fetchone()

        if student:

            st.success("Student Found")

            st.write(f"### ID: {student[0]}")
            st.write(f"**Name:** {student[1]}")
            st.write(f"**Age:** {student[2]}")
            st.write(f"**Standard:** {student[3]}")
            st.write(f"**Contact:** {student[4]}")

        else:

            st.error("Student Not Found")

# =========================================================
# UPDATE STUDENT
# =========================================================

elif menu == "Update Student":

    st.header("✏️ Update Student Information")

    update_id = st.number_input(
        "Enter Student ID",
        min_value=1,
        step=1
    )

    if st.button("Find Student"):

        cursor.execute("""
        SELECT * FROM students
        WHERE ID = ?
        """, (update_id,))

        student = cursor.fetchone()

        if student:

            st.success("Student Found")

            st.write("### Current Record")

            st.write({
                "ID": student[0],
                "Name": student[1],
                "Age": student[2],
                "Standard": student[3],
                "Contact": student[4]
            })

            # STORE ID IN SESSION
            st.session_state.update_id = update_id

        else:

            st.error("Student ID Not Found")

    # SHOW UPDATE FORM

    if "update_id" in st.session_state:

        new_standard = st.selectbox(
            "Update Standard",
            list(range(1, 13))
        )

        new_contact = st.text_input(
            "Update Contact Number"
        )

        if st.button("Update Student"):

            pattern = r'^[6-9]\d{9}$'

            if not re.match(pattern, new_contact):

                st.error("Invalid Contact Number")

            else:

                cursor.execute("""
                UPDATE students
                SET Standard = ?, Contact = ?
                WHERE ID = ?
                """, (
                    new_standard,
                    new_contact,
                    st.session_state.update_id
                ))

                conn.commit()

                st.success("✅ Student Updated Successfully")

                del st.session_state.update_id

# =========================================================
# DELETE STUDENT
# =========================================================

elif menu == "Delete Student":

    st.header("🗑️ Delete Student Record")

    delete_id = st.number_input(
        "Enter Student ID",
        min_value=1,
        step=1
    )

    if st.button("Delete Student"):

        cursor.execute("""
        SELECT * FROM students
        WHERE ID = ?
        """, (delete_id,))

        student = cursor.fetchone()

        if student:

            cursor.execute("""
            DELETE FROM students
            WHERE ID = ?
            """, (delete_id,))

            conn.commit()

            st.success("✅ Student Deleted Successfully")

        else:

            st.error("Student ID Not Found")

# =========================================================
# CLOSE DATABASE CONNECTION
# =========================================================

conn.close()
