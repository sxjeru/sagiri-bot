import random
from datetime import datetime

from graia.saya import Saya, Channel
from graia.ariadne.app import Ariadne
from graia.ariadne.message.element import Source, ForwardNode, Forward, Plain
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.parser.twilight import Twilight
from graia.ariadne.message.parser.twilight import FullMatch
from graia.ariadne.event.message import Group, Member, GroupMessage
from graia.saya.builtins.broadcast.schema import ListenerSchema

from sagiri_bot.core.app_core import AppCore
from statics.character_dict import character_dict
from sagiri_bot.control import FrequencyLimit, Function, BlackListControl, UserCalledCountControl

saya = Saya.current()
channel = Channel.current()

channel.name("RandomCharacter")
channel.author("SAGIRI-kawaii")
channel.description("随机生成人设插件，在群中发送 `随机人设` 即可")

core = AppCore.get_core_instance()
config = core.get_config()

@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage],
        inline_dispatchers=[Twilight([FullMatch("随机人设")])],
        decorators=[
            FrequencyLimit.require("random_character", 2),
            Function.require(channel.module, notice=True),
            BlackListControl.enable(),
            UserCalledCountControl.add(UserCalledCountControl.FUNCTIONS)
        ]
    )
)

async def random_character(app: Ariadne, message: MessageChain, group: Group, member: Member):
    forward_nodes = [
        ForwardNode(
            senderId = config.bot_qq,
            time = datetime.now(),
            senderName = "拂晓的水平线",
            messageChain = MessageChain.create([Plain(text=get_rand(member))]),
        )
    ]
    await app.sendGroupMessage(
        group,
        MessageChain.create(Forward(nodeList=forward_nodes))
    )

def get_rand(member: Member) -> str:
    s = "\n".join([f"{k}：{random.choice(character_dict[k])}" for k in character_dict.keys()])
    return member.name + ": \n" + s
