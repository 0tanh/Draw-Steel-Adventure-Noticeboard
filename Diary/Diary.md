Ok time to start learning

[sqlite in python](https://youtu.be/jsX99U8UkOo)

a cursor!! is a way of indexing through a database.

## 16 - 11

haven't worked on this project nearly enough today im structuring the database i couldn't sleep cuz i had a bunch of revelations abt how to set shit up lol

using sql and gemini to help build this database with supabase, gonna diarise as i learn.


the cascasde [[cascasde]] removes all links to the table


I NEED:
- User table:
    - Username text
    - User id (uuid) not null references auth.users on delete cascade
    - User discord
    - User characters json

- Game table:
    - Director references auth.users
    - Player spots remaining int
    - Game Date date
    - Current Players ##needs to reference
    - Current Characters
    - Continuing bool
    - OnlineOrIrl bool
    - Location text

- Games Noticeboard:
    - Director 
    - Game Date
    - Players so far
    - characters .

