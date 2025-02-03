import os
import disnake
import time
import asyncio

from datetime import datetime
from os import getenv
from traceback import format_exception
from disnake.ext import commands
from PIL import Image, ImageFont, ImageDraw

from src.db.postgres import *


class emoire(commands.InteractionBot):
    def __init__(self, **kwargs):
        intents = disnake.Intents.all()
        super().__init__(
            intents=intents,
            # sync_commands_debug=True,
            # activity=disnake.Activity(
            #     type=disnake.ActivityType.streaming,
            #     name="Moore FamQ",
            #     # url="https://www.twitch.tv/MooreFamQ"
            # ),
        )

        self.launch_time = datetime.now()
        self.bot_version = "1.0"
        self.db = PostgresqlDatabase(dsn=getenv("DATABASE"))
   
    async def on_connect(self):
        try:
            await self.db.connect()
            print("\032[31m [DATABASE] Connected.")
        except Exception as e:
            print(f"\033[31m {e}")


    async def on_ready(self):
        await self.wait_until_ready()
        # print(123)
        self.loop.create_task(self.shift_change())
        # self.shift_change.start()
        # self.loop.create_task(self.banner_change())
        # self.banner_change.start()
        
        print("\033[31m --------------------------------------")
        print("\033[32m Вошел в систему как:")
        print(f"\033[33m {self.user} | {self.user.id}")
        print(f"\033[33m Время запуска {datetime.now() - self.launch_time}")
        print("\033[31m --------------------------------------")

    async def on_slash_command_error(self, interaction: disnake.CommandInteraction, exception):
        # print(1)
        exception = getattr(exception, "original", exception)
        DEFAULT = 0x2F3136
        embed = disnake.Embed(color=DEFAULT)
        print(exception)
        if isinstance(exception, commands.MissingAnyRole):
            embed.description = "Вам недоступна эта команда."
            await interaction.send(embed=embed, delete_after=3)
        elif isinstance(exception, commands.MissingRole):
            embed.description = "Вам недоступна эта команда."
            await interaction.send(embed=embed, delete_after=3)
        elif isinstance(exception, commands.MemberNotFound):
            embed.description = "Указанного пользователя нет."
            await interaction.send(embed=embed, delete_after=3)
        elif isinstance(exception, commands.CommandOnCooldown):
            print(2)
            embed.description = f"Подождите еще <t:{int(time.time() + int(round(exception.retry_after, 2)))}:R>"
            await interaction.send(embed=embed, delete_after=3)
        else:
            embed.description = "".join(
                format_exception(
                    type(exception),
                    exception,
                    exception.__traceback__
                )
            )
            await interaction.send(embed=embed, delete_after=30)
    
    async def shift_change(self):
        while True:
            while not self.is_closed():
                data = await self.db.select_all(
                    "*", 
                    "member_shift", 
                where={
                    "status": True, 
                    }
                )  
                for row in data:
                    if row:
                        await self.db.update({
                            "time_second": {60: "+"},
                        }, "member_shift", where={
                            "member_id": row['member_id'],
                            "status": True, 
                        })

                await asyncio.sleep(60)

    def load_extensions(self):
        # print(12321)
        for filename in os.listdir("./src/ext"): 
            if filename.endswith(".py"):

                try:
                    self.load_extension(f"src.ext.{filename[:-3]}")
                    print(f"\033[32m [EXTENSION]: {filename} loaded...")
                except Exception as e:
                    print(f"\033[31m {e}")