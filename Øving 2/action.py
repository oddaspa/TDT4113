
plays = ["Rock","Paper","Scissors"]



class SingleGame():


    # Iterate an instance of the class. Player1 and player2 are players of the game.
    def __init__(self,player1,player2):

        return True


    # Asks each player of their choice in action. Figures out the result out of given
    # rule set and gives a point to the winner. (if its a draw both players gets 0.5 points)
    # method should also report the actions taken in the game back to the players.
    def play_game(self, player1, player2):
        player1action == player1.get_action()
        player2action == player2.get_action()

        return True
    # Checks the output of the game. 1 is player 1 won. 2 is player 2 won. 3 is draw.
    def result_of_play(self,play1,play2):
        if play1 >2 or play2 >2:
            print("Illeagal action made. %s or %s is not valid inputs." %play1 %play2)
        if play1 == play2:
            result = 3
        elif play1 == 0:
            if play2 == 1:
                return 1
            else:
                return 2
        elif play1 == 1:
            if play2 == 2:
                return 1
            else:
                return 2
        elif play1 == 2:
            if play2 == 0:
                return 1
            else:
                return 2
        else:
            print("That's not a valid play. Check your spelling!")