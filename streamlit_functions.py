import streamlit as st
import sql
from docxtpl import DocxTemplate
import datetime


@st.dialog("Добавление роли")
def adding_role():
    role_name = st.text_input("Название роли")
    with st.container(border=True):
        st.subheader("Роли")
        creating_roles = st.checkbox("Создание", key=1)
        editing_roles = st.checkbox("Редактирование", key=2)
        deleting_roles = st.checkbox("Удаление", key=3)
    with st.container(border=True):
        st.subheader("Пользователи")
        creating_users = st.checkbox("Создание", key=4)
        editing_users = st.checkbox("Редактирование", key=5)
        deleting_users = st.checkbox("Удаление", key=6)
    with st.container(border=True):
        st.subheader("Сезоны")
        adding_seasons = st.checkbox("Создание", key=7)
        editing_seasons = st.checkbox("Редактирование", key=8)
        deleting_seasons = st.checkbox("Удаление", key=9)
    with st.container(border=True):
        st.subheader("Филиалы")
        adding_filials = st.checkbox("Создание", key=10)
        editing_filials = st.checkbox("Редактирование", key=11)
        deleting_filials = st.checkbox("Удаление", key=12)
    with st.container(border=True):
        st.subheader("Группы")
        adding_groups = st.checkbox("Создание", key=13)
        editing_groups = st.checkbox("Редактирование", key=14)
        deleting_groups = st.checkbox("Удаление", key=15)
    with st.container(border=True):
        st.subheader("Жители")
        adding_leavers = st.checkbox("Создание", key=16)
        editing_leavers = st.checkbox("Редактирование", key=17)
        deleting_leavers = st.checkbox("Удаление", key=18)
    with st.container(border=True):
        st.subheader("Платежи")
        adding_payments = st.checkbox("Создание", key=19)
        editing_payments = st.checkbox("Редактирование", key=20)
        deleting_payments = st.checkbox("Удаление", key=21)
    with st.container(border=True):
        st.subheader("Списания")
        adding_cancelations = st.checkbox("Создание", key=22)
        editing_cancelations = st.checkbox("Редактирование", key=23)
        deleting_cancelations = st.checkbox("Удаление", key=24)
    if st.button("Создать роль", key="role_create_confirmation"):
        if not role_name:
            st.error("Ведите название роли")
        else:
            existing = sql.Role.get_roles_list()
            if role_name in existing:
                st.error("Роль с таким именем уже существует")
            else:
                sql.Role.add_role(role_name=role_name,
                                  creating_roles=creating_roles,
                                  editing_roles=editing_roles,
                                  deleting_roles=deleting_roles,
                                  creating_users=creating_users,
                                  editing_users=editing_users,
                                  deleting_users=deleting_users,
                                  adding_seasons=adding_seasons,
                                  editing_seasons=editing_seasons,
                                  deleting_seasons=deleting_seasons,
                                  adding_filials=adding_filials,
                                  editing_filials=editing_filials,
                                  deleting_filials=deleting_filials,
                                  adding_groups=adding_groups,
                                  editing_groups=editing_groups,
                                  deleting_groups=deleting_groups,
                                  adding_leavers=adding_leavers,
                                  editing_leavers=editing_leavers,
                                  deleting_leavers=deleting_leavers,
                                  adding_payments=adding_payments,
                                  editing_payments=editing_payments,
                                  deleting_payments=deleting_payments,
                                  adding_cancelations=adding_cancelations,
                                  editing_cancelations=editing_cancelations,
                                  deleting_cancelations=deleting_cancelations
                                  )
                st.rerun()


@st.dialog("Редактирование роли")
def editing_role():
    roles = sql.Role.get_roles()
    roles_list = roles["role_name"].tolist()
    selected_role = st.selectbox("Выберите роль", roles_list, index=None)
    if selected_role:
        info = roles[roles["role_name"] == selected_role].reset_index()
        new_name = st.text_input("Новое название роли", selected_role)
        with st.container(border=True):
            st.subheader("Роли")
            creating_roles = st.checkbox("Создание", key=1, value=info["creating_roles"][0])
            editing_roles = st.checkbox("Редактирование", key=2, value=info["editing_roles"][0])
            deleting_roles = st.checkbox("Удаление", key=3, value=info["deleting_roles"][0])
        with st.container(border=True):
            st.subheader("Пользователи")
            creating_users = st.checkbox("Создание", key=4, value=info["creating_users"][0])
            editing_users = st.checkbox("Редактирование", key=5, value=info["editing_users"][0])
            deleting_users = st.checkbox("Удаление", key=6, value=info["deleting_users"][0])
        with st.container(border=True):
            st.subheader("Сезоны")
            adding_seasons = st.checkbox("Создание", key=7, value=info["adding_seasons"][0])
            editing_seasons = st.checkbox("Редактирование", key=8, value=info["editing_seasons"][0])
            deleting_seasons = st.checkbox("Удаление", key=9, value=info["deleting_seasons"][0])
        with st.container(border=True):
            st.subheader("Филиалы")
            adding_filials = st.checkbox("Создание", key=10, value=info["adding_filials"][0])
            editing_filials = st.checkbox("Редактирование", key=11, value=info["editing_filials"][0])
            deleting_filials = st.checkbox("Удаление", key=12, value=info["deleting_filials"][0])
        with st.container(border=True):
            st.subheader("Группы")
            adding_groups = st.checkbox("Создание", key=13, value=info["adding_groups"][0])
            editing_groups = st.checkbox("Редактирование", key=14, value=info["editing_groups"][0])
            deleting_groups = st.checkbox("Удаление", key=15, value=info["deleting_groups"][0])
        with st.container(border=True):
            st.subheader("Жители")
            adding_leavers = st.checkbox("Создание", key=16, value=info["adding_leavers"][0])
            editing_leavers = st.checkbox("Редактирование", key=17, value=info["editing_leavers"][0])
            deleting_leavers = st.checkbox("Удаление", key=18, value=info["deleting_leavers"][0])
        with st.container(border=True):
            st.subheader("Платежи")
            adding_payments = st.checkbox("Создание", key=19, value=info["adding_payments"][0])
            editing_payments = st.checkbox("Редактирование", key=20, value=info["editing_payments"][0])
            deleting_payments = st.checkbox("Удаление", key=21, value=info["deleting_payments"][0])
        with st.container(border=True):
            st.subheader("Списания")
            adding_cancelations = st.checkbox("Создание", key=22, value=info["adding_cancelations"][0])
            editing_cancelations = st.checkbox("Редактирование", key=23, value=info["editing_cancelations"][0])
            deleting_cancelations = st.checkbox("Удаление", key=24, value=info["deleting_cancelations"][0])

        if st.button("Редактировать роль"):
            roles_list.remove(selected_role)
            if new_name in roles_list:
                st.error("Роль с таким названием уже существует")
            else:
                sql.Role.update_role(selected_role,
                                     new_data={"role_name": new_name,
                                               "creating_roles": creating_roles,
                                               "editing_roles": editing_roles,
                                               "deleting_roles": deleting_roles,
                                               "creating_users": creating_users,
                                               "editing_users": editing_users,
                                               "deleting_users": deleting_users,
                                               "adding_seasons": adding_seasons,
                                               "editing_seasons": editing_seasons,
                                               "deleting_seasons": deleting_seasons,
                                               "adding_filials": adding_filials,
                                               "editing_filials": editing_filials,
                                               "deleting_filials": deleting_filials,
                                               "adding_groups": adding_groups,
                                               "editing_groups": editing_groups,
                                               "deleting_groups": deleting_groups,
                                               "adding_leavers": adding_leavers,
                                               "editing_leavers": editing_leavers,
                                               "deleting_leavers": deleting_leavers,
                                               "adding_payments": adding_payments,
                                               "editing_payments": editing_payments,
                                               "deleting_payments": deleting_payments,
                                               "adding_cancelations": adding_cancelations,
                                               "editing_cancelations": editing_cancelations,
                                               "deleting_cancelations": deleting_cancelations
                                               })
                st.rerun()


@st.dialog("Удаление роли")
def deleting_role():
    role_selector = st.selectbox("Выберите роль", sql.Role.get_roles_list(), index=None)
    if st.button("Удалить роль", key="delete_role_accept"):
        try:
            sql.Role.delete_role(role_selector)
        except Exception as e:
            st.error("Нельзя удалить роль к которой привязаны пользователи")
        st.rerun()


@st.dialog("Добавление пользователя")
def add_user():
    username = st.text_input("Логин пользователя")
    existing_users_roles = sql.Role.get_roles_list()
    user_role = st.selectbox("Роль пользователя", existing_users_roles)
    user_pass = st.text_input("Пароль для пользователя", type="password")
    user_pass_confirmation = st.text_input("Подтверждение пароля", type="password")
    if st.button("Добавить пользователя", key="add_user_accept_btn"):
        if username in sql.User.get_user_list():
            st.error("Пользователь с таким именем уже существует")
        elif user_role is None:
            st.error("Выберите роль пользователя")
        elif user_pass != user_pass_confirmation:
            st.error("Пароли не совпадают")
        else:
            sql.User.add_user(role_name=user_role,
                              user_name=username,
                              password=user_pass)
            st.toast("Пользователь добавлен")
            st.rerun()


@st.dialog("Редактирование пользователя")
def edit_user():
    data = sql.User.get_users_data()
    users_list = data["user_name"].to_list()
    user_selector = st.selectbox("Пользователь", users_list)
    if user_selector:
        user_data = data[data["user_name"] == user_selector].reset_index(drop=True)
        current_user_name = user_data["user_name"][0]
        current_role_name = user_data["role_name"][0]
        current_password = user_data["password"][0]

        new_name = st.text_input("Новое имя пользователя", user_selector)
        roles = sql.Role.get_roles_list()
        new_role_name = st.selectbox("Новая роль", roles, index=roles.index(current_role_name))
        new_password = st.text_input("Новый пароль", current_password, type="password")

        name_changed = new_name != current_user_name
        role_changed = new_role_name != current_role_name
        pass_changed = new_password != current_password
        if pass_changed:
            new_password_confirmation = st.text_input("Подтверждение пароля", type="password")
        else:
            new_password_confirmation = st.text_input("Подтверждение пароля", current_password, type="password")

        something_changed = any([name_changed, role_changed, pass_changed])

        if st.button("Изменить данные пользователя", disabled=not something_changed):
            if new_password_confirmation != new_password:
                st.error("Пароли не совпадают")
            elif name_changed and new_name in users_list:
                st.error("Пользователь с таким именем уже существует")
            else:
                sql.User.edit_user(user_selector, new_name, new_role_name, new_password)
                st.rerun()


@st.dialog("Удаление пользователя")
def delete_user():
    user_list = sql.User.get_user_list()
    user_selector = st.selectbox("Пользователь", user_list, index=None)
    if user_selector:
        if st.button("Удалить пользователя"):
            sql.User.delete_user(user_selector)
            st.rerun()


@st.dialog("Добавление сезона")
def add_season():
    existing_seasons = sql.Season.get_season_list()
    season_name = st.text_input("Название сезона", key="name")
    season_start = st.date_input("Начало сезона", key="start", format="DD.MM.YYYY")
    season_end = st.date_input("Окончание сезона", key="end", format="DD.MM.YYYY")
    if st.button("Добавить сезон"):
        if season_name in existing_seasons:
            st.error("Сезон с таким названием уже существует")
        elif not season_name:
            st.error("Введите название сезона")
        else:
            sql.Season.add_season(name=season_name,
                                  start_date=season_start,
                                  end_date=season_end)
            st.rerun()


@st.dialog("Редактирование сезона")
def edit_season(season_selector):
    data = sql.Season.get_season_data(season_selector)

    current_name = data["name"]
    current_start = data["start_date"]
    current_end = data["end_date"]

    new_name = st.text_input("Название", current_name)
    new_start = st.date_input("Дата начала", current_start, format="DD.MM.YYYY")
    new_end = st.date_input("Дата окончания", current_end, format="DD.MM.YYYY")

    name_changed = new_name != current_name
    start_changed = new_start != current_start
    end_changed = new_end != current_end

    something_changed = any([name_changed, start_changed, end_changed])

    if st.button("Редактировать сезон", key="seas_edit",
                 disabled=not something_changed):
        if name_changed and new_name in sql.Season.get_season_list():
            st.error("Сезон с таким названием уже существует")
        else:
            sql.Season.edit_season(season_selector, new_name, new_start, new_end)
            st.rerun()


@st.dialog("Удаление сезона")
def delete_season(season_selector):
    st.write(f"Подтвердите удаление {season_selector}")
    if st.button("Удалить"):
        try:
            sql.Season.delete_season(season_selector)
        except:
            st.error("Нельзя удалить сезон в котором есть филиалы")
        st.rerun()


@st.dialog("Добавление филиала")
def add_filial(season_selector):
    filials = sql.Filial.show_filials_for_season(season_selector)["name"].tolist()
    fil_name = st.text_input("Название филиала")
    if st.button("Добавить филиал"):
        if fil_name in filials:
            st.error("Филиал с таким названием уже существует в сезоне")
        elif not fil_name:
            st.error("Введите название филиала")
        else:
            sql.Filial.add_filial(season_selector, name=fil_name)
            st.rerun()


@st.dialog("Редактирование филиала")
def edit_filial(season_selector, filial):
    filials = sql.Filial.show_filials_for_season(season_selector)["name"].tolist()
    new_name = st.text_input("Новое имя филиала", filial)

    name_changed = new_name != filial

    if st.button("Редактировать филиал", disabled=not name_changed, key="edit_fil"):
        if name_changed and new_name in filials:
            st.error("Филиал с таким именем уже существует в сезоне")
        else:
            sql.Filial.edit_filial(season_selector, filial, new_name)
            st.rerun()


@st.dialog("Удаление филиала")
def delete_filial(season_selector, filial):
    st.write(f"Удаление филиала {filial} из {season_selector}")
    if st.button("Удалить", key="del_fil"):
        try:
            sql.Filial.delete_filial_from_season(season_selector, filial)
        except:
            st.error("Нельзя удалить филиал, в котором есть группы")
        st.rerun()


@st.dialog("Добавление группы")
def add_group(season_selector, filial):
    groups_in_filial = sql.Group.get_groups_list_for_filial_in_season(season_selector, filial)
    group_name = st.text_input("Название группы")
    capacity = st.number_input("Количество детей", min_value=1, step=1)
    start_date = st.date_input("Дата начала", format="DD.MM.YYYY")
    end_date = st.date_input("Дата окончания", format="DD.MM.YYYY")
    if st.button("Добавить группу"):
        if not group_name:
            st.error("Введите название группы")
        elif group_name in groups_in_filial:
            st.error(f"Группа с таким названием уже существует в филиале {filial}")
        else:
            sql.Group.add_group_to_filial_in_season(season_selector, filial,
                                                    name=group_name,
                                                    capacity=capacity,
                                                    start_date=start_date,
                                                    end_date=end_date)
            st.rerun()


@st.dialog("Редактирование группы")
def edit_group(season_selector, filial, group):
    groups_in_filial_list = sql.Group.get_groups_list_for_filial_in_season(season_selector, filial)
    data = sql.Group.get_groups()
    group_info = data[data["name"] == group].reset_index(drop=True)

    current_name = group_info["name"][0]
    current_capacity = group_info["capacity"][0]
    current_start = group_info["start_date"][0]
    current_end = group_info["end_date"][0]

    new_name = st.text_input("Название группы", current_name)
    new_capacity = st.number_input("Кол-во детей", min_value=0, value=current_capacity)
    new_start = st.date_input("Дата начала", current_start, format="DD.MM.YYYY")
    new_end = st.date_input("Дата окончания", current_end, format="DD.MM.YYYY")

    name_changed = new_name != current_name
    capacity_changed = new_capacity != current_capacity
    start_changed = new_start != current_start
    end_changed = new_end != current_end

    something_changed = any([name_changed, capacity_changed, start_changed, end_changed])

    if st.button("Редактировать группу", disabled=not something_changed):
        if name_changed and new_name in groups_in_filial_list:
            st.error(f"Группа с таким названием уже существует в филиале {filial}")
        else:
            sql.Group.edit_group_in_filial_in_season(season_selector, filial, group,
                                                     new_group_data={"name": new_name,
                                                                     "capacity": new_capacity,
                                                                     "start_date": new_start,
                                                                     "end_date": new_end})
            st.rerun()


@st.dialog("Удаление группы")
def delete_group(season_selector, filial, group):
    st.write(f"Удаление группы {group} из {filial}")
    if st.button("Удалить", key="del_fil"):
        try:
            sql.Group.delete_group_from_filial_in_season(season_selector, filial, group)
        except:
            st.error("Нельзя удалить группу, в которой есть дети")
        st.rerun()


@st.dialog("Перенос ребенка между группами")
def move_child(season_selector_out, filial_out, group_out):
    child_list = sql.Group.get_children_list_in_group(season_selector_out, filial_out, group_out)
    child_selector = st.selectbox("Ребенок", child_list, index=None)
    if child_selector:
        seasons_list = sql.Season.get_season_list()
        season_selector_in = st.selectbox("Сезон", seasons_list, index=None)
        if season_selector_in:
            filials_list = sql.Filial.show_filials_for_season(season_selector_in)
            filial_selector_in = st.selectbox("Филиал", filials_list)
            if filial_selector_in:
                groups_list = sql.Group.get_groups_list_for_filial_in_season(season_selector_in,
                                                                             filial_selector_in)
                group_in = st.selectbox("Группа", groups_list)
                if st.button("Перенести", key="move"):
                    sql.Group.move_child_to_group(season_selector_out, filial_out, group_out,
                                                  child_selector,
                                                  season_selector_in, filial_selector_in, group_in)
                    st.rerun()


@st.dialog("Добавление ребенка в группу")
def add_child_to_group(season_selector, filial, group):
    addition_type = st.radio("Тип добавления", ["Жители городка", "Новый"])
    child_list = sql.Child.get_child_list()

    if addition_type == "Жители городка":
        child_selector = st.selectbox("Ребенок", child_list, index=None)
        if child_selector:
            if st.button("Добавить", key="add"):
                sql.Group.add_child_to_group(season_selector, filial, group, child_selector)
                st.rerun()
    else:
        child_name = st.text_input("Имя ребенка")
        age = st.number_input("Возраст ребенка", min_value=0, step=1, value=0)
        parent_name = st.text_input("Родитель")
        parent_phone = st.text_input("Номер телефона")
        if st.button("Добавить", key="add2"):
            if child_name in child_list:
                st.write("Ребенок с таким именем уже существует")
            else:
                sql.Child.add_child(name=child_name,
                                    age=age,
                                    parent_main_name=parent_name,
                                    parent_main_phone=parent_phone)
                sql.Group.add_child_to_group(season_selector, filial, group, child_name)
                st.rerun()


@st.dialog("Удаление ребенка из группы")
def delete_child_from_group(season_selector, filial, group):
    child_list = sql.Group.get_children_list_in_group(season_selector, filial, group)
    child_selector = st.selectbox("Ребенок", child_list, index=None)
    if child_selector:
        if st.button("Удалить ребенка из группы"):
            sql.Group.remove_child_from_group(season_selector, filial, group, child_selector)
            st.rerun()


@st.dialog("Редактирование данных ребенка")
def edit_child_data(child, new_data):
    if st.button("Редактировать", key="edit"):
        sql.Child.edit_child_data(child, new_data)
        st.rerun()


@st.dialog("Договор")
def generate_order(child_data):
    ord_num = st.text_input("Номер договора")
    checkbox = st.checkbox("Не из списка")

    if checkbox:
        child_fio_selector = st.text_input("ФИО ребенка:", value=None)
        adult_fio = st.text_input("ФИО родителя", value=None)
        child_birthday = st.date_input("ДР Ребенка", format="DD.MM.YYYY", value=None)
        adult_passport = st.text_input("Паспортные данные родителя", value=None)
        adult_adress = st.text_input("Адрес регистрации родителя", value=None)
        child_adress = st.text_input("Адрес проживания ребенка", value=None)
        adult_phonenum = st.text_input("Номер телефона родителя", value=None)
        adult_email = st.text_input("Email")
    else:
        child_fio_selector = st.text_input("ФИО ребенка:", child_data["name"][0])
        adult_fio = st.text_input("ФИО родителя", child_data["parent_main_name"][0])
        child_birthday = st.date_input("ДР Ребенка", child_data["child_birthday"][0], format="DD.MM.YYYY")
        adult_passport = st.text_input("Паспортные данные родителя", child_data["parent_passport"][0])
        adult_adress = st.text_input("Адрес регистрации родителя", child_data["parent_adress"][0])
        child_adress = st.text_input("Адрес проживания ребенка", child_data["addr"][0])
        adult_phonenum = st.text_input("Номер телефона родителя", child_data["parent_main_phone"][0])
        adult_email = st.text_input("Email", child_data["email"][0])

    if st.button("Сгенерировать договор", key="generate_order"):
        if not ord_num:
            st.error("Введите номер договора")
        elif not child_fio_selector:
            st.error("Введите ФИО ребенка")
        elif not adult_fio:
            st.error("Введите ФИО взрослого")
        elif not child_birthday:
            st.error("Введите ДР ребенка")
        elif not adult_passport:
            st.error("Введите паспортные данные")
        elif not adult_adress:
            st.error("Введите адрес регистрации")
        elif not child_adress:
            st.error("Введите адрес проживания ребенка")
        elif not adult_phonenum:
            st.error("Введите номер телефона")
        elif not adult_email:
            st.error("Введите email")
        else:
            day = datetime.date.today().day
            month = {1: "января", 2: "февраля", 3: "марта", 4: "апреля", 5: "мая", 6: "июня",
                     7: "июля", 8: "августа", 9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"}[
                datetime.date.today().month]
            year = datetime.date.today().year
            child_birth_year = child_birthday.year
            adult = adult_fio.split(" ")
            adult_initials = f"{adult[0]} {adult[1][0]}. {adult[2][0]}."
            doc = DocxTemplate("Order_mockup.docx")
            context = {'ord_num': ord_num, "day": day, "month": month, "year": year,
                       "adult_fio": adult_fio, "child_fio": child_fio_selector, "child_birth_year": child_birth_year,
                       "adult_passport": adult_passport, "adult_adress": adult_adress, "child_adress": child_adress,
                       "adult_phonenum": adult_phonenum, "adult_email": adult_email, "adult_initials": adult_initials}
            doc.render(context)
            doc.save("шаблон-final.docx")
            st.success("Договор сгенерирован")
            with open("шаблон-final.docx", "rb") as f:
                st.download_button('Скачать договор', f, file_name=f"Договор_{ord_num}.docx")
