import os
import ast
from pydantic import BaseModel


class Config(BaseModel):
    """Plugin Config Here"""
    ignore_users: list = [971852256, 2438868634]
    target_group: list = ast.literal_eval(os.getenv('GROUP_LIST', "None"))
    # target_group: list = [1016925587,339834885,1017112832,962870444,825771260]
