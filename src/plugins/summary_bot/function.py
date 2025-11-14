import datetime
import os
import jieba
import jieba.analyse
from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageSegment
from nonebot_plugin_orm import get_session
from nonebot.log import logger
from wordcloud import WordCloud

from .config import Config
from .encrypt import encrypt
from .models import Detail
from .models_method import DetailManger, ClipManger, HistoryManger

ignore_word = ["的","了","在","是","我","你","他","她","?","，","。","、","！","？","（","）","【","】","；",
               "：","“","”","‘","’","《","》","……","·","—","…","…"," "]
FONT_PATH = "fonts/simfang.ttf"
RESOURCES_DIR = "data/daily_summary"
async def Clip(dic,group_id):
    async with (get_session() as db_session):
        for i in dic:
            if i in ignore_word:
                continue
            id_text = str(group_id) + i
            id = await encrypt(id_text)
            existing_lanmsg = await ClipManger.get_Sign_by_student_id(
                db_session, id)
            if existing_lanmsg:
                logger.info(f"该 {id} 信息已存在")
                frequence = int(existing_lanmsg.frequency) + 1
                try:
                    await ClipManger.delete_id(db_session, id)
                    logger.info(f"删除 {id} 信息成功")
                    await ClipManger.create_signmsg(
                        db_session,
                        id=id,
                        group_id=group_id,
                        word=i,
                        frequency=frequence,
                    )
                    logger.info(f"创建 {id} 信息成功")
                except Exception as e:
                    logger.error(f"创建 {id} 信息失败: {e}")
            else:
                try:
                    await ClipManger.create_signmsg(
                        db_session,
                        id=id,
                        group_id=group_id,
                        word=i,
                        frequency=1,
                    )
                    logger.info(f"创建 {id} 信息成功")
                except Exception as e:
                    logger.error(f"创建 {id} 信息失败: {e}")


async def summary_top_10(group_id):
    async with (get_session() as db_session):
        full_text = ""
        sheet = await DetailManger.get_all_student_id(db_session)
        for id in sheet:
            lanmsg = await DetailManger.get_Sign_by_student_id(db_session, id)
            if int(lanmsg.group_id) == group_id:
                full_text += lanmsg.text + "\n"
        # 提取热词
        keywords = jieba.analyse.extract_tags(
            full_text,
            topK=20,
            withWeight=True,
            allowPOS=("n", "nt", "vn", "nz", "v", "nr", "ns", "nt")
        )
        word_freq = {word: weight for word, weight in keywords if word not in ignore_word}
        topics = jieba.analyse.textrank(full_text, topK=3, withWeight=False)
        # 生成词云
        wc = WordCloud(
            font_path=FONT_PATH,
            width=800,
            height=600,
            background_color="white"
        ).generate_from_frequencies(word_freq)
        avg_sentiment = await avg_group_sentiment()
        image_path = os.path.join(RESOURCES_DIR, f"{avg_sentiment}+{datetime.datetime.now():%Y%m%d}.png")
        wc.to_file(image_path)
        with open(image_path, "rb") as f:
            image_data = f.read()
        result = [
            f"📅 今日群聊分析报告（情感值: {avg_sentiment}）"+"\n",
            f"🔥 热门话题: {' '.join(topics)}"+"\n",
            "📌 今日热词榜："+"\n",
            *[f"{i + 1}. {word} ({weight:.2f}) "+"\n" for i, (word, weight) in enumerate(keywords[:10])],
            MessageSegment.image(image_data)
        ]
        return result

async def summary_top_3():
    async with (get_session() as db_session):
        summary = {}
        sheet = await ClipManger.get_all_student_id(db_session)
        dic = await ClipManger.get_top_3_words(db_session)
        totle = 0
        message = ""
        for id in sheet:
            lanmsg = await ClipManger.get_Sign_by_student_id(db_session, id)
            totle += int(lanmsg.frequency)
        for id in sheet:
            lanmsg = await ClipManger.get_Sign_by_student_id(db_session, id)
            for i in dic:
                if lanmsg.word == i:
                    summary[i] = format(int(lanmsg.frequency) / totle, '.3f')
        for i in summary:
            message += i + " " + summary[i] + "\n"
        avg_sentiment = await avg_group_sentiment()
        result = f"📅 今日群聊分析报告（情感值: {avg_sentiment}）\n📌 今日热词榜：\n{message}"
        return result

async def avg_group_sentiment():
    total = 0
    sentiment = 0
    async with (get_session() as db_session):
        sheet = await DetailManger.get_all_student_id(db_session)
        for id in sheet:
            lanmsg = await DetailManger.get_Sign_by_student_id(db_session, id)
            sentiment += float(lanmsg.sentiment)
            total += 1
        avg_sentiment = format(sentiment / total, '.3f')
        return avg_sentiment

async def History():
    async with (get_session() as db_session):
        sheet = await DetailManger.get_all_student_id(db_session)
        for id in sheet:
            lanmsg = await DetailManger.get_Sign_by_student_id(db_session, id)
            id = lanmsg.id
            group_id = lanmsg.group_id
            user_id = lanmsg.user_id
            updated = lanmsg.updated
            text = lanmsg.text
            clip = lanmsg.clip
            sentiment = lanmsg.sentiment
            await HistoryManger.create_signmsg(
                db_session,
                id=id,
                group_id=group_id,
                user_id=user_id,
                updated=updated,
                text=text,
                clip=clip,
                sentiment=sentiment
            )
        logger.info(f"创建历史信息成功")