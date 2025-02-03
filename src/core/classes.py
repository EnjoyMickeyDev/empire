import random
from typing import Optional
import requests
import json
import os
import time
import disnake
from disnake import TextInputStyle
from datetime import datetime, timedelta
import asyncio

class PickOne(disnake.ui.View):

    def __init__(self, member_id):
        super().__init__()

        self.member_id = member_id
        self.value = None

    async def interaction_check(self, interaction: disnake.MessageInteraction):
        ...

class join_1(disnake.ui.Modal):
    def __init__(self, bot, interaction, dol: str):
        self.bot = bot
        self.dol = dol
        components = [
            disnake.ui.TextInput(
                label="Ваш Static ID:",
                custom_id="_1",
                min_length=1,
                max_length=5
            ),
            disnake.ui.TextInput(
                label="Количество баллов:",
                custom_id="_2",
                min_length=2,
                max_length=10
            ),
            disnake.ui.TextInput(
                label="Сколько стоите на должности:",
                custom_id="_3",
                min_length=2,
                max_length=10
            ),
            disnake.ui.TextInput(
                label="Какую фракцию курируете:",
                custom_id="_4",
                min_length=2,
                max_length=10
            ),
            disnake.ui.TextInput(
                label="Количество закрытых репортов (форум):",
                custom_id="_5",
                # required = False,
                min_length=1,
                max_length=10
            ),
          
        ]
        super().__init__(
            title=str(f"Заявка на повышение"),
            custom_id="join_moore",
            components=components,
        )

    async def callback(self, interaction: disnake.ModalInteraction):
        
        embed = disnake.Embed(color=0x5dade2)
        embed.description = f"""
        • Discord - {interaction.author.mention} | `{interaction.author.display_name}`

        **• Static ID:** - `{interaction.text_values['_1']}` 
        **• Количество баллов:** - `{interaction.text_values['_2']}`
        **• В должности:** - `{interaction.text_values['_3']}`
        **• Курирует фракцию:** - `{interaction.text_values['_4']}`
        **• Закрытых репортов (форум):** - `{interaction.text_values['_5']}`
        """
        view = PickOne(interaction.author.id)
        view.add_item(disnake.ui.Button(style=disnake.ButtonStyle.green, label="Принять заявку", custom_id=f"fj_up_yes|{interaction.author.id}|{self.dol}"))
        view.add_item(disnake.ui.Button(style=disnake.ButtonStyle.red, label="Отклонить заявку", custom_id=f"fj_up_no|{interaction.author.id}|{interaction.author.mention}|{self.dol}"))

        channel = interaction.guild.get_channel(int(1333865736585744487))
        msg = await channel.send(embed=embed, view=view, content="<@&1332438630861508661>, <@&1332438630861508660>")
        await interaction.send(content=f"{interaction.author}, заявка успешно подана, ожидайте.", ephemeral=True)

        await self.bot.db.insert(
        {
            "member_id": interaction.author.id,
            "static_id": interaction.text_values['_1'],
            "ebal": interaction.text_values['_2'],
            "comment_1": interaction.text_values['_3'],
            "comment_2": interaction.text_values['_4'],
            "report": interaction.text_values['_5'],
            "message_id": msg.id,
        },
        "member_up"
        )

class vacation(disnake.ui.Modal):
    def __init__(self, bot, interaction):
        self.bot = bot
        components = [
            disnake.ui.TextInput(
                label="Ваш Static ID:",
                custom_id="_1",
                min_length=1,
                max_length=5
            ),
            disnake.ui.TextInput(
                label="Количество дней отпуска:",
                custom_id="_2",
                min_length=2,
                max_length=10
            ),
            disnake.ui.TextInput(
                label="Причина:",
                custom_id="_3",
            ),   
            
        ]
        super().__init__(
            title=str(f"Заявка на отпуск"),
            custom_id="join_moore",
            components=components,
        )

    async def callback(self, interaction: disnake.ModalInteraction):
        
        embed = disnake.Embed(color=0x5dade2)
        embed.description = f"""
        • Discord - {interaction.author.mention} | `{interaction.author.display_name}`

        **• Static ID:** - `{interaction.text_values['_1']}` 
        **• Количество дней отпуска:** - `{interaction.text_values['_2']}`
        **• Причина:** - `{interaction.text_values['_3']}`
      
        """
        view = PickOne(interaction.author.id)
        view.add_item(disnake.ui.Button(style=disnake.ButtonStyle.green, label="Принять заявку", custom_id=f"afk_yes"))
        view.add_item(disnake.ui.Button(style=disnake.ButtonStyle.red, label="Отклонить заявку", custom_id=f"afk_no"))

        channel = interaction.guild.get_channel(int(1334129989578264598))
        await channel.send(embed=embed, view=view, content="<@&1332438630861508661>, <@&1332438630861508660>")
        await interaction.send(content=f"{interaction.author}, заявка успешно подана, ожидайте решение.", ephemeral=True)

class time_off(disnake.ui.Modal):
    def __init__(self, bot, interaction):
        self.bot = bot
        components = [
            disnake.ui.TextInput(
                label="Ваш Static ID:",
                custom_id="_1",
                # min_length=1,
                max_length=5
            ),
            disnake.ui.TextInput(
                label="Количество времени отгула:",
                custom_id="_2",
                # min_length=2,
                max_length=15
            ),
            disnake.ui.TextInput(
                label="Причина:",
                custom_id="_3",
            ),   
            
        ]
        super().__init__(
            title=str(f"Заявка на отпуск"),
            custom_id="join_moore",
            components=components,
        )

    async def callback(self, interaction: disnake.ModalInteraction):
        
        embed = disnake.Embed(color=0x5dade2)
        embed.description = f"""
        • Discord - {interaction.author.mention} | `{interaction.author.display_name}`

        **• Static ID:** - `{interaction.text_values['_1']}` 
        **• Количество дней отпуска:** - `{interaction.text_values['_2']}`
        **• Причина:** - `{interaction.text_values['_3']}`
      
        """
        view = PickOne(interaction.author.id)
        view.add_item(disnake.ui.Button(style=disnake.ButtonStyle.green, label="Принять заявку", custom_id=f"afk_yes"))
        view.add_item(disnake.ui.Button(style=disnake.ButtonStyle.red, label="Отклонить заявку", custom_id=f"afk_no"))

        channel = interaction.guild.get_channel(int(1334129989578264598))
        await channel.send(embed=embed, view=view, content="<@&1332438630861508661>, <@&1332438630861508660>")
        await interaction.send(content=f"{interaction.author}, заявка успешно подана, ожидайте решение.", ephemeral=True)



class start_gos(disnake.ui.Modal):
    def __init__(self, bot, interaction, dol: str):
        self.bot = bot
        self.dol = dol
        components = [
            disnake.ui.TextInput(
                label="Ваш Static ID:",
                custom_id="_1",
                min_length=1,
                max_length=5
            ),
            disnake.ui.TextInput(
                label="Ваш средний онлайн:",
                custom_id="_2",
                min_length=2,
                max_length=10
            ),
            disnake.ui.TextInput(
                label="Какую фракцию хотите курировать:",
                custom_id="_3",
                min_length=2,
                max_length=15
            ),
            disnake.ui.TextInput(
                label="Знаний правил (0/10):",
                custom_id="_4",
                min_length=2,
                max_length=10
            ),
            disnake.ui.TextInput(
                label="Расскажите кратко обязаности следящего:",
                custom_id="_5",
            ),
          
        ]
        super().__init__(
            title=str(f"Заявка на следящего"),
            custom_id="join_moore",
            components=components,
        )

    async def callback(self, interaction: disnake.ModalInteraction):
        
        embed = disnake.Embed(color=0x5dade2)
        embed.description = f"""
        • Discord - {interaction.author.mention} | `{interaction.author.display_name}`
        • Заявка на - `{self.dol}`

        **• Static ID:** - `{interaction.text_values['_1']}` 
        **• Средний онлайн:** - `{interaction.text_values['_2']}`
        **• Хочет курировать фракцию:** - `{interaction.text_values['_3']}`
        **• Знаний правил:** - `{interaction.text_values['_4']}`
        **• Расскажите кратко обязаности следящего:** - `{interaction.text_values['_5']}`
        """
        view = PickOne(interaction.author.id)
        view.add_item(disnake.ui.Button(style=disnake.ButtonStyle.green, label="Принять заявку", custom_id=f"zauavka_yes|{interaction.author.id}|{self.dol}"))
        view.add_item(disnake.ui.Button(style=disnake.ButtonStyle.red, label="Отклонить заявку", custom_id=f"zauavka_no|{interaction.author.id}|{interaction.author.mention}|{self.dol}"))

        channel = interaction.guild.get_channel(int(1334233558092480552))
        msg = await channel.send(embed=embed, view=view, content="<@&1332438630861508661>, <@&1332438630861508660>")
        await interaction.send(content=f"{interaction.author}, заявка успешно подана, ожидайте.", ephemeral=True)