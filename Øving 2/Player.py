import random


class Player():
    # Class variables
    _actions = {0:'rock',1:'paper',2:'scissor'}
    i = 0

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
    def get_history(self):
        return self.history_of_actions
    #prettyPrints the history
    def get_nice_history(self):
        hist = self.get_history()
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
        self.history_of_actions.append(A)
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
        self.history_of_actions.append(A)
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
    def __init__(self, name, enemy):
        Player.__init__(self, name)
        self.enemy = enemy

    def pick_action(self):
        rock = 0
        paper = 0
        scissor = 0
        most_used = 1
        rockA = Action(Player._actions[0])
        paperA = Action(Player._actions[1])
        history = self.enemy.get_history()
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
        self.history_of_actions.append(A)
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
    def __init__(self,name,enemy):
        Player.__init__(self,name)
        self.enemy = enemy


    def pick_action(self):
        remember = [0]
        remember.append(0)
        remember.append(0)
        rockA = Action(Player._actions[0])
        paperA = Action(Player._actions[1])
        prev_action = 0
        history = self.enemy.get_history()
        if len(history) >1:
            last_move = history[-2]
            for action in history:
                if action == last_move:
                    index = history.index(action)
                    prev_action = history[index-1]
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
        A = Action(Player._actions[move])
        self.action = A
        self.history_of_actions.append(A)
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

    def get_scores(self):
        return "Score Player 1: " + str(self.score1) + ". Score Player 2: " + str(self.score2)


class Tournament:
    def __init__(self,player1,player2,numOfGames):
        self.p1 = player1
        self.p2 = player2
        self.games_left = numOfGames

    def do_tournament(self):
        print(str(self.p1.name) + " vs " + str(self.p2.name) + "!!")
        s = SingleGame(self.p1, self.p2)
        for i in range(self.games_left):
            s.do_a_game()
        if s.score2 > s.score1:
            print("Player 2 won!")
        elif s.score1 > s.score2:
            print("Player 1 won!")
        else:
            print("It's a draw!")
        string = s.get_scores()
        print(string)



def main():
    p1 = Random("Kari")
    p2 = Historian("Ola",p1)
    t = Tournament(p1,p2,10)
    t.do_tournament()
    # print(p1.get_nice_history())
    # print(p2.get_nice_history())
main()