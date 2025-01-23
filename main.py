import streamlit as st
import sql

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

st.set_page_config(
    page_title="Записи и группы Городок",
    layout="wide",
    page_icon="logo.png"
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

main_page = st.Page("pages/main_page.py", title="Пользователи и роли", icon=":material/manage_accounts:")
records_page = st.Page("pages/records.py", title="Записи", icon=":material/table_view:", default=True)
children = st.Page("pages/children.py", title="Жители Городка", icon=":material/diversity_3:")
group_cards = st.Page("pages/group_card.py", title="Карточки групп", icon=":material/folder_shared:")
payments = st.Page("pages/payments.py", title="Платежи", icon=":material/payments:")
bills = st.Page("pages/bills.py", title="Списания", icon=":material/receipt_long:")
old_base = st.Page("pages/old_base.py", title="Выгрузка", icon=":material/table_eye:")

if st.session_state.logged_in:
    pg = st.navigation(
        {
            "Администрирование": [logout_page, main_page],
            "Дети и группы": [records_page, children, group_cards],
            "Платежи и списания": [payments, bills],
            "База Мой класс": [old_base]
        }
    )
    big_logo = "logo_2.png"
    small_logo = "logo.png"
    st.logo(big_logo, size="large", icon_image=small_logo)
else:
    pg = st.navigation([login_page])

pg.run()
