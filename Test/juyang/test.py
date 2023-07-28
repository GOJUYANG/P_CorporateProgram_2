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
crew = '박호현, 박소연, 고주양'

print(f'이종혁, {crew}')