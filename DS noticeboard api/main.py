from re import Pattern
from pydantic import BaseModel, Field
from typing import Annotated
from fastapi import FastAPI
import sqlite3
from datetime import datetime, timezone
from dotenv import load_dotenv
import os
from pprint import pprint
from enum import Enum
import uuid
from zoneinfo import ZoneInfo

load_dotenv()
tz = ZoneInfo(os.getenv('LOCATION'))
dt_tz= datetime.now(tz)

db = os.getenv('TEST_DB')

dbq = db.split("/")[-1].split(".")[0]
app = FastAPI(title="Draw Steel Noticeboard API", 
              description="API for interacting with the 0tanh Draw Steel Noticeboard",
              summary="API that should allow for scheduling games and notifying users of the games being scheduled",
              contact={"Support and More!":"betty.lossless@gmail.com"})

class BoardInstance(BaseModel):
    name: str = Field(alias="Name of this Noticeboard", examples=['Local Gameshop Noticeboard','All my friends Noticeboard'])
    created_by: str

class Draw_Steel_Game(BaseModel):
    game_name: str= Field(example="Name of Game")
    player_limit: int = Field(default= 4)
    author_id: str = Field(example="my_discord")
    instance_id: str
    when: str = Field(alias="When the game is happening", example="Time24h, Day, Month, Year")
    content:str = Field(example="Description of the game")

@app.post('/games/new_game/')
async def new_game(game: Annotated[Draw_Steel_Game, "A new Draw Steel Game"]):
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        structure = "id,instance_id,author_id,content,when,game_name"
        schema = "public"
        table = "notices"
        game_id = uuid.uuid5(uuid.NAMESPACE_DNS ,game.game_name)
        
        q = f"INSERT INTO {'{}'*2} ({structure}) VALUES ({'{}'*6})".format(
            schema, #current database schema
            table, #current table
            f"'{game_id}'", #uuid of game
            f"'{game.instance_id}'", #instance_id
            f"'{game.author_id}'", #authors_id
            f"'{game.content}'", #description of game
            f"'{game.when}'", #when the game is happening
            f"'{game.game_name}'" #name of the game
            )
        cursor.execute(q)
        connection.commit()
        cursor.close()
    return q

@app.post('/games/new_players/')
async def new_player(discord_id):
    return {"player_id" :discord_id,
            "date_created":datetime.now()}

@app.post('/instances/new_instance')
async def new_instance(instance: BoardInstance):
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        structure = 'instance_id,instance_name,created_by'
        schema = 'public'
        table = 'instances'
        instance_id = uuid.uuid5(uuid.NAMESPACE_DNS, instance.name)

        q = f"INSERT INTO {'{}'*2} ({structure}) VALUES ({'{}'*3})".format(
            schema,
            table,
            f"'{instance_id}'",
            f"'{instance.name}'",
            f"'{instance.created_by}'"
            )
        
        cursor.execute(q)
        connection.commit()
        cursor.close()
    return f"{instance.name} instance created"


# @app.post('/query/insert_test')
# async def testing_an_insertion(ll: LongList_Entry):
#     q = "INSERT INTO {} (isbn,title,author,translator,format,pages,publisher,published,year,votes,rating) VALUES ({},{},{},{},{},{},{},{},{},{},{})".format(
#         dbq, f"'{ll.isbn}'",f"'{ll.title}'",f"'{ll.author}'",f"'{ll.translator}'",f"'{ll.format}'",ll.pages,f"'{ll.publisher}'",f"'{ll.published}'",ll.year,ll.votes,ll.rating)
    
#     connection = sqlite3.connect(db)
#     cursor = connection.cursor()
#     cursor.execute(q)
#     connection.commit()
#     cursor.close()
#     connection.close()
#     return q

