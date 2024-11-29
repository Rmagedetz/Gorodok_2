import streamlit as st
import sql

user = st.session_state.user
user_role = st.session_state.user_role_data

loaded = sql.Persons.get_persons()
data = loaded[["child_name", "child_birthday",
               "parent_main", "parent_phone_num", "parent_email",
               "parent_passport", "parent_adress", "child_adress"]]

names = data["child_name"].unique().tolist()

name_selector = st.selectbox("Фильтр по ребенку", names, index=None)
columns_config = {"child_name": "ФИО",
                  "child_birthday": st.column_config.DateColumn("ДР", format="DD.MM.YYYY", width="small"),
                  "parent_main": st.column_config.Column("Род.", help="Родитель", width="medium"),
                  "parent_phone_num": st.column_config.Column("Тел.", help="Телефон родителя", width="small"),
                  "parent_email": st.column_config.Column("Email", width="small"),
                  "parent_passport": st.column_config.Column("Паспорт", width="small", help="Паспорт родителя"),
                  "parent_adress": st.column_config.Column("Адр1", width="small", help="Адрес родителя"),
                  "child_adress": st.column_config.Column("Адр2", width="small", help="Адрес ребенка")}
if name_selector:
    filtered = st.dataframe(data[data["child_name"] == name_selector], column_config=columns_config)
else:
    filtered = st.dataframe(data, column_config=columns_config)
