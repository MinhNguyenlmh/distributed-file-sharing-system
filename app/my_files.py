import streamlit as st
import os

UPLOAD_FOLDER = 'uploads/'
PUBLIC_FOLDER = 'uploads/public/'

# Đảm bảo thư mục công khai tồn tại
if not os.path.exists(PUBLIC_FOLDER):
    os.makedirs(PUBLIC_FOLDER)

def my_files_view():
    st.header("Tệp của tôi")

    # Lấy tất cả các tệp trong thư mục uploads
    files = os.listdir(UPLOAD_FOLDER)

    if files:
        for file_name in files:
            file_path = os.path.join(UPLOAD_FOLDER, file_name)

            # Bỏ qua nếu là thư mục
            if os.path.isdir(file_path):
                continue

            st.subheader(f"File: {file_name}")
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])  # Tạo 4 cột cho các nút chức năng
            
            # Hiển thị ảnh nếu là tệp hình ảnh
            if file_name.lower().endswith(('png', 'jpg', 'jpeg')):
                with col1:
                    st.image(file_path, caption=file_name, use_column_width=False, width=100)
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

            # Nút công khai
            with col3:
                if st.button(f"Công khai {file_name}"):
                    public_file_path = os.path.join(PUBLIC_FOLDER, file_name)
                    os.rename(file_path, public_file_path)
                    st.success(f"Tệp {file_name} đã được công khai.")
                    st.experimental_rerun()  # Cập nhật trang sau khi công khai

            # Nút đổi tên
            with col4:
                new_name = st.text_input(f"Đổi tên {file_name}", value=file_name, key=f"rename_{file_name}")
                if st.button(f"Đổi tên {file_name}", key=f"btn_rename_{file_name}"):
                    new_file_path = os.path.join(UPLOAD_FOLDER, new_name)
                    os.rename(file_path, new_file_path)
                    st.success(f"Tệp {file_name} đã được đổi tên thành {new_name}.")
                    st.experimental_rerun()  # Cập nhật trang sau khi đổi tên

            # Nút xóa
            if st.button(f"Xóa {file_name}", key=f"delete_{file_name}"):
                os.remove(file_path)
                st.success(f"Tệp {file_name} đã được xóa.")
                st.experimental_rerun()  # Cập nhật trang sau khi xóa
    else:
        st.info("Không có tệp nào.")
