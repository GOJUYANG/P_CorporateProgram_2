import psycopg2 as pg
import pandas as pd

# pandas가 psycopg2를 직접 사용하여 db에 연결하는 방식으로 호출될 때 경고문구 발생.
# 보다 안정적인 데이터베이스 작업을 실행할 수 있도록 SQLAlchemy를 사용하기를 권장함.
from sqlalchemy import create_engine

class DataClass:
    def __init__(self):

        self.pgdb = pg.connect(
            host='10.10.20.104',
            dbname='data',
            user='postgres',
            password='1234',
            port=5432
            )

        self.guests_pgdb = pg.connect(
            host='10.10.20.104',
            dbname='data',
            user='guests',
            password='1111',
            port=5432
        )

    def end_conn(self):
        if self.type == 'guests':
            self.guests_pgdb.close()
        elif self.type == 'master':
            self.master_pgdb.close()

    def setting_engine(self):
        engine = create_engine(f'postgresql://postgres:1234@10.10.20.104:5432/data')
        return engine

    def select_user_info(self, column: str, user_email="", user_nm="", plus=""):
        cursor = self.pgdb.cursor()
        sql = f"select {column} from USERS"
        if user_nm:
            sql += f" where user_nm = '{user_nm}'"
        elif user_email:
            sql += f" where user_email = '{user_email}'"

        if plus:
            if user_nm:
                sql += " and"
            elif user_email:
                sql += " and"
            else:
                sql += " where"

            sql += plus
        cursor.execute(sql)
        select_list = cursor.fetchall()
        return select_list

    def update_user_info(self, img, name, state):
        cursor = self.pgdb.cursor()
        cursor.execute(f"update USERS set user_img='{img}', user_nm = '{name}', user_state = '{state}'"
                       f" where user_nm = '{name}'")
        self.pgdb.commit()

    def update_user_pw(self, pw_, name_):
        cursor = self.pgdb.cursor()
        cursor.execute(f"update USERS set user_pw='{pw_} where user_nm = '{name_}")
        self.pgdb.commit()

    def insert_user_info(self):
        cursor = self.pgdb.cursor()
        # cursor.execute("SELECT user_email, COUNT(*) FROM USERS GROUP BY user_email HAVING COUNT(*) > 1")
        # # 중복된 이메일 주소들 가져오기
        # duplicate_emails = cursor.fetchall()
        # print(duplicate_emails)
        # df = pd.read_csv(r'C:\Users\KDT104\Desktop\T4_WIAProject\users.csv', encoding='utf-8')
        # for i in range(len(df)):
        #     user_email = df.iloc[i].user_email
        #     if user_email == 'rhrnaka@naver.com' or user_email == 'ghgusghgus2085@gmail.com':
        #         pass
        #     else:
        #         user_nm = df.iloc[i].user_nm
        #         user_ip = df.iloc[i].user_ip
        #         user_sex = df.iloc[i].user_sex
        #         user_img = df.iloc[i].user_img
        #         user_state = df.iloc[i].user_state
        # cursor.execute(f"insert into USERS (user_email, user_nm, user_ip, user_sex, user_img, user_state)"
        #                f"values ('{}','{}','{}','{}','{}','{}')")
        self.pgdb.commit()

    def insert_team_info(self, team_list:list, num:int):
        cursor = self.pgdb.cursor()
        for i in range(len(team_list)):
            number = team_list[0]['Number'][0]
            captain = team_list[0]['captain'][0]
            crew = team_list[0]['crew'][0].split(',')

            captain_state_list = self.select_user_info(column='user_img, user_state', user_nm=captain)
            sql_1 = f"insert into TEAM (team_nm, captain, crew_nm, crew_img, crew_state) " \
                  f"values ('{number}', '{captain}', 'none','{captain_state_list[0][0]}', '{captain_state_list[0][1]}')"

            cursor.execute(sql_1)

            for j in range(num):
                user_state_list = self.select_user_info(column='user_img, user_state', user_nm=crew[j])
                sql = f"insert into TEAM (team_nm, captain, crew_nm, crew_img, crew_state) " \
                      f"values ('{number}', 'none', '{crew[j]}', '{user_state_list[0][0]}', '{user_state_list[0][1]}')"
                cursor.execute(sql)
            self.pgdb.commit()

    # def find_my_teammate(self):
    #     cursor = self.pgdb.cursor()
    #     cursor.execute(f"select team_nm from TEAM where crew_nm = '고주양'")
    #     my_team_nm = cursor.fetchone()[0]
    #     cursor.execute(f"select * from TEAM where team_nm = '{my_team_nm}'")
    #     my_teammate = cursor.fetchall()
    #     return my_teammate

# if __name__=='__main__':
#     data = DataClass(type='master')
#     data.insert_user_info()
