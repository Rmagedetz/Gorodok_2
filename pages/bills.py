import streamlit as st
import sql
import datetime

user = st.session_state.user
user_role = st.session_state.user_role_data


@st.dialog("Списание")
def payment_add():
    child = st.selectbox("Ребенок", sql.Child.get_child_list(), index=None)
    season = st.selectbox("Сезон", sql.Season.get_season_list(), index=None)
    if season:
        filial = st.selectbox("Филиал", sql.Filial.show_filials_for_season(season), index=None)
        if filial:
            group = st.selectbox("Группа", sql.Group.get_groups_list_for_filial_in_season(season, filial))
            summa = st.number_input("Сумма")
            comment = st.text_area("Комментарий")
            if st.button("Списать", key="payment_add_accept"):
                sql.add_bill(datetime.datetime.now(), child, group, summa, user, comment)
                st.rerun()


@st.dialog("Редактирование списания")
def payment_edit():
    payment_id = st.number_input("ID платежа", min_value=1, step=1)
    data = sql.get_bill_details(payment_id)
    if data.empty:
        st.write("Платеж не обнаружен в системе")
    else:
        payment_id = data["payment_id"][0]
        new_date = st.date_input("Дата платежа", value=data["payment_date"][0])
        new_child_name = st.selectbox("ФИО Ребенка", sql.Child.get_child_list(), index=None,
                                      help=f"{data["child_name"][0]}")

        new_amount = st.number_input("Сумма платежа", value=data["amount"][0])
        new_comment = st.text_area("Комментарий", value=data["comment"][0])
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Редактировать платеж", key="edit_payment"):
                sql.edit_payment_data(payment_id, new_date, new_child_name, new_amount, new_comment)
                st.rerun()
        with col2:
            if st.checkbox("Удалить платеж"):
                if st.button("Удалить платеж", key="delete_payment",
                             disabled=not user_role["deleting_payments"]):
                    sql.delete_payment(payment_id)
                    st.rerun()


st.write("Списания")
pays = sql.get_bills_dataframe()
pay_data = st.dataframe(pays, column_config={
    "payment_date": st.column_config.DateColumn("Дата", format="DD.MM.YYYY"),
    "amount": "Сумма",
    "user": "Кто провел",
    "comment": "Коментарий",
    "season_name": "Сезон",
    "filial_name": "Филиал",
    "group_name": "Группа",
    "child_name": "Ребенок"})

col1, col2, col3 = st.columns(3)
with col1:
    with st.container(border=True):
        if st.button("Добавить списание", key="add_payment",
                     disabled=not user_role["adding_payments"],
                     use_container_width=True):
            payment_add()
        # if st.button("Редактировать списание", key="payment_edit",
        #              disabled=not (sql.check_user_rights(user_logged, "editing_payments")),
        #              use_container_width=True):
        #     payment_edit()
