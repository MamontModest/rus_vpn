import sqlite3
import time
from telethon.sync import TelegramClient
from clients_ru import data_limit
from datetime import datetime,timedelta

con = sqlite3.connect("ru_vpn.db")
cur = con.cursor()
api_id = '29413118'
api_hash = 'e80eddcc8322873af477a85223fe5d57'
username = 'dsafdafth'
phone=77073292462
client = TelegramClient(username, int(api_id), api_hash)
while True:
    nw_day=datetime.today().strftime("%Y-%m-%d")
    day_before=(datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
    con = sqlite3.connect("vpn.db")
    cur = con.cursor()
    cur.execute('select * from dates where napomni=(?) ',[nw_day])
    object=cur.fetchall()
    con.commit()
    if len(object)==0:
        print(nw_day,day_before)
        con = sqlite3.connect("vpn.db")
        cur = con.cursor()
        cur.execute('select * from users')
        con.commit()
        s = cur.fetchall()
        con.close()
        for i in s:
            time.sleep(2)
            if i[3]==nw_day:
                client.start(phone=str(phone))
                client.send_message('god_vpn_bot',str(i[0]))
                client.disconnect()
                print('send',i[0])
            elif i[3]==day_before:
                data_limit(i[2],0)
                print('done',i[0])
        con = sqlite3.connect("vpn.db")
        cur = con.cursor()
        cur.execute('insert into dates values(?,?)',[nw_day,day_before])
        con.commit()
        time.sleep(60 * 60* 22)
    else:
        time.sleep(60 * 60 * 22)