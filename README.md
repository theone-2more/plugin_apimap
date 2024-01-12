## 插件说明

api 根据不同的群名、不同的人而变化

## 适用场景

如 fastgpt 中，即可利用不同的群，使用不懂的 openai_api_key 来实现不同的功能。

## 插件使用

将`config.json.template`复制为`config.json`。

- groups: 群组配置
- private: 私聊配置
- context_type: 信息类型，参考 bridge/context.py
- name: 群名称
- nickname: 发送人配置
- model: 模型名称
- openai_api_key: 对应的 api key


```
[INFO][2024-01-12 11:34:09][apimap.py:24] - [APIMap] inited
```

