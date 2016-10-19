import BeautifulSoup
from module import *
import urllib


class BoxScore:
    def __init__(self,url,losers):
        """Class to create an object for the boxscore. Takes a url of the game\
        as a parameter. BoxScore object displays as an array of all of the\
        player's stats (which are also displayed as an array) on the losing\
        team in the game modeled in the given url.\
        """
        p1, p2, p3, p4, p5, p6, p7,p8, p9, p10, p11, p12 = ([] for i in range(12))
        box_score = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12]
        rawList = []
        temp = []
        temp1 = []

        url = "http://" + url
        page = urllib.urlopen(url).read()
        soup = BeautifulSoup.BeautifulSoup(page)
        firstBox = str(soup.findAll("table", {"id": "nbaGITeamStats"})[0])
        secondBox = str(soup.findAll("table", {"id": "nbaGITeamStats"})[1])
        for loser in losers:
            # there are two boxes ()
            if translate_teams(loser) in firstBox:
                rawBox = firstBox
            if translate_teams(loser) in secondBox:
                rawBox = secondBox
        try:
             soup = BeautifulSoup.BeautifulSoup(rawBox)
        except UnboundLocalError:
            # print datetime.datetime.now().time()
            # print 'game not finished, waiting 20 minutes and checking again.'
            time.sleep(1200)
        index = 0
        while index<6:
            playerStatsOdd = str(soup.findAll("tr", {"class": "odd"})[index])
            rawList.append(playerStatsOdd)
            playerStatsEven = str(soup.findAll("tr", {"class": "even"})[index])
            rawList.append(playerStatsEven)
            index += 1
        for player in box_score:
            player.append(find_between(rawList[0],'/playerfile/','/index'))
            if(find_between(rawList[0],'nbaGIPosition">','</td>')=='&nbsp;'):
                player.append('')
            else:
                player.append(
                    find_between(rawList[0],'nbaGIPosition">','</td>'))
            rawList[0].rstrip("\n")
            soupy = BeautifulSoup.BeautifulSoup(rawList[0])
            for node in soupy.findAll('td'):
                player.append(''.join(node.findAll(text=True)))
            del rawList[0]
        for element in box_score:
            if len(element) <= 10:
                temp1.append(element)
            elif mins_to_seconds(element[4])<900:
                temp.append(element)
        for element in temp:
            box_score.remove(element)
        for element in temp1:
            box_score.remove(element)
        for stat in element:
            stat = str(stat)
        self.arr = box_score
