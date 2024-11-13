import streamlit as st
import os

UPLOAD_FOLDER = 'uploads/'

# Đảm bảo thư mục uploads tồn tại
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def upload_view():
    st.header("Tải lên tệp")

    uploaded_file = st.file_uploader("Chọn tệp để tải lên", type=["png", "jpg", "jpeg", "pdf", "txt", "zip"])

    if uploaded_file:
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        
        # Lưu tệp vào thư mục uploads
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.success(f"Đã tải lên tệp: {uploaded_file.name}")
        
        # Hiển thị phần "Tệp của tôi" ngay sau khi tải lên
        my_files_view()

    else:
        # Nếu chưa có tệp tải lên, chỉ hiển thị phần "Tệp của tôi"
        my_files_view()
