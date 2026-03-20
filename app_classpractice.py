import streamlit as st
import json
from pathlib import Path
from datetime import datetime

st.set_page_config("Excused Absence App", layout="wide", initial_sidebar_state="expanded")

if "page" not in st.session_state:
    st.session_state["page"] = "dashboard"

if "selected_request" not in st.session_state:
    st.session_state["selected_request"] = None

json_path_requests = Path("requests.json")

try:
    with open(json_path_requests, "r") as f:
        requests = json.load(f)
except:
    requests = []

with st.sidebar:
    if st.button("Dashboard", key="dashboard_btn", type="primary", use_container_width=True):
        st.session_state["page"] = "dashboard"
        st.session_state["selected_request"] = None
        st.rerun()

    if st.button("Request", key="request_btn", type="primary", use_container_width=True):
        st.session_state["page"] = "request"
        st.session_state["selected_request"] = None
        st.rerun()

if st.session_state["page"] == "dashboard":
    col1, col2 = st.columns([4, 2])

    with col1:
        st.markdown("## Excused Absence Dashboard")

        if len(requests) > 0:
            event = st.dataframe(
                requests,
                use_container_width=True,
                on_select="rerun",
                selection_mode="single-row",
                key="requests_table"
            )

            if event.selection.rows:
                index = event.selection.rows[0]
                st.session_state["selected_request"] = requests[index]

            if st.session_state["selected_request"]:
                selected = st.session_state["selected_request"]

                st.markdown("### Selected Request")
                st.write(f"Status: {selected['status']}")
                st.write(f"Course ID: {selected['course_id']}")
                st.write(f"Email: {selected['student_email']}")
                st.write(f"Absence Date: {selected['absence_date']}")
                st.write(f"Submitted: {selected['submitted_timestamp']}")
                st.write(f"Excuse Type: {selected['excuse_type']}")
                st.write(f"Explanation: {selected['explanation']}")
                st.write(f"Instructor Note: {selected['instructor_note']}")
        else:
            st.warning("No requests found")

    with col2:
        st.metric("Total Requests", f"{len(requests)}")

elif st.session_state["page"] == "request":
    st.markdown("## Submit Excused Absence Request")
    st.markdown("Under Construction...")

    tab1, tab2 = st.tabs(["New Request", "Info"])

    with tab1:
        col1, col2 = st.columns([3, 3])

        with col1:
            student_email = st.text_input("Student Email", key="email_input")

            absence_date = st.date_input("Absence Date", key="date_input")

            excuse_type = st.selectbox(
                "Excuse Type",
                ["Medical", "University Competitions", "Other"],
                key="excuse_input"
            )

            explanation = st.text_area("Explanation", key="explanation_input")

            if st.button("Submit Request", key="submit_request_btn", type="primary", use_container_width=True):

                if student_email == "" or explanation == "":
                    st.warning("Please fill in all required fields")

                else:
                    date_str = absence_date.strftime("%Y-%m-%d")

                    new_request = {
                        "request_id":"0111212",
                        "status": "Pending",
                        "course_id": "011101",
                        "student_email": student_email,
                        "absence_date": date_str,
                        "submitted_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "excuse_type": excuse_type,
                        "explanation": explanation,
                        "instructor_note": ""
                    }

                    requests.append(new_request)

                    with open(json_path_requests, "w") as f:
                        json.dump(requests, f, indent=4)

                    st.success("Request submitted")

                    st.session_state["page"] = "dashboard"
                    st.rerun()

        with col2:
            st.info("More features coming soon")

    with tab2:
        st.write("This section is under development")