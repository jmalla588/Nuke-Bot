from groupy import Group
from groupy import Member
from groupy import Bot
from groupy import User
from operator import itemgetter
import groupy

def selectGroup():
    i = 1
    groups = []
    for group in groupy.Group.list():
        msg = "%d:\t%s" % (i, group.name)
        print(msg)
        i += 1
        groups.append(group)

    prompt = "Which group would you like to nuke? "
    oldGroup = int(input(prompt))

    return groups[oldGroup - 1]

repeat = True
while repeat:
    oldGroup = selectGroup()
    members = oldGroup.members()

    msg = "Ok, I will remove all members from %s and migrate them to a group with the same name. Is that ok? (Y|N) " % oldGroup.name
    verify = input(msg)

    if verify == "Y" or verify == 'y':
        repeat = False

memsToAdd = []
newGroup = Group.create(oldGroup.name, None, None, False)
for member in members:
    if User.get().user_id == member.user_id:
        continue

    newGroup.add(member)
    try:
        oldGroup.remove(member)
    except:
        msg = "Could not remove %s from the group" % member.nickname
        print(msg)

