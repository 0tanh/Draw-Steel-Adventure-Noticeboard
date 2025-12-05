from re import Pattern
from pydantic import BaseModel, Field
from typing import Annotated
from fastapi import FastAPI
import sqlite3
from datetime import datetime, timezone
from dotenv import load_dotenv
import os
from enum import Enum
import uuid
from zoneinfo import ZoneInfo

load_dotenv()
tz = ZoneInfo(os.getenv('LOCATION'))
dt_tz= datetime.now(tz)

db = os.getenv('TEST_DB')

dbq = db.split("/")[-1].split(".")[0]
app = FastAPI(title="Draw Steel Noticeboard API", 
              summary="API for interacting with the 0tanh Draw Steel Noticeboard",
              description="API that should allow for scheduling games and notifying users of the games being scheduled",
              contact={"Support and More!":"betty.lossless@gmail.com"})

class BoardInstance(BaseModel):
    name: str = Field(alias="Name of this Noticeboard", example='Local Gameshop Noticeboard')
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

@app.get('/games/upcoming_games')
async def upcoming_games():
    return {"This will return future games"}

@app.get('/me/my_games')
async def my_games():
    return {"This will return games"}

@app.get('/me/my_characters')
async def my_characters():
    return {"This will return characters"}


