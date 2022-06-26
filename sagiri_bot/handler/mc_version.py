import time
import json
from urllib.request import urlopen

import aiohttp
import asyncio
from graia.saya import Saya, Channel
from graia.ariadne.app import Ariadne
from graia.ariadne.model import Group
from graia.scheduler.saya.schema import SchedulerSchema
from graia.scheduler.timers import crontabify
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.parser.twilight import Twilight, FullMatch
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Plain
from sagiri_bot.utils import group_setting
from sagiri_bot.orm.async_orm import Setting

saya = Saya.current()
channel = Channel.current()

channel.name("mcver")
channel.author("sxjeru")
channel.description("间隔 5 分钟跟踪一次 mc 版本\n输入 /mcver 可获取当前最新版本号")

# 获取初值
with urlopen('https://launchermeta.mojang.com/mc/game/version_manifest.json') as resp:
    data = json.load(resp)
    r=data['latest']['release']
    s=data['latest']['snapshot']

def getTime(id):
    for i in range(0,100):
        if id==data['versions'][i]['id']:
            time=data['versions'][i]['releaseTime']
            h=str((int(time[11:13])+8)%24)
            if len(h)==1:
                h='0'+h
            return time[0:10]+' '+h+time[13:19]

@channel.use(SchedulerSchema(crontabify("*/5 * * * *")))
async def mcver_scheduled(app: Ariadne):
    await mcverGet(app)

async def mcverGet(app: Ariadne):
    global data
    # with urlopen('https://file.sxjeru.top/version_manifest.json') as resp:
    with urlopen('https://launchermeta.mojang.com/mc/game/version_manifest.json') as resp:
        data = json.load(resp)
    rl=data['latest']['release']
    ss=data['latest']['snapshot']
    global r
    global s
    f=False
    if rl!=r:
        r=rl
        f=True
        for group in await app.getGroupList():
            if not await group_setting.get_setting(group, Setting.daily_newspaper):
                continue
            await app.sendMessage(group,MessageChain([Plain(f'Minecraft 有新的 正式版本 发布了！\n\n游戏版本：{r}\n发布时间：{getTime(r)}')]))
    if f:
        s=ss
        f=False
    if ss!=s:
        s=ss
        for group in await app.getGroupList():
            if not await group_setting.get_setting(group, Setting.daily_newspaper):
                continue
            await app.sendMessage(group,MessageChain([Plain(f'Minecraft 有新的 快照版本 发布了！\n\n游戏版本：{s}\n发布时间：{getTime(s)}')]))

@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage],
        inline_dispatchers=[Twilight([FullMatch("/mcver")])]
    )
)
async def main(app: Ariadne, group: Group):
    await app.sendMessage(group, MessageChain([Plain(f"Minecraft 最新版本现况如下：\n正式版本：{r}\n发布时间：{getTime(r)}\n快照版本：{s}\n发布时间：{getTime(s)}")]))


# with urlopen('https://launchermeta.mojang.com/mc/game/version_manifest.json') as resp:
#     data = json.load(resp)
# rl=data['latest']['release']
# ss=data['latest']['snapshot']
# for i in range(0,100):
#     if rl==data['versions'][i]['id']:
#         time=data['versions'][i]['releaseTime']
#         h=str((int(time[11:13])+8)%24)
#         if len(h)==1:
#             h='0'+h
#         print(time[0:10]+' '+h+time[13:19])

# print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

# with open('version_manifest.json') as f:
#     data = json.load(f)
#     print(data['versions'][0]['id'])
