import streamlit as st
import os
import json
import shutil

UPLOAD_FOLDER = 'uploads/'
PUBLIC_FOLDER = 'uploads/public/'

# Ensure upload and public folders exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(PUBLIC_FOLDER):
    os.makedirs(PUBLIC_FOLDER)

def load_users():
    """Load user data from JSON file."""
    with open('users.json', 'r') as f:
        return json.load(f)

def save_users(users):
    """Save user data to JSON file."""
    with open('users.json', 'w') as f:
        json.dump(users, f)

def my_files_view():
    st.header("Tệp của tôi")

    # Check if the user is logged in
    if 'username' not in st.session_state:
        st.error("Vui lòng đăng nhập để xem các tệp của bạn.")
        return

    # Load user files
    users = load_users()
    username = st.session_state['username']
    user_files = users[username].get('files', [])
    public_files = users[username].get('public_files', [])

    # Display user's files
    if user_files:
        for idx, file_name in enumerate(user_files):  # Use enumerate for unique keys
            file_path = os.path.join(UPLOAD_FOLDER, file_name)

            if os.path.exists(file_path):
                st.subheader(f"File: {file_name}")
                col1, col2 = st.columns([3, 1])

                # Display image if the file is an image
                if file_name.lower().endswith(('png', 'jpg', 'jpeg')):
                    with col1:
                        st.image(file_path, caption=file_name, width=80)
                else:
                    with col1:
                        st.write(file_name)

                # Download button
                with open(file_path, "rb") as f:
                    with col2:
                        st.download_button(
                            label="Tải xuống",
                            data=f,
                            file_name=file_name,
                            mime="application/octet-stream",
                            key=f"download_{idx}"  # Unique key for download button
                        )

                # Delete button
                if st.button(f"Xóa {file_name}", key=f"delete_{idx}"):
                    os.remove(file_path)
                    users[username]['files'].remove(file_name)
                    save_users(users)
                    st.success(f"Tệp {file_name} đã được xóa.")

                # Public button
                if st.button(f"Công khai {file_name}", key=f"public_{idx}"):
                    public_file_path = os.path.join(PUBLIC_FOLDER, file_name)

                    if not os.path.exists(public_file_path):
                        shutil.copy(file_path, public_file_path)

                        # Update public file list for user
                        if 'public_files' not in users[username]:
                            users[username]['public_files'] = []
                        users[username]['public_files'].append(file_name)

                        save_users(users)
                        st.success(f"Tệp {file_name} đã được công khai.")
                    else:
                        st.warning(f"Tệp {file_name} đã tồn tại trong thư mục công khai.")
    else:
        st.info("Không có tệp nào.")

# Simulate user login for testing
st.session_state['username'] = 'minh'

# Display files view
my_files_view()
