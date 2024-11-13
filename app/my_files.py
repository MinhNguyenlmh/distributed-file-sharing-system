import streamlit as st
import os

UPLOAD_FOLDER = 'uploads/'
PUBLIC_FOLDER = 'uploads/public/'

# Ensure public folder exists
if not os.path.exists(PUBLIC_FOLDER):
    os.makedirs(PUBLIC_FOLDER)

def my_files_view():
    st.header("Tệp của tôi")

    # Get all files in the uploads directory
    files = os.listdir(UPLOAD_FOLDER)

    if files:
        for file_name in files:
            file_path = os.path.join(UPLOAD_FOLDER, file_name)

            # Skip directories
            if os.path.isdir(file_path):
                continue

            st.subheader(f"File: {file_name}")
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])  # Create columns for functionality buttons
            
            # Display image if it's an image file
            if file_name.lower().endswith(('png', 'jpg', 'jpeg')):
                with col1:
                    st.image(file_path, caption=file_name, use_column_width=False, width=100)
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
                        mime="application/octet-stream"
                    )

            # Public button
            with col3:
                if st.button(f"Công khai {file_name}", key=f"public_{file_name}"):
                    public_file_path = os.path.join(PUBLIC_FOLDER, file_name)
                    if not os.path.exists(public_file_path):  # Avoid overwriting
                        os.rename(file_path, public_file_path)
                        st.success(f"Tệp {file_name} đã được công khai.")
                        st.experimental_rerun()  # Update the page after making public
                    else:
                        st.error(f"Tệp {file_name} đã tồn tại trong thư mục công khai.")

            # Rename section
            with col4:
                new_name = st.text_input(f"Đổi tên {file_name}", value=file_name, key=f"rename_input_{file_name}")
                rename_button_key = f"btn_rename_{file_name}"
                if st.button("Đổi tên", key=rename_button_key):
                    new_file_path = os.path.join(UPLOAD_FOLDER, new_name)
                    if not os.path.exists(new_file_path):  # Avoid overwriting
                        os.rename(file_path, new_file_path)
                        st.success(f"Tệp {file_name} đã được đổi tên thành {new_name}.")
                        st.experimental_rerun()  # Update the page after renaming
                    else:
                        st.error(f"Tệp với tên {new_name} đã tồn tại.")

            # Delete button
            if st.button(f"Xóa {file_name}", key=f"delete_{file_name}"):
                os.remove(file_path)
                st.success(f"Tệp {file_name} đã được xóa.")
                st.experimental_rerun()  # Update the page after deletion
    else:
        st.info("Không có tệp nào.")
