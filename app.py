# # # # # # # import streamlit as st
# # # # # # # import requests

# # # # # # # # Function to navigate to different pages
# # # # # # # def navigate_to(page_name):
# # # # # # #     st.session_state.page = page_name

# # # # # # # # Function to handle login
# # # # # # # def login(username, password):
# # # # # # #     session = requests.Session()
    
# # # # # # #     # Fetch CSRF token
# # # # # # #     response = session.get('http://localhost:8000/csrf/')
# # # # # # #     if response.status_code == 200:
# # # # # # #         csrftoken = session.cookies.get('csrftoken')
# # # # # # #     else:
# # # # # # #         st.error(f"Failed to fetch CSRF token. Status code: {response.status_code}")
# # # # # # #         return False
    
# # # # # # #     # Perform login request
# # # # # # #     login_data = {
# # # # # # #         'username': username,
# # # # # # #         'password': password,
# # # # # # #         'csrfmiddlewaretoken': csrftoken
# # # # # # #     }
# # # # # # #     response = session.post('http://localhost:8000/login/', data=login_data)
    
# # # # # # #     # Check login response
# # # # # # #     if response.status_code == 200 and 'Please enter a correct username and password.' not in response.text:
# # # # # # #         st.session_state.logged_in = True
# # # # # # #         st.session_state.session = session
# # # # # # #         navigate_to('Inbox')  # Redirect to inbox page upon successful login
# # # # # # #         return True
# # # # # # #     else:
# # # # # # #         st.error("Login failed. Please check your username and password.")
# # # # # # #         return False

# # # # # # # # Function to save message as draft
# # # # # # # def save_draft(to, subject, content):
# # # # # # #     session = st.session_state.session
    
# # # # # # #     # Prepare draft message data
# # # # # # #     draft_data = {
# # # # # # #         'recipient': to,
# # # # # # #         'subject': subject,
# # # # # # #         'body': content,
# # # # # # #         'action': 'Save as Draft'  # Specify the action to save as draft on the Django side
# # # # # # #     }
    
# # # # # # #     headers = {'X-CSRFToken': session.cookies.get('csrftoken')}  # Include CSRF token in headers
    
# # # # # # #     response = session.post('http://localhost:8000/compose/', data=draft_data, headers=headers)
    
# # # # # # #     if response.status_code == 200:
# # # # # # #         st.success('Draft saved successfully.')
# # # # # # #     else:
# # # # # # #         st.error(f"Failed to save draft. Status code: {response.status_code}")

# # # # # # # # Function to send message
# # # # # # # def send_message(to_username, subject, content):
# # # # # # #     session = st.session_state.session
    
# # # # # # #     # Prepare message data
# # # # # # #     message_data = {
# # # # # # #         'recipient': to_username,
# # # # # # #         'subject': subject,
# # # # # # #         'body': content,
# # # # # # #         'action': 'Send'  # Specify the action to send message on the Django side
# # # # # # #     }
    
# # # # # # #     headers = {'X-CSRFToken': session.cookies.get('csrftoken')}  # Include CSRF token in headers
    
# # # # # # #     response = session.post('http://localhost:8000/compose/', data=message_data, headers=headers)
    
# # # # # # #     if response.status_code == 200:
# # # # # # #         st.success('Message sent successfully.')
# # # # # # #     else:
# # # # # # #         st.error(f"Failed to send message. Status code: {response.status_code}")

# # # # # # # # Streamlit code for login, inbox page, and sidebar
# # # # # # # def main():
# # # # # # #     st.title("Mail Application")

# # # # # # #     # Initialize session state for storing logged-in status and current page
# # # # # # #     if 'logged_in' not in st.session_state:
# # # # # # #         st.session_state.logged_in = False
# # # # # # #     if 'page' not in st.session_state:
# # # # # # #         st.session_state.page = None

# # # # # # #     # Sidebar navigation
# # # # # # #     st.sidebar.title("Navigation")
# # # # # # #     if st.session_state.logged_in:
# # # # # # #         pages = ['Inbox', 'Compose', 'Drafts', 'Sent', 'Logout']
# # # # # # #     else:
# # # # # # #         pages = ['Login']
    
# # # # # # #     selected_page = st.sidebar.radio("Go to", pages)

# # # # # # #     if selected_page == 'Login':
# # # # # # #         # Login form
# # # # # # #         username = st.text_input("Username")
# # # # # # #         password = st.text_input("Password", type="password")
# # # # # # #         if st.button("Login"):
# # # # # # #             if login(username, password):
# # # # # # #                 st.success('Logged in successfully.')
# # # # # # #             # No need for else as login function handles errors

# # # # # # #     elif selected_page == 'Inbox':
# # # # # # #         st.write("Welcome to your Inbox!")
# # # # # # #         # Add inbox functionality here

# # # # # # #     elif selected_page == 'Compose':
# # # # # # #         st.write("Compose a new message:")

# # # # # # #         # Input fields for composing message
# # # # # # #         to = st.text_input("To")
# # # # # # #         subject = st.text_input("Subject")
# # # # # # #         content = st.text_area("Content")

# # # # # # #         # Buttons for actions
# # # # # # #         col1, col2 = st.columns([1, 3])  # Reversed column widths
# # # # # # #         if col1.button("Save as Draft"):
# # # # # # #             save_draft(to, subject, content)
# # # # # # #         if col1.button("Send"):
# # # # # # #             send_message(to, subject, content)

# # # # # # #     elif selected_page == 'Drafts':
# # # # # # #         st.write("Your Drafts:")
# # # # # # #         if 'drafts' in st.session_state and st.session_state.drafts:
# # # # # # #             for draft in st.session_state.drafts:
# # # # # # #                 st.write(f"To: {draft['to']}, Subject: {draft['subject']}")
# # # # # # #                 st.write(f"Content: {draft['content']}")
# # # # # # #                 st.write("---")

# # # # # # #     elif selected_page == 'Sent':
# # # # # # #         st.write("Sent Messages:")
# # # # # # #         # Add sent messages functionality here

# # # # # # #     elif selected_page == 'Logout':
# # # # # # #         st.session_state.logged_in = False
# # # # # # #         st.session_state.session = None
# # # # # # #         navigate_to('Login')
# # # # # # #         st.success('Logged out successfully.')

# # # # # # #     else:
# # # # # # #         st.error('Page not found.')

# # # # # # # # Start the Streamlit application
# # # # # # # if __name__ == '__main__':
# # # # # # #     main()
# # # # # # ##################################ADDED DROP DOWN####################################
# # # # # ##############################################################################
# # # # #########################################################################
# # # ###############################################################################################

# import streamlit as st
# import requests
# import sqlite3

# # Function to navigate to different pages
# def navigate_to(page_name):
#     st.session_state.page = page_name

# # Function to handle login
# def login(username, password):
#     session = requests.Session()
    
#     # Fetch CSRF token
#     response = session.get('http://localhost:8000/csrf/')  # Assuming CSRF endpoint is '/csrf/'
#     if response.status_code == 200:
#         csrftoken = session.cookies.get('csrftoken')
#     else:
#         st.error(f"Failed to fetch CSRF token. Status code: {response.status_code}")
#         return False
    
#     # Perform login request
#     login_data = {
#         'username': username,
#         'password': password,
#         'csrfmiddlewaretoken': csrftoken
#     }
#     response = session.post('http://localhost:8000/login/', data=login_data)
    
#     # Check login response
#     if response.status_code == 200 and 'Please enter a correct username and password.' not in response.text:
#         st.session_state.logged_in = True
#         st.session_state.session = session  # Save session for subsequent requests
#         st.session_state.username = username  # Store username in session state
#         navigate_to('Inbox')  # Redirect to inbox page upon successful login
#         return True
#     else:
#         st.error("Login failed. Please check your username and password.")
#         return False

# # Function to fetch all users
# def fetch_users():
#     db_path = 'mailapp/db.sqlite3'

#     connection = sqlite3.connect(db_path)
#     cursor = connection.cursor()

#     cursor.execute("SELECT username FROM auth_user")  # Adjust as per your Django model

#     users = cursor.fetchall()

#     cursor.close()
#     connection.close()

#     return [user[0] for user in users]

# # Function to fetch drafts for the logged-in user
# def fetch_drafts(username):
#     db_path = 'mailapp/db.sqlite3'

#     connection = sqlite3.connect(db_path)
#     cursor = connection.cursor()

#     cursor.execute("""
#         SELECT d.id, u.username, d.subject, d.body
#         FROM chat_draft d
#         JOIN auth_user u ON d.user_id = u.id
#         WHERE u.username = ?
#     """, (username,))

#     drafts = cursor.fetchall()

#     cursor.close()
#     connection.close()

#     return drafts

# # Function to fetch received messages for the logged-in user
# def fetch_received_messages(username):
#     db_path = 'mailapp/db.sqlite3'

#     connection = sqlite3.connect(db_path)
#     cursor = connection.cursor()

#     cursor.execute("""
#         SELECT m.id, u.username, m.subject, m.body
#         FROM chat_message m
#         JOIN auth_user u ON m.sender_id = u.id
#         JOIN auth_user r ON m.recipient_id = r.id
#         WHERE r.username = ?
#     """, (username,))

#     messages = cursor.fetchall()

#     cursor.close()
#     connection.close()

#     return messages

# # Function to save message as draft
# def save_draft(to, subject, content):
#     session = st.session_state.session
    
#     draft_data = {
#         'recipient': to,
#         'subject': subject,
#         'body': content,
#         'action': 'Save as Draft'  # Specify the action to save as draft on the Django side
#     }
    
#     headers = {'X-CSRFToken': session.cookies.get('csrftoken')}  # Include CSRF token in headers
    
#     response = session.post('http://localhost:8000/compose/', data=draft_data, headers=headers)
    
#     if response.status_code == 200:
#         st.success('Draft saved successfully.')
#     else:
#         st.error(f"Failed to save draft. Status code: {response.status_code}")

# # Function to send message
# def send_message(to_username, subject, content):
#     session = st.session_state.session
    
#     message_data = {
#         'recipient': to_username,
#         'subject': subject,
#         'body': content,
#         'action': 'Send'  # Specify the action to send message on the Django side
#     }
    
#     headers = {'X-CSRFToken': session.cookies.get('csrftoken')}  # Include CSRF token in headers
    
#     response = session.post('http://localhost:8000/compose/', data=message_data, headers=headers)
    
#     if response.status_code == 200:
#         st.success('Message sent successfully.')
#     else:
#         st.error(f"Failed to send message. Status code: {response.status_code}")

# # Function to delete draft
# def delete_draft(draft_id):
#     db_path = 'mailapp/db.sqlite3'

#     connection = sqlite3.connect(db_path)
#     cursor = connection.cursor()

#     cursor.execute("DELETE FROM chat_draft WHERE id = ?", (draft_id,))
#     connection.commit()

#     cursor.close()
#     connection.close()

#     st.success(f'Draft {draft_id} deleted successfully.')
#     # Refresh the page to show updated drafts list
#     st.experimental_rerun()

# # Streamlit code for login, inbox page, and sidebar
# def main():
#     st.title("Mail Application")

#     # Initialize session state for storing logged-in status and current page
#     if 'logged_in' not in st.session_state:
#         st.session_state.logged_in = False
#     if 'page' not in st.session_state:
#         st.session_state.page = None

#     # Sidebar navigation
#     st.sidebar.title("Navigation")
#     if st.session_state.logged_in:
#         pages = ['Inbox', 'Compose', 'Drafts', 'Sent', 'Logout']
#     else:
#         pages = ['Login']
    
#     selected_page = st.sidebar.radio("Go to", pages)

#     if selected_page == 'Login':
#         # Login form
#         username = st.text_input("Username")
#         password = st.text_input("Password", type="password")
#         if st.button("Login"):
#             if login(username, password):
#                 st.success('Logged in successfully.')
#             # No need for else as login function handles errors

#     elif selected_page == 'Inbox':
#         st.write("Your Inbox:")

#         # Fetch received messages for the logged-in user
#         messages = fetch_received_messages(st.session_state.username)
        
#         for message in messages:
#             message_id, from_user, subject, content = message
            
#             with st.container():
#                 st.markdown(f"**From:** {from_user}")
#                 st.markdown(f"**Subject:** {subject}")
#                 st.markdown(f"**Content:**\n{content}")
                
#                 if st.button("Reply", key=f"reply_{message_id}"):
#                     if f"reply_content_{message_id}" not in st.session_state:
#                         st.session_state[f"reply_content_{message_id}"] = ""
#                     st.text_area("Reply", key=f"reply_content_{message_id}")
#                     if st.button("Send Reply", key=f"send_reply_{message_id}"):
#                         send_message(from_user, f"Re: {subject}", st.session_state[f"reply_content_{message_id}"])
                
#                 st.markdown("---")

#     elif selected_page == 'Compose':
#         st.write("Compose a new message:")

#         # Fetch users and populate dropdown
#         users = fetch_users()
#         to = st.selectbox("To", users, key="compose_to") if users else st.text_input("To", key="compose_to")  # Show text input if no users fetched
#         subject = st.text_input("Subject", key="compose_subject")
#         content = st.text_area("Content", key="compose_content")

#         # Buttons for actions
#         col1, col2 = st.columns([1, 3])  # Reversed column widths
#         if col1.button("Save as Draft", key="compose_save_draft"):
#             save_draft(to, subject, content)
#         if col1.button("Send", key="compose_send"):
#             send_message(to, subject, content)

#     elif selected_page == 'Drafts':
#         st.write("Your Drafts:")
        
#         # Fetch drafts for the logged-in user
#         drafts = fetch_drafts(st.session_state.username)
        
#         for draft in drafts:
#             draft_id, to, subject, content = draft
            
#             st.write("Edit Draft:")
#             to = st.selectbox(f"To {draft_id}", fetch_users(), index=fetch_users().index(to), key=f"to_{draft_id}") if fetch_users() else st.text_input(f"To {draft_id}", value=to)
#             subject = st.text_input(f"Subject {draft_id}", value=subject, key=f"subject_{draft_id}")
#             content = st.text_area(f"Content {draft_id}", value=content, key=f"content_{draft_id}")
            
#             col1, col2, col3 = st.columns([1, 1, 2])
#             if col1.button(f"Save Draft {draft_id}", key=f"save_draft_{draft_id}"):
#                 save_draft(to, subject, content)
#             if col2.button(f"Send {draft_id}", key=f"send_{draft_id}"):
#                 send_message(to, subject, content)
#             if col3.button(f"Delete {draft_id}", key=f"delete_draft_{draft_id}"):
#                 delete_draft(draft_id)
#             st.write("---")

#     elif selected_page == 'Sent':
#         st.write("Sent Messages:")
#         # Add sent messages functionality here

#     elif selected_page == 'Logout':
#         st.session_state.logged_in = False
#         st.session_state.session = None
#         navigate_to('Login')
#         st.success('Logged out successfully.')

#     else:
#         st.error('Page not found.')

# # Start the Streamlit application
# if __name__ == '__main__':
#     main()
# ###################################################################################################
# ##############################################################################

import streamlit as st
import requests
import sqlite3
from datetime import datetime

# Function to navigate to different pages
def navigate_to(page_name):
    st.session_state.page = page_name

# Function to handle login
def login(username, password):
    session = requests.Session()
    
    # Fetch CSRF token
    response = session.get('http://localhost:8000/csrf/')  # Assuming CSRF endpoint is '/csrf/'
    if response.status_code == 200:
        csrftoken = session.cookies.get('csrftoken')
    else:
        st.error(f"Failed to fetch CSRF token. Status code: {response.status_code}")
        return False
    
    # Perform login request
    login_data = {
        'username': username,
        'password': password,
        'csrfmiddlewaretoken': csrftoken
    }
    response = session.post('http://localhost:8000/login/', data=login_data)
    
    # Check login response
    if response.status_code == 200 and 'Please enter a correct username and password.' not in response.text:
        st.session_state.logged_in = True
        st.session_state.session = session  # Save session for subsequent requests
        st.session_state.username = username  # Store username in session state
        navigate_to('Inbox')  # Redirect to inbox page upon successful login
        return True
    else:
        st.error("Login failed. Please check your username and password.")
        return False

# Function to fetch all users
def fetch_users():
    db_path = 'mailapp/db.sqlite3'

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute("SELECT username FROM auth_user")  # Adjust as per your Django model

    users = cursor.fetchall()

    cursor.close()
    connection.close()

    return [user[0] for user in users]

# Function to fetch drafts for the logged-in user
def fetch_drafts(username):
    db_path = 'mailapp/db.sqlite3'

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT d.id, u.username, d.subject, d.body
        FROM chat_draft d
        JOIN auth_user u ON d.user_id = u.id
        WHERE u.username = ?
        ORDER BY d.date_saved DESC            
    """, (username,))

    drafts = cursor.fetchall()

    cursor.close()
    connection.close()

    return drafts

# Function to fetch received messages for the logged-in user
def fetch_received_messages(username):
    db_path = 'mailapp/db.sqlite3'

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT m.id, u.username, m.subject, m.body, m.date_sent
        FROM chat_message m
        JOIN auth_user u ON m.sender_id = u.id
        JOIN auth_user r ON m.recipient_id = r.id
        WHERE r.username = ?
        ORDER BY m.date_sent DESC
    """, (username,))

    messages = cursor.fetchall()

    cursor.close()
    connection.close()

    return messages

# Function to fetch sent messages for the logged-in user
def fetch_sent_messages(username):
    db_path = 'mailapp/db.sqlite3'

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT m.id, u.username, m.subject, m.body, m.date_sent
        FROM chat_message m
        JOIN auth_user u ON m.recipient_id = u.id
        JOIN auth_user s ON m.sender_id = s.id
        WHERE s.username = ?
        ORDER BY m.date_sent DESC           
    """, (username,))

    sent_messages = cursor.fetchall()

    cursor.close()
    connection.close()

    return sent_messages

# Function to save message as draft
def save_draft(to, subject, content):
    session = st.session_state.session
    
    draft_data = {
        'recipient': to,
        'subject': subject,
        'body': content,
        'action': 'Save as Draft',  # Specify the action to save as draft on the Django side
        'date_saved': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }
    
    headers = {'X-CSRFToken': session.cookies.get('csrftoken')}  # Include CSRF token in headers
    
    response = session.post('http://localhost:8000/compose/', data=draft_data, headers=headers)
    
    if response.status_code == 200:
        st.success('Draft saved successfully.')
    else:
        st.error(f"Failed to save draft. Status code: {response.status_code}")

# Function to send message
def send_message(to_username, subject, content):
    session = st.session_state.session
    
    message_data = {
        'recipient': to_username,
        'subject': subject,
        'body': content,
        'action': 'Send'  # Specify the action to send message on the Django side
    }
    
    headers = {'X-CSRFToken': session.cookies.get('csrftoken')}  # Include CSRF token in headers
    
    response = session.post('http://localhost:8000/compose/', data=message_data, headers=headers)
    
    if response.status_code == 200:
        # Save sent message to the database
        save_sent_message(st.session_state.username, to_username, subject, content)
        st.success('Message sent successfully.')
    else:
        st.error(f"Failed to send message. Status code: {response.status_code}")

# Function to save sent message to database
def save_sent_message(sender_username, recipient_username, subject, content):
    db_path = 'mailapp/db.sqlite3'

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # Fetch sender and recipient IDs
    cursor.execute("SELECT id FROM auth_user WHERE username = ?", (sender_username,))
    sender_id = cursor.fetchone()[0]
    cursor.execute("SELECT id FROM auth_user WHERE username = ?", (recipient_username,))
    recipient_id = cursor.fetchone()[0]

    # Insert message into database
    date_sent = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("""
        INSERT INTO chat_message (sender_id, recipient_id, subject, body, date_sent)
        VALUES (?, ?, ?, ?, ?)
    """, (sender_id, recipient_id, subject, content, date_sent))

    connection.commit()
    cursor.close()
    connection.close()

# Function to delete draft
def delete_draft(draft_id):
    db_path = 'mailapp/db.sqlite3'

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute("DELETE FROM chat_draft WHERE id = ?", (draft_id,))
    connection.commit()

    cursor.close()
    connection.close()

    st.success(f'Draft {draft_id} deleted successfully.')
    # Refresh the page to show updated drafts list
    st.experimental_rerun()

# Streamlit code for login, inbox page, and sidebar
def main():
    st.title("Mail Application")

    # Initialize session state for storing logged-in status and current page
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'page' not in st.session_state:
        st.session_state.page = None

    # Sidebar navigation
    st.sidebar.title("Navigation")
    if st.session_state.logged_in:
        pages = ['Inbox', 'Compose', 'Drafts', 'Sent', 'Logout']
        st.sidebar.markdown(f"**Logged in as:** {st.session_state.username}")
    else:
        pages = ['Login']
    
    selected_page = st.sidebar.radio("Go to", pages)

    if selected_page == 'Login':
        # Login form
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if login(username, password):
                st.success('Logged in successfully.')
            # No need for else as login function handles errors

    elif selected_page == 'Inbox':
        st.write("Your Inbox:")

        # Fetch received messages for the logged-in user
        messages = fetch_received_messages(st.session_state.username)
        
        for message in messages:
            message_id, from_user, subject, content, date_sent = message
            
            with st.expander(f"From: {from_user}, Subject: {subject}, Sent: {date_sent}"):
                st.markdown(f"**Content:**\n{content}")
                
                if st.button("Reply", key=f"reply_{message_id}"):
                    if f"reply_content_{message_id}" not in st.session_state:
                        st.session_state[f"reply_content_{message_id}"] = ""
                    st.text_area("Reply", key=f"reply_content_{message_id}")
                    if st.button("Send Reply", key=f"send_reply_{message_id}"):
                        send_message(from_user, f"Re: {subject}", st.session_state[f"reply_content_{message_id}"])
                
                st.markdown("---")

    elif selected_page == 'Compose':
        st.write("Compose a new message:")

        # Fetch users and populate dropdown
        users = fetch_users()
        to = st.selectbox("To", users, key="compose_to") if users else st.text_input("To", key="compose_to")  # Show text input if no users fetched
        subject = st.text_input("Subject", key="compose_subject")
        content = st.text_area("Content", key="compose_content")

        # Buttons for actions
        col1, col2 = st.columns([1, 3])  # Reversed column widths
        if col1.button("Save as Draft", key="compose_save_draft"):
            save_draft(to, subject, content)
        if col1.button("Send", key="compose_send"):
            send_message(to, subject, content)

    elif selected_page == 'Drafts':
        st.write("Your Drafts:")
        
        # Fetch drafts for the logged-in user
        drafts = fetch_drafts(st.session_state.username)
        
        for draft in drafts:
            draft_id, to, subject, content = draft
            
            st.write("Edit Draft:")
            to = st.selectbox(f"To", fetch_users(), index=fetch_users().index(to), key=f"to_{draft_id}") if fetch_users() else st.text_input(f"To {draft_id}", value=to)
            subject = st.text_input(f"Subject", value=subject, key=f"subject_{draft_id}")
            content = st.text_area(f"Content", value=content, key=f"content_{draft_id}")
            
            col1, col2, col3 = st.columns([1, 1, 2])
            if col1.button(f"Save Draft", key=f"save_draft_{draft_id}"):
                save_draft(to, subject, content)
            if col2.button(f"Send", key=f"send_{draft_id}"):
                send_message(to, subject, content)
            if col3.button(f"Delete", key=f"delete_draft_{draft_id}"):
                delete_draft(draft_id)
            st.write("---")

    elif selected_page == 'Sent':
        st.write("Sent Messages:")

        # Fetch sent messages for the logged-in user
        sent_messages = fetch_sent_messages(st.session_state.username)

        for message in sent_messages:
            message_id, to_user, subject, content, date_sent = message

            with st.expander(f"To: {to_user}, Subject: {subject}, Sent: {date_sent}"):
                st.markdown(f"**Content:**\n{content}")
                st.markdown("---")

    elif selected_page == 'Logout':
        st.session_state.logged_in = False
        st.session_state.session = None
        navigate_to('Login')
        st.success('Logged out successfully.')

    else:
        st.error('Page not found.')

# Start the Streamlit application
if __name__ == '__main__':
    main()

######################################################################
