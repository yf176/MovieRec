import pymysql
import csv

conn = pymysql.connect(host='localhost',
                       user='root',
                       passwd='1234',
                        port = 3309,
                       charset='utf8')

cur = conn.cursor() # 创建一个可以执行SQL语句的游标对象
cur.execute("use bishe") # 使用数据库

with open('douban_users.csv', 'r', encoding='utf-8') as f:
    read = csv.reader(f)
    for each in list(read)[1:]:
        i = tuple(each)
        sql = "INSERT INTO rating_score VALUES" + str(i)
        cur.execute(sql)  # 执行SQL语句

    conn.commit()  # 提交数据
    cur.close()  # 关闭游标
    conn.close()  # 关闭数据库