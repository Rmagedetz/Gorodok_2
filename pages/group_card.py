import streamlit as st
import sql
import pandas as pd

user = st.session_state.user
user_role = st.session_state.user_role_data

if all(["season" in st.session_state,
        "filial" in st.session_state,
        "group" in st.session_state]):

    season = st.session_state.season
    filial = st.session_state.filial
    group = st.session_state.group

    st.write(f"Карточка группы {group}. Филиал {filial}. Сезон {season}")

    data = sql.Group.get_children_in_group(season, filial,group)
    if not data.empty:
        child_list, visits, data_list, lockers, pool, adress = st.tabs(
            ["Список", "Посещаемость", "Лист ознакомления", "Список на шкафчики", "Бассейн", "Адреса"])

        with child_list:
            df = data[["name", "child_birthday", "parent_main_name", "parent_main_phone",
                       "parent_add", "phone_add", "leave", "addr", "oms", "disease", "allergy",
                       "other", "physic", "swimm", "jacket_swimm", "hobby"]]
            child_list = st.data_editor(df,
                                        column_config={"name": "ФИО ребенка",
                                                       "child_birthday": "Дата рождения",
                                                       "parent_main_name": "ФИО родителя",
                                                       "parent_main_phone": "Телефон",
                                                       "parent_add": "ФИО другого родственника",
                                                       "phone_add": "Телефон",
                                                       "leave": "Уходит сам",
                                                       "addr": "Адрес проживания",
                                                       "oms": "Номер медицинского полиса",
                                                       "disease": "Заболевания",
                                                       "allergy": "Аллергия",
                                                       "other": "Травмы",
                                                       "physic": "Ограничения",
                                                       "swimm": "Бассейн",
                                                       "jacket_swimm": "Нарукавники",
                                                       "hobby": "Увлечения"
                                                       },
                                        disabled=True)
            with visits:
                df = data[["name", "parent_main_name", "parent_main_phone", "leave", "child_birthday"]]
                visits = sql.Visits.get_visits_dataframe_for_group(group)
                visits.rename(columns={"Имя ребенка": "name"}, inplace=True)

                merged_df = pd.merge(df, visits, on="name", how="left")
                day_columns = list(range(1, 11))

                merged_df = merged_df[
                    ["name", "parent_main_name", "parent_main_phone", "leave", "child_birthday"] + day_columns]

                merged_df.index += 1

                colunms_config = {"child_birthday": st.column_config.DateColumn("ДР",
                                                                                help="День рождения",
                                                                                width="small",
                                                                                format="DD-MM-YYYY",
                                                                                disabled=True),
                                  "name": st.column_config.Column("ФИО",
                                                                  help="ФИО",
                                                                  width="medium",
                                                                  disabled=True),
                                  "parent_main_name": st.column_config.Column("Родитель",
                                                                              help="ФИО родителя",
                                                                              width="small",
                                                                              disabled=True),
                                  "parent_main_phone": st.column_config.Column("Тел",
                                                                               help="Телефон родителя",
                                                                               width="small",
                                                                               disabled=True),
                                  "leave": st.column_config.Column("Уходит",
                                                                   help="Уходит сам",
                                                                   width="small",
                                                                   disabled=True),
                                  "1": st.column_config.SelectboxColumn("1",
                                                                        options=[1, 2, 3])}

                for day in day_columns:
                    colunms_config[f"{day}"] = st.column_config.SelectboxColumn(f"{day}",
                                                                                options=[1, "1Д", "X", "Н", "П",
                                                                                         "Б", "В"])

                editor = st.data_editor(merged_df,
                                        column_config=colunms_config)

                if st.button("Проставить посещаемость"):
                    day_columns = list(map(str, range(1, 11)))

                    df_melted = editor.melt(
                        id_vars=['name'],
                        value_vars=day_columns,
                        var_name='day', value_name='visit')

                    df_melted.dropna(subset=['visit'], inplace=True)
                    gr_id = sql.get_group_id_by_name_and_season_and_filial(group, season, filial)
                    df_melted["group_id"] = gr_id
                    df_melted["child_id"] = df_melted["name"].apply(sql.get_child_id_by_name)
                    df_melted.drop(columns=["name"], inplace=True)
                    sql.Visits.insert_or_update_visits(df_melted)

            with data_list:
                df = data[["name", "child_birthday", "disease", "allergy",
                           "other", "physic", "leave", "jacket_swimm", "additional_info",
                           "additional_contact"]]
                data_list = st.data_editor(df,
                                           column_config={"name": "ФИО ребенка",
                                                          "child_birthday": "Дата рождения",
                                                          "leave": "Уходит сам",
                                                          "disease": "Заболевания",
                                                          "allergy": "Аллергия",
                                                          "other": "Травмы",
                                                          "physic": "Ограничения",
                                                          "swimm": "Бассейн",
                                                          "jacket_swimm": "Нарукавники",
                                                          "additional_info": "Доп.данные",
                                                          "additional_contact": "Кто кроме родителя может забирать"
                                                          },
                                           disabled=True)
                with lockers:
                    df = data["name"]
                    for _, name in df.items():
                        col1, col2 = st.columns(2)
                        with col1:
                            with st.container(border=True):
                                st.subheader(name)
                with pool:
                    df = data[["name", "parent_main_phone", "physic", "swimm", "jacket_swimm"]]
                    pool_list = st.data_editor(df,
                                               column_config={"name": "ФИО ребенка",
                                                              "parent_main_phone": "Телефон",
                                                              "physic": "Ограничения",
                                                              "swimm": "Бассейн",
                                                              "jacket_swimm": "Нарукавники"},
                                               disabled=True)
                with adress:
                    df = data[["name", "addr", "parent_main_phone", "parent_main_name"]]
                    adr_list = st.data_editor(df,
                                              column_config={"name": "ФИО ребенка",
                                                             "addr": "Адрес проживания",
                                                             "parent_main_phone": "Телефон",
                                                             "parent_main_name": "ФИО Родителя"},
                                              disabled=True)
if st.button("Перейти в записи"):
    st.switch_page("pages/records.py")