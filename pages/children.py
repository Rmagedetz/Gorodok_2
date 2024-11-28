import streamlit as st
import sql
from datetime import datetime

from streamlit_functions import edit_child_data, generate_order
from gtables_functions import get_quiz_data

user = st.session_state.user
user_role = st.session_state.user_role_data

data = sql.Child.get_children()

if st.button("Подгрузить данные анкет"):
    st.toast("Подключаемся к анкетам")
    data = get_quiz_data()
    st.write(data)
    st.toast("Обновляем данные")
    sql.Child.add_children_from_dataframe(data)
    st.toast("Данные обновлены")

if not data.empty:
    child_list = data["name"].tolist()
    child_selector = st.selectbox("Ребенок", child_list, index=None)
    if child_selector:
        child_data = data[data["name"] == child_selector].reset_index(drop=True)

        quiz, payments, visits_info = st.tabs(["Анкетные данные", "Платежи и списания", "Посещения"])
        with visits_info:
            visits_info = sql.Visits.get_visits_by_child_name(child_selector)
            table = st.dataframe(visits_info, column_config={"season_name": "Сезон",
                                                             "filial_name": "Филиал",
                                                             "group_name": "Группа",
                                                             "day": "День",
                                                             "visit": "Статус"})
        with payments:
            pay_info = sql.Payments.get_payments_by_child_name(child_selector)
            if not pay_info.empty:
                del pay_info["child_name"]
                summa = pay_info["amount"].sum()
                st.subheader(f"Платежи: {summa}")
                tbl = st.dataframe(pay_info, key="pay_info",
                                   column_config={
                                       "payment_date": st.column_config.DateColumn("Дата", format="DD.MM.YYYY"),
                                       "amount": "Сумма",
                                       "recorded_by": "Кто провел",
                                       "comment": "Коментарий"})
            else:
                summa = 0
            bills_data = sql.Bills.get_bills_by_child_name(child_selector)

            if not bills_data.empty:
                del bills_data["child_name"]
                summa_bills = bills_data["amount"].sum()
                st.subheader(f"Списания: {summa_bills}")
                bl_tbl = st.dataframe(bills_data,
                                      column_config={
                                          "payment_date": st.column_config.DateColumn("Дата", format="DD.MM.YYYY"),
                                          "amount": "Сумма",
                                          "recorded_by": "Кто провел",
                                          "comment": "Коментарий",
                                          "season_name": "Сезон",
                                          "filial_name": "Филиал",
                                          "group_name": "Группа"}
                                      )
            else:
                summa_bills = 0
            balance = summa - summa_bills
            st.subheader(f"Баланс: {balance}")
        with quiz:
            with st.container(border=True):
                st.subheader("Общие данные")

                new_name = st.text_input("Имя ребенка",
                                         child_data["name"][0],
                                         key="new_name")
                new_age = st.number_input("Возраст ребенка",
                                          step=1,
                                          value=datetime.now().year - child_data["child_birthday"][0].year
                                          if child_data["child_birthday"][0] else 0,
                                          key="new_age")
                new_parent_name = st.text_input("ФИО Родителя",
                                                value=child_data["parent_main_name"][0],
                                                key="new_parent")
                new_parent_phone = st.text_input("Телефон Родителя",
                                                 value=child_data["parent_main_phone"][0],
                                                 key="new_phone")

            with st.container(border=True):
                st.subheader("Анкетные данные")

                new_mail = st.text_input("Электронная почта",
                                         value=child_data["email"][0],
                                         key="new_mail")
                new_birthday = st.date_input("Дата рождения",
                                             value=child_data["child_birthday"][0],
                                             key="new_birthday",
                                             format="DD.MM.YYYY")
                new_parent_add = st.text_input("Дополнительный контакт",
                                               value=child_data["parent_add"][0],
                                               key="new_p_a")
                new_phone_add = st.text_input("Дополнительный номер",
                                              value=child_data["phone_add"][0],
                                              key="new_p_p")
                leave_variants = data["leave"].unique().tolist()
                new_leave = st.selectbox("Уходит сам?", leave_variants,
                                         key="new_leave",
                                         index=leave_variants.index(child_data["leave"][0]))
                new_additional_contact = st.text_input("Дополнительный контакт",
                                                       value=child_data["additional_contact"][0],
                                                       key="new_a_c")
                new_addr = st.text_input("Адрес",
                                         value=child_data["addr"][0],
                                         key="new_adr")
                new_disease = st.text_input("Заболевания",
                                            value=child_data["disease"][0],
                                            key="new_disease")
                new_allergy = st.text_input("Аллергия",
                                            value=child_data["allergy"][0],
                                            key="new_aller")
                new_other = st.text_input("Операции",
                                          value=child_data["other"][0],
                                          key="new_oper")
                new_physic = st.text_input("Ограничения",
                                           value=child_data["physic"][0],
                                           key="new_phys")
                swimm_vars = data["swimm"].unique().tolist()
                new_swimm = st.selectbox("Бассейн", swimm_vars,
                                         key="swimm",
                                         index=swimm_vars.index(child_data["swimm"][0]))
                jacket_vars = data["jacket_swimm"].unique().tolist()
                new_jacket_swimm = st.selectbox("Нарукавники",
                                                jacket_vars,
                                                key="jacket",
                                                index=jacket_vars.index(child_data["jacket_swimm"][0]))
                new_hobby = st.text_input("Хобби",
                                          value=child_data["hobby"][0],
                                          key="hobby")
                new_school = st.text_input("Школа",
                                           value=child_data["school"][0],
                                           key="school")
                new_additional_info = st.text_input("Доп информация",
                                                    value=child_data["additional_info"][0],
                                                    key="add_info")
                new_departures = st.text_input("Прогулки",
                                               value=child_data["departures"][0],
                                               key="walks")
                new_referer = st.text_input("Откуда узнали",
                                            value=child_data["referer"][0],
                                            key="referer")
                new_ok = st.text_input("Подтверждение сведений",
                                       value=child_data["ok"][0],
                                       key="check")
                new_mailing = st.text_input("Согласие на рассылку",
                                            value=child_data["mailing"][0],
                                            key="mailing")
                new_personal_accept = st.text_input("Обработка персональных данных",
                                                    value=child_data["personal_accept"][0],
                                                    key="pd")
                new_oms = st.text_input("Номер ОМС",
                                        value=child_data["oms"][0],
                                        key="oms")

            with st.container(border=True):
                st.subheader("Паспортные данные")
                new_parent_passport = st.text_input("Паспорт",
                                                    value=child_data["parent_passport"][0],
                                                    key="passp")
                new_parent_adress = st.text_input("Адрес",
                                                  value=child_data["parent_adress"][0],
                                                  key="addr")
            if st.button("Редактировать данные", disabled=not user_role["editing_leavers"]):
                updated_data = {'name': new_name,
                                'age': new_age,
                                'parent_main_name': new_parent_name,
                                'parent_main_phone': new_parent_phone,
                                "email": new_mail,
                                "child_birthday": new_birthday,
                                "parent_add": new_parent_add,
                                "phone_add": new_phone_add,
                                "leave": new_leave,
                                "additional_contact": new_additional_contact,
                                "addr": new_addr,
                                "disease": new_disease,
                                "allergy": new_allergy,
                                "other": new_other,
                                "physic": new_physic,
                                "swimm": new_swimm,
                                "jacket_swimm": new_jacket_swimm,
                                "hobby": new_hobby,
                                "school": new_school,
                                "additional_info": new_additional_info,
                                "departures": new_departures,
                                "referer": new_referer,
                                "ok": new_ok,
                                "mailing": new_mailing,
                                "personal_accept": new_personal_accept,
                                "oms": new_oms,
                                "parent_passport": new_parent_passport,
                                "parent_adress": new_parent_adress}
                edit_child_data(child_selector, updated_data)

            if st.button("Сгенерировать договор", key="generate_order"):
                generate_order(child_data)

            if st.button("Удалить жителя",
                         key="del_leaver",
                         disabled=not user_role["deleting_leavers"]):
                sql.Child.delete_child(child_selector)
                st.rerun()
