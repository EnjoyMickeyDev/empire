import disnake
from disnake.ext import commands
from datetime import datetime
import re
from io import BytesIO
from src.emoire import emoire
from src.core.classes import PickOne
from src.core.enums import *
from src.core.time_util import *

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot: emoire = bot
    
    @commands.slash_command(name='post_up')
    @commands.has_permissions(administrator=True)
    async def post_up(self, interaction: disnake.GuildCommandInteraction):
        await interaction.response.defer()
        DEFAULT = 0x36393e
        embed = disnake.Embed(
                color=DEFAULT
            )
        embed.set_image(url="https://media.discordapp.net/attachments/1333838836614299770/1333864254431826024/ima3ge.png?ex=679a7164&is=67991fe4&hm=73aaaf06c9c4f657632deba942d22de88f97d250ddb86f76bcd069485f53c8c8&=&format=webp&quality=lossless&width=1348&height=676")
        options = [
            disnake.SelectOption(
                label='Helper -> Junior Adminstrator', 
                # description=f'Подать заявку как сотрудник LSPD', 
                value="jn|1",
            ),
            disnake.SelectOption(
                label='Junior Adminstrator -> Adminstrator', 
                # description=f'Подать заявку как сотрудник LSPD', 
                value="jn|2",
            ),
            disnake.SelectOption(
                label='Adminstrator -> Senior Administrator', 
                # description=f'Подать заявку как сотрудник LSPD', 
                value="jn|3",
            ),
        ]

        select = disnake.ui.Select(
            placeholder="Подать заявку",
            options=options
        )
#         context = """
# Что-ж, давай расскажу о нашей государственной семье **Shigeru**, которая находится в штате Dallas. Наша семья очень вайбовая и многие члены семьи работают в различных организациях, таких как FIB, SD, LSPD и SANG. Мы все равно смогли создать уникальную атмосферу поддержки и взаимопомощи, считая друг друга единомышленниками. Каждый член нашей семьи важен для нас, и это придаёт нам особую силу и согласие.\n
# В Shigeru мы придерживаемся принципов дружбы, доверия и уважения. Наша семья всегда открыта для новых лиц, и мы рады каждому, кто хочет стать частью нашего большого и дружного сообщества. Каждое новое знакомство обогащает нашу семью, добавляя новые краски в уже яркую палитру. Мы уверены, что вместе мы сможем преодолеть любые трудности и достичь успехов в каждой области, где представляем наши интересы.
#         """
        channel = interaction.guild.get_channel(int(1332438632442888337))
        await channel.send(
            embed=embed,
            components=[select]
        ) 
        await interaction.send("успешно", ephemeral=True)

    @commands.slash_command(name='post_afk')
    @commands.has_permissions(administrator=True)
    async def post_afk(self, interaction: disnake.GuildCommandInteraction):
        await interaction.response.defer()
        DEFAULT = 0x36393e
        embed = disnake.Embed(
                color=DEFAULT
            )
        view = PickOne(interaction.author.id)
        view.add_item(disnake.ui.Button(style=disnake.ButtonStyle.blurple, label="ㅤㅤㅤВзять отпускㅤㅤㅤ", custom_id=f"vacation"))
        view.add_item(disnake.ui.Button(style=disnake.ButtonStyle.blurple, label="ㅤㅤㅤВзять отгул ㅤㅤㅤ", custom_id=f"time_off"))

        channel = interaction.guild.get_channel(int(1332438632744620151))
        await channel.send(
            # embed=embed,
            view=view
        ) 
        await interaction.send("успешно", ephemeral=True)

    @commands.slash_command(name='post_shift')
    @commands.has_permissions(administrator=True)
    async def post_contract(self, interaction: disnake.GuildCommandInteraction):
        await interaction.response.defer()
        DEFAULT = 0x2F3136
        
        embed = disnake.Embed(
                color=DEFAULT
            )
        embed.set_image(url="https://media.discordapp.net/attachments/1333838836614299770/1333864255988170772/ima1213123ge.png?ex=679a7164&is=67991fe4&hm=cd3ae191472112409c42819d062bd7876adad5bd3f2efa1117140bb9f82b6047&=&format=webp&quality=lossless&width=1348&height=676")
        view = PickOne(interaction.author.id)
        view.add_item(disnake.ui.Button(style=disnake.ButtonStyle.green, label="ㅤㅤㅤНачать сменуㅤㅤㅤ", custom_id=f"start_shift"))
        view.add_item(disnake.ui.Button(style=disnake.ButtonStyle.red, label="ㅤㅤㅤЗакончить сменуㅤㅤㅤ", custom_id=f"end_shift"))

        channel = interaction.guild.get_channel(int(1332438632744620149))
        await channel.send(
            embed=embed,
            view=view
        ) 
        await interaction.send("успешно", ephemeral=True)

    @commands.slash_command(name='post_tracker')
    @commands.has_permissions(administrator=True)
    async def post_tracker(self, interaction: disnake.GuildCommandInteraction):
        await interaction.response.defer()
        DEFAULT = 0x2F3136
        
        embed = disnake.Embed(
                color=DEFAULT
            )
        embed.set_image(url="https://media.discordapp.net/attachments/1333838836614299770/1333864313848336457/image.png")
        channel_gos = interaction.guild.get_channel(int(1332438632744620145))
        if channel_gos:
            # embed.set_image(url="https://")
            view = PickOne(interaction.author.id)
            view.add_item(disnake.ui.Button(style=disnake.ButtonStyle.green, label="ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤПодать заявкуㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ", custom_id=f"start_gos"))
            await channel_gos.send(embed=embed, view=view) 

        channel_getto = interaction.guild.get_channel(int(1332438632744620146))
        if channel_getto:
            view = PickOne(interaction.author.id)
            view.add_item(disnake.ui.Button(style=disnake.ButtonStyle.green, label="ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤПодать заявкуㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ", custom_id=f"start_getto"))
            await channel_getto.send(embed=embed, view=view) 

        channel_maffia = interaction.guild.get_channel(int(1332438632744620147))
        if channel_maffia:
            # embed.set_image(url="https://")
            view = PickOne(interaction.author.id)
            view.add_item(disnake.ui.Button(style=disnake.ButtonStyle.green, label="ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤПодать заявкуㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ", custom_id=f"start_maffia"))
            await channel_maffia.send(embed=embed, view=view) 
 

    @commands.slash_command(name='activity')
    @commands.has_permissions(administrator=True)
    async def activity(self, interaction: disnake.GuildCommandInteraction, member: disnake.Member):
        await interaction.response.defer()
        embed = disnake.Embed(color=0x00BFFF)

        data = await self.bot.db.select_all(
                "*", 
                "member_shift", 
            where={
                "status": False,
                # "time_start": datetime.datetime.now().strftime('%Y-%m-%d'), 
                "member_id": member.id
                }
            )  
        if not data:
            return await interaction.send(content="Рабочих смен не обнаружено", ephemeral=True, delete_after=10)
        
        history = []
        for row in data:
     
            # print(row)
            # print(22, disnake.utils.format_dt(datetime.timestamp(row['time_start']), 'F')) (row['time_start'].timestamp()
            history.append(f"• <t:{int(row['time_start'].timestamp())}:d> - Отработано: `{display_time(row['time_second'], full=True)}`\n")
            embed.description = f"""
                # **ИСТОРИЯ АКТИВНОСТИ** 
                Discord - <@{row['member_id']}> 

                {" ".join(history)}
            
                """[:4000]
   
        return await interaction.send(embed=embed, delete_after=60)
    

    @commands.slash_command(name='sql')
    @commands.has_permissions(administrator=True)
    async def sql(
        self, 
        interaction: disnake.GuildCommandInteraction, 
        query: str
    ):  
        embed = disnake.Embed()
        try:
            resp = await self.bot.db.fetchrow(query)
            if not resp:
                resp = {}
        except Exception as e:
            await interaction.send("Не правильный запрос.")
            return

        embeds = []

        for key, value in resp.items():
            if len(embed.fields) == 25:
                embeds.append(embed)
            value = f"'{value}'" if isinstance(value, str) else str(value)
            embed.add_field(
                name=key,
                value=value,
                inline=True
            )
        if len(embed.fields) != 25:
            embeds.append(embed)

        embeds[0].description = query


        await interaction.send(embeds=embeds)
        # return
    
    
def setup(bot):
    bot.add_cog(Admin(bot))