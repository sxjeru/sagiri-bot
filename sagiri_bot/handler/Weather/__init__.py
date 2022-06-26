from graia.saya import Saya, Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.event.message import Group, Member, GroupMessage
from graia.ariadne.event.mirai import *
# from graia.ariadne.message.parser.kanata import Kanata
# from graia.ariadne.message.parser.signature import RegexMatch
# from graia.ariadne import GraiaMiraiApplication
from graia.ariadne.message.element import Plain, At, ForwardNode, Forward
# from graia.ariadne import session
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.app import Ariadne

from sagiri_bot.decorators import switch, blacklist
from sagiri_bot.handler.handler import AbstractHandler
from sagiri_bot.message_sender.message_item import MessageItem
from sagiri_bot.message_sender.message_sender import MessageSender
from sagiri_bot.control import FrequencyLimit, Function, BlackListControl, UserCalledCountControl
from sagiri_bot.core.app_core import AppCore


import re
from datetime import datetime
from .utils import text2params, get_weather
from .config import TIME


# 插件信息
__name__ = "Weather"
__description__ = "和风天气插件"
__author__ = "Roc"
__usage__ = (
    "发送 地区+时间+\"(详细)天气(预报)\"即可，如“北京近三天天气(预报)”或“北京近三天详细天气(预报)”\n"
    f"目前已支持大部分城市，支持的时间包括:{ [*TIME.keys(), *set(TIME.values())] }"
)


saya = Saya.current()
channel = Channel.current()

channel.name(__name__)
channel.description(f"{__description__}\n使用方法：{__usage__}")
channel.author(__author__)

core = AppCore.get_core_instance()
config = core.get_config()

@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def weather(app: Ariadne, message: MessageChain, group: Group, member: Member):
    if result := await Weather.handle(app, message, group, member):
        await MessageSender(result.strategy).send(app, result.message, message, group, member)

class Weather(AbstractHandler):
    @staticmethod
    @switch()
    @blacklist()
    async def handle(app: Ariadne, message: MessageChain, member: Member, group: Group):
        if re.fullmatch(r"(.*?)(天气预报|天气)", message.asDisplay()):
            if message.asDisplay() == "天气预报" or message.asDisplay() == "天气":
                reply = f"{__description__}\n使用方法：{__usage__}"
            else:
                city, time, flag = text2params(message.asDisplay())
                reply = get_weather(city, time, flag)
            # msg = MessageChain.create([At(member.id), Plain(' ' + reply)])
            # msg = MessageChain.create([Plain(reply)])
            forward_nodes = [
                ForwardNode(
                    senderId = config.bot_qq,
                    time = datetime.now(),
                    senderName = "拂晓的水平线",
                    messageChain = MessageChain.create([Plain(reply)]),
                )
            ]
            await app.sendGroupMessage(
                group,
                MessageChain.create(Forward(nodeList=forward_nodes))
            )
            # try:
            # return MessageItem(msg, QuoteSource())
                # await app.sendGroupMessage(
                #     group, msg
                # )
            # except AccountMuted:
            #     pass