# imports
from sqlalchemy import create_engine
from sqlalchemy.sql import text 
import os
import string 
import random 

#establish connection 
db_url = os.environ['DATABASE_URL'].replace("postgres://", "postgresql://")
engine = create_engine(db_url, echo=False)

#sql insert statement - add user
usr_insert = text(""" INSERT INTO users(username, email, salt, bio, hashed_password) VALUES(:username, :email, :salt, :bio, :hashed_password) ON CONFLICT DO NOTHING""")

#sql - get last user id
last_usr_id = text("""SELECT * FROM users ORDER BY id DESC LIMIT 1""")

#sql - add item 
item_insert = text("""INSERT INTO items(slug, title, description, seller_id) VALUES(:slug, :title, :description, :seller_id) ON CONFLICT DO NOTHING""")

#sql - select last item id
last_item_id = text("""SELECT * FROM items ORDER BY id DESC LIMIT 1""")

#sql - add comment 
comment_insert = text("""INSERT INTO comments(body, seller_id, item_id)VALUES(:body,:seller_id, :item_id ) ON CONFLICT DO NOTHING""")

#loop code 100 times 
with engine.connect() as con: 
    for i in range(100):
        rnd_username = f'user{i}'
        user = {'username': rnd_username, 'email':f'{rnd_username}@mail.com', 'salt': 'abc', 'bio': 'bio', 'hashed_password': '12345689'}
        con.execute(usr_insert, **user)

        result = con.execute(last_usr_id)
        for row in result: 
            generated_usr_id = row['id']
        
        item = {'slug': f'slug-{rnd_username}', 'title': f'title{i}', 'description': f'desc{i}', 'seller_id': generated_usr_id}
        con.execute(item_insert, **item)

        item_res = con.execute(last_item_id)
        for row in item_res: 
            generated_item_id = row['id']
        
        comment = {'body': f'comment{i}', 'seller_id':generated_usr_id, 'item_id': generated_item_id}
        con.execute(comment_insert, **comment)
        #test