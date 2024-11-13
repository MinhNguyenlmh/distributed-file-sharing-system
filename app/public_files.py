import streamlit as st
import os

UPLOAD_FOLDER = 'uploads/public/'  # Định nghĩa đúng thư mục

def public_files_view():
    st.header("Tệp công khai")

    # Lấy tất cả các tệp trong thư mục uploads/public
    files = os.listdir(UPLOAD_FOLDER)  # Sử dụng đúng biến UPLOAD_FOLDER

    if files:
        for file_name in files:
            file_path = os.path.join(UPLOAD_FOLDER, file_name)

            # Kiểm tra nếu file_path là thư mục, nếu là thì bỏ qua
            if os.path.isdir(file_path):
                continue

            st.subheader(f"File: {file_name}")

            # Hiển thị ảnh nếu tệp là ảnh
            if file_name.lower().endswith(('png', 'jpg', 'jpeg')):
                col1, col2, col3 = st.columns([3, 1, 1])  # Chia cột cho ảnh và nút
                with col1:
                    st.image(file_path, caption=file_name, use_column_width=False, width=100)  # Điều chỉnh kích thước ảnh
                with col2:
                    # Nút tải xuống cho ảnh
                    with open(file_path, "rb") as f:
                        st.download_button(
                            label="Tải xuống",
                            data=f,
                            file_name=file_name,
                            mime="application/octet-stream"
                        )
                with col3:
                    # Nút xóa (chỉ có thể xóa tệp công khai nếu người dùng có quyền)
                    if st.button(f"Xóa {file_name}"):
                        os.remove(file_path)
                        st.success(f"Tệp {file_name} đã được xóa.")
            else:
                col1, col2, col3 = st.columns([3, 1, 1])  # Chia cột cho tệp không phải ảnh
                with col1:
                    st.write(file_name)
                with col2:
                    # Nút tải xuống
                    with open(file_path, "rb") as f:
                        st.download_button(
                            label="Tải xuống",
                            data=f,
                            file_name=file_name,
                            mime="application/octet-stream"
                        )
                with col3:
                    # Nút xóa (chỉ có thể xóa tệp công khai nếu người dùng có quyền)
                    if st.button(f"Xóa {file_name}"):
                        os.remove(file_path)
                        st.success(f"Tệp {file_name} đã được xóa.")
    else:
        st.info("Không có tệp công khai nào.")
