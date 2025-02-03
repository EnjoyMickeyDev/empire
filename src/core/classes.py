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
    def __init__(self, bot, interaction, role: str):
        self.bot = bot
        self.role = role 
        self.channel_id = 1333865736585744487 

        components = [
            disnake.ui.TextInput(
                label="Ваш Static ID:",
                custom_id="static_id",
                min_length=1,
                max_length=5
            ),
            disnake.ui.TextInput(
                label="Количество баллов:",
                custom_id="points",
                min_length=2,
                max_length=10
            ),
            disnake.ui.TextInput(
                label="Сколько стоите на должности (дней):",
                custom_id="tenure",
                min_length=2,
                max_length=10
            ),
            disnake.ui.TextInput(
                label="Какую фракцию курируете:",
                custom_id="faction",
                min_length=2,
                max_length=10
            ),
            disnake.ui.TextInput(
                label="Количество закрытых репортов (форум):",
                custom_id="reports_closed",
                min_length=1,
                max_length=10
            ),
        ]

        super().__init__(
            title=f"Заявка на повышение ({role})",
            custom_id="promotion_request",
            components=components,
        )

    async def callback(self, interaction: disnake.ModalInteraction):
        try:
            embed = disnake.Embed(color=0x5dade2)
            embed.description = (
                f"• Discord - {interaction.author.mention} | `{interaction.author.display_name}`\n"
                f"**• Static ID:** `{interaction.text_values.get('static_id', 'Не указано')}`\n"
                f"**• Количество баллов:** `{interaction.text_values.get('points', 'Не указано')}`\n"
                f"**• В должности (дней):** `{interaction.text_values.get('tenure', 'Не указано')}`\n"
                f"**• Курирует фракцию:** `{interaction.text_values.get('faction', 'Не указана')}`\n"
                f"**• Закрытых репортов (форум):** `{interaction.text_values.get('reports_closed', 'Не указано')}`"
            )

            channel = interaction.guild.get_channel(self.channel_id)
            if not channel:
                await interaction.send(content="Ошибка: Канал для отправки заявки не найден.", ephemeral=True)
                return

            # Создаем View с кнопками "Принять" и "Отклонить"
            view = PickOne(interaction.author.id)
            view.add_item(
                disnake.ui.Button(
                    style=disnake.ButtonStyle.green,
                    label="Принять заявку",
                    custom_id=f"fj_up_yes|{interaction.author.id}|{self.role}"
                )
            )
            view.add_item(
                disnake.ui.Button(
                    style=disnake.ButtonStyle.red,
                    label="Отклонить заявку",
                    custom_id=f"fj_up_no|{interaction.author.id}|{interaction.author.mention}|{self.role}"
                )
            )

            content = "<@&1332438630861508661>, <@&1332438630861508660>"
            try:
                msg = await channel.send(embed=embed, view=view, content=content)
            except Exception as e:
                await interaction.send(content=f"Произошла ошибка при отправке заявки: {str(e)}", ephemeral=True)
                return

            try:
                await self.bot.db.insert(
                    {
                        "member_id": interaction.author.id,
                        "static_id": interaction.text_values.get("static_id", "Не указано"),
                        "points": interaction.text_values.get("points", "Не указано"),
                        "tenure": interaction.text_values.get("tenure", "Не указано"),
                        "faction": interaction.text_values.get("faction", "Не указана"),
                        "reports_closed": interaction.text_values.get("reports_closed", "Не указано"),
                        "message_id": msg.id,
                    },
                    "member_up"
                )
            except Exception as e:
                await interaction.send(content=f"Произошла ошибка при сохранении данных: {str(e)}", ephemeral=True)
                return

            await interaction.send(
                content=f"{interaction.author.mention}, заявка успешно подана, ожидайте решение.",
                ephemeral=True
            )

        except Exception as e:
            await interaction.send(content=f"Произошла ошибка: {str(e)}", ephemeral=True)

class vacation(disnake.ui.Modal):
    def __init__(self, bot, interaction):
        self.bot = bot
        self.channel_id = 1334129989578264598 

        components = [
            disnake.ui.TextInput(
                label="Ваш Static ID:",
                custom_id="static_id",
                min_length=1,
                max_length=5
            ),
            disnake.ui.TextInput(
                label="Количество дней отпуска:",
                custom_id="days_off",
                min_length=2,
                max_length=10
            ),
            disnake.ui.TextInput(
                label="Причина:",
                custom_id="reason",
            ),
        ]

        super().__init__(
            title="Заявка на отпуск",
            custom_id="vacation_modal",
            components=components,
        )

    async def callback(self, interaction: disnake.ModalInteraction):
        try:
            embed = disnake.Embed(color=0x5dade2)
            embed.description = (
                f"• Discord - {interaction.author.mention} | `{interaction.author.display_name}`\n"
                f"**• Static ID:** `{interaction.text_values.get('static_id', 'Не указано')}`\n"
                f"**• Количество дней отпуска:** `{interaction.text_values.get('days_off', 'Не указано')}`\n"
                f"**• Причина:** `{interaction.text_values.get('reason', 'Не указана')}`"
            )

            channel = interaction.guild.get_channel(self.channel_id)
            if not channel:
                await interaction.send(content="Ошибка: Канал для отправки заявки не найден.", ephemeral=True)
                return

            view = PickOne(interaction.author.id)
            view.add_item(
                disnake.ui.Button(
                    style=disnake.ButtonStyle.green,
                    label="Принять заявку",
                    custom_id=f"afk_yes|{interaction.author.id}"
                )
            )
            view.add_item(
                disnake.ui.Button(
                    style=disnake.ButtonStyle.red,
                    label="Отклонить заявку",
                    custom_id=f"afk_no|{interaction.author.id}"
                )
            )

            content = "<@&1332438630861508661>, <@&1332438630861508660>"
            try:
                msg = await channel.send(embed=embed, view=view, content=content)
            except Exception as e:
                await interaction.send(content=f"Произошла ошибка при отправке заявки: {str(e)}", ephemeral=True)
                return

            await interaction.send(
                content=f"{interaction.author.mention}, заявка успешно подана, ожидайте решение.",
                ephemeral=True
            )

        except Exception as e:
            await interaction.send(content=f"Произошла ошибка: {str(e)}", ephemeral=True)

class time_off(disnake.ui.Modal):
    def __init__(self, bot, interaction):
        self.bot = bot
        self.channel_id = 1334129989578264598 

        components = [
            disnake.ui.TextInput(
                label="Ваш Static ID:",
                custom_id="_static_id",
                max_length=5
            ),
            disnake.ui.TextInput(
                label="Количество времени отгула (дней):",
                custom_id="_days_off",
                max_length=15
            ),
            disnake.ui.TextInput(
                label="Причина:",
                custom_id="_reason",
            ),
        ]

        super().__init__(
            title="Заявка на отпуск",
            custom_id="time_off_modal",
            components=components,
        )

    async def callback(self, interaction: disnake.ModalInteraction):
        try:
            embed = disnake.Embed(color=0x5dade2)
            embed.description = (
                f"• Discord - {interaction.author.mention} | `{interaction.author.display_name}`\n"
                f"**• Static ID:** `{interaction.text_values.get('_static_id', 'Не указано')}`\n"
                f"**• Количество дней отпуска:** `{interaction.text_values.get('_days_off', 'Не указано')}`\n"
                f"**• Причина:** `{interaction.text_values.get('_reason', 'Не указана')}`"
            )

            channel = interaction.guild.get_channel(self.channel_id)
            if not channel:
                await interaction.send(content="Ошибка: Канал для отправки заявки не найден.", ephemeral=True)
                return

            view = PickOne(interaction.author.id)
            view.add_item(
                disnake.ui.Button(
                    style=disnake.ButtonStyle.green,
                    label="Принять заявку",
                    custom_id=f"afk_yes|{interaction.author.id}"
                )
            )
            view.add_item(
                disnake.ui.Button(
                    style=disnake.ButtonStyle.red,
                    label="Отклонить заявку",
                    custom_id=f"afk_no|{interaction.author.id}"
                )
            )

            content = "<@&1332438630861508661>, <@&1332438630861508660>"
            try:
                msg = await channel.send(embed=embed, view=view, content=content)
            except Exception as e:
                await interaction.send(content=f"Произошла ошибка при отправке заявки: {str(e)}", ephemeral=True)
                return

            await interaction.send(
                content=f"{interaction.author.mention}, заявка успешно подана, ожидайте решение.",
                ephemeral=True
            )

        except Exception as e:
            await interaction.send(content=f"Произошла ошибка: {str(e)}", ephemeral=True)



class start_gos(disnake.ui.Modal):
    def __init__(self, bot, interaction, dol: str):
        self.bot = bot
        self.dol = dol  
        self.channel_id = 1334233558092480552

        components = [
            disnake.ui.TextInput(
                label="Ваш Static ID:",
                custom_id="_static_id",
                min_length=1,
                max_length=5
            ),
            disnake.ui.TextInput(
                label="Ваш средний онлайн:",
                custom_id="_avg_online",
                min_length=2,
                max_length=10
            ),
            disnake.ui.TextInput(
                label="Какую фракцию хотите курировать:",
                custom_id="_faction",
                min_length=2,
                max_length=15
            ),
            disnake.ui.TextInput(
                label="Знание правил (0/10):",
                custom_id="_rules_knowledge",
                min_length=2,
                max_length=10
            ),
            disnake.ui.TextInput(
                label="Расскажите кратко обязанности следящего:",
                custom_id="_responsibilities",
            ),
        ]

        super().__init__(
            title=f"Заявка на должность",
            custom_id="1234",
            components=components,
        )

    async def callback(self, interaction: disnake.ModalInteraction):
        try:
            embed = disnake.Embed(color=0x5dade2)
            embed.description = (
                f"• Discord - {interaction.author.mention} | `{interaction.author.display_name}`\n"
                f"• Заявка на - `{self.dol}`\n"
                f"**• Static ID:** `{interaction.text_values.get('_static_id', 'Не указано')}`\n"
                f"**• Средний онлайн:** `{interaction.text_values.get('_avg_online', 'Не указано')}`\n"
                f"**• Хочет курировать фракцию:** `{interaction.text_values.get('_faction', 'Не указано')}`\n"
                f"**• Знание правил:** `{interaction.text_values.get('_rules_knowledge', 'Не указано')}`\n"
                f"**• Обязанности следящего:** `{interaction.text_values.get('_responsibilities', 'Не указано')}`"
            )

            channel = interaction.guild.get_channel(self.channel_id)
            if not channel:
                await interaction.send(content="Ошибка: Канал для отправки заявки не найден.", ephemeral=True)
                return

            view = PickOne(interaction.author.id)
            view.add_item(
                disnake.ui.Button(
                    style=disnake.ButtonStyle.green,
                    label="Принять заявку",
                    custom_id=f"zauavka_yes|{interaction.author.id}|{self.dol}"
                )
            )
            view.add_item(
                disnake.ui.Button(
                    style=disnake.ButtonStyle.red,
                    label="Отклонить заявку",
                    custom_id=f"zauavka_no|{interaction.author.id}|{interaction.author.mention}|{self.dol}"
                )
            )

            content = "<@&1332438630861508661>, <@&1332438630861508660>"
            msg = await channel.send(embed=embed, view=view, content=content)

            await self.bot.db.insert(
                "member_up",
                {
                    "message_id": msg.id,
                    "author_id": interaction.author.id,
                    "role": self.dol,
                    "status": "pending"
                }
            )

            await interaction.send(
                content=f"{interaction.author.mention}, заявка успешно подана, ожидайте.",
                ephemeral=True
            )

        except Exception as e:
            await interaction.send(content=f"Произошла ошибка: {str(e)}", ephemeral=True)