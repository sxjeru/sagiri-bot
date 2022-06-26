import re
import random
from datetime import datetime

from graia.saya import Saya, Channel
from graia.ariadne.app import Ariadne
from graia.ariadne.message.element import Plain
from graia.ariadne.message.chain import MessageChain
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.event.message import Group, Member, GroupMessage

from sagiri_bot.decorators import switch, blacklist
from sagiri_bot.handler.handler import AbstractHandler
from sagiri_bot.message_sender.message_item import MessageItem
from sagiri_bot.message_sender.message_sender import MessageSender
from sagiri_bot.message_sender.strategy import QuoteSource, Normal


saya = Saya.current()
channel = Channel.current()

channel.name("jrrp")
channel.author("sxjeru")
channel.description("发送 '.jrrp' 以获取今日人品")

@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def jrrp(app: Ariadne, message: MessageChain, group: Group, member: Member):
    if result := await jrrp.handle(app, message, group, member):
        await MessageSender(result.strategy).send(app, result.message, message, group, member)

class jrrp(AbstractHandler):
    @staticmethod
    @switch()
    @blacklist()
    async def handle(app: Ariadne, message: MessageChain, group: Group, member: Member):
        if re.match(r"(\.|。)jrrp", message.asDisplay()):
            random.seed(int(datetime.today().strftime('%Y%m%d') + str(member.id) + str(group.id if group else 0)))
            rndnum = str(random.randint(0, 100))
            result = '[' + member.name + ']' + "你的今日人品为：" + rndnum
            return MessageItem(
                MessageChain.create([Plain(text=result)]), Normal()
            )
