import streamlit as st
import os
import json

# Đường dẫn đến thư mục chứa các tệp công khai
PUBLIC_FOLDER = 'uploads/public/'

# Đảm bảo thư mục công khai tồn tại
if not os.path.exists(PUBLIC_FOLDER):
    os.makedirs(PUBLIC_FOLDER)

# Đọc dữ liệu từ tệp JSON chứa thông tin người dùng
def load_user_data():
    try:
        with open('users.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Hiển thị tệp công khai
def public_files_view():
    st.header("Tệp công khai")

    # Lấy danh sách các tệp công khai từ thư mục
    public_files = os.listdir(PUBLIC_FOLDER)

    # Lấy dữ liệu người dùng từ users.json
    users_data = load_user_data()

    if not public_files:
        st.info("Không có tệp công khai.")
        return

    # Duyệt qua từng tệp công khai
    for file_name in public_files:
        file_path = os.path.join(PUBLIC_FOLDER, file_name)

        # Kiểm tra và lấy tên người dùng đã đăng tệp
        uploaded_by = None
        for user_name, user_data in users_data.items():
            if file_name in user_data.get('public_files', []):
                uploaded_by = user_name
                break

        # Nếu không tìm thấy người dùng đăng tệp, bỏ qua tệp này
        if uploaded_by is None:
            continue

        # Hiển thị thông tin về tệp
        st.subheader(f"Tệp công khai: {file_name}")
        
        col1, col2 = st.columns([3, 1])

        # Hiển thị tên người dùng đã đăng tệp
        with col1:
            st.write(f"Được đăng lên bởi: {uploaded_by}")

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

# Giả lập người dùng đang đăng nhập
st.session_state['username'] = 'minh'  # Thay đổi theo cách bạn quản lý đăng nhập

# Hiển thị các tệp công khai
public_files_view()
