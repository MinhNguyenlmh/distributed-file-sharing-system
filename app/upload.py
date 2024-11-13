import os
import streamlit as st  # Đảm bảo đã import streamlit
import json

UPLOAD_FOLDER = 'uploads/'

# Đảm bảo thư mục tải lên tồn tại
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def load_users():
    """Tải danh sách người dùng từ tệp JSON"""
    with open('users.json', 'r') as f:
        return json.load(f)

def save_users(users):
    """Lưu danh sách người dùng vào tệp JSON"""
    with open('users.json', 'w') as f:
        json.dump(users, f)

def upload_view():
    st.header("Tải lên tệp")

    # Kiểm tra người dùng đã đăng nhập chưa
    if 'username' not in st.session_state:
        st.error("Vui lòng đăng nhập để tải lên tệp.")
        return

    uploaded_file = st.file_uploader("Chọn tệp để tải lên", type=["png", "jpg", "jpeg", "pdf", "txt", "zip"])

    if uploaded_file:
        # Lưu tệp vào thư mục uploads
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Thêm tệp vào danh sách tệp của người dùng
        users = load_users()
        username = st.session_state['username']

        # Kiểm tra xem người dùng có tồn tại trong users hay không
        if username not in users:
            st.error(f"Không tìm thấy người dùng {username} trong hệ thống.")
            return

        # Kiểm tra nếu người dùng chưa có trường 'files', nếu không, khởi tạo nó
        if 'files' not in users[username]:
            users[username]['files'] = []

        # Thêm tệp vào danh sách 'files'
        users[username]['files'].append(uploaded_file.name)
        save_users(users)

        st.success(f"Đã tải lên tệp: {uploaded_file.name}")
