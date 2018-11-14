from praw import Reddit
from os import path
from time import sleep
from datetime import datetime
from threading import Thread
from base64 import decodebytes
from re import sub
from re import split as rexSplit

bots = {"Base64_Bot": Reddit(user_agent='', username='', password='', client_id='', client_secret=''),
        "DDLC_TagBot": Reddit(user_agent='', username='', password='', client_id='', client_secret=''),
        "SuS_Bot": Reddit(user_agent='', username='', password='', client_id='', client_secret='')
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


def binConvert(string):
    string = sub("[^01]", "", string)
    integer = int(string, 2)
    string = integer.to_bytes((integer.bit_length() + 7) // 8, 'big').decode()
    return string


def hexConvert(string):
    string = sub("[^1234567890abcdf]", "", string)
    integer = int(string, 16)
    string = integer.to_bytes((integer.bit_length() + 7) // 8, 'big').decode()
    return string


def fileSync(tup, num):
    tup[1] = tup[1][int(-1.25 * num)::]
    with open(filePath + tup[0], "w") as f:
        for postId in tup[1]:
            f.write(postId + "\n")


def log(message):
    with open(filePath + "Bot.log", "a") as f:
        f.write(str(datetime.utcnow().isoformat(" ")) + "  " + message + "\n")


class Base64_Bot (Thread):
    def __init__(self, bot):
        Thread.__init__(self)
        self.bot = bot

    def run(self):
        bot = self.bot
        list_ = ['Base64_Bot.txt', readFile('Base64_Bot.txt')]
        while True:
            for Sub in ["ddlc"]:
                for comment in bot.subreddit(Sub).comments(limit=50):
                    flag = False
                    try:
                        if "!base64" in comment.body.lower() and comment.parent().id not in list_[1]:
                            list_[1].append(comment.parent().id)
                            flag = True
                            if "force" in comment.body.lower():
                                string = ""
                                if "full" in comment.body.lower() or "both" in comment.body.lower() or "title" in comment.body.lower() or comment.is_root and comment.parent().is_self:
                                    encodedList = rexSplit("\s", comment.submission.selftext)
                                else:
                                    encodedList = rexSplit("\s", comment.parent().body.replace("\n***\n^(If this bot is malfunctioning report it to u/JtBryant96)", ""))
                                for encodedPiece in encodedList:
                                    if encodedPiece is not "":
                                        string += decodebytes(bytes(encodedPiece, 'utf-8')).decode() + "\n\n"
                                if "full" in comment.body.lower() or "both" in comment.body.lower():
                                    message = "#" + decodebytes(bytes(comment.submission.title, 'utf-8')).decode() + "\n\n" + string
                                elif "title" in comment.body.lower():
                                    message = decodebytes(bytes(comment.submission.title, 'utf-8')).decode()
                                else:
                                    message = string
                            else:
                                if "full" in comment.body.lower() or "both" in comment.body.lower():
                                    message = "#" + decodebytes(bytes(comment.submission.title, 'utf-8')).decode() + "\n\n" + decodebytes(bytes(rexSplit('\s', comment.submission.selftext, 1)[0], 'utf-8')).decode()
                                elif "title" in comment.body.lower():
                                    message = decodebytes(bytes(comment.submission.title, 'utf-8')).decode()
                                elif comment.is_root and comment.parent().is_self:
                                    message = decodebytes(bytes(rexSplit("\s", comment.parent().selftext, 1)[0], 'utf-8')).decode()
                                else:
                                    message = decodebytes(bytes(rexSplit("\s", comment.parent().body, 1)[0], 'utf-8')).decode()
                                # the decoder adds a second \ for some reason.
                            message = message.replace("\\n", "\n").replace("\\'", "\'").replace("\\r", "\r")
                        elif "!binary" in comment.body.lower() and comment.parent().id not in list_[1]:
                            list_[1].append(comment.parent().id)
                            flag = True
                            if "full" in comment.body.lower() or "both" in comment.body.lower():
                                message = "#" + binConvert(comment.submission.title) + "\n\n" + binConvert(comment.submission.selftext)
                            elif "title" in comment.body.lower():
                                message = binConvert(comment.submission.title)
                            elif comment.is_root:
                                message = binConvert(comment.parent().selftext)
                            else:
                                message = binConvert(comment.parent().body)
                        elif "!hex" in comment.body.lower() and comment.parent().id not in list_[1]:
                            list_[1].append(comment.parent().id)
                            flag = True
                            if "full" in comment.body.lower() or "both" in comment.body.lower():
                                message = "#" + hexConvert(comment.submission.title) + "\n\n" + hexConvert(comment.submission.selftext)
                            elif "title" in comment.body.lower():
                                message = hexConvert(comment.submission.title)
                            elif comment.is_root:
                                message = hexConvert(comment.parent().selftext)
                            else:
                                message = hexConvert(comment.parent().body)
                    except:
                        log("Error in Base64_Bot: " + comment.id)
                        message += "Error: unable to decode."
                    if flag:
                        message += "\n***\n^(If this bot is malfunctioning report it to u/JtBryant96)"
                        if len(message) > 10000:
                            message = "Error: Message to long\n***\n" \
                                      "^(If this bot is malfunctioning report it to /u/JtBryant96)"
                            log(comment.parent.id)
                        while True:
                            try:
                                comment.reply(message)
                                log(comment.id)
                                sleep(10)
                                break
                            except Exception as e:
                                log(e)
            fileSync(list_, 50)
            log("__Base64")
            sleep(60)


class DDLC_TagBot_Messages (Thread):
    def __init__(self, bot, tagFile):
        Thread.__init__(self)
        self.bot = bot
        self.tagFile = tagFile

    def run(self):
        bot = self.bot
        tagFile = self.tagFile
        respondedList = ['DDLC_TagBot/Messages.txt', readFile('DDLC_TagBot/Messages.txt')]
        while True:
            tagList = readTagFile(tagFile)
            for message in bot.inbox.all(limit=25):
                if message not in respondedList[1] and not message.was_comment:
                    respondedList[1].append(message.id)
                    if message.first_message_name is not None and "stop" in message.body.lower():
                        for i in range(len(tagList)):
                            if message.first_message_name[3:] == tagList[i][0]:
                                tagList.pop(i)
                                break
                        message.reply("Thank you again for using DDLC_TagBot.")
                    elif message.first_message_name is None:
                        tempTag = [message.id, []]
                        body = message.body.lower()
                        confirmation = "Thank you for using DDLC_TagBot.\n\nYou've selected to be messaged links to "
                        if "nsfw" in body:
                            tempTag[1].append('NSFW')
                            body.replace("nsfw", "")
                        if "all" in body:
                            tempTag[1].append('All')
                            body.replace("all", "")
                            confirmation += "All posts"
                            if "NSFW" in tempTag[1]:
                                confirmation += " including NSFW content."
                            else:
                                confirmation += " excludeing NSFW content."
                            confirmation += "\n\nTo stop these messages, reply \"Stop\""
                            message.reply(confirmation)
                        else:
                            confirmation += "posts flaired as:"
                            for i in range(len(mainTags)):
                                if mainTags[i].lower().replace("_", " ") in body:
                                    tempTag[1].append(mainTags[i])
                                    body.replace(mainTags[i].lower().replace("_", " "), "")
                                    confirmation += " " + mainTags[i].replace("_", " ")
                            if "special" in body:
                                tempTag[1].append('Special')
                                body.replace("special", "")
                                confirmation += " *Moderator Edited Flairs*"
                            if "NSFW" in tempTag[1]:
                                confirmation += " including NSFW content."
                            else:
                                confirmation += " excludeing NSFW content."
                            confirmation += "\n\nTo stop these messages, reply \"Stop\""
                            message.reply(confirmation)
                        tagList.append(tempTag)
            with open(filePath + tagFile, "w") as f:
                for x in tagList:
                    line = x[0]
                    for tag in x[1]:
                        line += " " + tag
                    f.write(line + "\n")
            fileSync(respondedList, 25)
            log("__TagBot")
            sleep(120)


class SuS_Bot (Thread):
    def __init__(self, bot):
        Thread.__init__(self)
        self.bot = bot

    def run(self):
        bot = self.bot
        list_ = ['SuS_Bot.txt', readFile('SuS_Bot.txt')]
        while True:
            for Sub in ["ddlc"]:
                for comment in bot.subreddit(Sub).comments(limit=50):
                    try:
                        if "SuS" in comment.body and comment.id not in list_[1] and len(comment.body) < 6:
                            list_[1].append(comment.id)
                            comment.reply("SuS")
                            sleep(1)
                            list_[1].append(bot.user.me().comments.new(limit=1).next().id)
                    except:
                        log("Error in SuS_Bot: " + comment.id)
            fileSync(list_, 50)
            log("__SuS")
            sleep(60)


def main():
    Base64_Bot_Thread = Base64_Bot(bots["Base64_Bot"]).start()
    DDLC_TagBot_Messages_Thread = DDLC_TagBot_Messages(bots["DDLC_TagBot"], 'DDLC_TagBot/TagList.txt').start()
    SuS_Bot_Thread = SuS_Bot(bots["SuS_Bot"]).start()
    log("Rebooting")


if __name__ == '__main__':
    main()
