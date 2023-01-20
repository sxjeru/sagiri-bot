import requests as r
from graia.saya import Saya, Channel
from graia.ariadne.app import Ariadne
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.parser.twilight import Twilight
from graia.ariadne.event.message import Group, GroupMessage
from graia.ariadne.message.parser.twilight import FullMatch, RegexMatch, RegexResult
from graia.ariadne.message.element import Plain
from sagiri_bot.control import FrequencyLimit, Function, BlackListControl, UserCalledCountControl

saya = Saya.current()
channel = Channel.current()

channel.name("chatgpt")
channel.author("sxjeru")
channel.description("发送 /chat+内容，即可与机器人聊天")

@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage],
        inline_dispatchers=[Twilight([FullMatch("/chat "), RegexMatch(r".+") @ "content"])],
        decorators=[
            FrequencyLimit.require("chatgpt", 2),
            Function.require(channel.module, notice=True),
            BlackListControl.enable(),
            UserCalledCountControl.add(UserCalledCountControl.FUNCTIONS)
        ]
    )
)
async def chatgpt(app: Ariadne, group: Group, content: RegexResult):
    content=content.result.asDisplay()
    # print(content)
    url = "https://v1.gptapi.cn"
    data = {"message": content}
    res = r.post(url, json=data)
    await app.sendGroupMessage(group, MessageChain.create([Plain(res.text)]))