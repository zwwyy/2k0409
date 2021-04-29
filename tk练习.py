from tkinter import *
from PIL import Image, ImageTk
from blackjack1 import *


class Initface:
    def __init__(self, master):
        self.master = master
        self.master.title('Black Jack')
        self.master.geometry('1024x768')
        self.master.config(bg='white')

        self.initface = Frame(self.master, )
        self.initface.pack()
        self.image = ImageTk.PhotoImage(Image.open('C:/python_work/21poker/cards/puke1.jpg'))
        self.logo = Label(self.initface, text='庄稼-张老三', fg='red', font='隶书 30', image=self.image,
                          compound=BOTTOM)
        self.accountL = Label(self.initface, text='你的名字', font='宋体 12')
        self.accountL.grid(row=1, pady=30)
        self.logo.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

        self.accountR = Entry(self.initface, font="Helvetica 15 bold")
        self.accountR.grid(row=1, column=1)
        self.play_name = ""

        self.btn = Button(self.initface, text='开始', font='黑体 20 bold', command=self.change)
        self.btn.grid(row=2, column=0, columnspan=2, pady=20)

    def get_input(self):
        self.play_name = self.accountR.get()
        if not self.play_name:
            self.play_name = '狗蛋'
        return self.play_name

    def change(self):
        self.get_input()
        self.initface.destroy()
        Gameface(self.master, self.play_name)


class Gameface:
    def __init__(self, master, name):
        self.master = master
        self.master.config(bg='green')
        self.name = name
        self.card_image = None
        self.game = Game(self.name)
        self.game.start_game()

        self.satsframe = Frame(self.master, bg='green')
        self.satsframe.pack()
        self.player_score = Label(self.satsframe, text=self.name + ' {}'.format(''), font='黑体 20',
                                  bg='green')
        self.player_score.grid(row=0, column=0, padx=20, pady=5)
        self.banker_score = Label(self.satsframe, text="        张老三  {}".format(''), font='黑体 20', bg='green')
        self.banker_score.grid(row=0, column=1, padx=20, pady=5)

        self.cardframe = Frame(self.master, bg='green')
        self.cardframe.pack(pady=50)
        self.banker_list = []
        self.player_list = []
        Label(self.cardframe, text="张老三", font='楷书 15', bg='green').grid(row=0, column=3, pady=10)
        for _ in range(7):
            banker_label = Label(self.cardframe, bg='green', borderwidth=0, highlightthickness=0)
            banker_label.grid(row=1, column=_, padx=10, pady=5)
            self.banker_list.append(banker_label)
            self.card_image = self.get_image('C:/python_work/21poker/cards/blank.png')
            self.banker_list[_].config(image=self.card_image)
            self.banker_list[_].image = self.card_image
        Label(self.cardframe, text=self.name, font='楷书 15', bg='green').grid(row=2, column=3, pady=10)
        for _ in range(7):
            player_label = Label(self.cardframe, bg='green')
            player_label.grid(row=3, column=_, pady=10)
            self.player_list.append(player_label)
            self.card_image = self.get_image('C:/python_work/21poker/cards/blank.png')
            self.player_list[_].config(image=self.card_image)
            self.player_list[_].image = self.card_image

        self.controlframe = Frame(self.master, bg='green')
        self.controlframe.pack()
        self.msglab = Label(self.controlframe, text='点数：{}'.format(''),
                            font='黑体 20', bg='green', width=30, height=2)
        self.msglab.grid(row=0, column=2, padx=10)
        self.btn1 = Button(self.controlframe, text='发牌', font='黑体 15',
                           width=8, command=self.deal_show)
        self.btn1.grid(row=1, column=0, padx=20, pady=60, columnspan=2)
        self.btn2 = Button(self.controlframe, text='要牌', font='黑体 15',
                           width=8, command=self.hit_show, state=DISABLED)
        self.btn2.grid(row=1, column=2, columnspan=2, padx=20, pady=20)
        self.btn3 = Button(self.controlframe, text='停牌', font='黑体 15',
                           width=8, command=self.stand_show, state=DISABLED)
        self.btn3.grid(row=1, column=4, columnspan=2, pady=20)
        self.btn4 = Button(self.controlframe, text='重置', font='黑体 15',
                           width=8, command=self.restart, state=DISABLED)
        self.btn4.grid(row=1, column=6, columnspan=2, padx=20, pady=20)

    def get_image(self, image_path):
        image = Image.open(image_path)
        self.card_image = ImageTk.PhotoImage(image)
        return self.card_image

    @staticmethod
    def get_path(card):
        face, value = card[0], card[1:]
        if face == '♠':
            face = 'spade'
        elif face == '♦':
            face = 'diamond'
        elif face == '♥':
            face = 'heart'
        elif face == '♣':
            face = 'club'
        if value == 'J':
            value = 'jack'
        elif value == 'Q':
            value = 'queen'
        elif value == 'K':
            value = 'king'
        elif value == 'A':
            value = str(1)
        else:
            value = str(value)
        path = '%s_%s' % (value, face)
        return path

    def blank(self):
        for _ in range(6):
            self.card_image = self.get_image('C:/python_work/21poker/cards/blank.png')
            self.banker_list[_].config(image=self.card_image)
            self.banker_list[_].image = self.card_image
            self.player_list[_].config(image=self.card_image)
            self.player_list[_].image = self.card_image

    def deal_show(self):
        self.gameover_show()
        if self.game.cards.flag:
            self.blank()
            self.game.game_deal()
            self.btn1['state'] = DISABLED
            self.btn2['state'] = NORMAL
            self.btn3['state'] = NORMAL
            self.card_image = self.get_image('C:/python_work/21poker/cards/back.png')
            self.banker_list[0].config(image=self.card_image)
            self.banker_list[0].image = self.card_image
            path = self.get_path(self.game.role1.handcards[1])
            self.card_image = self.get_image('C:/python_work/21poker/cards/%s.png' % path)
            self.banker_list[1].config(image=self.card_image)
            self.banker_list[1].image = self.card_image
            self.card_display(self.player_list, self.game.role2.handcards)
            self.msglab.config(text='点数：{}'.format(self.game.role2._point()))

    def card_display(self, role, handcards):
        for _ in range(len(handcards)):
            path = self.get_path(handcards[_])
            self.card_image = self.get_image('C:/python_work/21poker/cards/%s.png' % path)
            role[_].config(image=self.card_image)
            role[_].image = self.card_image

    def hit_show(self):
        self.game.gamer2_hit()
        self.card_display(self.player_list, self.game.role2.handcards)
        self.msglab.config(text='点数：{}'.format(self.game.role2._point()))
        if not self.game.role2.hit:
            self.game.role1.hit = 0
            self.btn2['state'] = DISABLED
            self.btn3['state'] = DISABLED
            self.btn1['state'] = NORMAL
            self.card_display(self.banker_list, self.game.role1.handcards)
            self.game.game_judge()
            self.msg_update()

    def stand_show(self):
        self.game.role2.stand()
        self.game.gamer1_hit()
        self.card_display(self.banker_list, self.game.role1.handcards)
        self.game.game_judge()
        self.msg_update()
        self.btn1['state'] = NORMAL
        self.btn2['state'] = DISABLED
        self.btn3['state'] = DISABLED

    def gameover_show(self):
        self.game.cards.game_over()
        if not self.game.cards.flag:
            self.btn1['state'] = DISABLED
            self.btn2['state'] = DISABLED
            self.btn3['state'] = DISABLED
            self.btn4['state'] = NORMAL
            self.msglab.config(text='没牌了！重置吧！')
            self.blank()

        else:
            pass

    def msg_update(self):
        self.msglab.config(text='点数:{} 张老三:{}  {}'.format(self.game.role2._point(),
                                                          self.game.role1._point(), self.game.msg))
        self.player_score.config(text=self.name + ' {}'.format(self.game.score[1]))
        self.banker_score.config(text="        张老三  {}".format(self.game.score[0]))

    def restart(self):
        self.game.start_game()
        self.game.cards.flag = 1
        self.btn1['state'] = NORMAL
        self.btn4['state'] = DISABLED
        self.msglab.config(text='我们愉快的玩下去！')


if __name__ == '__main__':
    root = Tk()
    Initface(root)

    root.mainloop()
