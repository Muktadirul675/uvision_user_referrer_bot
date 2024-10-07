from models import User as UserModel, Group as GroupModel, Member as MemberModel
from telebot.types import Message
import matplotlib.pyplot as plt

groups = [

]

members = [

]

class User:
    def __init__(self, info):
        obj, created = UserModel.get_or_create(user_id=info.id, username=info.username, first_name=info.first_name, last_name=info.last_name)
        self.obj = obj

    def __str__(self):
        return f"{self.obj.first_name} {self.obj.last_name}"

    def add_referrals(self, message: Message):
        new_users = message.new_chat_members
        chat = message.chat
        # print(chat)
        group, created = GroupModel.get_or_create(group_id=f"{chat.id}",name=chat.title)
        referrer_user, created = UserModel.get_or_create(user_id=message.from_user.id, username=message.from_user.username, first_name=message.from_user.first_name, last_name=message.from_user.last_name)
        referrer, created = MemberModel.get_or_create(user=referrer_user,group=group)

        for user in new_users:
            referred, created = UserModel.get_or_create(user_id=user.id, username=user.username, first_name=user.first_name, last_name=user.last_name)
            member, created = MemberModel.get_or_create(user=referred, referrer=referrer,group=group)

def get_user(ref):
    id = ref.from_user.id
    user = User.get(user_id=id)
    return user

def get_stats(group_id):
    group = GroupModel.get(group_id=group_id)
    x,y=[],[]
    for member in group.members:
        x.append(member.user.username)
        y.append(member.referrals.count())
        # Sample data   
    
    return (x,y)

if __name__ == "__main__":
    get_stats("-1002317230736")