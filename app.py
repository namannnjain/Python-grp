
import streamlit as st

st.set_page_config(page_title="Smart Campus Allocator", page_icon="🏫")

# RESOURCE DICTIONARY
resources = {
    1: "Seminar Hall",
    2: "Computer Lab",
    3: "Conference Room",
    4: "Classroom 101",
    5: "Projector"
}

# CREATE FILE IF IT DOES NOT EXIST
open("bookings.txt", "a").close()


# 1. LOAD BOOKINGS
def load_bookings():
    bookings = []
    file = open("bookings.txt", "r")

    for line in file:
        data = line.strip().split(",")

        if len(data) == 5:
            bookings.append({
                "enrollment": data[0],
                "resource": data[1],
                "day": data[2],
                "start": data[3],
                "end": data[4]
            })

    file.close()
    return bookings


# 2. SAVE BOOKING
def save_booking(enrollment, resource, day, start, end):
    file = open("bookings.txt", "a")

    file.write(
        enrollment + "," + resource + "," + day + "," +
        str(start) + "," + str(end) + "\n"
    )

    file.close()


# 3. CHECK CONFLICT
def check_conflict(resource, day, start, end):
    bookings = load_bookings()

    for b in bookings:
        if b["resource"] == resource and b["day"] == day:

            old_start = int(b["start"])
            old_end = int(b["end"])

            if start < old_end and end > old_start:
                return True

    return False


# LOGIN SESSION
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "enrollment" not in st.session_state:
    st.session_state.enrollment = ""


# LOGIN PAGE
if not st.session_state.logged_in:

    st.title("🏫 Smart Campus Resource Allocator")
    st.subheader("Student Login")

    enrollment = st.text_input("Enter Enrollment Number")

    if st.button("Login"):
        if enrollment.strip():
            st.session_state.enrollment = enrollment.strip()
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Enter Enrollment Number")


# MAIN APPLICATION
else:

    st.sidebar.title("Smart Campus")
    st.sidebar.write("Welcome " + st.session_state.enrollment)

    menu = st.sidebar.radio("Menu", [
        "Dashboard",
        "Resource Catalog",
        "Book a Resource",
        "My Bookings"
    ])

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.enrollment = ""
        st.rerun()


    # DASHBOARD
    if menu == "Dashboard":

        st.title("Student Dashboard")

        bookings = load_bookings()
        count = 0

        for b in bookings:
            if b["enrollment"] == st.session_state.enrollment:
                count += 1

        col1, col2 = st.columns(2)
        col1.metric("Total Resources", len(resources))
        col2.metric("My Bookings", count)

        st.success("Welcome to Smart Campus!")


    # RESOURCE CATALOG
    elif menu == "Resource Catalog":

        st.title("Resource Catalog")

        for key, value in resources.items():
            st.write(key, "-", value)


    # BOOK A RESOURCE
    elif menu == "Book a Resource":

        st.title("Book a Resource")

        with st.form("booking"):

            resource = st.selectbox(
                "Select Resource", list(resources.values())
            )

            day = st.selectbox("Select Day", [
                "Monday", "Tuesday", "Wednesday",
                "Thursday", "Friday", "Saturday", "Sunday"
            ])

            start = st.number_input("Starting Hour", 0, 23, 10)
            end = st.number_input("Ending Hour", 1, 24, 11)

            submit = st.form_submit_button("Confirm Booking")

        if submit:

            if start >= end:
                st.error("Invalid Time Slot")

            elif check_conflict(resource, day, start, end):
                st.error("Conflict Detected! Already Booked.")

            else:
                save_booking(
                    st.session_state.enrollment,
                    resource, day, start, end
                )

                st.success("Booking Successful!")


    # MY BOOKINGS
    elif menu == "My Bookings":

        st.title("My Bookings")

        bookings = load_bookings()
        found = False

        for b in bookings:

            if b["enrollment"] == st.session_state.enrollment:

                found = True

                st.write("Resource:", b["resource"])
                st.write("Day:", b["day"])
                st.write("Time:", b["start"], "to", b["end"])
                st.divider()

        if not found:
            st.info("No Bookings Found")
