import psycopg2 as pg
import pandas as pd

from datetime import datetime, timedelta
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

        self.engine = create_engine(f'postgresql://postgres:1234@10.10.20.104:5432/data')

    def end_conn(self):
        self.pgdb.close()

    def show_all_df(self, tb_name):
        df = pd.read_sql(f"select * from {tb_name}", self.engine)
        pd.set_option('display.max_columns', None)
        print(df)

    def select_user_info(self, column: str, user_email="", user_nm="", plus=""):
        """
        :param column:
        :param user_email:
        :param user_nm:
        :param plus:
        :return: USERS 테이블에서 인자로 select 열을 지정하고 조건을 설정하여 값 추출
        """
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

        df = pd.read_sql(sql, self.engine)
        return df.values

    def update_user_pw(self, pw, email):
        """
        :param pw:
        :param email:
        :사용자가 비밀번호 변경 시 DB 해당 내용을 DB에 업데이트
        """
        cursor = self.pgdb.cursor()
        cursor.execute(f"update USERS set user_pw='{pw} where user_email='{email}")
        self.pgdb.commit()

    def update_user_info(self, img, name, state, email):
        """
        :param img:
        :param name:
        :param state:
        :사용자가 상태메세지 변경 시 해당 내용을 DB에 업데이트
        """
        cursor = self.pgdb.cursor()
        cursor.execute(f"update USERS set user_img='{img}', user_nm='{name}', user_state='{state}'"
                       f" where user_email = '{email}'")
        self.pgdb.commit()

    def insert_user_info(self):
        """
        :USERS 테이블에 정보 입력
        """
        cursor = self.pgdb.cursor()
        df = pd.read_csv(r'C:\Users\KDT104\Desktop\T4_WIAProject\users.csv', encoding='utf-8')
        for i in range(len(df)):
            user_email = df.iloc[i].user_email
            user_nm = df.iloc[i].user_nm
            user_ip = df.iloc[i].user_ip
            user_sex = df.iloc[i].user_sex
            user_img = df.iloc[i].user_img
            user_state = df.iloc[i].user_state
            cursor.execute(f"insert into USERS (user_email, user_nm, user_ip, user_sex, user_img, user_state)"
                           f"values ('{user_email}','{user_nm}','{user_ip}','{user_sex}','{user_img}','{user_state}')")
        self.pgdb.commit()

    def insert_team_info(self, dict_team: dict):
        """
        :param team_list:
        :param num:
        :서버에서 팀 구성 시 팀장+팀원의 정보를 DB team 테이블에 입력
        """
        cursor = self.pgdb.cursor()

        number = dict_team['Number']
        captain = dict_team['captain']
        crew = dict_team['crew'].split(',')

        captain_state_list = self.select_user_info(column='user_img, user_state', user_nm=captain)
        sql_captain = f"insert into TEAM (team_nm, captain, crew_nm, crew_img, crew_state) " \
              f"values ('{number}', '{captain}', 'none','{captain_state_list[0][0]}', '{captain_state_list[0][1]}')"

        cursor.execute(sql_captain)

        for j in range(len(crew)):
            user_state_list = self.select_user_info(column='user_img, user_state', user_nm=crew[j])
            sql_crew = f"insert into TEAM (team_nm, captain, crew_nm, crew_img, crew_state) " \
                  f"values ('{number}', 'none', '{crew[j]}', '{user_state_list[0][0]}', '{user_state_list[0][1]}')"
            cursor.execute(sql_crew)

        self.pgdb.commit()

    def find_my_team_nm(self, name):
        cursor = self.pgdb.cursor()

        cursor.execute(f"select team_nm from TEAM where captain = '{name}'")
        my_team_nm = cursor.fetchone()

        if my_team_nm is None:
            cursor.execute(f"select team_nm from TEAM where crew_nm = '{name}'")
            my_team_nm = cursor.fetchone()
        return my_team_nm

    def find_my_teammate(self, name):
        """
        :return: 사용자가 속한 팀리스트 반환
        """
        my_team_nm = self.find_my_team_nm(name)

        df = pd.read_sql(f"select * from TEAM where team_nm = '{my_team_nm}'", self.engine)

        return df.values

    def insert_chatroom(self, dict_team):
        """
        :채팅방 정보를 담고 있는 chatroom 테이블에 형성된 테이블 정보입력 (팀 채팅)
        """
        cursor = self.pgdb.cursor()

        # type : single
        # nm_list = self.select_user_info(column='user_nm')
        # for i in range(len(self.select_user_info(column='*'))):
        #     cursor.execute(f"insert into chatroom (room_type, room_nm, member_nm) "
        #                    f"values ('single','{nm_list[i][0]}', '관리자, {nm_list[i][0]}')")

        # type : team
        number = dict_team['Number']
        captain = dict_team['captain']
        crew = dict_team['crew']

        cursor.execute(f"insert into chatroom (room_type, room_nm, member_nm) "
                       f"values ('team', '{number}', '{captain},{crew}')")

        self.pgdb.commit()

    def insert_chat_manager(self, message, user_nm, room_nm):

        send_time = datetime.now().strptime('%Y-%m-%d %H:%M:%S') # 2023-07-28 13:30:45

        cursor = self.pgdb.cursor()
        cursor.execute(f"insert into chat_manager (message, send_nm, room_nm, send_time) "
                       f"values ('{message}','{user_nm}','{room_nm}','{send_time}')")
        self.pgdb.commit()

    def select_chat_manager(self, user_nm):
        """
        :return:사용자가 속한 개인 채팅방 내용 조회
        """
        df = pd.read_sql(f"select * from chat_manager where room_nm = '{user_nm}'", self.engine)
        return df.values

    def insert_chat_team(self, message, user_nm):

        send_time = datetime.now().strptime('%Y-%m-%d %H:%M:%S')  # 2023-07-28 13:30:45
        room_nm = self.find_my_team_nm(user_nm)

        cursor = self.pgdb.cursor()
        cursor.execute(f"insert into chat_team (message, send_nm, room_nm, send_time) "
                       f"values ('{message}','{user_nm}','{room_nm}','{send_time}')")
        self.pgdb.commit()

    def select_chat_team(self, user_nm):
        """
        :return:사용자가 속한 팀의 채팅방 내용 조회
        """
        room_nm = self.find_my_team_nm(user_nm)
        df = pd.read_sql(f"select * from chat_team where room_nm = '{room_nm[0]}'", self.engine)
        return df.values

    def delete_chat(self, c_type: str, chat_nm):
        cursor = self.pgdb.cursor()

        if c_type == "single":
            cursor.execute(f"delete from chat_manager where chat_nm = '{chat_nm}'")
        elif c_type == 'team':
            cursor.execute(f"delete from chat_team where chat_nm = '{chat_nm}'")
        self.pgdb.commit()

    def insert_board(self, user_nm, content, tag, title):
        cursor = self.pgdb.cursor()
        cursor.execute(f"insert into board (user_nm, content, cnt_answer, cnt_views, tag, title from board)"
                       f" values ('{user_nm}','{content}',0,0,'{tag}','{title}')")
        self.pgdb.commit()

    def select_board(self):
        """
        :return: 게시판 내용 조회
        """
        df = pd.read_sql(f"select cnt_answer, cnt_views, title, content, user_nm, tag from board", self.engine)
        return df.values

    def specific_select_board(self, title):
        """
        :return: 특정 게시판 내용 조회
        """
        df = pd.read_sql(f"select cnt_answer, cnt_views, title, content, user_nm, tag from board where title = '{title}'")
        return df.values

    def update_views_board(self, title, cnt_view):
        cursor = self.pgdb.cursor()
        cursor.execute(f"update board set cnt_views = {cnt_view} where title = '{title}'")
        self.pgdb.commit()

    def update_answer_board(self, title, content):
        cursor = self.pgdb.cursor()
        cursor.execute(f"insert into board (content, title) "
                       f"values ('{title}', '{content}')")
        self.pgdb.commit()

    def insert_calendar(self, team_nm, user_nm, workstate, work):
        """
        :사용자가 일정공유 캘린더에 입력한 내용 DB 저장
        """
        cursor = self.pgdb.cursor()
        cursor.execute(f"insert into calendar (team_nm, member_nm, workstate, work) "
                       f"values ('{team_nm}', '{user_nm}', '{workstate}', '{work}')")
        self.pgdb.commit()

    def select_calendar(self, user_nm):
        """
        :return:사용자가 속한 팀의 캘린더 조회
        """
        team_nm = self.find_my_team_nm(user_nm)
        df = pd.read_sql(f"select * from calendar where team_nm = '{team_nm}'", self.engine)
        return df.values

    def delete_calendar(self):
        current_time = datetime.now()

        # 하루 후 시간 계산
        one_day_ago = current_time - timedelta(days=1)

        # 하루가 지났는지 확인
        if current_time < one_day_ago:
            print("하루가 지나지 않았습니다.")
        else:
            print("하루가 지났습니다.")
            cursor = self.pgdb.cursor()
            cursor.execute(f"delete from team")
            self.pgdb.commit()
            print(" [ 삭제/DB ] : 일정공유 테이블 ")
        pass

    def insert_data(self, tb_name, data: dict, email=""):
        """
        :param tb_name:
        :param data:
        :param email:
        :원하는 테이블에 정보를 일괄적으로 추가함
        """
        cursor = self.pgdb.cursor()

        size = len(data)
        column = ""

        for i, k in enumerate(data):
            column += "?, "
            column = column[:-2]

            sql = f"insert into {tb_name} ({k}) values ({column})"

            if email != "":
                sql += f" where user_email = '{email}'"
            else:
                cursor.execute(sql, data[k])

        self.pgdb.commit()
        self.end_conn()

        #================읽지않은메세지===================#

    def count_not_read_msg(self, room_nm, member_nm):
        """채팅방 별 메시지 읽음 구분 테이블 생성"""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor = self.pgdb.cursor()
        cursor.executescript(f"""
        CREATE TABLE IF NOT EXISTS "READ_{room_nm}" (
        "room_nm" TEXT,
        "user_nm" TEXT,
        "last_read_time" TEXT,
        FOREIGN KEY("user_nm") REFERENCES "chat_team" ("send_nm") );
        """)

        for i in range(len(member_nm)):
            cursor.execute(f"""
            INSERT INTO READ_{room_nm} (room_nm, user_nm, last_read_time) VALUES ('{room_nm}', '{member_nm}', '{now}' ) ;
            """)

        self.pgdb.commit()

    def update_last_read_time(self, room_nm, user_nm):
        """유저가 방을 입장할때마다(버튼클릭) 안읽은 날짜를 갱신한다"""

        cursor = self.pgdb.cursor()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = f"UPDATE READ_{room_nm} SET last_read_time = '{now}' WHERE user_nm = '{user_nm}'"
        cursor.execute(sql)

        self.pgdb.commit()

    def count_not_read_chatnum(self, room_nm, user_nm):
        """
        :return: 읽지 않은 메세지 수량 반환
        """

        print(room_nm)
        print(user_nm)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor = self.pgdb.cursor()

        try:
            cursor.execute(f"select last_read_time from READ_{room_nm} where user_nm = '{user_nm}'")
            formatted_time = cursor.fetchone()[0]
        except:
            self.count_not_read_msg(room_nm=room_nm, member_nm=user_nm)
            cursor.execute(f"select last_read_time from READ_{room_nm} where user_nm = '{user_nm}'")
            formatted_time = cursor.fetchone()[0]

        cursor.execute(f"SELECT send_time FROM chat_team where send_nm = '{user_nm}' ORDER BY msg_no DESC LIMIT 1")
        last_content = cursor.fetchone()[0]

        print(f"{user_nm}가 채팅방에서 마지막으로 읽은 시간 : {formatted_time}")
        print(f"채팅방 {room_nm}의 마지막 메세지발송시간 : {last_content}")

        #마지막으로 읽은 시간보다 더 이후에 메시지가 발송되었는지 확인
        #메시지 발송 시간이 마지막 메시지 발송 시간보다 이전 또는 동일한지 확인
        cursor.execute(f"SELECT send_time "
                       f"FROM chat_team LEFT JOIN READ_{room_nm} ON "
                       f"chat_team.send_nm = READ_{room_nm}.user_nm "
                       f"WHERE '{formatted_time}' < SEND_TIME AND SEND_TIME <= '{last_content}' "
                       f"AND chat_team.send_nm = READ_{room_nm}.user_nm")
        cnt = cursor.fetchall()

        if len(cnt) == 0:
            return 0
        else:
            return len(cnt[0])

if __name__=='__main__':
    DB = DataClass()
    # print(DB.select_user_info(column="*", user_email='ghgusghgus2085@gmail.com'))
    # print(DB.find_my_teammate('박호현'))
    # print(len(DB.select_user_info(column='*')))
    # print(DB.insert_chatroom())
    # print(DB.insert_chatroom(team_list))
    # DB.show_all_df('users')
    # print(DB.select_chat_team('박호현'))