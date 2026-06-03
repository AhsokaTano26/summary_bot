import datetime
import os
import re
import jieba
from apscheduler.triggers.cron import CronTrigger
from nonebot import get_plugin_config, on_message, get_bot
from nonebot.adapters.onebot.v11 import GroupMessageEvent
from nonebot.plugin import PluginMetadata, on_command
from nonebot_plugin_apscheduler import scheduler
from nonebot_plugin_orm import get_session
from snownlp import SnowNLP
from nonebot.log import logger

from .config import Config
from .encrypt import encrypt
from .models import Detail
from .models_method import DetailManger, ClipManger, HistoryManger
from .function import Clip, summary_top_10, summary_top_3, History, llm_summary

__plugin_meta__ = PluginMetadata(
    name="summary_bot",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)


collector = on_message()
@collector.handle()
async def collect_message(event: GroupMessageEvent):
    if not event.message.extract_plain_text():
        return
    if event.group_id not in config.target_group:
        return
    if event.user_id in config.ignore_users:
        return
    group_id = event.group_id
    user_id = event.user_id
    plain_text = re.sub(r"\[CQ:at,qq=\d+]|https?://\S+", "", event.message.extract_plain_text())
    id_msg = str(group_id) + str(user_id) + plain_text + str(datetime.datetime.now())
    id = await encrypt(id_msg)
    sentiment = SnowNLP(plain_text).sentiments
    clip = jieba.lcut(plain_text)
    str_clip = str(clip)
    async with (get_session() as db_session):
        try:
            async with (get_session() as db_session):
                existing_lanmsg = await DetailManger.get_Sign_by_student_id(
                    db_session, id)
                if existing_lanmsg:
                    logger.info(f"该 {id} 信息已存在")
                else:
                    await DetailManger.create_signmsg(
                        db_session,
                        id=id,
                        group_id=group_id,
                        user_id=user_id,
                        updated=datetime.datetime.now(),
                        clip=str_clip,
                        text=plain_text,
                        sentiment=sentiment
                    )
        except Exception as e:
            logger.error(f"创建 {id} 信息时出错: {e}")
    await Clip(clip,group_id)

cmd = on_command("今日总结",aliases={"<UNK>"})
@cmd.handle()
async def summary(event: GroupMessageEvent):
    group_id = event.group_id
    try:
        async with (get_session() as db_session):
            await DetailManger.is_database_empty(db_session)
            if await DetailManger.is_database_empty(db_session):
                await cmd.send("无聊天记录")
            else:
                msg = await summary_top_10(group_id)
                await cmd.send(msg)
                # 发送 LLM 语义总结
                llm_msg = await llm_summary(group_id)
                if llm_msg:
                    await cmd.send(llm_msg)
    except Exception as e:
        logger.error(f"创建信息时出错: {e}")


@scheduler.scheduled_job(CronTrigger(hour=23, minute=55), misfire_grace_time=60)
async def senf_summary():
    logger.success(f"开始执行定时任务")
    bot = get_bot()
    try:
        await History()
        logger.info(f"创建历史信息成功")
    except Exception as e:
        logger.error(f"创建历史信息时出错: {e}")

    # 发送详细结果到指定群
    detail_group = config.detail_group
    for group_id in config.target_group:
        try:
            async with (get_session() as db_session):
                await DetailManger.is_database_empty(db_session)
                if await DetailManger.is_database_empty(db_session):
                    await bot.call_api("send_group_msg",group_id=group_id,message="无聊天记录")
                else:
                    msg = await summary_top_10(group_id)
                    mmsg = ""
                    for i in msg:
                        mmsg += i
                    await bot.call_api("send_group_msg", group_id=group_id, message=mmsg)
                    # 发送 LLM 语义总结
                    llm_msg = await llm_summary(group_id)
                    if llm_msg:
                        await bot.call_api("send_group_msg", group_id=group_id, message=llm_msg)
                logger.info(f"发送 {group_id} 信息成功")
        except Exception as e:
            logger.error(f"创建信息时出错: {e}")

    # 清理 daily_summary 图片
    try:
        summary_dir = "data/daily_summary"
        if os.path.exists(summary_dir):
            for filename in os.listdir(summary_dir):
                file_path = os.path.join(summary_dir, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            logger.info(f"清理 {summary_dir} 图片成功")
    except Exception as e:
        logger.error(f"清理图片时出错: {e}")

    try:
        async with (get_session() as db_session):
            await ClipManger.delete_all_student_id(db_session)
            logger.info(f"删除所有Clip信息成功")
            await DetailManger.delete_all_student_id(db_session)
            logger.info(f"删除所有Detail信息成功")
    except Exception as e:
        logger.error(f"删除所有信息时出错: {e}")