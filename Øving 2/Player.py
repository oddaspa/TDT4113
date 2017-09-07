



class player():

    #  This method chooses which action should be played and returns the value.
    def pick_action(self,action):
        if action >2 or action <0:
            return "Illegal action"
        else:
            return action


    # After a single game is over the player gets to know the plays of the game
    # of each player. It can choose to learn from this information. (Especially if player is
    # historian or most_usual)


    def get_result(self):
        player