import random
import matplotlib.pyplot as plt

class Player():
    # Class variables
    _actions = {0:'rock',1:'paper',2:'scissor'}
    i = 0
    # helper
    def counter(self, num):
        a = {0: 1, 1: 2, 2: 0}
        return a[num]
    # Initializer
    def __init__(self,name):
        self.name = name
        self.history_of_actions = []

    #  This method chooses which action should be played and returns the value.
    def pick_action(self):
        return

    # After a single game is over the player gets to know the plays of the game
    # of each player. It can choose to learn from this information. (Especially if player is
    # historian or most_usual)

    # sets name of player
    def __set_name__(self, name):
        self.name = name

    # retrives past moves
    def remember_move(self, action):
        self.history_of_actions.append(action)
    #prettyPrints the history
    def get_nice_history(self):
        hist = self.history_of_actions
        res = []
        for x in range(len(hist) -1):
            res.append(hist[x].action)
        return res

    #sends recent action back to
    def get_action(self):
        return self.action

    def give_name(self):
        return self.name

    # Tilfeldig: Denne velger tilfeldig om den skal gjøre stein, saks, eller papir. For ˚a implementere denne kan
    # det for eksempel være greit ˚a bruke random.randint(0, 2).For ˚a f˚a tak i denne metoden m˚a du først gjøre import
    # random.
class Random(Player):
    def __init__(self,name):
        Player.__init__(self,name)

    def pick_action(self):
        action = random.randint(0,2)
        A = Action(Player._actions[action])
        self.action = A
        return A




    # Sekvensiell: Denne spilleren g˚ar sekvensielt gjennom de forskjellige aksjonene, og spiller stein, saks, papir,
    #  stein, saks, papir, stein, saks...i en fast sekvens uansett hvordan motstander oppfører seg.
class Secquential(Player):
    def __init__(self,name):
        Player.__init__(self, name)
        self.prev_move = 0

    def pick_action(self):
        if self.history_of_actions == []:
            self.prev_move = 0
        if self.history_of_actions != []:
            self.prev_move+=1
            if self.prev_move == 3:
                self.prev_move = 0
        A = Action(Player._actions[self.prev_move])
        self.action = A
        return A


    #  MestVanlig: Denne spilleren ser p˚a motstanderens valg over tid, og teller opp hvor mange ganger motstander har
    # spilt stein, saks og papir. S˚a antar den at motstander igjen vil spille det som han / hun / den har spilt mest
    # av s˚a langt, og MestVanllig velger derfor optimalt ut fra dette.I det første spillet, der MestVanllig ikke
    # har sett noen av valgene til motstander og dermed ikke vet hva den bør velge, velger den i stedet tilfeldig.
    # Eksempel: La oss anta at motstander har spilt denne sekvensen: stein, saks, stein, stein, papir, saks, papir,
    #  stein, papir, stein, stein, saks, papir, saks.Vi ser at stein er mest vanlig i historien til motstanderen,
    # s˚a MestVanlig antar at stein vil komme igjen. Trekket fra MestVanllig er følgelig papir(ettersom papir sl˚ar
    # stein).
class MostRegular(Player):
    def __init__(self, name):
        Player.__init__(self, name)

    def pick_action(self):
        rock = 0
        paper = 0
        scissor = 0
        most_used = 1
        rockA = Action(Player._actions[0])
        paperA = Action(Player._actions[1])
        history = self.history_of_actions
        if history != []:
            for action in history:
                if (action == rockA):
                    rock += 1
                elif (action) == (paperA):
                    paper += 1
                else:
                    scissor += 1
            if rock > paper and rock > scissor:
                most_used = 1
            elif paper > rock and paper > scissor:
                most_used = 2
            else:
                most_used = 0
        A = Action(Player._actions[most_used])
        self.action = A
        return A

    # Historiker: Denne spilleren ser etter mønstre i m˚aten motstanderen spiller p˚a. Historiker defineres med en
    # parameter “husk”.Beskrivelsen starter med ˚a se p˚a situasjonen husk = 1. Eksempel: La oss igjen anta at
    # motstander har spilt sekvensen stein, saks, stein, stein, papir, saks, papir, stein, papir, stein, stein,
    # saks, papir, saks.Historiker ser p˚a det siste valget(saks), og g˚ar tilbake i historien for ˚a finne hva
    #  motstanderen pleier ˚a spille etter en saks. Motstanderen har spilt saks tre ganger tidligere; to av disse
    # ble etterfulgt av papir, mens en ble etterfulgt av stein.Historiker tenker dermed at det mest vanlige etter
    # en saks er papir, og antar derfor at den neste aksjonen til motstanderen blir papir. Historiker velger dermed
    # saks(fordi saks vinner over papir).
class Historian(Player):
    def __init__(self,name,numOfActions):
        Player.__init__(self,name)
        self.history_of_enemy = []
        self.numOfActions = numOfActions

    def get_valid_input(self):
        vhistory = []
        if(len(self.history_of_actions) > self.numOfActions):
            mlist = []
            for x in range(self.numOfActions-1):
                x+=1
                mlist.append(self.history_of_actions[-x])
            i=0
            j=0
            for actions in self.history_of_actions:
                i += 1
                if j < self.numOfActions:
                    if i < len(self.history_of_actions)-self.numOfActions:
                        if actions == mlist[j]:
                            j += 1
                        if j == self.numOfActions-1:
                            move = self.history_of_actions.index(actions)
                            if i < len(self.history_of_actions):
                                vhistory.append(self.history_of_actions[move+1])
                                j = 0
                        elif actions != mlist[j]:
                            j = 0
        return vhistory



    def pick_action(self):
        i = 0
        remember = [0]
        remember.append(0)
        remember.append(0)
        rockA = Action(Player._actions[0])
        paperA = Action(Player._actions[1])
        prev_action = 0
        history = self.get_valid_input()
        if len(history) >1:
            # checks what the previous move is
            last_move = history[-1]
            for action in history:
                # we keep track of where we are in history-list
                i += 1
                # if we are at the last element: break
                if i == (len(history)):
                    break
                if action == last_move:
                    # get index of previous move
                    index = history.index(action)
                    # check what action before that move was
                    prev_action = history[index+1]
                    # if action is rock append value to rock slot in remember array
                    if prev_action == rockA:
                        # increase rock by 1
                        remember[0] += 1
                    elif prev_action == paperA:
                        # increase paper by 1
                        remember[1] += 1
                    else:
                        # increase scissor by 1
                        remember[2] += 1
            max_value = max(remember)
            move = remember.index(max_value)
        else:
            move = random.randint(0,2)
        move = self.counter(move)
        A = Action(Player._actions[move])
        self.action = A
        return A

class Action:
    def __init__(self, action1):
        self.action = action1

    def get_weakness(self):
        if self.action == 'rock':
            return 'paper'
        elif self.action == 'paper':
            return 'scissor'
        else:
            return 'rock'
    def __eq__(self, other):
        return self.action == other.action

    def __gt__(self,other):
        if(self.action == other.get_weakness()):
            return True
    def get_type(self):
        return self.action


class SingleGame:

    def __init__(self,player1,player2):
        self.p1 = player1
        self.p2 = player2
        # Score
        self.score1 = 0
        self.score2 = 0

    def increase_score(self,score):
        if score == 1:
            self.score1 += 1
        else:
            self.score2 += 1
    def do_a_game(self):
        self.p1.pick_action()
        self.p2.pick_action()
        action1 = self.p1.get_action()
        action2 = self.p2.get_action()
        if action1 > action2:
            self.increase_score(1)
        elif action2 > action1:
            self.increase_score(2)
        self.p1.remember_move(action2)
        self.p2.remember_move(action1)
    def get_scores(self):
        return "Score Player 1: " + str(self.score1) + ". Score Player 2: " + str(self.score2)


class Tournament:
    def __init__(self,player1,player2,numOfGames):
        self.p1 = player1
        self.p2 = player2
        self.games_left = numOfGames

    def do_tournament(self):
        tot_p1 = 0
        tot_p2 = 0
        score_p1 = []
        x_axis = []
        count = 0
        print(str(self.p1.name) + " vs " + str(self.p2.name) + "!!")
        s = SingleGame(self.p1, self.p2)
        for i in range(self.games_left):
            s.do_a_game()
            count += 1
            x_axis.append(count)
            score_p1.append(s.score1 / count)
        if s.score2 > s.score1:
            print("Player 2 won!")
        elif s.score1 > s.score2:
            print("Player 1 won!")
        else:
            print("It's a draw!")
        print("\nTotal score in tournament:\n" + str(self.p1.name) + ": " + str(s.score1) + " poeng" +
              "\n" + str(self.p2.name) + ": " + str(s.score2) + " poeng")


        ##PYPLOT##
        plt.plot(x_axis, score_p1)
        plt.axis([0, self.games_left, 0, 1])
        plt.grid(True)
        plt.axhline(y=0.5, linewidth=0.5, color="r")
        plt.xlabel("Antall Spill")
        plt.ylabel("Gevinstprosent: " + str(self.p1.name))
        plt.show()

def main():
    husk = 2
    name1 = input("Name Player 1: ")
    name2 = input("Name Player 2: ")
    print("For Random press 0, for Sequential press 1, for Most Regular press 2, for Historian press 3")
    playerType1 = int(input("Which player type do Player 1 want to be : "))
    playerType2 = int(input("Which player type do Player 2 want to be : "))
    if playerType1 == 0:
        p1 = Random(name1)
    elif playerType1 == 1:
        p1 = Secquential(name1)
    elif playerType1 == 2:
        p1 = MostRegular(name1)
    else:
        p1 = Historian(name1, husk)
    if playerType2 == 0:
        p2 = Random(name2)
    elif playerType2 == 1:
        p2 = Secquential(name2)
    elif playerType2 == 2:
        p2 = MostRegular(name2)
    else:
        p2 = Historian(name2, husk)

    games = int(input("How many games would you like to play: "))
    t = Tournament(p1,p2,games)
    t.do_tournament()

main()