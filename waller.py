from PyEasyQiwi import QiwiConnection
from db import delete_platej
from clients_ru import data_limit
import sqlite3
import time
from datetime import datetime,timedelta
api_key = "eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6IjJ0dDUyaS0wMCIsInVzZXJfaWQiOiI3OTgxMDE3ODcwNiIsInNlY3JldCI6ImY0Mzc4MDBhZDdlM2E3ZGUwYTcxNmEwN2QyY2JlZGFlYzE3NzIwMmFhYTU5NjI1NGM3MjQwZWVjN2Y5MThiMjQifX0="
qiwi = QiwiConnection(api_key)
con = sqlite3.connect("ru_vpn.db")
cur = con.cursor()
while True:
    cur.execute('select * from active_payments')
    con.commit()
    time.sleep(5)
    for i in cur.fetchall():
        try:
            status,responce=qiwi.check_bill(str(i[0])+':'+i[1])
            uid = i[0]
            if status == 'PAID':
                for_month = i[2]
                print(i[2])
                if for_month == 1:
                    cur.execute(f'SELECT * FROM users WHERE uid = {uid}')
                    con.commit()
                    all_info=cur.fetchone()
                    key_id=all_info[2]
                    data_limit(key_id,400000000000)
                    day_to = all_info[3]
                    now_day = datetime.today().strftime("%Y-%m-%d")
                    new_day=(max(datetime.strptime(now_day,"%Y-%m-%d"),datetime.strptime(day_to,"%Y-%m-%d"))+timedelta(days=30)).strftime("%Y-%m-%d")
                    cur.execute(f'update  users set for_date=(?)   WHERE uid = {uid}', [new_day])
                    con.commit()
                    cur.execute('insert into History_payments values(?,?,?,?)',[uid,149,'OK',now_day])
                    con.commit()
                    delete_platej(uid)



                elif for_month ==3:
                    cur.execute(f'SELECT * FROM users WHERE uid = {uid}')
                    con.commit()
                    all_info = cur.fetchone()
                    key_id = all_info[2]
                    data_limit(key_id, 400000000000)
                    day_to = all_info[3]
                    now_day = datetime.today().strftime("%Y-%m-%d")
                    new_day = (max(datetime.strptime(now_day, "%Y-%m-%d"),
                                   datetime.strptime(day_to, "%Y-%m-%d")) + timedelta(days=90)).strftime("%Y-%m-%d")
                    cur.execute(f'update  users set for_date=(?)   WHERE uid = {uid}', [new_day])
                    con.commit()
                    delete_platej(uid)
                    cur.execute('insert into History_payments values(?,?,?,?)', [uid, 349, 'OK', now_day])
                    con.commit()



                elif for_month == 12:
                    cur.execute(f'SELECT * FROM users WHERE uid = {uid}')
                    con.commit()
                    all_info=cur.fetchone()
                    key_id=all_info[2]
                    data_limit(key_id,400000000000)
                    day_to = all_info[3]
                    now_day = datetime.today().strftime("%Y-%m-%d")
                    new_day=(max(datetime.strptime(now_day,"%Y-%m-%d"),datetime.strptime(day_to,"%Y-%m-%d"))+timedelta(days=365)).strftime("%Y-%m-%d")
                    cur.execute(f'update  users set for_date=(?)   WHERE uid = {uid}', [new_day])
                    con.commit()
                    delete_platej(uid)
                    cur.execute('insert into History_payments values(?,?,?,?)', [uid, 999, 'OK', now_day])
                    con.commit()



            elif status == 'EXPIRED' or status == 'REJECTED':
                delete_platej(uid)
            elif status == 'WAITING':
                pass
        except:
            print('eror')






