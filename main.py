# Hello, this is a project that I made because I like making things that
# I think are funny. This program tweets at one player per game, finding
# the worst player, and criticises their performance based on how bad they
# did and in what area they messed up in. (Rebounds, turnovers, missed shots, etc.)
# Find the bot at https://twitter.com/pro_nba_critic.

import datetime
import urllib
import BeautifulSoup
import json
from random import randint
import time
from time import strftime
import tweepy
# from google import search
from module import *
from classes.boxscore import BoxScore
from classes.player import Player
from classes.twitterapi import TwitterAPI



#helpful function to return things in between tags.
#find_between used to be here, putting it into boscore.py

#returns a list of the games on the current day.
def listGames():
    now = datetime.datetime.now()
    cmonth = '04'
    cday = '08'
    cyear = '2016'
    games = []
    #0323 is temp.
    url = "http://www.nba.com/gameline/{0}{1}{2}/".format(cyear,cmonth,cday)
    # print url
    page = urllib.urlopen(url).read()
    soup = BeautifulSoup.BeautifulSoup(page)
    boxscore = str(soup.find("div", {"id": "nbaSSOuter"}))
    # print boxscore
    for line in boxscore.splitlines():
        if '"nbaFnlStatTx"' in line and 'href="/games/201' in line:
            games.append('nba.com/games/201'+find_between(line, 'href="/games/201', '"><div class="nbaActionBtn'))
    return games

#returns a list of the losers on the current day.
def listLosers(games):
    now = datetime.datetime.now()
    # cmonth = str(now.month).zfill(2)
    # cday = str(now.day).zfill(2)
    # cyear = now.year
    cmonth = '04'
    cday = '08'
    cyear = '2016'
    losers = []
    for game in games:
        url = "http://" + game
        page = urllib.urlopen(url).read()
        for line in page.splitlines():
            if 'teamHome win' in line:
                #date is temp
                losers.append(find_between(game, '{0}{1}{2}/'.format(cyear,cmonth,cday),'/gameinfo')[:3])
                continue
            if 'teamAway win' in line:
                #date is temp
                losers.append(find_between(game, '{0}{1}{2}/'.format(cyear,cmonth,cday),'/gameinfo')[3:])
                continue
    if not losers:
        print datetime.datetime.now().time()
        print 'no winners found yet. sleeping for 20 minutes and checking again.'
        time.sleep(1200)
    return losers

#this function takes an abbreviation of a team and turns it into the team name.
#translateTeams() used to be here, put it into boxscore.py

#takes mm:ss into seconds
#minstoseconds() used to be here, put it into boxscore.py (because that was the only shit that used it.)

#returns the box score of the losing team as array of arrays.
#boxscore() used to be here, put it into boxscore.py as BoxScore (class)

#returns field goal percentage
def badFieldGoal(player):
    fieldGoal = player[5].split('-')
    if int(fieldGoal[1]) < 3:
        return False
    if float(fieldGoal[0])/float(fieldGoal[1]) < 0.4:
        return True
    else:
        return False

#returns three point percentage
def badThreePointer(player):
    threePointer = player[6].split('-')
    if int(threePointer[1]) < 3:
        return False
    if float(threePointer[0])/float(threePointer[1]) < 0.33:
        return True
    else:
        return False

#returns free throw percentage
def badFreeThrow(player):
    freeThrow = player[7].split('-')
    if int(freeThrow[1]) < 3:
        return False
    if float(freeThrow[0])/float(freeThrow[1]) < 0.67:
        return True
    else:
        return False

# returns amt. of offensive rebounds
def playerOffensiveRebounds(player):
    offensiveRebound = player[9]
    return int(offensiveRebound)

#returns amt. of defensive rebounds
def playerDefensiveRebounds(player):
    defensiveRebound = player[10]
    return int(defensiveRebound)

def badRebounds(player):
    if playerDefensiveRebounds(player)-playerOffensiveRebounds(player) > 4:
        return True
    else:
        return False

#returns amt. of assists
def playerAssist(player):
    assist = player[12]
    return int(assist)

#returns amt. of personal fouls
def badPersonalFoul(player):
    foul = player[13]
    if int(foul)>5:
        return True
    else:
        return False

#returns amount of turnovers
def badTurnOver(player):
    turnOver = player[15]
    if int(turnOver) >2:
        return True
    else:
        return False

def rateStat(badStatList, player):
    rating = 0
    if 5 in badStatList:
        fieldGoal = player[5].split('-')
        ratio = float(fieldGoal[0])/float(fieldGoal[1])
        if float(fieldGoal[1]) < 5 and  ratio > 0.24:
            rating += 1
        if ratio <= 0.4 and ratio > 0.3:
            rating += 2
        if ratio <= 0.3 and ratio > 0.25:
            rating += 3
        elif ratio <= 0.25:
            rating += 4
    if 6 in badStatList:
        threePointer = player[6].split('-')
        ratio =float(threePointer[0])/float(threePointer[1])
        if float(threePointer[1]) < 4:
            rating += 1
        if float(threePointer[1]) > 5 and ratio <= 0.19:
            rating += 4
        if float(threePointer[1]) > 5 and ratio <= 0.32:
            rating += 3
        elif ratio <= 0.25 and ratio > 0.19:
            rating += 2
    if 7 in badStatList:
        freeThrow = player[7].split('-')
        ratio = float(freeThrow[0])/float(freeThrow[1])
        if float(freeThrow[1])<3:
            rating += 1
        if float(freeThrow[1])==4 and ratio > 0:
            rating += 2
        if ratio < 0.67 and ratio >= 0.5:
            rating += 2
        if ratio < 0.5 and ratio >= 0.4:
            rating += 3
        if ratio < 0.4:
            rating += 4
    if 9 in badStatList:
        oReb = int(player[9])
        dReb = int(player[10])
        diff = dReb - oReb
        tReb = oReb+dReb
        if player[1] == 'C' and tReb < 10 and tReb > 4:
            rating += 1
        if player[1] == 'C' and tReb < 5 and tReb > 3:
            rating += 2
        if player[1] == 'C' and tReb < 4 and tReb > 1:
            rating += 3
        if player[1] == 'C' and tReb < 2:
            rating += 4
        if player[1] != 'C' and diff >4 and diff <7:
            rating += 1
        if player[1] != 'C' and diff >6 and diff <9:
            rating += 2
        if player[1] != 'C' and diff >8 and diff <11:
            rating += 3
        if player[1] != 'C' and diff >10:
            rating += 4
    if 13 in badStatList:
        pFouls = int(player[13])
        if pFouls > 5:
            rating += 3
    if 15 in badStatList:
        turnOver = player[15]
        if turnOver == 3:
            rating += 1
        if turnOver == 4:
            rating += 2
        if turnOver == 5:
            rating += 3
        if turnOver > 5:
            rating +=4
    return rating

def badStats(boxScore):
    badStats = []
    badPlayerBox = []
    for player in boxScore:
        tempArray = []
        if badFieldGoal(player) == True:
            tempArray.append(5)
            badPlayerBox.append(player)
        if badThreePointer(player)== True:
            tempArray.append(6)
            if player not in badPlayerBox:
                badPlayerBox.append(player)
        if badFreeThrow(player) == True:
            tempArray.append(7)
            if player not in badPlayerBox:
                badPlayerBox.append(player)
        if badRebounds(player) == True:
            tempArray.append(9)
            if player not in badPlayerBox:
                badPlayerBox.append(player)
        if badPersonalFoul(player) == True:
            tempArray.append(13)
            if player not in badPlayerBox:
                badPlayerBox.append(player)
        elif badTurnOver(player) == True:
            tempArray.append(15)
            if player not in badPlayerBox:
                badPlayerBox.append(player)
        badStats.append(tempArray)
    badStats = [x for x in badStats if x != []]
    return badStats

def badPlayerBox(boxScore):
    badStats = []
    badPlayerBox = []
    for player in boxScore:
        tempArray = []
        if badFieldGoal(player) == True:
            tempArray.append(5)
            badPlayerBox.append(player)
        if badThreePointer(player)== True:
            tempArray.append(6)
            if player not in badPlayerBox:
                badPlayerBox.append(player)
        if badFreeThrow(player) == True:
            tempArray.append(7)
            if player not in badPlayerBox:
                badPlayerBox.append(player)
        if badRebounds(player) == True:
            tempArray.append(9)
            if player not in badPlayerBox:
                badPlayerBox.append(player)
        if badPersonalFoul(player) == True:
            tempArray.append(13)
            if player not in badPlayerBox:
                badPlayerBox.append(player)
        elif badTurnOver(player) == True:
            tempArray.append(15)
            if player not in badPlayerBox:
                badPlayerBox.append(player)
        badStats.append(tempArray)
    badStats = [x for x in badStats if x != []]
    return badPlayerBox


#returns the player we are going to cyber bully and his stats in a list
def worstPlayer(boxScore):
    badStatList= badStats(boxScore)
    badPlayerBoxList = badPlayerBox(boxScore)
    ratingList = []
    for i, val in enumerate(badStatList):
        ratingList.append(rateStat(badStatList[i],badPlayerBoxList[i]))
    worstIndex = max(ratingList)
    for i, val in enumerate(ratingList):
        if val == worstIndex:
            rightIndex = i
            break
    return badPlayerBoxList[rightIndex]

#returns an int signifying how bad a player is
#the higher the number is the worse they did
def worstPlayerRanking(boxScore):
    badStatList= badStats(boxScore)
    badPlayerBoxList = badPlayerBox(boxScore)
    ratingList = []
    for i, val in enumerate(badStatList):
        ratingList.append(rateStat(badStatList[i],badPlayerBoxList[i]))
    worstIndex = max(ratingList)
    return worstIndex

#turns 'first_last' into 'first last'
def correctName(name):
    return (name.replace('_',' ')).title()

# google searches for the player's twitter handle
# returns player's twitter handle
# def getHandle(handle):
#     query = urllib.urlencode({'q': handle})
#     url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % query
#     search_response = urllib.urlopen(url)
#     search_results = search_response.read()
#     results = json.loads(search_results)
#     data = results['responseData']
#     if data is None:
#         print 'retrying, dont want to use google api'
#         main()
#     hits = data['results']
#     findHandle = hits[0]
#     rightHandle= '@'+ find_between(str(findHandle), '(@',')')
#     if rightHandle == '@':
#         print handle.rstrip(' nba twitter')
#         return handle.rstrip(' nba twitter')
#     else:
#         return rightHandle

def getHandle(name):
    # this is only temp but i just need to test this code to see what's really good
    # for url in search(name, num = 1, start =0, stop=1):
        # return '@'+find_between(url, 'twitter.com/','?lang=')
    return '@'+name

def fgRank(player):
    fg = 0
    fieldGoal = (player.field_goal).split('-')
    if float(fieldGoal[1]) == 0:
        ratio = 0
    else:
        ratio = float(fieldGoal[0])/float(fieldGoal[1])

    if float(fieldGoal[1]) < 5 and  ratio > 0.24:
        fg = 1
    if int(fieldGoal[1])-int(fieldGoal[0]) >=10 and ratio > 0.5:
        fg = 4
    if ratio <= 0.4 and ratio > 0.3:
        fg = 2
    if ratio <= 0.3 and ratio > 0.25:
        fg = 3
    if ratio <= 0.25:
        fg = 4
    return fg

def tpRank(player):
    tp = 0
    threePointer = (player.three_point).split('-')
    if float(threePointer[1]) == 0:
        ratio = 0
    else:
        ratio =float(threePointer[0])/float(threePointer[1])

    if float(threePointer[1]) < 4:
        tp = 1
    if float(threePointer[1]) > 5 and ratio <= 0.19:
        tp = 4
    if float(threePointer[1]) > 5 and ratio <= 0.32:
        tp = 3
    if ratio <= 0.25 and ratio > 0.19:
        tp = 2
    return tp

def ftRank(player):
    ft = 0
    freeThrow = (player.free_throw).split('-')
    if float(freeThrow[1]) == 0:
        ratio = 0
    else:
        ratio = float(freeThrow[0])/float(freeThrow[1])

    if ratio < 0.67 and ratio >= 0.5:
        ft = 2
    if ratio < 0.5 and ratio >= 0.4:
        ft = 3
    if ratio < 0.4:
        ft = 4
    if float(freeThrow[1]) < 3:
        ft = 1
    if float(freeThrow[1])==4 and ratio > 0:
        ft = 2
    return ft

def rbRank(player):
    reb = 0
    oReb = int(player.o_reb)
    dReb = int(player.d_reb)
    diff = dReb - oReb
    tReb = oReb+dReb
    if player[1] == 'C' and tReb < 10 and tReb > 4:
        reb = 1
    if player[1] == 'C' and tReb < 5 and tReb > 3:
        reb = 2
    if player[1] == 'C' and tReb < 4 and tReb > 1:
        reb = 3
    if player[1] == 'C' and tReb < 2:
        reb = 4
    if player[1] != 'C' and diff >4 and diff <7:
        reb = 1
    if player[1] != 'C' and diff >6 and diff <9:
        reb = 2
    if player[1] != 'C' and diff >8 and diff <11:
        reb = 3
    if player[1] != 'C' and diff >10:
        reb = 4
    return reb

def flRank(player):
    foul = 0
    pFouls = int(player.foul)
    if pFouls > 5:
        foul = 3
    return foul

def toRank(player):
    to = 0
    turnOver = int(player[15])
    if turnOver == 3:
        to = 1
    if turnOver == 4:
        to = 2
    if turnOver == 5:
        to = 3
    if turnOver > 5:
        to = 4
    return to

#finds the players worst stat
def worstStat(player):
    fg = fgRank(player)
    tp = tpRank(player)
    ft = ftRank(player)
    rb = rbRank(player)
    fl = flRank(player)
    to = toRank(player)


    statList = []
    statList.extend((fg, tp, ft, reb, fl, to))
    worstStat = max(statList)
    worstIndex = statList.index(worstStat)

    if worstIndex == 0:
        return 'fg'
    if worstIndex == 1:
        return 'tp'
    if worstIndex == 2:
        return 'ft'
    if worstIndex == 3:
        return 'reb'
    if worstIndex == 4:
        return 'foul'
    if worstIndex == 5:
        return 'to'


#determines what kind of tweet the bot should tweet about
def tweet(rank, badStat, handle, player):
    if badStat == 'fg':
        return fieldGoalTweet(rank, handle, player)
    if badStat == 'tp':
        return threePointTweet(rank, handle, player)
    if badStat == 'ft':
        return freeThrowTweet(rank, handle, player)
    if badStat == 'reb':
        return reboundTweet(rank, handle, player)
    if badStat == 'fl':
        return foulTweet(rank, handle, player)
    if badStat == 'to':
        return turnOverTweet(rank, handle, player)

#tweets about the player shooting poorly
def fieldGoalTweet(rank, handle, player):
    fieldGoal = player[5].split('-')
    attempted = fieldGoal[0]
    made = fieldGoal[1]
    shooting = attempted+' for '+made
    if rank <=5:
        return '.'+handle+' had a poor showing this evening, shooting '+shooting+' from the field. #nba'
    if rank>5 and rank <= 11:
        return '.'+handle+" just shot "+shooting+" from the field. Please retire. #nba"
    elif rank >11:
        return '.'+handle+' played horribly this evening, shooting '+shooting+' from the field. Garbage player. #nba'

#tweets about the player shooting poorly
def threePointTweet(rank, handle, player):
    threePoint = player[6].split('-')
    attempted = threePoint[0]
    made = threePoint[1]
    shooting = attempted+' for '+made
    if rank <=5:
        return 'A poor performance from '+handle+' tonight where he shot '+shooting+' from the 3. #nba'
    if rank >5 and rank <=11:
        return 'Bricks for days. '+handle+' shot '+shooting+' from the 3 this evening. #nba'
    elif rank >11:
        return '.'+handle+'shot a horrendous '+shooting+" from the 3 this evening. Wake me up when he retires. #nba"

#tweets about the player shooting poorly
def freeThrowTweet(rank, handle, player):
    threePoint = player[7].split('-')
    attempted = threePoint[0]
    made = threePoint[1]
    shooting = attempted+' for '+made
    if rank <=5:
        return '.'+handle+' shot '+shooting+' from the line this evening. Yikes. #nba'
    if rank >5 and rank <=11:
        return shooting+' from the line. '+handle+' is trash. #nba'
    elif rank >11:
        return "In an appallingly bad game, '+handle+' shot '+shooting+' from the line. I honestly didn't know shooting this bad was possible. #nba"

#tweets about the player shooting poorly
def reboundTweet(rank, handle, player):
    tempOReb = int(player[9])
    tempDReb = int(player[10])
    tReb = str(tempOReb+tempDReb)
    oReb = str(tempOReb)
    dReb = str(tempDReb)
    if player[1] == 'C':
        isCenter = True
    else:
        isCenter = False
    if rank <= 5 and isCenter == True and tReb <10:
        return 'In a poor showing, center '+handle+' only secured '+tReb+' rebounds. #nba'
    if rank <= 5 and isCenter == False:
        return 'Despite filling the role of getting defensive rebounds this evening, '+handle+' only managed to secure '+oReb+' offensive rebounds. #nba'
    if rank > 5 and rank <=11 and isCenter == True and tReb <10:
        return 'Center '+handle+' had a poor perfomance this evening, securing only '+tReb+' rebounds. #nba'
    if rank > 5 and rank <=11 and isCenter == False:
        return '.'+handle+' failed to succesfully rebound offensively, securing '+oReb+' offensive rebounds despite '+dReb+' rebounds on defense. #nba'
    if rank >11 and isCenter == True and tReb <10:
        return 'Securing only '+tReb+' rebounds, '+handle+' had an terrible performance tonight. Awful awful awful. #nba'
    elif rank > 11 and isCenter == False:
        return 'In an awful performance this evening, '+handle+' secured only '+oReb+' rebounds despite '+dReb+' rebounds on defense. Yuck. #nba'

#tweets about the player fouling out
def foulTweet(rank, handle, player):
    pFouls = (player[13])
    if rank <=5:
        return 'In an uninspiring performance, '+handle+' fouled out this evening. #nba'
    if rank >5 and rank <=11:
        return '.'+handle+' fouled out this evening. He has absolutely no sportsmanship #nba'
    if rank >11:
        return 'In an absolutely awful performance, '+handle+' fouled out tonight. Terrible sportsmanship and terrible player. #nba'


def turnOverTweet(rank, handle, player):
    turnOver = player[15]
    if rank <=5:
        return '.'+handle+' had a dissapointing game this evening, turning the ball over '+turnOver+' times. #nba'
    if rank >5 and rank <= 11:
        return 'With '+turnOver+' turnovers, '+handle+' had an awful performance this evening. #nba'
    elif rank>11:
        return 'In an awful performance, '+handle+' had '+turnOver+' turnovers tonight. #nba'


def main():
    alreadyTweeted = []
    games = listGames()
    losers = listLosers(games)
    print losers
    for game in games:
        boxscore_obj = BoxScore(game,losers)
        boxscore = boxscore_obj.arr
        player_arr = worstPlayer(boxscore)
        player = Player(player_arr)



            #the block of code below is cool and works but doesnt use the classes that i made.
            #this will be changed

            #|||||||||||||||||
            #vvvvvvvvvvvvvvvvv

            # shitter = worstPlayer(boxScores(game, losers))
            # print shitter
            # print '\n'
            # name = correctName(shitter[0])
            # handle = getHandle(name+' nba twitter')
            # # print name
            # nbaTweet =  tweet(worstPlayerRanking(boxScores(game, losers)), worstStat(shitter), handle, shitter)
            # print nbaTweet

            #below is commented out because i am testing this.
            #10/17

            # if __name__ == "__main__":
            #     twitter = TwitterAPI()
            #     try:
            #         twitter.tweet(nbaTweet)
            #     except tweepy.error.TweepError:
            #         continue
            # alreadyTweeted.append(game)


while True:
    main()
    # print datetime.datetime.now().time()
    print '___________________________'
    time.sleep(1200)
