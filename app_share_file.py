import streamlit as st
from app.auth import register_user, login_user, logout_user
from app.upload import upload_view
from app.my_files import my_files_view
from app.public_files import public_files_view

def main():
    """Hàm chính của ứng dụng"""
    st.title("Ứng Dụng Chia Sẻ Tệp")
    
    # Kiểm tra session state
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    
    if 'show_login_register' not in st.session_state:
        st.session_state['show_login_register'] = True

    # Kiểm tra trạng thái đăng nhập
    if not st.session_state['logged_in']:
        # Nếu chưa đăng nhập, hiển thị các lựa chọn đăng ký và đăng nhập
        login_option()
    else:
        # Nếu đã đăng nhập, hiển thị giao diện chính
        app_menu()

def login_option():
    """Giao diện đăng nhập hoặc đăng ký"""
    if st.session_state['show_login_register']:
        option = st.radio("Chọn một thao tác:", ["Đăng ký", "Đăng nhập"])

        if option == "Đăng ký":
            st.header("Đăng ký người dùng")
            username = st.text_input("Tên đăng nhập")
            password = st.text_input("Mật khẩu", type="password")

            if st.button("Đăng ký"):
                if register_user(username, password):
                    # Đặt trạng thái đã đăng nhập và ẩn giao diện đăng ký, đăng nhập
                    st.session_state['logged_in'] = True
                    st.session_state['show_login_register'] = False
                    # Sau khi đăng ký thành công, hiển thị menu chính
                    app_menu()

        elif option == "Đăng nhập":
            st.header("Đăng nhập")
            username = st.text_input("Tên đăng nhập")
            password = st.text_input("Mật khẩu", type="password")

            if st.button("Đăng nhập"):
                if login_user(username, password):
                    # Đặt trạng thái đã đăng nhập và ẩn giao diện đăng ký, đăng nhập
                    st.session_state['logged_in'] = True
                    st.session_state['show_login_register'] = False
                    # Sau khi đăng nhập thành công, hiển thị menu chính
                    app_menu()



def app_menu():
    """Hiển thị menu sau khi người dùng đã đăng nhập"""
    st.sidebar.header("Chọn chức năng")
    menu_choice = st.sidebar.radio("Menu", ["Tải lên tệp", "Tệp của tôi", "Tệp công khai", "Đăng xuất"])

    if menu_choice == "Tải lên tệp":
        upload_view()
    elif menu_choice == "Tệp của tôi":
        my_files_view()
    elif menu_choice == "Tệp công khai":
        public_files_view()
    elif menu_choice == "Đăng xuất":
        logout_user()


def logout_user():
    """Hàm đăng xuất"""
    # Đặt lại trạng thái đăng nhập
    st.session_state['logged_in'] = False
    st.session_state['show_login_register'] = True

    # Hiển thị thông báo thành công
    st.success("Đăng xuất thành công!")
    
    # Tải lại trang và quay lại màn hình đăng nhập
    st.session_state['show_login_register'] = True
    st.rerun()  # Thay thế experimental_rerun() bằng st.rerun()


if __name__ == "__main__":
    main()
