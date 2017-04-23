from groupy import Group
from groupy import Member
from groupy import Bot
from groupy import User
from operator import itemgetter
import groupy
from time import sleep

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


#get best messages from old group
messages = oldGroup.messages()

stats = []
for mem in members:
        stats.append([mem.user_id,mem.nickname,0,0])

while messages.iolder():
    pass

#create bot to post status of old group
StatusBot = Bot.create('StatusBot', newGroup, avatar_url='https://pbs.twimg.com/media/BtxcH_cIgAAXAC9.jpg')


#count likes per message
for m in messages:
    likes = m.likes()
    likesCount = len(likes)
    sender = m.user_id
    for person in stats:
        if person[0]==sender:
            person[2] += 1
            person[3] += likesCount

#store data in results list
results = []
for s in stats:
    if s[2] == 0:
        ratio = 0
    else:
        ratio = round((float(s[3])/float(s[2])),2)
    results.append([ratio,s[1]])
results.sort()
results.reverse()


#create ranking message
i = 1
ranking = "Old GroupMe Rankings:\n\n"
for r in results:
    r.reverse()
    print(r)
    newString = "%d: %s with %.2f average likes per message\n\n" % (i, r[0], r[1])
    
    if len(ranking) + len(newString) < 1000:
        ranking+=newString

    i+=1;

#post message
StatusBot.post(ranking)
Bot.destroy(StatusBot)


#iterate and delete members from old group
#NukeBot = Bot.create('NukeBot', oldGroup, avatar_url='http://i3.mirror.co.uk/incoming/article6291589.ece/ALTERNATES/s1200/MAIN-Kim-Jong-Un-missiles.jpg')
#NukeBot.post("Nuking...")

for member in members:
    exemptname = "Janak Malla"
    if member.nickname != exemptname:
        try:
            oldGroup.remove(member)
        except:
            msg = "Could not remove %s from the group" % member.nickname
            print(msg)


#NukeBot.post("Nuke completed")
#Bot.destroy(NukeBot)
