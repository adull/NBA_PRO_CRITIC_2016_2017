def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def translate_teams(team):
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

def mins_to_seconds(time):
    l = time.split(':')
    return int(l[0])*60+int(l[1])
