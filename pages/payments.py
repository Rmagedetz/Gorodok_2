import streamlit as st
import sql
import pandas as pd
import datetime

user = st.session_state.user
user_role = st.session_state.user_role_data


@st.dialog("Внесение платежа")
def payment_add():
    child = st.selectbox("Ребенок", sql.Child.get_child_list(), index=None)
    summa = st.number_input("Сумма")
    comment = st.text_area("Комментарий")
    if st.button("Внести платеж", key="payment_add_accept"):
        sql.add_payment(datetime.datetime.now(), child, summa, user, comment)
        st.rerun()


@st.dialog("Редактирование платежа")
def payment_edit():
    payment_id = st.number_input("ID платежа", min_value=1, step=1)
    data = sql.get_payment_details(payment_id)
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


st.write("Платежи")
pays = sql.get_payments_dataframe()
df = st.dataframe(pays, column_config={
    "payment_date": st.column_config.DateColumn("Дата", format="DD.MM.YYYY"),
    "payment_amount": "Сумма",
    "user": "Кто провел",
    "comment": "Коментарий",
    "child_name": "Ребенок"})

col1, col2, col3 = st.columns(3)
with col1:
    with st.container(border=True):
        if st.button("Добавить платеж", key="add_payment",
                     disabled=not user_role["adding_payments"],
                     use_container_width=True):
            payment_add()
        if st.button("Редактировать платеж", key="payment_edit",
                     disabled=not user_role["editing_payments"],
                     use_container_width=True):
            payment_edit()
