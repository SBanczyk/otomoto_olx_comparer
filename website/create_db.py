import sqlite3
import os


def create_db():
    conn = sqlite3.connect(os.getenv('DB_NAME'))
    users = """create table if not exists users
        (
            user_id integer primary key autoincrement not null,
            email text not null,
            password text not null,
            registration_date text not null default (datetime('now','localtime'))
        );"""
    cars = """create table if not exists cars
        (
            car_id integer primary key autoincrement not null,
            brand text not null,
            model text not null,
            production_year integer not null,
            price integer not null,
            url text not null
        );"""
    comparisons = """create table if not exists comparisons
        (
            comparison_id integer primary key autoincrement not null,
            user_id integer not null,
            car1_id integer not null,
            car2_id integer not null,
            is_active integer not null,
            foreign key(user_id) references users(user_id),
            foreign key(car1_id) references cars(car_id),
            foreign key(car2_id) references cars(car_id)
        );"""
    conn.cursor().execute(users)
    conn.commit()
    conn.cursor().execute(cars)
    conn.commit()
    conn.cursor().execute(comparisons)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_db()
