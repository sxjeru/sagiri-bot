import requests
import re

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

channel.name("mcmod_state")
channel.author("sxjeru")
channel.description("发送'/mcmod'以获取百科服务器状态")

@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def state(app: Ariadne, message: MessageChain, group: Group, member: Member):
    if result := await state.handle(app, message, group, member):
        await MessageSender(result.strategy).send(app, result.message, message, group, member)


class state(AbstractHandler):
    @staticmethod
    @switch()
    async def handle(app: Ariadne, message: MessageChain, group: Group, member: Member):
        if message.asDisplay() == '/mcmod':
            proxies = {"http": None, "https": None}
            url = 'https://openapi.nekochocolate.space:8443/WebsiteTest.php'
            rq = requests.get(url, proxies=proxies)
            m = re.search(r"静态网页测试:", rq.text)
            if(rq.text[m.end():m.end()+3] == '200' and rq.text[m.end()+15:m.end()+18] == '200'):
                result = "√ 喵呜机正在飞速运转ing——"
            else:
                result = "× 啊，百科服务器可能挂了呢，请速速通知重生喵！"
            return MessageItem(
                MessageChain.create([Plain(text=result)]), QuoteSource()
            )