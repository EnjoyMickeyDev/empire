import time
import disnake

from datetime import datetime
from enum import IntEnum, Enum
from PIL import Image, ImageChops, ImageFont, ImageDraw, ImageFilter


def unix_time():
    return int(datetime.utcnow().timestamp())

class ROLE_SERVER(IntEnum):
    AUTOROLE = 1301172276166656020
    LIDER = 1301169881571655751
    ZAM = 1301170347264970762
    FAMILY = 1291799098864828447
    FREND = 1303109825332248688

class CHANNEL_SERVER(IntEnum):
    FORUM = 1303613591005564980
    ZAEVKA = 1301165911209676820

mask_welcome = Image.new('L', (1002, 1002), 0)
draws = ImageDraw.Draw(mask_welcome)
draws.ellipse((0, 0) + (1002, 1002), fill=255)
mask_welcome = mask_welcome.resize((248, 248), Image.ANTIALIAS)

chech_button_time = {}
cached_voice_joins = {}

top_dict = {
    "lvl": 'xp',
    "money": 'money',
    "messages": "message",
    "voice": "voice"
}

def chech_time(cd, member_id: int):
    if not member_id in chech_button_time:
        chech_button_time.update({member_id: time.time()})
        return True, 0
    else:
        member_data = chech_button_time[member_id]
        time_click = time.time() - member_data

        if time_click > cd:
            chech_button_time.update({member_id: time.time()})
            return True
        else:
            return False, cd - int(time_click)

class TimeEnum(int, Enum):
    SECOND = 1
    MINUTE = 60
    HOUR = 60 * 60
    DAY = 60 * 60 * 24
    WEEK = 60 * 60 * 24 * 30
    YEAR = 60 * 60 * 24 * 30 * 12

DISPLAYABLE_TIME = (
    TimeEnum.HOUR,
    TimeEnum.MINUTE,
    TimeEnum.SECOND,
)
    
def display_time(
    seconds: float,
    granularity: int = 3,
    full: bool = False
) -> str:
    if seconds == 0:
        return '0'

    result = []

    for item in DISPLAYABLE_TIME:
        name, count = item.localizable_name(), item.value
        value = int(seconds // count)
        if value:
            seconds -= value * count
            if full:
                result.append(f"{value} {name}")
            else:
                result.append(f"{value}{name[:1]}")
    return ' '.join(result[:granularity])

async def created_private_room(member: disnake.Member, after=None):

    overwrites = {
        member.guild.default_role: disnake.PermissionOverwrite.from_pair(
            disnake.Permissions(
                permissions=36701696),
            disnake.Permissions(permissions=0)
        ),
        member: disnake.PermissionOverwrite.from_pair(
            disnake.Permissions(
                permissions=16),
            disnake.Permissions(permissions=0)
        )
    }
    
    room_channel = await member.guild.create_voice_channel(
        name=member.name,
        category=after.channel.category,
        overwrites=overwrites,
        user_limit=0,
        reason="GuildAutoRoom -> CreateRoom"
    )   

    await member.edit(
        voice_channel=room_channel,
        reason="GuildAutoRoom -> RoomEditMember"
    )
async def check_room_voice(member: disnake.member, channel: disnake.channel):
    if not (channel.category and channel.category_id == 1303636288569868298 and channel.id != 1303636499207688193 and len(channel.members) == 0):
            return

    await channel.delete(reason="GuildAutoRoom -> RoomDelete")

mask_top = Image.new('L', (165, 165), 0)
draws_top = ImageDraw.Draw(mask_top)
draws_top.ellipse((0, 0) + (165, 165), fill=255)
mask_top = mask_top.resize((165, 165), Image.ANTIALIAS)

mask_top_back = Image.new('L', (549, 549), 0)
draws_top_back = ImageDraw.Draw(mask_top_back)
draws_top_back.rectangle((274, 0) + (374, 549), fill=255)
mask_top_back = mask_top_back.resize((549, 549), Image.ANTIALIAS)
