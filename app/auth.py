import streamlit as st
import json

def load_users():
    """Tải danh sách người dùng từ tệp JSON"""
    try:
        with open('users.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_users(users):
    """Lưu danh sách người dùng vào tệp JSON"""
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=4)

def register_user(username, password):
    """Hàm đăng ký người dùng"""
    if username and password:
        # Tải danh sách người dùng hiện có từ tệp
        users = load_users()
        
        # Kiểm tra xem người dùng đã tồn tại chưa
        if username in users:
            st.error("Tên đăng nhập đã tồn tại. Vui lòng chọn tên khác.")
            return False
        
        # Thêm người dùng mới vào danh sách
        users[username] = {'password': password, 'files': []}
        
        # Lưu lại vào tệp users.json
        save_users(users)
        
        # Lưu thông tin đăng nhập vào session_state
        st.session_state['username'] = username
        st.session_state['password'] = password
        st.success("Đăng ký thành công!")
        return True
    else:
        st.error("Vui lòng điền đầy đủ thông tin!")
        return False

def login_user(username, password):
    """Hàm đăng nhập"""
    users = load_users()
    
    if username in users and users[username]['password'] == password:
        # Lưu thông tin đăng nhập vào session_state
        st.session_state['username'] = username
        st.session_state['password'] = password
        st.success("Đăng nhập thành công!")
        return True
    else:
        st.error("Sai tên đăng nhập hoặc mật khẩu!")


def logout_user():
    """Hàm đăng xuất"""
    # Đặt lại trạng thái đăng nhập
    st.session_state['logged_in'] = False
    st.session_state['show_login'] = True
    
    # Hiển thị thông báo thành công
    st.success("Đăng xuất thành công!")
    
    # Tải lại trang và quay lại màn hình đăng nhập
    # Sau khi đăng xuất, chúng ta cần đặt lại trạng thái để quay lại trang đăng nhập/đăng ký
    st.session_state['show_login'] = True
    st.rerun()  # Thay thế experimental_rerun() bằng st.rerun()
