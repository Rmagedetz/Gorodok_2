import streamlit as st
import sql
from streamlit_functions import adding_role, editing_role, deleting_role, edit_user, add_user, delete_user

user = st.session_state.user
user_role = st.session_state.user_role_data

roles, users = st.tabs(["Роли", "Пользователи"])
with roles:
    roles = sql.Role.get_roles()
    data = st.dataframe(roles, column_config={"role_name": "Роль",
                                              "creating_roles": st.column_config.Column("Роли +",
                                                                                        help="Создание ролей",
                                                                                        width="small"),
                                              "editing_roles": st.column_config.Column("Роли *",
                                                                                       help="Редактирование ролей",
                                                                                       width="small"),
                                              "deleting_roles": st.column_config.Column("Роли -",
                                                                                        help="Удаление ролей",
                                                                                        width="small"),
                                              "creating_users": st.column_config.Column("Польз+",
                                                                                        help="Создание пользователей",
                                                                                        width="small"),
                                              "editing_users": st.column_config.Column("Польз*",
                                                                                       help="Редактирование "
                                                                                            "пользователей",
                                                                                       width="small"),
                                              "deleting_users": st.column_config.Column("Польз-",
                                                                                        help="Удаление пользователей",
                                                                                        width="small"),
                                              "adding_seasons": st.column_config.Column("Сез+",
                                                                                        help="Создание сезонов",
                                                                                        width="small"),
                                              "editing_seasons": st.column_config.Column("Сез*",
                                                                                         help="Редактирование сезонов",
                                                                                         width="small"),
                                              "deleting_seasons": st.column_config.Column("Сез-",
                                                                                          help="Удаление сезонов",
                                                                                          width="small"),
                                              "adding_filials": st.column_config.Column("Фил+",
                                                                                        help="Создание филиалов",
                                                                                        width="small"),
                                              "editing_filials": st.column_config.Column("Фил*",
                                                                                         help="Редактирование филиалов",
                                                                                         width="small"),
                                              "deleting_filials": st.column_config.Column("Фил-",
                                                                                          help="Удаление филиалов",
                                                                                          width="small"),
                                              "adding_groups": st.column_config.Column("Гр+",
                                                                                       help="Создание групп",
                                                                                       width="small"),
                                              "editing_groups": st.column_config.Column("Гр*",
                                                                                        help="Редактирование групп",
                                                                                        width="small"),
                                              "deleting_groups": st.column_config.Column("Гр-",
                                                                                         help="Удаление групп",
                                                                                         width="small"),
                                              "adding_leavers": st.column_config.Column("Жит+",
                                                                                        help="Создание жителей",
                                                                                        width="small"),
                                              "editing_leavers": st.column_config.Column("Жит*",
                                                                                         help="Редактирование жителей",
                                                                                         width="small"),
                                              "deleting_leavers": st.column_config.Column("Жит-",
                                                                                          help="Удаление жителей",
                                                                                          width="small"),
                                              "adding_payments": st.column_config.Column("Плт+",
                                                                                         help="Создание платежей",
                                                                                         width="small"),
                                              "editing_payments": st.column_config.Column("Плт*",
                                                                                          help="Редактирование платежей",
                                                                                          width="small"),
                                              "deleting_payments": st.column_config.Column("Плт-",
                                                                                           help="Удаление платежей",
                                                                                           width="small"),
                                              "adding_cancelations": st.column_config.Column("Спис+",
                                                                                             help="Создание списаний",
                                                                                             width="small"),
                                              "editing_cancelations": st.column_config.Column("Спис*",
                                                                                              help="Редактирование "
                                                                                                   "списаний",
                                                                                              width="small"),
                                              "deleting_cancelations": st.column_config.Column("Спис-",
                                                                                               help="Удаление списаний",
                                                                                               width="small")
                                              }, hide_index=True)

    if st.button("Добавить роль", disabled=not user_role["creating_roles"], key="add_role"):
        adding_role()
    if st.button("Редактировать роль", disabled=not user_role["editing_roles"], key="edit_role"):
        editing_role()
    if st.button("Удалить роль", disabled=not user_role["deleting_roles"], key="delete_role"):
        deleting_role()

with users:
    users = sql.User.get_users_with_roles()
    data = st.dataframe(users, column_config={"user_name": "Пользователь",
                                              "role_name": "Роль"}, hide_index=True)

    if st.button("Добавить пользователя", disabled=not user_role["creating_users"], key="add_user"):
        add_user()
    if st.button("Редактировать пользователя", disabled=not user_role["editing_users"], key="edit_user"):
        edit_user()
    if st.button("Удалить пользователя", disabled=not user_role["deleting_users"], key="delete_user"):
        delete_user()

