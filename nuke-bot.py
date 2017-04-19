from groupy import Group
from groupy import Member
from groupy import Bot
from groupy import User
from operator import itemgetter
import groupy

#select a group
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

#print("fuk u Joey Nedland")
#...*shruggy*

#selectgroup until valid entry given
repeat = True
while repeat:
    oldGroup = selectGroup()
    members = oldGroup.members()

    msg = "Ok, I will remove all members from %s and migrate them to a group with the same name. Is that ok? (Y|N) " % oldGroup.name
    verify = input(msg)

    if verify == "Y" or verify == 'y':
        repeat = False

#make new group and add all members (easier than the old way, does it all at once)
newGroup = Group.create(oldGroup.name, None, None, False)
newGroup.add(*members)

#iterate and delete members from old group
for member in members:
    try:
        oldGroup.remove(member)
    except:
        msg = "Could not remove %s from the group" % member.nickname
        print(msg)
