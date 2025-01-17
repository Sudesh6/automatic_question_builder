# import streamlit as st
# from utils.notifications import get_unseen_notifications

# from pages.employee.request_question_bank import request_question_bank
# from pages.employee.self_assessment import self_assessment
# from pages.employee.submit_feedback import submit_feedback
# from pages.employee.learning_development import learning_development
# from pages.employee.request_learning_plan import request_learning_plan

# def show_employee_dashboard():
#     st.title("Employee Dashboard")
#     st.write(f"Welcome, {st.session_state.username}")

#     user_id = st.session_state.user_id  # Assuming user_id is stored in session state
#     notifications = get_unseen_notifications(user_id)
#     unread_count = len(notifications)

#     # Change button text based on unread notifications
#     notification_button_text = f"Notifications ({unread_count})"
#     notification_button_color = "green" if unread_count > 0 else "gray"

#     st.subheader("Quick Links")
#     if st.button("Request Question Bank"):
#         st.session_state.page = "request_question_bank"
#     if st.button("Self-Assessment"):
#         st.session_state.page = "self_assessment"
#     if st.button("Submit Feedback"):
#         st.session_state.page = "submit_feedback"
#     if st.button("Learning and Development"):
#         st.session_state.page = "learning_development"
#     if st.button("Request Learning Plan"):
#         st.session_state.page = "request_learning_plan"
    
#     # Notification button with dynamic text
#     if st.button(notification_button_text):
#         st.session_state.page = "notifications"  # Redirect to notifications page

#     # Logout button logic
#     if st.button("Logout"):
#         # Clear session state
#         st.session_state.authenticated = False
#         st.session_state.role = None
#         st.session_state.username = ''
#         st.session_state.user_id = None  # Clear user ID
#         st.session_state.page = "login"  # Set the page to login
#         st.rerun()  # Refresh to redirect to login page

#     # Check and load the correct page
#     if 'page' in st.session_state:
#         if st.session_state.page == "request_question_bank":
#             request_question_bank()
#         elif st.session_state.page == "self_assessment":
#             self_assessment()
#         elif st.session_state.page == "submit_feedback":
#             submit_feedback()
#         elif st.session_state.page == "learning_development":
#             learning_development()
#         elif st.session_state.page == "request_learning_plan":
#             request_learning_plan()
#         elif st.session_state.page == "notifications":
#             # Load the notifications page here
#             from pages.employee.notifications import show_notifications_page
#             show_notifications_page()  # Adjust this import based on your file structure

# if __name__ == "__main__":
#     show_employee_dashboard()

import streamlit as st
from utils.notifications import get_unseen_notifications

from pages.employee.request_question_bank import request_question_bank
from pages.employee.self_assessment import self_assessment
from pages.employee.submit_feedback import submit_feedback
from pages.employee.learning_development import learning_development
from pages.employee.request_learning_plan import request_learning_plan
from pages.employee.notifications import show_notifications_page  # Importing notifications page

def show_employee_dashboard():
    st.title("Employee Dashboard")
    st.write(f"Welcome, {st.session_state.username}")

    user_id = st.session_state.user_id  # Assuming user_id is stored in session state
    notifications = get_unseen_notifications(user_id)
    unread_count = len(notifications)

    # Change button text based on unread notifications
    notification_button_text = f"Notifications ({unread_count})"
    
    # Add custom CSS to increase tab font size
    st.markdown(
        """
        <style>
        .streamlit-tabs .tab {
            font-size: 40px;  /* Change this value to adjust font size */
            font-weight: bold; /* Optional: make the font bold */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Create tabs for the different sections
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
        ["Request Question Bank", "Self-Assessment", "Submit Feedback", 
         "Learning and Development", "Request Learning Plan", "Notifications", "Logout"]
    )

    # Display the appropriate content in each tab
    with tab1:
        request_question_bank()
    
    with tab2:
        self_assessment()
    
    with tab3:
        submit_feedback()
    
    with tab4:
        learning_development()
    
    with tab5:
        request_learning_plan()
    
    with tab6:
        show_notifications_page()

    # Logout tab functionality
    with tab7:
        if st.button("Logout"):
            # Clear session state
            st.session_state.authenticated = False
            st.session_state.role = None
            st.session_state.username = ''
            st.session_state.user_id = None  # Clear user ID
            st.session_state.page = "login"  # Set the page to login
            st.rerun()  # Refresh to redirect to login page

if __name__ == "__main__":
    show_employee_dashboard()
