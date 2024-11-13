import streamlit as st
import os
import json
import shutil

UPLOAD_FOLDER = 'uploads/'
PUBLIC_FOLDER = 'uploads/public/'

# Đảm bảo thư mục tải lên và thư mục công khai tồn tại
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(PUBLIC_FOLDER):
    os.makedirs(PUBLIC_FOLDER)

def load_users():
    """Tải danh sách người dùng từ tệp JSON"""
    with open('users.json', 'r') as f:
        return json.load(f)

def save_users(users):
    """Lưu danh sách người dùng vào tệp JSON"""
    with open('users.json', 'w') as f:
        json.dump(users, f)

def my_files_view():
    st.header("Tệp của tôi")

    # Kiểm tra người dùng đã đăng nhập chưa
    if 'username' not in st.session_state:
        st.error("Vui lòng đăng nhập để xem các tệp của bạn.")
        return

    # Lấy danh sách tệp của người dùng
    users = load_users()
    username = st.session_state['username']
    user_files = users[username].get('files', [])
    public_files = users[username].get('public_files', [])

    # Hiển thị các tệp của người dùng
    if user_files:
        for file_name in user_files:
            file_path = os.path.join(UPLOAD_FOLDER, file_name)

            if os.path.exists(file_path):
                st.subheader(f"File: {file_name}")
                col1, col2 = st.columns([3, 1])

                # Hiển thị hình ảnh nếu là tệp hình ảnh
                if file_name.lower().endswith(('png', 'jpg', 'jpeg')):
                    with col1:
                        st.image(file_path, caption=file_name, width=80)
                else:
                    with col1:
                        st.write(file_name)

                # Nút tải xuống
                with open(file_path, "rb") as f:
                    with col2:
                        st.download_button(
                            label="Tải xuống",
                            data=f,
                            file_name=file_name,
                            mime="application/octet-stream"
                        )

                # Nút xóa
                if st.button(f"Xóa {file_name}", key=f"delete_{file_name}"):
                    os.remove(file_path)
                    users[username]['files'].remove(file_name)
                    save_users(users)
                    st.success(f"Tệp {file_name} đã được xóa.")

                # Nút công khai
                if st.button(f"Công khai {file_name}", key=f"public_{file_name}"):
                    # Di chuyển tệp từ thư mục cá nhân sang thư mục công khai
                    public_file_path = os.path.join(PUBLIC_FOLDER, file_name)

                    if not os.path.exists(public_file_path):
                        shutil.copy(file_path, public_file_path)

                        # Cập nhật danh sách tệp công khai
                        if 'public_files' not in users[username]:
                            users[username]['public_files'] = []
                        users[username]['public_files'].append(file_name)

                        # Không xóa tệp khỏi thư mục cá nhân
                        save_users(users)
                        st.success(f"Tệp {file_name} đã được công khai.")
                    else:
                        st.warning(f"Tệp {file_name} đã tồn tại trong thư mục công khai.")
    else:
        st.info("Không có tệp nào.")
