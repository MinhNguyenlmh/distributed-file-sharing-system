import streamlit as st
from app.upload import upload_view
from app.my_files import my_files_view
from app.public_files import public_files_view

def main():
    st.title("Ứng dụng chia sẻ file - Mini Drive")
    st.sidebar.title("Tùy chọn")
    
    menu = ["Tải lên tệp", "Tệp của tôi", "Tệp công khai"]
    choice = st.sidebar.selectbox("Chọn chức năng", menu)
    
    if choice == "Tải lên tệp":
        upload_view()
    elif choice == "Tệp của tôi":
        my_files_view()
    elif choice == "Tệp công khai":
        public_files_view()

if __name__ == "__main__":
    main()

