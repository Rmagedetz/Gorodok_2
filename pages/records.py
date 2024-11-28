import streamlit as st
import sql
from streamlit_functions import (add_season, edit_season, delete_season,
                                 add_filial, edit_filial, delete_filial,
                                 add_group, edit_group, delete_group,
                                 move_child, add_child_to_group, delete_child_from_group)


user = st.session_state.user
user_role = st.session_state.user_role_data

season_list = sql.Season.get_season_list()
season_selector = st.selectbox("Сезон", season_list)


groups_info = sql.get_groups_with_children_count_and_paid_by_season(season_selector)

for filial, groups_list in groups_info.items():

    st.subheader(filial, divider=True)

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        if st.button(":material/edit:", use_container_width=True,
                     key=f"edit_filial_{filial}_in{season_selector}",
                     help=f"Редактировать {filial}",
                     disabled=not user_role["editing_filials"]
                     ):
            edit_filial(season_selector, filial)
    with c2:
        if st.button(":material/backspace:", use_container_width=True,
                     key=f"delete_filial_{filial}_in{season_selector}",
                     help=f"Удалить {filial}",
                     disabled=not user_role["deleting_filials"]
                     ):
            delete_filial(season_selector, filial)

    col1, col2, col3, col4, col5 = st.columns(5)

    cols = [col1, col2, col3, col4, col5]
    num_cols = 5

    last_filled_col = -1

    for i, group in enumerate(groups_list):
        col_idx = i % num_cols
        with cols[col_idx]:

            with st.container(border=True):
                if st.button(group, key=f"{season_selector}_{filial}_{group}"):
                    st.session_state.season = season_selector
                    st.session_state.filial = filial
                    st.session_state.group = group
                    st.switch_page("pages/group_card.py")

                st.write(f"Мест: {groups_list[group]["capacity"]}")
                st.write(f"Бронь: {groups_list[group]["children_count"]}")
                st.write(f"Оплачено: {groups_list[group]["paid_children_count"]}")
                st.write(f"Осталось: {groups_list[group]["remaining_capacity"]}")

                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button(":material/person_add:", key=f"add_child_to{season_selector}{filial}{group}",
                                 help=f"Добавить ребенка в {group}",
                                 disabled=not user_role["editing_groups"]):
                        add_child_to_group(season_selector, filial, group)
                with col2:
                    if st.button(":material/person_remove:", key=f"remove_child_from{season_selector}{filial}{group}",
                                 help=f"Удалить ребенка из {group}",
                                 disabled=not user_role["editing_groups"]):
                        delete_child_from_group(season_selector, filial, group)
                with col3:
                    if st.button(":material/directions_run:", key=f"move_child_from{season_selector}{filial}{group}",
                                 help=f"Переместить ребенка из {group}",
                                 disabled=not user_role["editing_groups"]):
                        move_child(season_selector, filial, group)
                with col1:
                    if st.button(":material/edit:", key=f"edit_{season_selector}{filial}{group}",
                                 help=f"Редактировать {group}",
                                 disabled=not user_role["editing_groups"]):
                        edit_group(season_selector, filial, group)
                with col2:
                    if st.button(":material/remove:", key=f"delete_{season_selector}{filial}{group}",
                                 help=f"Удалить {group}",
                                 disabled=not user_role["deleting_groups"]):
                        delete_group(season_selector, filial, group)

        last_filled_col = col_idx

    next_col = (last_filled_col + 1) % num_cols
    with cols[next_col]:
        if st.button(":material/group_add:", key=f"add_group_to{filial}",
                     help=f"Добавить группу в {filial}",
                     disabled=not user_role["adding_groups"],
                     use_container_width=True):
            add_group(season_selector, filial)

st.divider()


if st.button(":material/add_box:", key=f"add_filial{season_selector}",
             help=f"Добавить филиал в {season_selector}",
             disabled=not user_role["adding_seasons"]):
    add_filial(season_selector)
with st.expander("Сезоны"):
    if st.button("Добавить сезон", key="add_season",
                 disabled=not user_role["adding_seasons"]):
        add_season()
    if st.button("Редактировать сезон", key="edit_season",
                 disabled=not user_role["editing_seasons"]):
        edit_season(season_selector)
    if st.button("Удалить сезон", key="delete_season",
                 disabled=not user_role["deleting_seasons"]):
        delete_season(season_selector)
