# Делаем импорты
import datetime
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()
# подключение базы
def connect_db(): 
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()
# описание таблиц
class Athelete(Base):
    __tablename__ = 'athelete'
    id = sa.Column(sa.Integer, primary_key=True)
    age = sa.Column(sa.Integer)
    birthdate = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    height = sa.Column(sa.Float)
    weight = sa.Column(sa.Integer)
    name = sa.Column(sa.Text)
    gold_medals = sa.Column(sa.Integer)
    silver_medals = sa.Column(sa.Integer)
    bronze_medals = sa.Column(sa.Integer)
    total_medals = sa.Column(sa.Integer)
    sport = sa.Column(sa.Text)
    country = sa.Column(sa.Text)
class User(Base) :
    __tablename__ = 'user'
    id = sa.Column(sa.Integer, primary_key=True)
    first_name = sa.Column(sa.Text)
    last_name = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    email = sa.Column(sa.Text)
    birthdate = sa.Column(sa.Text)
    height = sa.Column(sa.REAL)
# Запрос пользователя:
def request_data():
    user_id = input("Введите идентификатор пользователя: ")
    return int(user_id)
# Конвертация строки в дату
def conv_str_to_date(date_str):
    parts = date_str.split("-")
    date_parts = map(int, parts)
    date = datetime.date(*date_parts)
    return date
# Функция поиска по  дате рождения
def find_bd(user, session):
    athletes_list = session.query(Athelete).all()
    athlete_id_bd = {}
    for athlete in athletes_list:
        bd = conv_str_to_date(athlete.birthdate)
        athlete_id_bd[athlete.id] = bd
    user_bd = conv_str_to_date(user.birthdate)
    min_dist= None
    athlete_id= None
    athlete_bd= None
    for id_, bd in athlete_id_bd.items():
        dist = abs(user_bd - bd)
        if not min_dist or dist < min_dist:
            min_dist = dist
            athlete_id = id_
            athlete_bd = bd
    return athlete_id, athlete_bd
# Функция поиска по росту
def find_height(user, session):
    athletes_list = session.query(Athelete).all()
    atlhete_id_height = {athlete.id: athlete.height for athlete in athletes_list}
    user_height = user.height
    min_dist= None
    athlete_id= None
    athlete_height= None
    for id_, height in atlhete_id_height.items():
        if height is None:
            continue
        dist = abs(user_height - height)
        if not min_dist or dist < min_dist:
            min_dist = dist
            athlete_id = id_
            athlete_height = height
    return athlete_id, athlete_height

# основная функция    
def main ():
    session = connect_db()
    user_id = request_data()
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        print("Нет такого пользователя")
    else:
        bd_athlete, bd = find_bd(user, session)
        height_athlete, height = find_height(user, session)
        print(
            "Ближайший по дате рождения атлет: {}, его дата рождения: {}".format(bd_athlete, bd)
        )
        print(
            "Ближайший по росту атлет: {}, его рост: {}".format(height_athlete, height)
        )
    
if __name__ == "__main__":
    main()
    