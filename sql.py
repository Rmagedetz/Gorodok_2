import pandas as pd
from sqlalchemy import (Column, Integer, String, Date, Float, create_engine, ForeignKey, func, Boolean, case,
                        UniqueConstraint, DateTime, Text)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, aliased, joinedload
from sqlalchemy.exc import IntegrityError
from contextlib import contextmanager
from connections import sql_connection_string
from datetime import datetime

engine = create_engine(sql_connection_string)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_list(cls, field_name):
    with session_scope() as session:
        field = getattr(cls, field_name)
        results = session.query(field).all()
        result_list = [getattr(result, field_name) for result in results]
    return result_list


class Role(Base):
    __tablename__ = 'roles'

    role_id = Column(Integer, primary_key=True)
    role_name = Column(String(300), unique=True, nullable=False)

    creating_roles = Column(Boolean, default=False)
    editing_roles = Column(Boolean, default=False)
    deleting_roles = Column(Boolean, default=False)

    creating_users = Column(Boolean, default=False)
    editing_users = Column(Boolean, default=False)
    deleting_users = Column(Boolean, default=False)

    adding_seasons = Column(Boolean, default=False)
    editing_seasons = Column(Boolean, default=False)
    deleting_seasons = Column(Boolean, default=False)

    adding_filials = Column(Boolean, default=False)
    editing_filials = Column(Boolean, default=False)
    deleting_filials = Column(Boolean, default=False)

    adding_groups = Column(Boolean, default=False)
    editing_groups = Column(Boolean, default=False)
    deleting_groups = Column(Boolean, default=False)

    adding_leavers = Column(Boolean, default=False)
    editing_leavers = Column(Boolean, default=False)
    deleting_leavers = Column(Boolean, default=False)

    adding_payments = Column(Boolean, default=False)
    editing_payments = Column(Boolean, default=False)
    deleting_payments = Column(Boolean, default=False)

    adding_cancelations = Column(Boolean, default=False)
    editing_cancelations = Column(Boolean, default=False)
    deleting_cancelations = Column(Boolean, default=False)

    users = relationship("User", back_populates="user_role")

    @classmethod
    def add_role(cls, **parameters):
        with session_scope() as session:
            add = cls(**parameters)
            session.add(add)

    @classmethod
    def delete_role(cls, role_name):
        with session_scope() as session:
            contact = session.query(cls).filter_by(role_name=role_name).first()
            session.delete(contact)

    @classmethod
    def update_role(cls, role_name, new_data):
        with session_scope() as session:
            record = session.query(cls).filter_by(role_name=role_name).first()
            for key, value in new_data.items():
                setattr(record, key, value)

    @classmethod
    def get_roles_list(cls):
        role_list = get_list(cls, "role_name")
        role_list.remove("superadmin")
        return role_list

    @classmethod
    def get_roles(cls):
        with session_scope() as session:
            roles = session.query(cls).filter(cls.role_name != "superadmin").all()

            roles_list = [
                {key: value for key, value in role.__dict__.items() if key != '_sa_instance_state'}
                for role in roles
            ]

            roles_df = pd.DataFrame(roles_list)
            column_order = ["role_name",
                            "creating_roles", "editing_roles", "deleting_roles",
                            "creating_users", "editing_users", "deleting_users",
                            "adding_seasons", "editing_seasons", "deleting_seasons",
                            "adding_filials", "editing_filials", "deleting_filials",
                            "adding_groups", "editing_groups", "deleting_groups",
                            "adding_leavers", "editing_leavers", "deleting_leavers",
                            "adding_payments", "editing_payments", "deleting_payments",
                            "adding_cancelations", "editing_cancelations", "deleting_cancelations"]

            roles_df = roles_df[column_order]
            roles_df.index += 1
            return roles_df


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    user_name = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)

    role_id = Column(Integer, ForeignKey('roles.role_id'), nullable=False)
    user_role = relationship("Role", back_populates="users")

    @classmethod
    def add_user(cls, role_name, **parameters):
        with session_scope() as session:
            role = session.query(Role).filter_by(role_name=role_name).first()
            add = cls(role_id=role.role_id, **parameters)
            session.add(add)

    @classmethod
    def edit_user(cls, username, new_name, new_role, new_pass):
        with session_scope() as session:
            role = session.query(Role).filter_by(role_name=new_role).first()
            user = session.query(cls).filter_by(user_name=username).first()
            user.role_id = role.role_id
            user.user_name = new_name
            user.password = new_pass
            session.commit()

    @classmethod
    def delete_user(cls, user_name):
        with session_scope() as session:
            contact = session.query(cls).filter_by(user_name=user_name).first()
            session.delete(contact)

    @classmethod
    def get_user_list(cls):
        user_list = get_list(cls, "user_name")
        user_list.remove("superadmin")
        return user_list

    @classmethod
    def get_user_list_for_login(cls):
        user_list = get_list(cls, "user_name")
        return user_list

    @classmethod
    def check_user_password(cls, username):
        with session_scope() as session:
            result = session.query(cls.password).filter_by(user_name=username).first()
            return result[0] if result else None

    @classmethod
    def get_user_role_data(cls, user_name):
        with session_scope() as session:
            role = (
                session.query(Role)
                .join(cls, Role.role_id == cls.role_id)
                .filter(cls.user_name == user_name)
                .first()
            )

            role_dict = role.__dict__.copy()
            role_dict.pop('_sa_instance_state', None)
            return role_dict

    @classmethod
    def get_users_with_roles(cls):
        with session_scope() as session:
            users = session.query(cls.user_name, Role.role_name).join(Role).filter(
                User.user_name != "superadmin").all()
            df = pd.DataFrame(users)
            return df

    @classmethod
    def get_users_data(cls):
        with session_scope() as session:
            users = session.query(cls.user_name, cls.password, Role.role_name).join(Role).filter(
                User.user_name != "superadmin").all()
            df = pd.DataFrame(users)
            return df


class Season(Base):
    __tablename__ = 'seasons'

    id = Column(Integer, primary_key=True)
    name = Column(String(300), unique=True, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    filials = relationship("Filial", back_populates="season")

    @classmethod
    def get_season_list(cls):
        return get_list(cls, "name")

    @classmethod
    def add_season(cls, **parameters):
        with session_scope() as session:
            add = cls(**parameters)
            session.add(add)

    @classmethod
    def delete_season(cls, season_name):
        with session_scope() as session:
            contact = session.query(cls).filter_by(name=season_name).first()
            session.delete(contact)

    @classmethod
    def edit_season(cls, name, new_name, new_start, new_end):
        with session_scope() as session:
            season = session.query(cls).filter_by(name=name).first()
            season.name = new_name
            season.start_date = new_start
            session.end_date = new_end

    @classmethod
    def get_season_data(cls, season_name):
        with session_scope() as session:
            role = (
                session.query(cls)
                .filter(cls.name == season_name)
                .first()
            )

            role_dict = role.__dict__.copy()
            role_dict.pop('_sa_instance_state', None)
            return role_dict


class Filial(Base):
    __tablename__ = 'filials'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    season_id = Column(Integer, ForeignKey('seasons.id'), nullable=False)

    season = relationship("Season", back_populates="filials")
    groups = relationship("Group", back_populates="filial")

    __table_args__ = (UniqueConstraint('name', 'season_id', name='_filial_season_uc'),)

    @classmethod
    def show_filials_for_season(cls, season_name):
        with session_scope() as session:
            season = session.query(Season).filter_by(name=season_name).first()
            filials = session.query(cls.name).filter_by(season_id=season.id).all()
            df = pd.DataFrame(filials)
            df.index += 1
            return df

    @classmethod
    def add_filial(cls, season_name, **parameters):
        with session_scope() as session:
            season = session.query(Season).filter_by(name=season_name).first()
            add = cls(season_id=season.id, **parameters)
            session.add(add)

    @classmethod
    def edit_filial(cls, season_name, filial_name, new_filial_name):
        with session_scope() as session:
            season = session.query(Season).filter_by(name=season_name).first()
            filial = session.query(cls).filter_by(name=filial_name, season_id=season.id).first()
            filial.name = new_filial_name
            session.commit()

    @classmethod
    def delete_filial_from_season(cls, season_name, filial_name):
        with session_scope() as session:
            season = session.query(Season).filter_by(name=season_name).first()
            filial = session.query(cls).filter_by(name=filial_name, season_id=season.id).first()
            session.delete(filial)
            session.commit()


class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    capacity = Column(Integer, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    season_id = Column(Integer, ForeignKey('seasons.id'), nullable=False)
    filial_id = Column(Integer, ForeignKey('filials.id'), nullable=False)

    filial = relationship("Filial", back_populates="groups")
    children = relationship("GroupChild", back_populates="group")
    bills = relationship("Bills", back_populates="group")

    __table_args__ = (UniqueConstraint('name', 'filial_id', name='_group_filial_uc'),)

    @classmethod
    def get_groups_list_for_filial_in_season(cls, season_name, filial_name):
        with session_scope() as session:
            season = session.query(Season).filter_by(name=season_name).first()
            filial = session.query(Filial).filter_by(name=filial_name, season_id=season.id).first()
            groups = session.query(cls).filter_by(filial_id=filial.id).all()
            return [group.name for group in groups]

    @classmethod
    def add_group_to_filial_in_season(cls, season_name, filial_name, **parameters):
        with session_scope() as session:
            season = session.query(Season).filter_by(name=season_name).first()
            filial = session.query(Filial).filter_by(name=filial_name, season_id=season.id).first()
            add = cls(season_id=season.id,
                      filial_id=filial.id,
                      **parameters)
            session.add(add)

    @classmethod
    def delete_group_from_filial_in_season(cls, season_name, filial_name, group_name):
        with session_scope() as session:
            season = session.query(Season).filter_by(name=season_name).first()
            filial = session.query(Filial).filter_by(name=filial_name, season_id=season.id).first()
            group = session.query(cls).filter_by(name=group_name, filial_id=filial.id).first()
            session.delete(group)
            session.commit()

    @classmethod
    def edit_group_in_filial_in_season(cls, season_name, filial_name, group_name, new_group_data):
        with session_scope() as session:
            season = session.query(Season).filter_by(name=season_name).first()
            filial = session.query(Filial).filter_by(name=filial_name, season_id=season.id).first()
            group = session.query(cls).filter_by(name=group_name, filial_id=filial.id, season_id=season.id).first()

            for key, value in new_group_data.items():
                setattr(group, key, value)

    @classmethod
    def get_groups(cls):
        with session_scope() as session:
            roles = session.query(cls).all()

            groups_list = [
                {key: value for key, value in role.__dict__.items() if key != '_sa_instance_state'}
                for role in roles
            ]

            roles_df = pd.DataFrame(groups_list)
            column_order = ["name", "capacity", "start_date", "end_date"]

            roles_df = roles_df[column_order]
            roles_df.index += 1
            return roles_df

    @classmethod
    def add_child_to_group(cls, season_name, filial_name, group_name, child_name):
        with session_scope() as session:
            season = session.query(Season).filter_by(name=season_name).first()
            filial = session.query(Filial).filter_by(name=filial_name, season_id=season.id).first()
            group = session.query(cls).filter_by(name=group_name, filial_id=filial.id).first()
            child = session.query(Child).filter(Child.name == child_name).first()

            # Проверяем, есть ли ребенок уже в группе
            existing_entry = session.query(GroupChild).filter_by(group_id=group.id, child_id=child.id).first()
            if existing_entry:
                return False, f"Ребенок '{child_name}' уже добавлен в группу '{group_name}'."

            # Создаем запись о добавлении ребенка в группу
            new_group_child = GroupChild(group_id=group.id, child_id=child.id)
            session.add(new_group_child)

            try:
                session.commit()
            except IntegrityError:
                session.rollback()

    @classmethod
    def get_children_in_group(cls, season_name, filial_name, group_name):
        with session_scope() as session:
            season = session.query(Season).filter_by(name=season_name).first()
            filial = session.query(Filial).filter_by(name=filial_name, season_id=season.id).first()
            group = session.query(cls).filter_by(name=group_name, filial_id=filial.id).first()

            children = session.query(GroupChild).filter(GroupChild.group_id == group.id).all()

            if not children:
                return pd.DataFrame()

            children_data = []
            for group_child in children:
                child = session.query(Child).filter(Child.id == group_child.child_id).first()
                if child:
                    children_data.append(
                        {column.name: getattr(child, column.name) for column in Child.__table__.columns})

            df = pd.DataFrame(children_data)
            df = df.drop("id", axis=1)
            df.index += 1
            return df

    @classmethod
    def get_children_list_in_group(cls, season_name, filial_name, group_name):
        with session_scope() as session:
            children = (
                session.query(Child.name)
                .join(GroupChild, GroupChild.child_id == Child.id)
                .join(Group, Group.id == GroupChild.group_id)
                .join(Filial, Filial.id == Group.filial_id)
                .join(Season, Season.id == Filial.season_id)
                .filter(Season.name == season_name, Filial.name == filial_name, Group.name == group_name)
                .all()
            )

            return [child.name for child in children]

    @classmethod
    def remove_child_from_group(cls, season_name, filial_name, group_name, child_name):
        with session_scope() as session:
            season = session.query(Season).filter_by(name=season_name).first()
            filial = session.query(Filial).filter_by(name=filial_name, season_id=season.id).first()
            group = session.query(cls).filter_by(name=group_name, filial_id=filial.id).first()
            child = session.query(Child).filter_by(name=child_name).first()
            group_child = session.query(GroupChild).filter_by(group_id=group.id, child_id=child.id).first()
            session.delete(group_child)
            session.commit()

    @classmethod
    def move_child_to_group(cls, out_season_name, out_filial_name, out_group_name, child_name, in_season_name,
                            in_filial_name, in_group_name):
        with session_scope() as session:
            out_season = session.query(Season).filter(Season.name == out_season_name).first()
            out_filial = session.query(Filial).filter(Filial.name == out_filial_name,
                                                      Filial.season_id == out_season.id).first()
            out_group = session.query(Group).filter(Group.name == out_group_name,
                                                    Group.filial_id == out_filial.id).first()
            in_season = session.query(Season).filter(Season.name == in_season_name).first()
            in_filial = session.query(Filial).filter(Filial.name == in_filial_name,
                                                     Filial.season_id == in_season.id).first()
            in_group = session.query(Group).filter(Group.name == in_group_name, Group.filial_id == in_filial.id).first()
            child = session.query(Child).filter(Child.name == child_name).first()
            group_child_out = session.query(GroupChild).filter(GroupChild.group_id == out_group.id,
                                                               GroupChild.child_id == child.id).first()
            session.delete(group_child_out)
            group_child_in = GroupChild(group_id=in_group.id, child_id=child.id)
            session.add(group_child_in)
            session.commit()


class Child(Base):
    __tablename__ = 'children'

    # базовые данные
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    age = Column(Integer, nullable=False)
    parent_main_name = Column(String(50), nullable=False)
    parent_main_phone = Column(String(50), nullable=False)

    # анкетные данные
    email = Column(String(100), nullable=True, default="")
    child_birthday = Column(Date, nullable=True, default=None)
    parent_add = Column(String(50), nullable=True, default="")
    phone_add = Column(String(20), nullable=True, default="")
    leave = Column(String(10), nullable=True, default="")
    additional_contact = Column(Text, nullable=True, default="")
    addr = Column(String(200), nullable=True, default="")
    disease = Column(Text, nullable=True, default="")
    allergy = Column(Text, nullable=True, default="")
    other = Column(Text, nullable=True, default="")
    physic = Column(Text, nullable=True, default="")
    swimm = Column(String(10), nullable=True, default="")
    jacket_swimm = Column(String(10), nullable=True, default="")
    hobby = Column(Text, nullable=True, default="")
    school = Column(String(100), nullable=True, default="")
    additional_info = Column(Text, nullable=True, default="")
    departures = Column(String(10), nullable=True, default="")
    referer = Column(String(100), nullable=True, default="")
    ok = Column(String(10), nullable=True, default="")
    mailing = Column(Text, nullable=True, default="")
    personal_accept = Column(String(10), nullable=True, default="")
    oms = Column(String(20), nullable=True, default="")

    # данные для договора
    parent_passport = Column(String(100), nullable=True, default="")
    parent_adress = Column(String(100), nullable=True, default="")

    groups = relationship("GroupChild", back_populates="child")
    payments = relationship("Payments", back_populates="child")
    bills = relationship("Bills", back_populates="child")

    __table_args__ = (UniqueConstraint('name', name='_child_name_uc'),)

    @classmethod
    def add_child(cls, **parameters):
        with session_scope() as session:
            add = cls(**parameters)
            session.add(add)

    @classmethod
    def delete_child(cls, child_name):
        with session_scope() as session:
            contact = session.query(cls).filter_by(name=child_name).first()
            session.delete(contact)

    @classmethod
    def get_child_list(cls):
        return get_list(cls, "name")

    @classmethod
    def get_children(cls):
        with session_scope() as session:
            roles = session.query(cls).all()

            roles_list = [
                {key: value for key, value in role.__dict__.items() if key != '_sa_instance_state'}
                for role in roles
            ]

            roles_df = pd.DataFrame(roles_list)

            roles_df.index += 1
            return roles_df

    @classmethod
    def edit_child_data(cls, child_name, new_data):
        with session_scope() as session:
            record = session.query(cls).filter_by(name=child_name).first()
            for key, value in new_data.items():
                setattr(record, key, value)

    @classmethod
    def add_children_from_dataframe(cls, df):
        with session_scope() as session:
            new_children = []

            for _, row in df.iterrows():
                row_data = row.to_dict()
                if 'child_birthday' in row_data:
                    row_data['child_birthday'] = datetime.strptime(row_data['child_birthday'], '%d.%m.%Y').strftime(
                        '%Y-%m-%d')

                if not session.query(cls).filter_by(name=row_data["name"]).first():
                    new_children.append(cls(**row_data))

            session.add_all(new_children)


class GroupChild(Base):
    __tablename__ = 'group_children'

    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    child_id = Column(Integer, ForeignKey('children.id'), nullable=False)

    group = relationship("Group", back_populates="children", lazy='joined')
    child = relationship("Child", back_populates="groups", lazy='joined')


class Payments(Base):
    __tablename__ = 'payments'
    __mapper_args__ = {'eager_defaults': True}

    id = Column(Integer, primary_key=True)
    payment_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    child_id = Column(Integer, ForeignKey('children.id'), nullable=False)
    amount = Column(Float, nullable=False)
    recorded_by = Column(String(50), nullable=False)
    comment = Column(String(200), nullable=True)

    child = relationship("Child", back_populates="payments")

    @classmethod
    def get_payments_by_child_name(cls, child_name):
        with session_scope() as session:
            # Ищем ребенка по имени
            child = session.query(Child).filter_by(name=child_name).first()

            if not child:
                return pd.DataFrame()  # Если ребенка не нашли, возвращаем пустой DataFrame

            # Получаем все платежи для найденного ребенка
            payments = session.query(Payments).filter_by(child_id=child.id).all()

            if not payments:
                return pd.DataFrame()  # Если нет платежей, возвращаем пустой DataFrame

            payments_data = []

            # Перебираем все платежи
            for payment in payments:
                payments_data.append({
                    'child_name': child.name,  # Добавляем имя ребенка
                    'payment_date': payment.payment_date,
                    'amount': payment.amount,
                    'recorded_by': payment.recorded_by,
                    'comment': payment.comment
                })

            # Создаем DataFrame из собранных данных
            df = pd.DataFrame(payments_data)
            df.index += 1  # Чтобы индексы начинались с 1
            return df


def add_payment(payment_date, child_name, amount, user_name, comment):
    with session_scope() as session:
        # Находим ребенка по имени
        child = session.query(Child).filter(Child.name == child_name).first()

        if not child:
            return False  # Возвращаем False, если ребенок не найден

        # Создаем новый объект платежа
        new_payment = Payments(
            payment_date=payment_date,
            child_id=child.id,  # Используем ID найденного ребенка
            amount=amount,
            recorded_by=user_name,  # Имя пользователя, записавшего платеж
            comment=comment
        )

        try:
            session.add(new_payment)  # Добавляем новый платеж в сессию
            session.commit()  # Подтверждаем изменения
            return True  # Возвращаем True при успешном добавлении
        except IntegrityError:
            session.rollback()  # Откатываем изменения при ошибке
            return False  # Возвращаем False при ошибке


def get_payment_details(payment_id):
    with session_scope() as session:
        # Получаем информацию о платеже по ID
        payment = session.query(Payments).filter(Payments.id == payment_id).first()

        if not payment:
            return pd.DataFrame()  # Возвращаем пустой DataFrame, если платеж не найден

        # Получаем информацию о ребенке, связанном с платежом
        child = session.query(Child).filter(Child.id == payment.child_id).first()

        # Создаем словарь с данными о платеже
        payment_data = {
            "payment_id": payment.id,
            "payment_date": payment.payment_date,
            "child_name": child.name if child else "Неизвестный ребенок",
            "amount": payment.amount,
            "user_name": payment.recorded_by,
            "comment": payment.comment
        }

        # Преобразуем словарь в DataFrame
        payment_df = pd.DataFrame([payment_data])

        return payment_df


def edit_payment_data(payment_id, payment_date=None, child_name=None, amount=None, comment=None):
    with session_scope() as session:
        payment_id = int(payment_id)
        payment = session.query(Payments).filter(Payments.id == payment_id).first()

        if not payment:
            return False

        if payment_date:
            payment.payment_date = payment_date
        if amount is not None:
            payment.amount = amount
        if comment:
            payment.comment = comment

        if child_name:
            child = session.query(Child).filter(Child.name == child_name).first()
            if child:
                payment.child_id = child.id
            else:
                return False

        session.commit()
        return True


def delete_payment(payment_id):
    with session_scope() as session:
        payment_id = int(payment_id)

        payment = session.query(Payments).filter(Payments.id == payment_id).first()

        if not payment:
            return False

        session.delete(payment)
        session.commit()

        return True


def get_payments_dataframe():
    with session_scope() as session:
        # Выполняем запрос, включая связь с Child и User
        payments = (
            session.query(Payments)
            .options(joinedload(Payments.child))  # Загрузка связанных данных о ребенке
            .all()
        )

        # Создаем списки для формирования датафрейма
        payment_data = []
        for payment in payments:
            child = payment.child  # Получаем объект ребенка через связь
            payment_data.append({
                "id": payment.id,
                "payment_date": payment.payment_date,
                "user": payment.recorded_by,  # Имя пользователя, записавшего платеж
                "child_name": child.name,
                "payment_amount": payment.amount,
                "comment": payment.comment
            })

        # Создаем датафрейм
        df = pd.DataFrame(payment_data)
        df.index += 1

        return df


class Bills(Base):
    __tablename__ = 'bills'
    __mapper_args__ = {'eager_defaults': True}

    id = Column(Integer, primary_key=True)
    payment_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    child_id = Column(Integer, ForeignKey('children.id'), nullable=False)
    amount = Column(Float, nullable=False)
    recorded_by = Column(String(50), nullable=False)
    comment = Column(String(200), nullable=True)

    child = relationship("Child", back_populates="bills")
    group = relationship("Group", back_populates="bills")

    @classmethod
    def get_bills_by_child_name(cls, child_name):
        with session_scope() as session:
            # Ищем ребенка по имени
            child = session.query(Child).filter_by(name=child_name).first()

            if not child:
                return pd.DataFrame()  # Если ребенка не нашли, возвращаем пустой DataFrame

            # Получаем все счета для найденного ребенка
            bills = session.query(Bills).filter_by(child_id=child.id).all()

            if not bills:
                return pd.DataFrame()  # Если нет счетов, возвращаем пустой DataFrame

            bills_data = []

            # Перебираем все счета
            for bill in bills:
                # Ищем соответствующую группу
                group = session.query(Group).filter_by(id=bill.group_id).first()
                # Ищем соответствующий филиал
                filial = session.query(Filial).filter_by(id=group.filial_id).first()
                # Ищем сезон
                season = session.query(Season).filter_by(id=filial.season_id).first()

                bills_data.append({
                    'child_name': child.name,
                    'payment_date': bill.payment_date,
                    'amount': bill.amount,
                    'recorded_by': bill.recorded_by,
                    'comment': bill.comment,
                    'season_name': season.name if season else None,
                    'filial_name': filial.name if filial else None,
                    'group_name': group.name if group else None
                })

            # Преобразуем собранные данные в DataFrame
            df = pd.DataFrame(bills_data)

            # Возвращаем DataFrame
            return df


def get_bill_details(bill_id):
    with session_scope() as session:
        # Получаем информацию о платеже по ID
        bill = session.query(Bills).filter(Bills.id == bill_id).first()

        if not bill:
            return pd.DataFrame()  # Возвращаем пустой DataFrame, если платеж не найден

        # Получаем информацию о ребенке, связанном с платежом
        child = session.query(Child).filter(Child.id == bill.child_id).first()
        group = session.query(Group).filter(Group.id == bill.group_id).first()

        # Создаем словарь с данными о платеже
        payment_data = {
            "payment_id": bill.id,
            "payment_date": bill.payment_date,
            "child_name": child.name if child else "Неизвестный ребенок",
            "group_name": group.name if group else "Неизвестная группа",
            "amount": bill.amount,
            "user_name": bill.recorded_by,
            "comment": bill.comment
        }

        # Преобразуем словарь в DataFrame
        payment_df = pd.DataFrame([payment_data])

        return payment_df


def add_bill(payment_date, child_name, group_name, amount, user_name, comment):
    with session_scope() as session:
        # Находим ребенка по имени
        child = session.query(Child).filter(Child.name == child_name).first()
        group = session.query(Group).filter(Group.name == group_name).first()

        if not child:
            return False  # Возвращаем False, если ребенок не найден

        # Создаем новый объект платежа
        new_payment = Bills(
            payment_date=payment_date,
            child_id=child.id,  # Используем ID найденного ребенка
            group_id=group.id,
            amount=amount,
            recorded_by=user_name,  # Имя пользователя, записавшего платеж
            comment=comment
        )

        try:
            session.add(new_payment)  # Добавляем новый платеж в сессию
            session.commit()  # Подтверждаем изменения
            return True  # Возвращаем True при успешном добавлении
        except IntegrityError:
            session.rollback()  # Откатываем изменения при ошибке
            return False  # Возвращаем False при ошибке


def get_bills_dataframe():
    with session_scope() as session:
        # Выполняем запрос, включая связь с Child и Group
        bills = (
            session.query(Bills)
            .options(
                joinedload(Bills.child),  # Загрузка связанных данных о ребенке
                joinedload(Bills.group)  # Загрузка связанных данных о группе
            )
            .all()
        )

        # Создаем список данных для формирования датафрейма
        bill_data = []
        for bill in bills:
            child = bill.child  # Получаем объект ребенка через связь
            group = bill.group  # Получаем объект группы через связь
            bill_data.append({
                "id": bill.id,
                "payment_date": bill.payment_date,
                "user": bill.recorded_by,  # Имя пользователя, записавшего счет
                "child_name": child.name,
                "group_name": group.name if group else None,  # Имя группы (если оно есть)
                "amount": bill.amount,  # Сумма счета
                "comment": bill.comment
            })

        # Создаем датафрейм
        df = pd.DataFrame(bill_data)
        df.index += 1  # Индексация с 1, а не с 0

        return df


class Visits(Base):
    __tablename__ = 'visits'

    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    child_id = Column(Integer, ForeignKey('children.id'), nullable=False)
    day = Column(Integer)
    visit = Column(String(10))

    __table_args__ = (UniqueConstraint('group_id', 'child_id', 'day', name='_unique_visit'),)

    @classmethod
    def get_visits_dataframe_for_group(cls, group_name):
        with session_scope() as session:
            # Выполняем запрос с объединением таблиц Groups и Children
            results = session.query(
                Child.name.label("Имя ребенка"),
                cls.day.label("День"),
                cls.visit.label("Посещение")
            ).join(
                Child, cls.child_id == Child.id
            ).join(
                Group, cls.group_id == Group.id
            ).filter(
                Group.name == group_name  # Фильтруем по названию группы
            ).all()

            # Преобразуем результаты в DataFrame
            df = pd.DataFrame(results, columns=["Имя ребенка", "День", "Посещение"])

            if df.empty:
                return pd.DataFrame(columns=["Имя ребенка"] + list(range(1, 11)))

            # Пивотируем данные, чтобы получить дни как столбцы
            pivot_df = df.pivot(index="Имя ребенка", columns="День", values="Посещение").reset_index()

            # Упорядочиваем столбцы
            pivot_df.columns.name = None  # Убираем имя уровня колонок
            all_days = list(range(1, 11))  # Дни от 1 до 10
            for day in all_days:
                if day not in pivot_df.columns:
                    pivot_df[day] = pd.NA  # Добавляем отсутствующие дни как NaN

            pivot_df = pivot_df[["Имя ребенка"] + all_days]
            pivot_df.index += 1
            return pivot_df

    @classmethod
    def set_visit(cls, child_name, group_name, day, visit):
        with session_scope() as session:
            child = session.query(Child).filter(Child.name == child_name).first()
            group = session.query(Group).filter(Group.name == group_name).first()
            try:
                add = cls(group_id=group.id,
                          child_id=child.id,
                          day=day,
                          visit=visit)
                session.add(add)
            except:
                pass

    @classmethod
    def insert_or_update_visits(cls, df_melted):
        with session_scope() as session:
            # Перебираем строки DataFrame и вставляем или обновляем записи в таблице visits
            for _, row in df_melted.iterrows():
                group_id = row['group_id']
                child_id = row['child_id']
                day = row['day']
                visit = row['visit']

                # Пытаемся найти существующую запись
                existing_visit = session.query(cls).filter_by(
                    group_id=group_id, child_id=child_id, day=day).first()

                if existing_visit:
                    # Если запись существует, проверяем отличается ли visit
                    if existing_visit.visit != visit:
                        # Если отличается, обновляем запись
                        existing_visit.visit = visit
                else:
                    # Если записи нет, создаем новую
                    new_visit = cls(
                        group_id=group_id,
                        child_id=child_id,
                        day=day,
                        visit=visit
                    )
                    session.add(new_visit)

            # После завершения цикла коммитим изменения
            session.commit()

    @classmethod
    def get_visits_by_child_name(cls, child_name):
        with session_scope() as session:
            # Ищем ребенка по имени
            child = session.query(Child).filter_by(name=child_name).first()

            if not child:
                return pd.DataFrame()  # Если ребенка не нашли, возвращаем пустой DataFrame

            # Получаем все посещения для найденного ребенка
            visits = session.query(cls).filter_by(child_id=child.id).all()

            if not visits:
                return pd.DataFrame()  # Если нет посещений, возвращаем пустой DataFrame

            visits_data = []

            # Перебираем все посещения
            for visit in visits:
                # Получаем информацию о группе
                group = session.query(Group).filter_by(id=visit.group_id).first()
                # Получаем информацию о филиале
                filial = session.query(Filial).filter_by(id=group.filial_id).first()
                # Получаем информацию о сезоне
                season = session.query(Season).filter_by(id=filial.season_id).first()

                visits_data.append({
                    'season_name': season.name if season else None,
                    'filial_name': filial.name if filial else None,
                    'group_name': group.name if group else None,
                    'day': visit.day,
                    'visit': visit.visit
                })

            # Создаем DataFrame из собранных данных
            df = pd.DataFrame(visits_data)
            df.index += 1  # Чтобы индексы начинались с 1
            return df


def get_groups_with_children_count_and_paid_by_season(season_name):
    with session_scope() as session:
        season = session.query(Season).filter(Season.name == season_name).first()

        if not season:
            return {}

        # Получаем все филиалы в данном сезоне
        filials = session.query(Filial).filter(Filial.season_id == season.id).all()

        # Создаем словарь для хранения результатов
        result = {}

        for filial in filials:
            filial_data = {}

            # Получаем все группы для каждого филиала
            groups = session.query(Group).filter(Group.filial_id == filial.id).all()

            for group in groups:
                # Получаем количество детей в группе
                children_count = session.query(GroupChild).filter(GroupChild.group_id == group.id).count()

                # Получаем количество уникальных детей с платежами
                paid_children_count = session.query(Payments.child_id).join(GroupChild,
                                                                            GroupChild.child_id == Payments.child_id) \
                    .filter(GroupChild.group_id == group.id) \
                    .distinct().count()

                # Рассчитываем оставшуюся вместимость группы
                remaining_capacity = group.capacity - children_count

                # Записываем данные по группе
                group_data = {
                    "group_name": group.name,
                    "children_count": children_count,
                    "paid_children_count": paid_children_count,
                    "capacity": group.capacity,
                    "remaining_capacity": remaining_capacity
                }

                filial_data[group.name] = group_data

            # Записываем данные по филиалу в результат
            result[filial.name] = filial_data

        # Возвращаем результат без ключа сезона
        return result


def get_group_id_by_name_and_season_and_filial(group_name, season_name, filial_name):
    with session_scope() as session:
        # Получаем сезон по имени
        season = session.query(Season).filter_by(name=season_name).first()
        if not season:
            raise ValueError(f"Сезон с именем {season_name} не найден.")

        # Получаем филиал по имени и сезону
        filial = session.query(Filial).filter_by(name=filial_name, season_id=season.id).first()
        if not filial:
            raise ValueError(f"Филиал с именем {filial_name} в сезоне {season_name} не найден.")

        # Получаем группу по имени и ID филиала
        group = session.query(Group).filter_by(name=group_name, filial_id=filial.id).first()
        if not group:
            raise ValueError(f"Группа с именем {group_name} в филиале {filial_name} не найдена.")

        # Возвращаем ID группы
        return group.id


def get_child_id_by_name(child_name):
    with session_scope() as session:
        # Ищем ребенка по имени
        child = session.query(Child).filter_by(name=child_name).first()

        # Если ребенок не найден, выбрасываем ошибку
        if not child:
            raise ValueError(f"Ребенок с именем {child_name} не найден.")

        # Возвращаем ID ребенка
        return child.id


Base.metadata.create_all(bind=engine)


@contextmanager
def session_scope():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except IntegrityError:
        db.rollback()
        raise
    finally:
        db.close()
