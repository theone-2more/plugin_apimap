# encoding:utf-8

import plugins
from bridge.context import ContextType, Context
# from bridge.reply import Reply, ReplyType
from channel.chat_message import ChatMessage
from common.log import logger
from plugins import *
from config import conf


@plugins.register(
    name="APIMap",
    desire_priority=-1,
    hidden=True,
    desc="多群聊API",
    version="0.1",
    author="theone.io",
)
class APIMap(Plugin):
    def __init__(self):
        super().__init__()
        self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
        logger.info("[APIMap] inited")

        try:
           conf = super().load_config()
           self.config = conf
           if not conf:
                raise Exception("config.json not found")
        
        except Exception as e:
            logger.warn("[GroupAPIMap] init failed, ignore ")
            raise e

    def on_handle_context(self, e_context: EventContext):
        allow_types = [
            ContextType.TEXT,
            ContextType.VOICE,
            ContextType.IMAGE,
        ]
        context: Context = e_context["context"]
        msg_type = context.get('type')
        if msg_type not in allow_types:
            return
        
        isgroup = context.get("isgroup", False)
        msg: ChatMessage = context.get("msg")

        if isgroup:
            group_confs = self.config.get('groups', [])
            group_name = msg.other_user_nickname
            # 根据 group_confs 里的 ContextType 和 name, 筛选出一个 group_conf
            match_conf = None

            for item in group_confs:
                if item.get('name') == group_name and item.get('context_type') == msg_type.value:
                    match_conf = item
                    break
            
            # 修改 context 的 model 和  openai_api_key, 等
            if match_conf:
                context['model'] = match_conf.get('model')
                context['openai_api_key'] = match_conf.get('openai_api_key')

                e_context.action = EventAction.CONTINUE
                return

        else:
            user_confs = self.config.get('private', [])
            user_name = msg.from_user_nickname
            match_conf = None

            for item in user_confs:
                if item.get('nickname') == user_name and item.get('context_type') == msg_type.value:
                    match_conf = item
                    break
            
            # 尝试 修改 context 的 model 和  openai_api_key, 等
            if match_conf:
                context['model'] = match_conf.get('model')
                context['openai_api_key'] = match_conf.get('openai_api_key')

                e_context.action = EventAction.CONTINUE
                return

    def get_help_text(self, **kwargs):
        help_text = "本插件会根据不同的群、不同的用户不同的消息类型，调用不同的API，实现不同的功能\n"
        return help_text
