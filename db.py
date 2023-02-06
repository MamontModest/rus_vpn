import sqlite3
con = sqlite3.connect("ru_vpn.db")
cur = con.cursor()


#Работа с таблицей юзерс
def select_key(uid):
    cur.execute(f'SELECT keys FROM users WHERE uid = {uid}')
    con.commit()
    return 'ss:'+str(cur.fetchone()[0])+':5046/?outline=1'

def select_day(uid):
    cur.execute(f'SELECT for_date FROM users WHERE uid = {uid}')
    con.commit()
    date=cur.fetchone()[0].split('-')
    return date[2]+" / "+date[1]+' / '+date[0]

def first_time(uid):
    cur.execute(f'SELECT * FROM users WHERE uid = {uid}')
    con.commit()
    if len(cur.fetchall())==0:
        return True
    return False
def update_date(uid,month,now_day):
    day_before=select_day(uid)


def create_user(uid,keys,key_id,period):
    cur.execute('insert  into  users values (?,?,?,?)',[uid,keys,key_id,period])
    con.commit()



#Работа с рефералами
def select_referal(referal_nickname):
    cur.execute(f'SELECT * FROM all_referals WHERE referal_nickname = (?)',[referal_nickname])
    object=cur.fetchall()
    con.commit()
    if len(object) == 1:
        return True,object[0]
    return False,False

def create_user_ref(uid,referal_nickname,percent_referal,kolichestvo_platejei,user_percent):
    cur.execute('insert  into  referal values (?,?,?,?,?)', [uid,referal_nickname,percent_referal,kolichestvo_platejei,user_percent])
    con.commit()


def create_referal(referal_nickname,percent_referal,kolichestvo_platejei,user_percent):
    cur.execute('insert  into  all_referals values (?,?,?,?)', [referal_nickname,percent_referal,kolichestvo_platejei,user_percent])
    con.commit()




#Активные платежки и оплата
def delete_platej(uid):
    cur.execute('delete  from  active_payments where uid=(?)', [uid])
    con.commit()



def create_platej(uid,id_plateja,for_month):
    cur.execute('insert  into  active_payments values (?,?,?)', [uid,id_plateja,for_month])
    con.commit()

def chek_platej(uid):
    cur.execute(f'SELECT * FROM active_payments WHERE uid = {uid}')
    con.commit()
    if len(cur.fetchall()) == 0:
        return True
    return False
# оплата со скидкой

def cupon_payment(uid):
    cur.execute(f'SELECT user_percent,kolichestvo_platejei FROM referal WHERE uid = {uid}')
    con.commit()
    object=cur.fetchall()
    if len(object)==0:
        return False
    else:
        cur.execute(f'SELECT * FROM History_payments WHERE uid = {uid}')
        con.commit()
        if len(cur.fetchall())<object[0][1]:
            return object[0][0]
        return False






