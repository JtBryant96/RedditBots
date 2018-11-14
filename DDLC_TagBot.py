from praw import Reddit
from os import path
from time import sleep
from datetime import datetime
from threading import Thread


bots = {"DDLC_TagBot": Reddit(user_agent='', username='', password='', client_id='', client_secret='')
        }

filePath = ""

mainTags = ["Discussion", "Question", "Reaction", "OC_Fanart", "Found_Fanart", "Music", "Video", "Cosplay", "OC_Edited_Media", "Found_Edited_Media", "Poetry", "Fanfic", "Custom_Dialogue", "News", "Meta", "Fun", "Misc", "Gameplay", "Game_Mod", "IRL_Media"]


def readFile(fileName):
    posts_replied_to = []
    if not path.isfile(filePath + fileName):
        f = open(filePath + fileName, "w")
        f.close()
    else:
        with open(filePath + fileName, "r") as f:
            posts_replied_to = f.read()
            posts_replied_to = posts_replied_to.split("\n")
            posts_replied_to = list(filter(None, posts_replied_to))
    return posts_replied_to


def readTagFile(fileName):
    with open(filePath + fileName, "r") as f:
        lines = f.read()
        lines = lines.split("\n")
        lines = list(filter(None, lines))
        list_ = []
        for line in lines:
            temp = line.split(" ")
            list_.append([temp[0], temp[1:]])
    return list_


def fileSync(tup, num):
    tup[1] = tup[1][int(-1.25 * num)::]
    with open(filePath + tup[0], "w") as f:
        for postId in tup[1]:
            f.write(postId + "\n")


def log(message):
    with open(filePath + "Bot.log", "a") as f:
        f.write(str(datetime.utcnow().isoformat(" ")) + "  " + message + "\n")


class DDLC_TagBot (Thread):
    def __init__(self, bot):
        Thread.__init__(self)
        self.bot = bot

    def run(self):
        bot = self.bot
        postList = ['DDLC_TagBot/Posts.txt', readFile('DDLC_TagBot/Posts.txt')]
        tagList = ['DDLC_TagBot/TagList.txt', readTagFile('DDLC_TagBot/TagList.txt')]
        messageList = []
        for i in range(len(tagList[1])):
            messageList.append("")
        for post in bot.subreddit("ddlc").new(limit=1000):
            if post.id not in postList[1]:
                postList[1].append(post.id)
                if post.link_flair_text is not None:
                    flair = post.link_flair_text.replace(" ", "_")
                else:
                    flair = None
                for i in range(len(tagList[1])):
                    if (("NSFW" in tagList[1][i][1] or not post.over_18) and
                        (("All" in tagList[1][i][1]) or
                         ("Special" in tagList[1][i][1] and flair is not None and flair not in mainTags) or
                         (flair in tagList[1][i][1]))):
                        messageList[i] += "[{title}](https://redd.it/{id})\n\n".format(title=post.title, id=post.id)
                        if len(messageList[i]) > 9600:
                            bot.inbox.message(tagList[1][i][0]).reply(messageList[i])
                            # print(tagList[1][i][0] + "\n" + messageList[i])
                            messageList[i] = ""
                            sleep(2)
        for i in range(len(tagList[1])):
            if messageList[i] != "":
                bot.inbox.message(tagList[1][i][0]).reply(messageList[i])
                # print(tagList[1][i][0] + "\n" + messageList[i])
                messageList[i] = ""
                sleep(2)
        fileSync(postList, 1000)
        log("__TagBot")


def main():
    DDLC_TagBot_Thread = DDLC_TagBot(bots["DDLC_TagBot"]).start()


if __name__ == '__main__':
    main()
