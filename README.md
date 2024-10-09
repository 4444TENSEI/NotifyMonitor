<p align="center"><img src="https://testingcf.jsdelivr.net/gh/4444TENSEI/CDN/img/avatar/AngelDog/AngelDog-rounded.png" alt="Logo"
    width="200" height="200"/></p>
<h1 align="center">NotifyWind</h1>
<h4 align="center">云函数配合Python实现HTTP定时监控同时进行消息推送。无需任何成本、轻易部署到云函数运行。支持的推送服务: 微信推送(pushplus)、系统级推送(ntfy、gotify)</h4>
<p align="center">
<img src="https://img.shields.io/badge/Python-276DC3?style=for-the-badge&logo=python&logoColor=white" />
</p>    



</p>

<br/>

<hr/>

# 暂时没力气写较为详细的文档，先记点配置参数中要注意的地方

`monitor`中的`ip`和url块：

- 可以为自己的多个服务增加多组键值对，键名可以自定义，值是服务器具体的IP地址。

无需改动的地方：

- pushplus的`url`，毕竟只能用官方服务。
- `gotify`目前只支持`post`方式，故配置文件中的`method`**保持目前这样即可**

`priority`（消息推送的重要程度数值）：

- `ntfy`的`priority`设置为`5`手机端收到通知会发出系统铃声，可以往小点改，完整范围是0-5。
- `gotify`的`priority`设置为`8-10`范围手机端收到通知会发出系统铃声，可以往小点改，完整范围是0、1-3、4-7、8-10。

`onlyError`（仅在有服务掉线时发起通知推送）：

- 设置为true后：仅在出错时，对于出错的服务发起消息推送通知，建议开启、避免高频率的推送。

# 建议使用`华为云函数`部署

环境变量文件示例`variable.json`，已经位于项目根目录下了：

```json
{
    "monitor": {
        "ip": {
            "服务器IP": "123.123.123.123",
            "键名可以自定义作为备注": "321.321.321.321",
            "键值对可以是多个": "255.255.255.233"
        },
        "url": {
            "后端服务地址": "http://meow.meow.meow",
            "键名可以自定义作为备注": "http://aaa.com",
            "键值对可以是多个": "http://ddd.eee.com"
        }
    },
    "pushService": {
        "pushplus": {
            "url": "https://www.pushplus.plus",
            "token": "上方官方服务url是固定的, 不要改, 此处填申请到的TOKEN",
            "method": "get"
        },
        "ntfy": {
            "url": "https://ntfy.example.com/test",
            "token": "上方url后缀需要有你的订阅主题端点, 然后如果你没配置权限访问, 可以删掉这组键值对。下方priority设置为4刚刚好, 如果设置为5会发出系统铃声",
            "priority": 4,
            "method": "post"
        },
        "gotify": {
            "url": "https://gotify.example.com",
            "token": "在gotify服务页面右上角APPS处创建新的主题, 复制主题token到此, 注意点在于目前只支持post方式推送消息故下方method不要动, priority设置为7刚刚好, 如果设置为8-10会发出系统铃声",
            "priority": 7,
            "method": "post"
        }
    },
    "onlyError": false
}
```
