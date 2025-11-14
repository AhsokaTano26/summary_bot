from typing import Optional
from sqlalchemy import text
from nonebot_plugin_orm import async_scoped_session
from sqlalchemy import select
from .models import Detail , hot_history, Clip, History # 导入你的模型定义


class DetailManger:
    @classmethod
    async def get_all_student_id(cls, session: async_scoped_session) -> set:
        """获取数据库中所有 student_id"""
        result = await session.execute(select(Detail.id))
        return {row[0] for row in result}

    @classmethod
    async def get_Sign_by_student_id(cls, session: async_scoped_session, student_id: str) -> Optional[Detail]:
        """根据 student_id 获取单个信息"""
        return await session.get(Detail, student_id)

    @staticmethod
    async def is_database_empty(db_session):
        # 查询数据库，判断是否有数据
        result = await db_session.execute(text("SELECT 1 FROM Detail LIMIT 1"))
        return not result.fetchone()

    @classmethod
    async def create_signmsg(cls, session: async_scoped_session, **kwargs) -> Detail:
        """创建新的数据"""
        new_signmsg = Detail(**kwargs)
        session.add(new_signmsg)
        await session.commit()
        return new_signmsg

    @classmethod
    async def delete_all_student_id(cls, session: async_scoped_session) -> bool:
        """删除所有数据"""
        sheet = await cls.get_all_student_id(session)
        for student_id in sheet:
            lanmsg = await cls.get_Sign_by_student_id(session, student_id)
            if lanmsg:
                await session.delete(lanmsg)
                await session.commit()
        return True


class hot_historyManger:
    @classmethod
    async def get_all_student_id(cls, session: async_scoped_session) -> set:
        """获取数据库中所有 student_id"""
        result = await session.execute(select(hot_history.id))
        return {row[0] for row in result}

    @classmethod
    async def get_Sign_by_student_id(cls, session: async_scoped_session, student_id: str) -> Optional[hot_history]:
        """根据 student_id 获取单个信息"""
        return await session.get(hot_history, student_id)

    @staticmethod
    async def is_database_empty(db_session):
        # 查询数据库，判断是否有数据
        result = await db_session.execute(text("SELECT 1 FROM hot_history LIMIT 1"))
        return not result.fetchone()

    @classmethod
    async def create_signmsg(cls, session: async_scoped_session, **kwargs) -> hot_history:
        """创建新的数据"""
        new_signmsg = hot_history(**kwargs)
        session.add(new_signmsg)
        await session.commit()
        return new_signmsg

    @classmethod
    async def delete_id(cls, session: async_scoped_session, id: str) -> bool:
        """删除数据"""
        lanmsg = await cls.get_Sign_by_student_id(session, id)
        if lanmsg:
            await session.delete(lanmsg)
            await session.commit()
            return True
        return False


class ClipManger:
    @classmethod
    async def get_all_student_id(cls, session: async_scoped_session) -> set:
        """获取数据库中所有 student_id"""
        result = await session.execute(select(Clip.id))
        return {row[0] for row in result}

    @classmethod
    async def get_Sign_by_student_id(cls, session: async_scoped_session, student_id: str) -> Optional[Clip]:
        """根据 student_id 获取单个信息"""
        return await session.get(Clip, student_id)

    @staticmethod
    async def is_database_empty(db_session):
        # 查询数据库，判断是否有数据
        result = await db_session.execute(text("SELECT 1 FROM Clip LIMIT 1"))
        return not result.fetchone()

    @classmethod
    async def delete_id(cls, session: async_scoped_session, id: str) -> bool:
        """删除数据"""
        lanmsg = await cls.get_Sign_by_student_id(session, id)
        if lanmsg:
            await session.delete(lanmsg)
            await session.commit()
            return True
        return False

    @classmethod
    async def create_signmsg(cls, session: async_scoped_session, **kwargs) -> Clip:
        """创建新的数据"""
        new_signmsg = Clip(**kwargs)
        session.add(new_signmsg)
        await session.commit()
        return new_signmsg

    @classmethod
    async def delete_all_student_id(cls, session: async_scoped_session) -> bool:
        """删除所有数据"""
        sheet = await cls.get_all_student_id(session)
        for student_id in sheet:
            lanmsg = await cls.get_Sign_by_student_id(session, student_id)
            if lanmsg:
                await session.delete(lanmsg)
                await session.commit()
        return True

    @classmethod
    async def get_top_3_words(cls, session: async_scoped_session) -> list:
        """获取数据库中所有 student_id"""
        dic = []
        result = await session.execute(text("""
                                            SELECT word
                                            FROM Clip
                                            ORDER BY frequency DESC
                                            LIMIT 3;
                                            """))
        for row in result:
            dic.append(row[0])
        return dic


class HistoryManger:
    @classmethod
    async def get_all_student_id(cls, session: async_scoped_session) -> set:
        """获取数据库中所有 student_id"""
        result = await session.execute(select(History.id))
        return {row[0] for row in result}

    @classmethod
    async def get_Sign_by_student_id(cls, session: async_scoped_session, student_id: str) -> Optional[History]:
        """根据 student_id 获取单个信息"""
        return await session.get(History, student_id)

    @staticmethod
    async def is_database_empty(db_session):
        # 查询数据库，判断是否有数据
        result = await db_session.execute(text("SELECT 1 FROM History LIMIT 1"))
        return not result.fetchone()

    @classmethod
    async def create_signmsg(cls, session: async_scoped_session, **kwargs) -> History:
        """创建新的数据"""
        new_signmsg = History(**kwargs)
        session.add(new_signmsg)
        await session.commit()
        return new_signmsg

    @classmethod
    async def delete_all_student_id(cls, session: async_scoped_session) -> bool:
        """删除所有数据"""
        sheet = await cls.get_all_student_id(session)
        for student_id in sheet:
            lanmsg = await cls.get_Sign_by_student_id(session, student_id)
            if lanmsg:
                await session.delete(lanmsg)
                await session.commit()
        return True