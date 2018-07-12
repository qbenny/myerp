import sqlite3

con = sqlite3.connect('foods.db')
cur = con.cursor()
print("Opened database successfully")

# cursor = c.execute('SELECT * from COMPANY where SALARY >= ?',('500',))
sql = """ 
    SELECT f.name, types.name 
    FROM foods f INNER JOIN(SELECT * FROM food_types WHERE id = 6) types on f.type_id = types.id;
      """
cur.execute(sql)

for row in cur:
    print(row)

# row = cur.fetchone()
# while row:
#     print(row)
#     row = cur.fetchone()


# print(cur.fetchall())

cur.close()
con.close()
print("close conn")

"""   外键查询 多对一 P81
      SELECT foods.name, food_types.name
      FROM foods, food_types
      WHERE foods.type_id = food_types.id limit 10;    

    内连接  交集 P82
    SELECT *
    FROM foods inner join food_types on foods.id = food_types.id;

    交叉连接 笛卡尔积 交叉乘积 无条件没关系
    SELECT *
    FROM foods, food_types;

    外连接  左外连接 (右外连接可以由左外连接代替，全外连接可以通过复合查询执行) 和外键查询一样？？
    SELECT *
    FROM foods left outer join foods_episodes on foods.id = foods_episodes.food_id;

    别名
    SELECT f.name, t.name
    FROM foods f, food_types t
    WHERE f.type_id = t.id
    LIMIT 10;

    自我连接，各有两个实例
    SELECT f.name as food, e1.name, e1.season, e2.name, e2.season
    FROM episodes e1, foods_episodes fe1, foods f,
         episodes e2, foods_episodes fe2
    WHERE
        --Get foods in season 4
        (e1.id = fe1.episode_id and e1.season = 4) and fe1.food_id = f.id
        --Link foods with all other episodes
        and (fe1.food_id = fe2.food_id)
        --Link with their respective episodes and filter out e1's season
        and (fe2.episode_id = e2.id AND e2.season != e1.season)
    ORDER BY f.name;

    子查询 先在food_types根据名字查询id
    SELECT count(*)
    FROM foods
    WHERE type_id IN
    (SELECT id
     FROM food_types
     WHERE name = 'Bakery' or name = 'Cereal')

    相关子查询，引用外部查询变量
    添加额外数据，子查询统计每种食物在电影里出现的次数
    SELECT name,
    (SELECT count(food_id) FROM foods_episodes WHERE food_id = f.id) count
    FROM foods f ORDER BY count desc LIMIT 10;

    子查询用到ORDER BY
    根据各食品所属组的食品数量排序
    SELECT * FROM foods f
    ORDER BY (SELECT count(type_id) FROM foods WHERE type_id = f.type_id) DESC;

    from 子查询  内联视图/派生表
    SELECT f.name, types.name 
    FROM foods f INNER JOIN(SELECT * FROM food_types WHERE id = 6) types on f.type_id = types.id;

    复合查询 多个查询结果UNION联合, INTERSECT并集, EXCEPT差集
    结果字段必须相同







"""