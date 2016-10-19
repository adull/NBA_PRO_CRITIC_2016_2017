class Player:
    def __init__(self, player_arr):
        """Class to represent players, you pass an array of
        the player's stats(can be created by using BoxScore
        class) with this object you can get particular
        statistics of the player by creating a Player object.
        """

        self.full_name = (player_arr[0].replace('_',' ')).title()
        self.position = player_arr[1]
        self.short_name = player_arr[2]
        self.time_played = player_arr[4]
        self.field_goal = player_arr[5]
        self.three_point = player_arr[6]
        self.free_throw = player_arr[7]
        self.o_reb = player_arr[9]
        self.d_reb = player_arr[10]
        self.foul = player_arr[13]
        self.turnover = player_arr[15]
        
