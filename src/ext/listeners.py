import disnake
from disnake.ext import commands
from datetime import datetime, timedelta
import re
from PIL import Image, ImageChops, ImageFont, ImageDraw, ImageFilter

from io import BytesIO

from src.emoire import emoire
from src.core.classes import *
from src.core.enums import *
from src.core.time_util import *

class Listeners(commands.Cog):
    def __init__(self, bot):
        self.bot: emoire = bot

    @commands.Cog.listener("on_dropdown")
    async def on_dropdown(self, interaction: disnake.MessageInteraction):
        

        if interaction.data.values[0].split("|")[0] == "jn":
            uid = interaction.data.values[0].split("|")[1]

            if uid == "1":
                await interaction.response.send_modal(modal=join_1(self.bot, interaction, "Junior Adminstrator"))
            if uid == "2":
                await interaction.response.send_modal(modal=join_1(self.bot, interaction, "Adminstrator"))
            if uid == "3":
                await interaction.response.send_modal(modal=join_1(self.bot, interaction, "Senior Adminstrator"))

    @commands.Cog.listener("on_button_click")
    async def on_button_click(self, interaction: disnake.MessageInteraction):
        DEFAULT = 0x2F3136
        embed = disnake.Embed(
                # timestamp=datetime.now(),
                color=DEFAULT
            )
        
        if str(interaction.data.custom_id.split("|")[0]) == "start_gos":
            await interaction.response.send_modal(modal=start_gos(self.bot, interaction, "Следящего за государственной организациями"))
        if str(interaction.data.custom_id.split("|")[0]) == "start_getto":
            await interaction.response.send_modal(modal=start_gos(self.bot, interaction, "Следящего за гетто"))
        if str(interaction.data.custom_id.split("|")[0]) == "start_maffia":
            await interaction.response.send_modal(modal=start_gos(self.bot, interaction, "Следящего за мафией"))

        if str(interaction.data.custom_id.split("|")[0]) == "zauavka_yes":
        role_ids = {
            "ROLE_1": 1332438630861508661,
            "ROLE_2": 1332438630861508660,
            "ROLE_3": 1332438630861508658,
            "ROLE_4": 1332438630861508660
        }

        # Получаем объекты ролей
        roles = {name: interaction.guild.get_role(role_id) for name, role_id in role_ids.items()}

        # Проверяем, что все роли существуют
        if None in roles.values():
            missing_roles = [name for name, role in roles.items() if role is None]
            await interaction.response.send_message(
                content=f"Ошибка: Роли с ID {', '.join(str(role_ids[name]) for name in missing_roles)} не найдены.",
                ephemeral=True
            )
            return

        # Проверяем, имеет ли пользователь хотя бы одну из указанных ролей
        user_roles = [roles["ROLE_1"], roles["ROLE_2"], roles["ROLE_3"], roles["ROLE_4"]]
        if any(role in interaction.author.roles for role in user_roles):
            # Создаем новое представление с кнопкой
            view_o = PickOne(222)
            view_o.add_item(
                disnake.ui.Button(
                    style=disnake.ButtonStyle.green,
                    label=f"Рассмотрел - {interaction.author.name} | Итог - Одобрен.",
                    custom_id=f"qq",
                    disabled=True
                )
            )

            # Обновляем сообщение и отправляем ответ
            try:
                await interaction.message.edit(view=view_o)
                await interaction.response.send_message(content="Решение вынесено.", ephemeral=True)
            except Exception as e:
                await interaction.response.send_message(
                    content=f"Произошла ошибка при обновлении сообщения: {str(e)}",
                    ephemeral=True
                )
        else:
            # Если у пользователя нет необходимых ролей
            await interaction.response.send_message(
                content="У вас недостаточно прав для выполнения этого действия.",
                ephemeral=True
        )

        if str(interaction.data.custom_id.split("|")[0]) == "zauavka_no":
            ROLE_1 = interaction.guild.get_role(1332438630861508661)
            ROLE_2 = interaction.guild.get_role(1332438630861508660)
            if ROLE_1 in interaction.author.roles or ROLE_2 in interaction.author.roles:
                view_o = PickOne(222)
                view_o.add_item(disnake.ui.Button(style=disnake.ButtonStyle.green, label=f"Рассмотрел -  {interaction.author.name} | Итог - Одобрен.", custom_id=f"qq", disabled=True))
                await interaction.message.edit(view=view_o)
                await interaction.response.send_message(content="Решение вынесено.", ephemeral=True)


        if str(interaction.data.custom_id.split("|")[0]) == "afk_yes":
            ROLE_1 = interaction.guild.get_role(1332438630861508661)
            ROLE_2 = interaction.guild.get_role(1332438630861508660)
            if ROLE_1 in interaction.author.roles or ROLE_2 in interaction.author.roles:
                view_o = PickOne(222)
                view_o.add_item(disnake.ui.Button(style=disnake.ButtonStyle.green, label=f"Рассмотрел -  {interaction.author.name} | Итог - Одобрен.", custom_id=f"qq", disabled=True))
                await interaction.message.edit(view=view_o)
                await interaction.response.send_message(content="Решение вынесено.", ephemeral=True)

        if str(interaction.data.custom_id.split("|")[0]) == "afk_no":
            ROLE_1 = interaction.guild.get_role(1332438630861508661)
            ROLE_2 = interaction.guild.get_role(1332438630861508660)
            if ROLE_1 in interaction.author.roles or ROLE_2 in interaction.author.roles:
                view_o = PickOne(222)
                view_o.add_item(disnake.ui.Button(style=disnake.ButtonStyle.red, label=f"Рассмотрел -  {interaction.author.name} | Итог - Отказано.", custom_id=f"qq", disabled=True))
                await interaction.message.edit(view=view_o)
                await interaction.response.send_message(content="Решение вынесено.", ephemeral=True)

        if str(interaction.data.custom_id.split("|")[0]) == "vacation":
            await interaction.response.send_modal(modal=vacation(self.bot, interaction))
        if str(interaction.data.custom_id.split("|")[0]) == "time_off":
            await interaction.response.send_modal(modal=time_off(self.bot, interaction))

        if str(interaction.data.custom_id.split("|")[0]) == "start_shift":
            dba = await self.bot.db.select(
                "*", 
                "member_shift", 
                where={
                    "time_start": datetime.datetime.now().strftime('%Y-%m-%d'),
                    "status": True,
                    }
                )
            if dba:
                return await interaction.response.send_message(content="У вас уже открыта рабочая смена.", ephemeral=True)

            db = await self.bot.db.select(
                "*", 
                "member_shift", 
                where={
                    "time_start": datetime.datetime.now().strftime('%Y-%m-%d'),
                    }
                )
            if db:
                await self.bot.db.update({
                    "status": True,
                }, "member_shift", where={
                    "member_id": interaction.author.id,
                    "status": False,
                    "time_start": datetime.datetime.now().strftime('%Y-%m-%d'),
                })
                embed.description = f"""
                • Discord - {interaction.author.mention}
                ОТКРЫЛ РАБОЧИЮ СМЕНУ - {disnake.utils.format_dt(datetime.datetime.now(), "F")}
                """
                channel = interaction.guild.get_channel(1334067276147855430)
                await channel.send(embed=embed)
                await interaction.response.send_message(content="Рабочая смена успешно начата.", ephemeral=True)
            else:
                await self.bot.db.insert(
                    {
                        "member_id": interaction.author.id,
                        "time_start": datetime.datetime.now().strftime('%Y-%m-%d'),
                        "status": True,
                    },
                    "member_shift"
                    )
                embed.description = f"""
                • Discord - {interaction.author.mention}
                ОТКРЫЛ РАБОЧИЮ СМЕНУ - {disnake.utils.format_dt(datetime.datetime.now(), "F")}
                """
                channel = interaction.guild.get_channel(1334067276147855430)
                await channel.send(embed=embed)
                await interaction.response.send_message(content="Рабочая смена успешно начата.", ephemeral=True)

        if str(interaction.data.custom_id.split("|")[0]) == "end_shift":
            db = await self.bot.db.select(
                "*", 
                "member_shift", 
                where={
                    "time_start":  datetime.datetime.now().strftime('%Y-%m-%d'),
                    "status": True,
                    }
                )
            if db:
                await self.bot.db.update({
                    "status": False,
                }, "member_shift", where={
                    "member_id": interaction.author.id,
                    "status": True, 
                    "time_start":  datetime.datetime.now().strftime('%Y-%m-%d'),
                })
                embed.description = f"""
                • Discord - {interaction.author.mention}
                ЗАКРЫЛ РАБОЧИЮ СМЕНУ - {disnake.utils.format_dt(datetime.datetime.now(), "F")}
                РАБОЧАЯ СМЕНА СОСТАВИЛА - `{display_time(db['time_second'], full=True)}`
                """
                channel = interaction.guild.get_channel(1334067554712424479)
                await channel.send(embed=embed)
                await interaction.response.send_message(content="Рабочая смена успешно завершена.", ephemeral=True)
            else:
                await interaction.response.send_message(content="У вас нет активной рабочий смены.", ephemeral=True)
          
        if str(interaction.data.custom_id.split("|")[0]) == "fj_up_yes":
            uid = interaction.data.custom_id.split("|")[1]
            member = interaction.guild.get_member(int(uid))
            if not member:
                    member = self.bot.get_user(int(uid)) 

            # print(interaction.message.id)
            db = await self.bot.db.select(
                "*", 
                "member_up", 
                where={
                    "message_id": interaction.message.id
                    }
                )
            if db: 
                ROLE_1 = interaction.guild.get_role(1332438630861508661)
                ROLE_2 = interaction.guild.get_role(1332438630861508660)
                if ROLE_1 in interaction.author.roles or ROLE_2 in interaction.author.roles:
                    embed = disnake.Embed(color=0x32CD32)
                    content = "<@&1332438630861508661>, <@&1332438630861508660>"
                    embed.description = f"""
                    • Discord - {member.mention} повышен до `{interaction.data.custom_id.split("|")[2]}`
                    **• Рассмотрел:** - {interaction.author.mention}
                    """
                    channel = interaction.guild.get_channel(1332438632442888338)
                    await channel.send(embed=embed, content=content)
     
                    msg = await interaction.channel.fetch_message(db['message_id'])
                    await msg.edit(view=None)
                    await interaction.response.send_message(content="Решение успешно вынесено.", ephemeral=True)

        if str(interaction.data.custom_id.split("|")[0]) == "fj_up_no":
        try:
            action, uid, _, role_name = interaction.data.custom_id.split("|")
            uid = int(uid)
            role_name = role_name.strip()
            member = interaction.guild.get_member(uid) or self.bot.get_user(uid)

            if not member:
                await interaction.response.send_message(
                    content="Ошибка: Пользователь не найден.",
                    ephemeral=True
                )
                return

            db = await self.bot.db.select(
                "*",
                "member_up",
                where={"message_id": interaction.message.id}
            )

            if not db:
                await interaction.response.send_message(
                    content="Ошибка: Запись в базе данных не найдена.",
                    ephemeral=True
                )
                return

            role_ids = {
                "ROLE_1": 1332438630861508661,
                "ROLE_2": 1332438630861508660
            }
            channel_id = 1332438632442888338

            roles = {name: interaction.guild.get_role(role_id) for name, role_id in role_ids.items()}

            if None in roles.values():
                missing_roles = [name for name, role in roles.items() if role is None]
                await interaction.response.send_message(
                    content=f"Ошибка: Роли с ID {', '.join(str(role_ids[name]) for name in missing_roles)} не найдены.",
                    ephemeral=True
                )
                return

            required_roles = [roles["ROLE_1"], roles["ROLE_2"]]
            if not any(role in interaction.author.roles for role in required_roles):
                await interaction.response.send_message(
                    content="У вас недостаточно прав для выполнения этого действия.",
                    ephemeral=True
                )
                return

            embed = disnake.Embed(color=0x8B0000)
            embed.description = (
                f"• Discord - {member.mention} отказано в повышении до `{role_name}`\n"
                f"**• Рассмотрел:** {interaction.author.mention}"
            )

            channel = interaction.guild.get_channel(channel_id)

            if not channel:
                await interaction.response.send_message(
                    content="Ошибка: Канал для отправки сообщения не найден.",
                    ephemeral=True
                )
                return

            content = "<@&1332438630861508661>, <@&1332438630861508660>"
            try:
                await channel.send(content=content, embed=embed)
            except Exception as e:
                await interaction.response.send_message(
                    content=f"Произошла ошибка при отправке сообщения: {str(e)}",
                    ephemeral=True
                )
                return

            try:
                msg = await interaction.channel.fetch_message(db['message_id'])
                await msg.edit(view=None)
            except Exception as e:
                await interaction.response.send_message(
                    content=f"Произошла ошибка при редактировании сообщения: {str(e)}",
                    ephemeral=True
                )
                return

            await interaction.response.send_message(content="Решение успешно вынесено.", ephemeral=True)

        except ValueError:
            await interaction.response.send_message(
                content="Ошибка: Неверный формат `custom_id`.",
                ephemeral=True
            )
            return
                    
          
def setup(bot):
    bot.add_cog(Listeners(bot))