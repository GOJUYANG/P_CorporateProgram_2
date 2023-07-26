
import pandas as pd

df = pd.read_csv(r'C:\Users\KDT104\Desktop\T4_WIAProject\users.csv', encoding='utf-8')
for i in range(len(df)):
    text = df.iloc[i].user_nm
    print(len(text.encode()))

