<p align="center"><img src="https://testingcf.jsdelivr.net/gh/4444TENSEI/CDN/img/avatar/AngelDog/AngelDog-rounded.png" alt="Logo"
    width="200" height="200"/></p>
<h1 align="center">NotifyMonitor</h1>
<h4 align="center">云函数配合Python实现HTTP定时监控同时进行消息推送。无需任何成本轻易部署。支持的推送服务: 微信推送(pushplus)、系统级推送(ntfy、gotify)</h4>
<p align="center">
<img src="https://img.shields.io/badge/Python-276DC3?style=for-the-badge&logo=python&logoColor=white" />
</p>    



</p>

<br/>

<hr/>

> # 部署到`华为云函数`

> 打个广告：**本项目**的**消息推送**功能依赖**NotifyWind**插件化实现，[点击前往项目仓库](https://github.com/4444TENSEI/NotifyWind)（一个就算集成到已有项目也非常便捷的消息推送SDK）

### 具体部署步骤：

1. 拉取项目源码或者是直接在[最新发行版版](https://github.com/4444TENSEI/NotifyMonitor/releases/latest)下载最新版源码的`ZIP压缩包`，用于上传到华为云函数
2. 查看本项目作者所写的**部署教程**：[华为云函数部署Python定时任务](https://blog.yokaze.top/archives/930)，
3. 需要在**环境变量**中配置`键`为`NOTIFYWIND`，`值`就是下方json配置文件中的内容，关键部位自行修改

### **环境变量**内容示例，位于项目根目录下`example.notifywind.json`，内容如下：

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
    "NotifyWind": {
        "pushplus": {
            "token": "xxxxxxxxxxxxxxxxxxxx"
        },
        "ntfy": {
            "server_url": "https://example.com",
            "token": "xxxxxxxxxxxxxxxxxxxx",
            "priority": 4
        },
        "gotify": {
            "server_url": "https://example.com",
            "token": "xxxxxxxxxxxxxxxxxxxx",
            "priority": 8
        }
    }
    "onlyError": false
}
```

> ## 环境变量中的注意事项

### `monitor`中的`ip`和`url`块：

- 可以为自己的多个服务增加**多组**键值对，键名可以自定义，值是服务器具体的IP地址。

### `priority`（消息推送的重要程度数值）：

- `ntfy`的`priority`设置为`5`手机端收到通知会发出系统铃声，可以往小点改，完整范围是0-5。
- `gotify`的`priority`设置为`8-10`范围手机端收到通知会发出系统铃声，可以往小点改，完整范围是0、1-3、4-7、8-10。

### `onlyError`（仅在有服务掉线时发起通知推送）：

- 设置为`true`后：**仅在由服务掉线时**对于出错的服务发起消息推送通知，建议开启、避免高频率的推送。
