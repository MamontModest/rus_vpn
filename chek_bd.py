import sqlite3
con = sqlite3.connect("ru_vpn.db")
cur = con.cursor()
cur.execute('select * from dates')
print('\n\n\n\ndates:')
for i in cur.fetchall():
    print(i)
cur.execute('select * from users')
print('\n\n\n\nusers:')
for i in cur.fetchall():
    print(i)
cur.execute('select * from referal')
print('\n\n\n\nreferal:')
for i in cur.fetchall():
    print(i)
cur.execute('select * from all_referals')
print('\n\n\n\nall referals:')
for i in cur.fetchall():
    print(i)
cur.execute('select * from History_payments')
print('\n\n\n\nHistory_payments:')
for i in cur.fetchall():
    print(i)
cur.execute('select * from active_payments')
print('\n\n\n\nactive_payments:')
for i in cur.fetchall():
    print(i)