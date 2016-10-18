class BoxScore:
    """Class to create an object for the boxscore. Takes a url of the game as
    a parameter. """
    def __init__(self,url):
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
            if translateTeams(loser) in firstBox:
                rawBox = firstBox
            else:
                rawBox = secondBox
        try:
             soup = BeautifulSoup.BeautifulSoup(rawBox)
        except UnboundLocalError:
            print datetime.datetime.now().time()
            print 'game not finished, waiting 20 minutes and checking again.'
            time.sleep(1200)
        index = 0
        while index<6:
            playerStatsOdd = str(soup.findAll("tr", {"class": "odd"})[index])
            rawList.append(playerStatsOdd)
            playerStatsEven = str(soup.findAll("tr", {"class": "even"})[index])
            rawList.append(playerStatsEven)
            index += 1
        for player in boxScore:
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
        for element in boxScore:
            if len(element) <= 10:
                temp1.append(element)
            elif minsToSeconds(element[4])<900:
                temp.append(element)
        for element in temp:
            boxScore.remove(element)
        for element in temp1:
            boxScore.remove(element)
        for stat in element:
            stat = str(stat)
        return boxScore

    def translateTeams(team):
        teamDict = {'ATL': 'Hawks',
                    'BKN': 'Nets',
                    'BOS': 'Celtics',
                    'CHA': 'Hornets',
                    'CHI': 'Bulls',
                    'CLE': 'Cavaliers',
                    'DAL': 'Mavericks',
                    'DEN': 'Nuggets',
                    'DET': 'Pistons',
                    'GSW': 'Warriors',
                    'HOU': 'Rockets',
                    'IND': 'Pacers',
                    'LAC': 'Clippers',
                    'LAL': 'Lakers',
                    'MEM': 'Grizzlies',
                    'MIA': 'Heat',
                    'MIL': 'Bucks',
                    'MIN': 'Timberwolves',
                    'NOP': 'Pelicans',
                    'NYK': 'Knicks',
                    'OKC': 'Thunder',
                    'ORL': 'Magic',
                    'PHI': '76ers',
                    'PHX': 'Suns',
                    'POR': 'Trailblazers',
                    'SAC': 'Kings',
                    'SAS': 'Spurs',
                    'TOR': 'Raptors',
                    'UTA': 'Jazz',
                    'WAS': 'Wizards'    }
        return teamDict[team]
