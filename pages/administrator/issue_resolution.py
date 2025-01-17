import streamlit as st
import pandas as pd
from utils.database import fetch_all, execute_query, get_db_connection
import sqlite3
'''
def load_issues():
    """Load issues from the database and return as a DataFrame."""
    query = "SELECT * FROM issue_resolution"
    results = fetch_all(query)
    
    if results:
        columns = [column[0] for column in get_db_connection().execute(query).description]
        return pd.DataFrame(results, columns=columns)
    
    return pd.DataFrame()

def create_issue_from_feedback(user_id, issue_description):
    """Create a new issue in the issue_resolution table from feedback."""
    query = """
    INSERT INTO issue_resolution (reported_by, issue_description, resolution_status)
    VALUES (?, ?, 'Pending')
    """
    execute_query(query, (user_id, issue_description))
''
def update_issue_resolution(issue_id, resolution_notes, resolution_status):
    """Update the issue resolution notes and status."""
    query = """
    UPDATE issue_resolution
    SET resolution_notes = ?, resolution_status = ?, resolved_at = CURRENT_TIMESTAMP
    WHERE id = ?
    """
    try:
        execute_query(query, (resolution_notes, resolution_status, issue_id))
        st.success(f"Updated Issue ID {issue_id}: Status={resolution_status}, Notes={resolution_notes}")
    except Exception as e:
        st.error(f"Error updating issue: {e}")
''

def update_issue_resolution(issue_id, resolution_notes, resolution_status):
    """Update the issue resolution notes and status in the database."""
    query = """
    UPDATE issue_resolution
    SET resolution_notes = ?, resolution_status = ?, resolved_at = CURRENT_TIMESTAMP
    WHERE id = ?
    """
    # Establish database connection
    conn = None
    try:
        # Adjust this path to point to your SQLite database
        conn = sqlite3.connect("path/to/your/database.db")
        cursor = conn.cursor()
        
        # Execute the query with provided parameters
        cursor.execute(query, (resolution_notes, resolution_status, issue_id))
        conn.commit()

        st.success(f"Updated Issue ID {issue_id}: Status={resolution_status}, Notes={resolution_notes}")
    except sqlite3.Error as e:
        st.error(f"Error updating issue: {e}")
    finally:
        # Ensure the connection is closed
        if conn:
            conn.close()




def load_feedback():
    """Load feedback from the database and return as a DataFrame."""
    query = "SELECT * FROM feedback"
    results = fetch_all(query)
    
    if results:
        columns = [column[0] for column in get_db_connection().execute(query).description]
        return pd.DataFrame(results, columns=columns)
    
    return pd.DataFrame()

def show_issue_resolution_page():
    st.title("Issue Resolution")

    # Load and display feedback
    st.subheader("Feedback")
    feedback_df = load_feedback()
    st.dataframe(feedback_df)
    
    if feedback_df.empty:
        st.warning("No feedback found.")
    else:
        selected_feedback_id = st.selectbox("Select Feedback to Convert to Issue", feedback_df["id"])

        # Get the selected feedback details
        selected_feedback = feedback_df[feedback_df["id"] == selected_feedback_id]
        
        if not selected_feedback.empty:
            feedback_row = selected_feedback.iloc[0]
            st.write(f"**Feedback ID:** {feedback_row['id']}")
            st.write(f"**User ID:** {feedback_row['user_id']}")
            st.write(f"**Feedback Type:** {feedback_row['feedback_type']}")
            st.write(f"**Feedback Text:** {feedback_row['feedback_text']}")
        
            # Form to create an issue from the selected feedback
            if st.button("Create Issue from Feedback"):
                user_id = st.session_state.user_id  # Get user_id from session state
                if user_id is not None:
                    create_issue_from_feedback(user_id, feedback_row['feedback_text'])
                    st.success(f"Issue has been created from feedback ID {feedback_row['id']}.")
                else:
                    st.error("User ID is not available. Cannot create issue.")
                st.rerun()

    # Load and display existing issues
    st.subheader("Existing Issues")
    issues_df = load_issues()
    st.dataframe(issues_df)
    
    if issues_df.empty:
        st.warning("No issues found.")
    else:
        selected_issue_id = st.selectbox("Select Issue to Edit", issues_df["id"])
        selected_issue = issues_df[issues_df["id"] == selected_issue_id]

        if not selected_issue.empty:
            issue_row = selected_issue.iloc[0]
            st.write(f"**Issue ID:** {issue_row['id']}")
            st.write(f"**Reported By:** {issue_row['reported_by']}")
            st.write(f"**Issue Description:** {issue_row['issue_description']}")
            st.write(f"**Resolution Status:** {issue_row['resolution_status']}")
            st.write(f"**Resolution Notes:** {issue_row.get('resolution_notes', 'No notes added.')}")

            # Input for resolution notes
            resolution_notes = st.text_area("Add/Edit Resolution Notes", value=issue_row.get('resolution_notes', ''))

            # Dropdown for resolution status
            resolution_status = st.selectbox("Select Resolution Status", ["Pending", "Resolved"], 
                                              index=["Pending", "Resolved"].index(issue_row['resolution_status']))
            
            if st.button("Update Issue Resolution"):
                update_issue_resolution(issue_row['id'], resolution_notes, resolution_status)
                st.rerun()  # Refresh to show updated data

if __name__ == "__main__":
    show_issue_resolution_page()
'''
'''
import streamlit as st
import pandas as pd
import sqlite3
from utils.database import fetch_all, execute_query, get_db_connection

# Helper function to connect directly for isolated debug
def get_connection():
    return sqlite3.connect("path/to/your/database.db")

# Load all issues from the database and return as a DataFrame
def load_issues():
    query = "SELECT * FROM issue_resolution"
    results = fetch_all(query)
    
    if results:
        columns = [column[0] for column in get_db_connection().execute(query).description]
        return pd.DataFrame(results, columns=columns)
    return pd.DataFrame()

# Create an issue from feedback data
def create_issue_from_feedback(user_id, issue_description):
    query = """
    INSERT INTO issue_resolution (reported_by, issue_description, resolution_status)
    VALUES (?, ?, 'Pending')
    """
    try:
        execute_query(query, (user_id, issue_description))
        st.success(f"Issue created from feedback with user ID {user_id}.")
    except Exception as e:
        st.error(f"Failed to create issue from feedback: {e}")

# Update issue resolution
def update_issue_resolution(issue_id, resolution_notes, resolution_status):
    query = """
    UPDATE issue_resolution
    SET resolution_notes = ?, resolution_status = ?, resolved_at = CURRENT_TIMESTAMP
    WHERE id = ?
    """
    try:
        execute_query(query, (resolution_notes, resolution_status, issue_id))
        st.success(f"Issue ID {issue_id} updated successfully.")
        # Set a flag to reload issues in session state
        st.session_state['issues_updated'] = True
    except Exception as e:
        st.error(f"Error updating issue: {e}")

# Load all feedback from the database as a DataFrame
def load_feedback():
    query = "SELECT * FROM feedback"
    results = fetch_all(query)
    
    if results:
        columns = [column[0] for column in get_db_connection().execute(query).description]
        return pd.DataFrame(results, columns=columns)
    return pd.DataFrame()

# Main Issue Resolution Page
def show_issue_resolution_page():
    st.title("Issue Resolution")

    # Display feedback and allow creating an issue
    st.subheader("Feedback")
    feedback_df = load_feedback()
    st.dataframe(feedback_df)
    
    if feedback_df.empty:
        st.warning("No feedback found.")
    else:
        selected_feedback_id = st.selectbox("Select Feedback to Convert to Issue", feedback_df["id"])
        selected_feedback = feedback_df[feedback_df["id"] == selected_feedback_id]
        
        if not selected_feedback.empty:
            feedback_row = selected_feedback.iloc[0]
            st.write(f"**Feedback ID:** {feedback_row['id']}")
            st.write(f"**User ID:** {feedback_row['user_id']}")
            st.write(f"**Feedback Type:** {feedback_row['feedback_type']}")
            st.write(f"**Feedback Text:** {feedback_row['feedback_text']}")
        
            if st.button("Create Issue from Feedback"):
                user_id = feedback_row['user_id']
                create_issue_from_feedback(user_id, feedback_row['feedback_text'])
                feedback_df = load_feedback()

    # Display and update issues
    st.subheader("Existing Issues")
    # Reload issues if an update occurred
    if 'issues_updated' in st.session_state and st.session_state['issues_updated']:
        issues_df = load_issues()
        st.session_state['issues_updated'] = False
    else:
        issues_df = load_issues()
    
    st.dataframe(issues_df)
    
    if issues_df.empty:
        st.warning("No issues found.")
    else:
        selected_issue_id = st.selectbox("Select Issue to Edit", issues_df["id"])
        selected_issue = issues_df[issues_df["id"] == selected_issue_id]

        if not selected_issue.empty:
            issue_row = selected_issue.iloc[0]
            st.write(f"**Issue ID:** {issue_row['id']}")
            st.write(f"**Reported By:** {issue_row['reported_by']}")
            st.write(f"**Issue Description:** {issue_row['issue_description']}")
            st.write(f"**Resolution Status:** {issue_row['resolution_status']}")
            st.write(f"**Resolution Notes:** {issue_row.get('resolution_notes', 'No notes added.')}")

            # Update form
            resolution_notes = st.text_area("Add/Edit Resolution Notes", value=issue_row.get('resolution_notes', ''))
            resolution_status = st.selectbox("Select Resolution Status", ["Pending", "Resolved"], 
                                              index=["Pending", "Resolved"].index(issue_row['resolution_status']))
            
            if st.button("Update Issue Resolution"):
                update_issue_resolution(issue_row['id'], resolution_notes, resolution_status)

if __name__ == "__main__":
    show_issue_resolution_page()

'''
import streamlit as st
import pandas as pd
from datetime import datetime
from utils.database import fetch_all, execute_query, get_db_connection
from datetime import datetime

# Load issues from CSV
def load_issues_from_csv():
    try:
        return pd.read_csv('data/issues.csv')
    except FileNotFoundError:
        return pd.DataFrame(columns=["id", "reported_by", "issue_description", "resolution_status", "resolution_notes", "created_at", "resolved_at"])

# Save issues to CSV
def save_issues_to_csv(df):
    df.to_csv('data/issues.csv', index=False)

# Create an issue from feedback
# Create an issue from feedback
def create_issue_from_feedback(user_id, issue_description):
    """Create a new issue in the CSV from feedback."""
    try:
        # Load existing issues
        issues_df = load_issues_from_csv()
        
        # Get the next issue ID
        new_issue_id = issues_df['id'].max() + 1 if not issues_df.empty else 1
        
        # Create a new issue DataFrame
        new_issue = pd.DataFrame({
            "id": [new_issue_id],
            "reported_by": [user_id],
            "issue_description": [issue_description],
            "resolution_status": ["Pending"],
            "resolution_notes": [None],
            "created_at": [datetime.now()],
            "resolved_at": [None]
        })
        
        # Concatenate the new issue with the existing issues DataFrame
        issues_df = pd.concat([issues_df, new_issue], ignore_index=True)
        
        # Save to CSV
        save_issues_to_csv(issues_df)
        st.success(f"Issue created from feedback with user ID {user_id}.")
    except Exception as e:
        st.error(f"Failed to create issue from feedback: {e}")


# Update issue resolution
def update_issue_in_csv(issue_id, resolution_notes, resolution_status):
    issues_df = load_issues_from_csv()
    if issue_id not in issues_df['id'].values:
        st.error(f"No issue found with ID {issue_id}.")
        return

    issues_df.loc[issues_df['id'] == issue_id, 'resolution_notes'] = resolution_notes
    issues_df.loc[issues_df['id'] == issue_id, 'resolution_status'] = resolution_status
    issues_df.loc[issues_df['id'] == issue_id, 'resolved_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    save_issues_to_csv(issues_df)
    st.success(f"Issue ID {issue_id} updated successfully.")
    st.session_state['issues_updated'] = True  # Mark as updated

# Load feedback from the database
def load_feedback():
    query = "SELECT * FROM feedback"
    results = fetch_all(query)
    if results:
        columns = [column[0] for column in get_db_connection().execute(query).description]
        return pd.DataFrame(results, columns=columns)
    return pd.DataFrame()

# Main Issue Resolution Page
def show_issue_resolution_page():
    st.title("Issue Resolution")
    if 'issues_updated' not in st.session_state:
        st.session_state['issues_updated'] = False

    st.subheader("Feedback")
    feedback_df = load_feedback()
    st.dataframe(feedback_df)

    if feedback_df.empty:
        st.warning("No feedback found.")
    else:
        selected_feedback_id = st.selectbox("Select Feedback to Convert to Issue", feedback_df["id"])
        selected_feedback = feedback_df[feedback_df["id"] == selected_feedback_id]

        if not selected_feedback.empty:
            feedback_row = selected_feedback.iloc[0]
            st.write(f"**Feedback ID:** {feedback_row['id']}")
            st.write(f"**User ID:** {feedback_row['user_id']}")
            st.write(f"**Feedback Type:** {feedback_row['feedback_type']}")
            st.write(f"**Feedback Text:** {feedback_row['feedback_text']}")

            if st.button("Create Issue from Feedback"):
                user_id = feedback_row['user_id']
                create_issue_from_feedback(user_id, feedback_row['feedback_text'])

    st.subheader("Existing Issues")
    issues_df = load_issues_from_csv()
    if st.session_state['issues_updated']:
        st.write("Issues have been updated, reloading data...")
        issues_df = load_issues_from_csv()
        st.session_state['issues_updated'] = False

    st.dataframe(issues_df)

    if issues_df.empty:
        st.warning("No issues found.")
    else:
        selected_issue_id = st.selectbox("Select Issue to Edit", issues_df["id"])
        selected_issue = issues_df[issues_df["id"] == selected_issue_id]

        if not selected_issue.empty:
            issue_row = selected_issue.iloc[0]
            st.write(f"**Issue ID:** {issue_row['id']}")
            st.write(f"**Reported By:** {issue_row['reported_by']}")
            st.write(f"**Issue Description:** {issue_row['issue_description']}")
            st.write(f"**Resolution Status:** {issue_row['resolution_status']}")
            st.write(f"**Resolution Notes:** {issue_row.get('resolution_notes', 'No notes added.')}")

            resolution_notes = st.text_area("Add/Edit Resolution Notes", value=issue_row.get('resolution_notes', ''))
            resolution_status = st.selectbox("Select Resolution Status", ["Pending", "Resolved"],
                                             index=["Pending", "Resolved"].index(issue_row['resolution_status']))

            if st.button("Update Issue Resolution"):
                st.write(f"Updating issue ID {issue_row['id']} with notes '{resolution_notes}' and status '{resolution_status}'")
                update_issue_in_csv(issue_row['id'], resolution_notes, resolution_status)

    if st.button("Refresh Issues"):
        st.write("Manual refresh triggered.")
        st.session_state['issues_updated'] = True

if __name__ == "__main__":
    show_issue_resolution_page()
