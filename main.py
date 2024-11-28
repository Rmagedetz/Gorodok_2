import streamlit as st
import sql

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

st.set_page_config(
    page_title="Городок",  # Заголовок страницы
    layout="wide"  # Широкий режим
)


def login():
    with st.form("login_form", clear_on_submit=True):
        st.title("Вход в приложение")
        user_input = st.text_input("Введите логин")
        password_input = st.text_input("Введите пароль", type="password")
        submit = st.form_submit_button("Войти")

        if submit:
            if user_input in sql.User.get_user_list_for_login():
                if password_input == sql.User.check_user_password(user_input):
                    st.session_state.logged_in = True
                    st.session_state.user = user_input
                    st.session_state.user_role_data = sql.User.get_user_role_data(user_input)
                    st.rerun()
                else:
                    st.error("Неверный логин или пароль")
            else:
                st.error("Неверный логин или пароль")


def logout():
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.role = None
    st.rerun()


login_page = st.Page(login, title="Log in", icon=":material/login:")
logout_page = st.Page(logout, title="Выйти", icon=":material/logout:")

main_page = st.Page("pages/main_page.py", title="Главная", icon=":material/home:", default=True)
records_page = st.Page("pages/records.py", title="Записи")
children = st.Page("pages/children.py", title="Жители Городка")
group_cards = st.Page("pages/group_card.py", title="Карточки групп")
payments = st.Page("pages/payments.py", title="Платежи")
bills = st.Page("pages/bills.py", title="Списания")

if st.session_state.logged_in:
    pg = st.navigation(
        {
            "Логин": [logout_page],
            "Страницы": [main_page, records_page, children, group_cards, payments, bills]
        }
    )
else:
    pg = st.navigation([login_page])

pg.run()
