import random
import numpy as np
import sys


class Poker(object):
    def __init__(self, cards, current, deck=3):
        self.cards = cards * deck
        self.handcards = []
        self.current = current
        self.flag = 1

    @classmethod
    def cards_str(cls):
        current = 0
        cards = []
        for suite in '♠♥♣♦':
            for face in range(1, 14):
                if face == 1:
                    face = 'A'
                elif face == 11:
                    face = 'J'
                elif face == 12:
                    face = 'Q'
                elif face == 13:
                    face = 'K'
                else:
                    face = str(face)
                cards.append(str(suite + face))
        return cls(cards, current)

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, role):
        role.handcards = []
        for _ in range(self.current, self.current + 2):
            role.handcards.append(self.cards[_])
        self.current += 2
        return role.handcards

    def hit(self, role):
        card = self.cards[self.current]
        role.handcards.append(card)
        self.current += 1
        return card

    def game_over(self):
        if self.current > len(self.cards) - 10:
            self.flag = 0
        else:
            self.flag = 1


class Judge:
    def __init__(self, handcards):
        self.handcards = handcards
        self.point = 0

    @staticmethod
    def get_values(_):
        values = _[1:]
        return values

    def arrange(self):
        backup = self.handcards[:]
        for _ in backup:
            value = self.get_values(_)

            if value == 'A':
                backup.remove(_)
                backup.append(_)
        return backup

    def counting(self):
        backup = self.arrange()
        for _ in backup:
            value = self.get_values(_)
            if value != 'A':
                if value == 'J':
                    self.point += 10
                elif value == 'Q':
                    self.point += 10
                elif value == 'K':
                    self.point += 10
                else:
                    self.point += int(value)
            else:
                if backup.index(_) < len(backup) - 1:
                    self.point += 1
                else:
                    if self.point <= 10:
                        self.point += 11
                    else:
                        self.point += 1
        return self.point

    @staticmethod
    def judgement(role1_point, role2_point):
        if role1_point <= 21 < role2_point:
            var = '张老三赢了！'
            score = np.array([1, 0])
        elif role1_point > 21 >= role2_point:
            var = '你赢了！'
            score = np.array([0, 1])
        elif role1_point > role2_point:
            var = '张老三赢了！'
            score = np.array([1, 0])
        elif role1_point < role2_point:
            var = '你赢了！'
            score = np.array([0, 1])
        elif role1_point > 21 and role2_point > 21:
            var = '平局！'
            score = np.array([0, 0])
        else:
            var = '平局！'
            score = np.array([0, 0])

        return var, score


class Player:
    def __init__(self, name):
        self.name = name
        self.point = 0
        self.handcards = []
        self.hit = 1

    def name(self):
        return self.name

    def _point(self):
        self.point = self.get_point(self.handcards)
        return self.point

    def player_bust(self):
        if self.point > 21:
            self.hit = 0
        else:
            self.hit = 1
        return self.hit

    @staticmethod
    def get_point(handcards):
        point = Judge(handcards).counting()
        return point

    def computer_bust(self, cards, current, role2_point):
        _point = self.point = self.get_point(self.handcards)
        _bust = 0
        if role2_point > 21:
            _chance = float(1)
        else:
            if _point < 17:
                for _ in cards[current:]:
                    _a = self.handcards[:]
                    _a.append(_)
                    if Judge(_a).counting() > 21:
                        _bust += 1
                    else:
                        continue
                _chance = float('%.2f' % (_bust / (len(cards) - current)))
            else:
                _chance = float(1)
        if _chance <= 0.53:
            self.hit = 1
        else:
            self.hit = 0
        return self.hit

    def stand(self):
        self.hit = 0
        return self.hit


class Game:
    def __init__(self, name):
        self.name = name
        self.cards = Poker.cards_str()
        self.role1 = Player('张老三')
        self.role2 = Player('name')
        self.msg = ''
        self.score = np.array([0, 0])

    def start_game(self):
        self.cards.current = 0
        self.cards.shuffle()

    def run_game(self):
        self.cards.flag = 1
        while self.cards.flag:
            self.game_deal()
            self.gamer2_hit()
            self.gamer1_hit()
            self.game_judge()
            self.cards.game_over()
        self.restart()

    def game_deal(self):
        self.reset()
        self.cards.deal(self.role1)
        self.cards.deal(self.role2)

    def gamer2_hit(self):
        self.cards.hit(self.role2)
        self.role2._point()
        self.role2.player_bust()

    def gamer1_hit(self):
        while self.role1.hit:
            self.role1.computer_bust(self.cards.cards, self.cards.current, self.role2.point)
            if self.role1.hit:
                self.cards.hit(self.role1)
                self.role1._point()
            else:
                self.role1._point()
                self.role1.stand()
                break

    def game_judge(self):
        if not self.role1.hit:
            if not self.role2.hit:
                self.role2._point()
                self.role1._point()
                var, score = Judge.judgement(self.role1.point, self.role2.point)
                self.msg = var
                self.score += score

    def restart(self):
        restart = input('再来一盘？y/n')
        if restart == 'y':
            self.start_game()
        elif restart == 'n':
            sys.exit()

    def reset(self):
        self.role1.hit = 1
        self.role2.hit = 1


if __name__ == '__main__':
    app = Game('zxw')
    app.start_game()
