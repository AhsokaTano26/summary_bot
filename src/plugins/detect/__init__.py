import os
from nonebot import get_plugin_config, require, logger, get_driver, get_bot
from nonebot.plugin import PluginMetadata
scheduler = require("nonebot_plugin_apscheduler").scheduler
import requests
from apscheduler.triggers.cron import CronTrigger

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="detect",
    description="此插件用于检测机器人连接状态",
    usage="",
    config=Config,
)
URL = os.getenv('URL', "None")

plugin_config = get_plugin_config(Config)

@scheduler.scheduled_job(CronTrigger(minute="*/5"),misfire_grace_time=60)
async def detect():
    try:
        bot = get_bot()
        status_data = await bot.get_status()
        # 提取关键信息
        is_online = status_data.get("online", False)
        is_good = status_data.get("good", False)

        # 构造回复消息
        if is_online and is_good:
            logger.info("🟢 **OneBot 客户端运行良好，Bot 在线。**")
            requests.get(URL)
            logger.info("成功发送请求")
        elif is_online and not is_good:
            logger.warning("🟡 Bot 在线，但客户端状态可能存在异常（Good: False）。")
        else:
            logger.error("🔴 **OneBot 客户端似乎已离线或连接断开（Online: False）。**")

    except Exception as e:
        # 处理 API 调用失败的情况（例如连接已断开）
        logger.error(f"❌ 无法获取 Bot 状态，可能已下线或出现连接错误: {e}")

driver = get_driver()
@driver.on_bot_connect
async def handle_bot_connect(bot):
    # 当有新的机器人连接时触发
    plugin_config.if_connected = True
    logger.debug(f"机器人 {bot.self_id} 已连接！")
    bot = get_bot()
    await bot.call_api("send_group_msg", **{
        "group_id": plugin_config.target_groups,
        "message": f"nsybot已连接"
    })

@driver.on_bot_disconnect
async def handle_bot_disconnect(bot):
    plugin_config.if_connected = False
    logger.debug(f"机器人 {bot.self_id} 已断开连接！")