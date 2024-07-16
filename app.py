import streamlit as st
import requests
import sqlite3
from datetime import datetime
import google.generativeai as genai


# Function to navigate to different pages
def navigate_to(page_name):
    st.session_state.page = page_name

genai.configure(api_key='AIzaSyD040mK5kKMExKdU-qzOil9kT-yDIp2d5Q  ')

 
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

def fetch_all_users():
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
        SELECT m.id, u.username, m.subject, m.body, strftime('%Y-%m-%d %H:%M', m.date_sent) AS formatted_date_sent
        FROM chat_message m
        JOIN auth_user u ON m.sender_id = u.id
        JOIN auth_user r ON m.recipient_id = r.id
        WHERE r.username = ?
        GROUP BY m.id  -- Ensure distinct messages by message ID
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
        SELECT DISTINCT m.id, u.username, m.subject, m.body, m.date_sent
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
def save_draft(to_list, subject, content):
    session = st.session_state.session
    
    for to in to_list:
        draft_data = {
            'recipient': to,
            'subject': subject,
            'body': content,
            'action': 'Save as Draft'  # Specify the action to save as draft on the Django side
        }
        
        headers = {'X-CSRFToken': session.cookies.get('csrftoken')}  # Include CSRF token in headers
        
        response = session.post('http://localhost:8000/compose/', data=draft_data, headers=headers)
        
        if response.status_code == 200:
            st.success(f'Draft saved successfully for {to}.')
        else:
            st.error(f"Failed to save draft for {to}. Status code: {response.status_code}")

#Function to send message
def send_message(to_usernames, subject, content, send_to_all=False):
    session = st.session_state.session
    
    if send_to_all:
        # Send to all users
        # users = fetch_all_users()
        users = fetch_users()
        for user in users:
            message_data = {
                'recipient': user,
                'subject': subject,
                'body': content,
                'action': 'Send'  # Specify the action to send message on the Django side
            }
            headers = {'X-CSRFToken': session.cookies.get('csrftoken')}  # Include CSRF token in headers
            response = session.post('http://localhost:8000/compose/', data=message_data, headers=headers)
            save_sent_message(st.session_state.username,user, subject, content)
            if response.status_code != 200:
                st.error(f"Failed to send message to {user}. Status code: {response.status_code}")
                return False
        st.success('Message sent to all users successfully.')
        return True
    # else:
    #     for to_username in to_usernames:
    #     # Send to a specific user
    #         message_data = {
    #             'recipient': to_username,
    #             'subject': subject,
    #             'body': content,
    #             'action': 'Send'  # Specify the action to send message on the Django side
    #         }
    #         headers = {'X-CSRFToken': session.cookies.get('csrftoken')}  # Include CSRF token in headers
    #         response = session.post('http://localhost:8000/compose/', data=message_data, headers=headers)
    #         if response.status_code == 200:
    #             save_sent_message(st.session_state.username, to_username, subject, content)
    #             st.success('Message sent successfully.')
    #             return True
    #         else:
    #             st.error(f"Failed to send message. Status code: {response.status_code}")
    #             return False

def send_multi_message(to_list, subject, content):
    session = st.session_state.session
    
    for to in to_list:
        message_data = {
            'recipient': to,
            'subject': subject,
            'body': content,
            'action': 'Send'  # Specify the action to send message on the Django side
        }
        
        headers = {'X-CSRFToken': session.cookies.get('csrftoken')}  # Include CSRF token in headers
        
        response = session.post('http://localhost:8000/compose/', data=message_data, headers=headers)
        
        if response.status_code == 200:
            save_sent_message(st.session_state.username, to, subject, content)
            st.success(f'Message sent successfully to {to}.')
        else:
            st.error(f"Failed to send message to {to}. Status code: {response.status_code}")

# Function to save sent message to database
# def save_sent_message(sender_username, recipient_username, subject, content):
#     db_path = 'mailapp/db.sqlite3'

#     connection = sqlite3.connect(db_path)
#     cursor = connection.cursor()

#     # Fetch sender and recipient IDs
#     cursor.execute("SELECT id FROM auth_user WHERE username = ?", (sender_username,))
#     sender_id = cursor.fetchone()[0]
#     cursor.execute("SELECT id FROM auth_user WHERE username = ?", (recipient_username,))
#     recipient_id = cursor.fetchone()[0]

#     # Insert message into database
#     date_sent = datetime.now().strftime('%Y-%m-%d %H:%M')
#     cursor.execute("""
#         INSERT INTO chat_message (sender_id, recipient_id, subject, body, date_sent)
#         VALUES (?, ?, ?, ?, ?)
#     """, (sender_id, recipient_id, subject, content, date_sent))

#     connection.commit()
#     cursor.close()
#     connection.close()

def save_sent_message(sender_username, recipient_username, subject, content):
    db_path = 'mailapp/db.sqlite3'

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # Fetch sender and recipient IDs
    cursor.execute("SELECT id FROM auth_user WHERE username = ?", (sender_username,))
    sender_result = cursor.fetchone()
    if sender_result is None:
        st.error(f"Sender '{sender_username}' not found.")
        return
    sender_id = sender_result[0]

    cursor.execute("SELECT id FROM auth_user WHERE username = ?", (recipient_username,))
    recipient_result = cursor.fetchone()
    if recipient_result is None:
        st.error(f"Recipient '{recipient_username}' not found.")
        return
    recipient_id = recipient_result[0]

    # Insert message into database
    date_sent = datetime.now().strftime('%Y-%m-%d %H:%M')
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

def fetch_messages_by_subject(username, subject):
    db_path = 'mailapp/db.sqlite3'

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # Fetch received messages
    cursor.execute("""
        SELECT m.id, u.username, m.subject, m.body, strftime('%Y-%m-%d %H:%M', m.date_sent) AS formatted_date_sent, 'received' AS message_type
        FROM chat_message m
        JOIN auth_user u ON m.sender_id = u.id
        JOIN auth_user r ON m.recipient_id = r.id
        WHERE r.username = ? AND m.subject = ?
        GROUP BY m.id  -- Ensure distinct messages by message ID
        ORDER BY m.date_sent DESC
    """, (username, subject))
    received_messages = cursor.fetchall()

    # Fetch sent messages
    cursor.execute("""
        SELECT m.id, u.username, m.subject, m.body, strftime('%Y-%m-%d %H:%M', m.date_sent) AS formatted_date_sent, 'sent' AS message_type
        FROM chat_message m
        JOIN auth_user u ON m.recipient_id = u.id
        JOIN auth_user s ON m.sender_id = s.id
        WHERE s.username = ? AND m.subject = ?
        ORDER BY m.date_sent DESC
    """, (username, subject))
    sent_messages = cursor.fetchall()

    cursor.close()
    connection.close()

    return received_messages, sent_messages

# def reply_message(subject, reply_content):
#     session = st.session_state.session

#     # Fetch original message to get recipient details
#     db_path = 'mailapp/db.sqlite3'
#     connection = sqlite3.connect(db_path)
#     cursor = connection.cursor()
#     cursor.execute("""
#         SELECT m.sender_id, m.subject
#         FROM chat_message m
#         JOIN auth_user u ON m.sender_id = u.id
#         WHERE m.subject = ? AND u.username != ?
#         ORDER BY m.date_sent DESC
#         LIMIT 1
#     """, (subject, st.session_state.username))
#     original_message = cursor.fetchone()
#     cursor.close()
#     connection.close()

#     if original_message:
#         original_sender_id, original_subject = original_message

#         # Fetch original sender username
#         connection = sqlite3.connect(db_path)
#         cursor = connection.cursor()
#         cursor.execute("SELECT username FROM auth_user WHERE id = ?", (original_sender_id,))
#         sender = cursor.fetchone()
#         cursor.close()
#         connection.close()

#         if sender:
#             original_sender = sender[0]
#             reply_data = {
#                 'recipient': original_sender,
#                 'subject': f'Re: {original_subject}',
#                 'body': reply_content,
#                 'action': 'Send'
#             }
#             headers = {'X-CSRFToken': session.cookies.get('csrftoken')}
#             response = session.post('http://localhost:8000/compose/', data=reply_data, headers=headers)

#             if response.status_code == 200:
#                 save_sent_message(st.session_state.username, original_sender, f'Re: {original_subject}', reply_content)
#                 st.success('Reply sent successfully.')
#             else:
#                 st.error(f"Failed to send reply. Status code: {response.status_code}")
#         else:
#             st.error("Original message sender not found.")
#     else:
#         st.error("No original message found with the given subject.")

# Streamlit code for login, inbox page, and sidebar

def generate_email(prompt):
    # Use the Google Generative AI model to generate content
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text.strip()
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
        pages = ['Inbox', 'Compose', 'Drafts', 'Sent', 'Chat', 'Logout']
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

        # Extract unique subjects
        subjects = list(set([message[2] for message in messages]))
        subjects.sort()

        selected_subject = st.selectbox("Filter by subject", ["All"] + subjects)

        if selected_subject != "All":
            messages = [message for message in messages if message[2] == selected_subject]

        for message in messages:
            message_id, from_user, subject, content, formatted_date_sent = message

            with st.expander(f"From: {from_user}, Subject: {subject}, Sent: {formatted_date_sent}"):
                st.markdown(f"**Content:**\n{content}")
                
                # Add a reply button
                if st.button("Reply", key=f"reply_btn_{message_id}"):
                    st.session_state[f"show_reply_{message_id}"] = True
                
                if st.session_state.get(f"show_reply_{message_id}", False):
                    # reply_to = st.text_input("To", [from_user], key=f"to_{message_id}")
                    reply_to = st.multiselect("To", [from_user], key=f"to_{message_id}")  # Allow selecting multiple recipients if needed
                    reply_subject = st.text_input("Subject", f"Re: {subject}", key=f"subject_{message_id}")
                    # reply_subject=st.text_input("subject")
                    reply_content = st.text_area("Content", key=f"content_{message_id}")
                    # reply_content=st.text_area("reply Content")

                    if st.button("Send Reply", key=f"send_reply_{message_id}"):
                        send_multi_message(reply_to, reply_subject, reply_content)
                        # reply_message(reply_subject, reply_content)

                        st.success("Reply sent successfully.")
                        st.session_state[f"show_reply_{message_id}"] = False
                        st.experimental_rerun()  # Refresh the inbox after sending the reply
            
    elif selected_page == 'Compose':
        st.write("Compose a new message:")

        # Fetch users and populate dropdown
        users = fetch_users()
        to_usernames = st.multiselect('To', users)
        # to = st.multiselect("To", users, key="compose_to") if users else st.text_input("To", key="compose_to")  # Show text input if no users fetched
        
        if 'reply_subject' in st.session_state:
            subject = st.session_state.reply_subject
            to = st.session_state.reply_to[0] if len(st.session_state.reply_to) == 1 else st.multiselectselect("To", st.session_state.reply_to)
            st.session_state.pop('reply_subject')
            st.session_state.pop('reply_to')
        else:
            subject = st.text_input("Subject", key="compose_subject")
        content = st.text_area("Content", key="compose_content")
        send_to_all = st.checkbox("Send to all users")
        st.write("Or let AI help you write the email:")
        ai_prompt = st.text_input("Enter a prompt for AI to generate email content:", key="ai_prompt")
        if st.button("Generate with AI"):
            if ai_prompt:
                generated_content = generate_email(ai_prompt)
                st.session_state.generated_content = generated_content
            else:
                st.warning("Please enter a prompt for AI to generate content.")

        if 'generated_content' in st.session_state:
            st.text_area("Generated Content", value=st.session_state.generated_content, key="compose_content_generated", height=200)
            if st.button("Use Generated Content"):
                content = st.session_state.generated_content
                st.session_state.compose_content = content
                st.success("Generated content has been applied.")

        # Buttons for actions
        col1, col2 = st.columns([1, 3])  # Reversed column widths
        if col1.button("Save as Draft", key="compose_save_draft"):
            save_draft(to_usernames, subject, content)
        if col1.button("Send", key="compose_send"):
            if send_to_all:
                send_message(users, subject, content, send_to_all=True)
            else:
                send_multi_message(to_usernames, subject, content)
        
            

    elif selected_page == 'Drafts':
        st.write("Your Drafts:")
    
    # Fetch drafts for the logged-in user
        drafts = fetch_drafts(st.session_state.username)
    
        for draft in drafts:
            draft_id, to, subject, content = draft
            
            st.write("Edit Draft:")
            to = st.multiselect(f"To {draft_id}", fetch_users(), default=[to], key=f"to_{draft_id}") if fetch_users() else [st.text_input(f"To {draft_id}", value=to)]
            subject = st.text_input(f"Subject {draft_id}", value=subject, key=f"subject_{draft_id}")
            content = st.text_area(f"Content {draft_id}", value=content, key=f"content_{draft_id}")
            
            col1, col2, col3 = st.columns([1, 1, 2])
            if col1.button(f"Save Draft {draft_id}", key=f"save_draft_{draft_id}"):
                save_draft(to, subject, content)
            if col2.button(f"Send {draft_id}", key=f"send_{draft_id}"):
                send_multi_message(to, subject, content)
                delete_draft(draft_id)
            if col3.button(f"Delete {draft_id}", key=f"delete_draft_{draft_id}"):
                delete_draft(draft_id)
            st.write("---")
    elif selected_page == 'Sent':
        st.write("Sent Messages:")

        # Fetch sent messages for the logged-in user
        sent_messages = fetch_sent_messages(st.session_state.username)

        # Extract unique subjects
        subjects = list(set([message[2] for message in sent_messages]))
        subjects.sort()

        selected_subject = st.selectbox("Filter by subject", ["All"] + subjects)

        if selected_subject != "All":
            sent_messages = [message for message in sent_messages if message[2] == selected_subject]

        for message in sent_messages:
            message_id, to_user, subject, content, date_sent = message

            with st.expander(f"To: {to_user}, Subject: {subject}, Sent: {date_sent}"):
                st.markdown(f"**Content:**\n{content}")
                st.markdown("---")

    elif selected_page == 'Chat':
        st.write("Chat Page:")

        # Fetch distinct subjects from received and sent messages
        db_path = 'mailapp/db.sqlite3'

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""
            SELECT DISTINCT subject
            FROM chat_message
            WHERE sender_id IN (SELECT id FROM auth_user WHERE username = ?)
               OR recipient_id IN (SELECT id FROM auth_user WHERE username = ?)
        """, (st.session_state.username, st.session_state.username))

        subjects = cursor.fetchall()

        cursor.close()
        connection.close()

        subjects = [subject[0] for subject in subjects]

        selected_subject = st.selectbox("Select Subject:", subjects)

        if st.button("Filter"):
            received_messages, sent_messages = fetch_messages_by_subject(st.session_state.username, selected_subject)

            if received_messages:
                st.write("Received Messages:")
                for message in received_messages:
                    st.write(f"**Subject:** {message[2]}")
                    st.write(f"**From:** {message[1]}")
                    st.write(f"**Date Sent:** {message[4]}")
                    st.write(f"**Message:** {message[3]}")
                    st.write("---")
            else:
                st.write("No received messages with selected subject.")

            if sent_messages:
                st.write("Sent Messages:")
                for message in sent_messages:
                    st.write(f"**Subject:** {message[2]}")
                    st.write(f"**To:** {message[1]}")
                    st.write(f"**Date Sent:** {message[4]}")
                    st.write(f"**Message:** {message[3]}")
                    st.write("---")
            else:
                st.write("No sent messages with selected subject.")    

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
