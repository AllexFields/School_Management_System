import streamlit as st
import pandas as pd
import re

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="School Management System",
    page_icon="🏫",
    layout="centered"
)

# ---------------- TITLE ---------------- #

st.title("🏫 School Management System")
st.write("Manage student records easily")

# ---------------- SESSION STORAGE ---------------- #

if "students" not in st.session_state:
    st.session_state.students = []

if "student_id" not in st.session_state:
    st.session_state.student_id = 1

# ---------------- SIDEBAR MENU ---------------- #

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

        if not name.strip():
            st.error("Student name cannot be empty")

        elif not all(i.isalpha() for i in name.split()):
            st.error("Only alphabets are allowed in name")

        elif not re.match(pattern, contact):
            st.error(
                "Invalid contact number. Must start from 6-9 and contain 10 digits"
            )

        else:

            student = {
                "ID": st.session_state.student_id,
                "Name": name.title(),
                "Age": age,
                "Standard": standard,
                "Contact": contact
            }

            st.session_state.students.append(student)

            st.session_state.student_id += 1

            st.success("✅ Student Registered Successfully")

# =========================================================
# VIEW STUDENTS
# =========================================================

elif menu == "View Students":

    st.header("📋 All Student Records")

    if st.session_state.students:

        df = pd.DataFrame(st.session_state.students)

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

        found = False

        for student in st.session_state.students:

            if student["ID"] == search_id:

                found = True

                st.success("Student Found")

                st.write(f"### ID: {student['ID']}")
                st.write(f"**Name:** {student['Name']}")
                st.write(f"**Age:** {student['Age']}")
                st.write(f"**Standard:** {student['Standard']}")
                st.write(f"**Contact:** {student['Contact']}")

        if not found:
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

    found = False

    for student in st.session_state.students:

        if student["ID"] == update_id:

            found = True

            st.success("Student Found")

            st.write(f"### Current Record")
            st.write(student)

            new_standard = st.selectbox(
                "Update Standard",
                list(range(1, 13))
            )

            new_contact = st.text_input(
                "Update Contact Number",
                value=student["Contact"]
            )

            if st.button("Update Student"):

                pattern = r'^[6-9]\d{9}$'

                if not re.match(pattern, new_contact):

                    st.error("Invalid Contact Number")

                else:

                    student["Standard"] = new_standard
                    student["Contact"] = new_contact

                    st.success("✅ Student Updated Successfully")

    if not found:
        st.warning("Student ID not found")

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

        found = False

        for student in st.session_state.students:

            if student["ID"] == delete_id:

                st.session_state.students.remove(student)

                found = True

                st.success("✅ Student Deleted Successfully")

                break

        if not found:
            st.error("Student ID Not Found")