import random
from collections import defaultdict

class Card:
    def __init__(self, row = 3, 
                col = 9, 
                numbers_in_row = 5, 
                max_number = 15,
                max_cell = 27,
                name = None):
        self._row = row
        self._col = col
        self._numbers_in_row = numbers_in_row
        self._max_number = max_number
        self._max_cell = max_cell
        self.min_bochonok = 1
        self.max_bochonok = 90
        self.card = []
        self.name = name

    def check_numbers(self, card, tmp):
        card.append(tmp)
        count = 0
        for i in range(self._col):
            count = 0
            for j in range(i*10, (i+1)*10):
                if j in card:
                    count += 1
                if j > 88 and 90 in card:
                    count += 1
                if count > self._row:
                    return False
        return True    

    def check_card_shuffle(self, card):
        dont_shuffle = []
        for num, i in enumerate(card):
            null = 0
            digit = 0
            for j in i:
                if j == 0:
                    null += 1
                    if null > 2:
                        dont_shuffle.append(num)
                else:
                    digit += 1
                    if digit > 2:
                        dont_shuffle.append(num)

        def get_shuffle_card(card, dont_shuffle):
            tmp = []
            for num, e in enumerate(card):
                if num not in dont_shuffle:
                    random.shuffle(e)
                    tmp.append(e)
                else:
                    tmp.append(card[num])
            return tmp
        b = True
        while b:
            res = []
            result = list(map(list, zip(*card)))
            for i in result:
                count = 0
                for num, j in enumerate(i):
                    if j != 0:
                        count += 1
                if count > 5 or count < 5:
                    self.card = get_shuffle_card(self.card, dont_shuffle)
                if count == 5 and len(res) < 3:
                    res.append(count)
                if count == 5 and len(res) == 3:
                    b = False

    def initialize_card(self):
        self.card = []
        while len(self.card) < self._max_number:
            tmp = random.randint(self.min_bochonok, self.max_bochonok)
            if tmp not in self.card and self.check_numbers(self.card.copy(), tmp):
                self.card.append(tmp)
        card_init = []
        for i in range(self._col):
            tmp = []
            for j in range(i*10, (i+1)*10):
                if j in self.card:
                    tmp.append(j)
                if j > 88 and 90 in self.card:
                    tmp.append(j+1)
            if tmp:
                if len(tmp) == 1:
                    tmp.append(0)
                    tmp.append(0)
                if len(tmp) == 2:
                    tmp.append(0)
                random.shuffle(tmp)
            else:
                tmp.append(0)
                tmp.append(0)
                tmp.append(0)
            card_init.append(tmp)
        self.card = card_init
        self.check_card_shuffle(card_init.copy())
    
    def card_view_user(self, name):
        result = list(map(list, zip(*self.card)))
        print('-'*9 + ' Карточка ' + name + ' ' + '-'*9)
        for i in result:
            print('  '.join(str(e) if e != 0 else '  ' for e in i))
        print('-'*35)
        
    
    def card_view_comp(self, name):
        result = list(map(list, zip(*self.card)))
        print('-'*9 + ' Карточка ' + name + ' ' + '-'*9)
        for i in result:
            print('  '.join(str(e) if e != 0 else '  ' for e in i))
        print('-'*35)

    def check_game_over(self):
        count = 0
        for i in self.card:
            for j in i:
                if j == '-':
                    count += 1
        if count == 15:
            return True
        else:
            return False

    def check_bochonok_comp(self, bochonok):
        for i in self.card:
            try:
                z = i.index(bochonok)
                i[z] = '-'
            except:
                pass

    def check_bochonok_user(self, bochonok, answer):
        tmp = True
        for i in self.card:
            try:
                z = i.index(bochonok)
                i[z] = '-'
                tmp = False
            except:
                pass
        if tmp and answer == 'y':
            return True
        if not tmp and answer != 'y':
            return True


class Bochonok:
    def __init__(self, count = 90, number = 0, ostatok = 0):
        self.number = number
        self.ostatok = ostatok
        self.bag = [x for x in range(1, count + 1)]

    def get_bochonok(self):
        try:
            id = random.randrange(0, len(self.bag))
            self.number = self.bag[id]
            self.bag.pop(id)
            self.ostatok = len(self.bag)
            return True
        except:
            print('Мешок пуст!')
            return False


class User:
    def __init__(self):
        self.name = defaultdict(list)
        self.sum_user = None
        self.sum_comp = None

    def sum_gamers(self):
        user = int(input("Введите, пожалуйста, количество пользователей (число): "))
        if isinstance(user, int):
            self.sum_user = user
        else:
            print('Вводить необходимо число')
        comp = int(input("Введите, пожалуйста, количество компьютерных игроков (число): "))
        if isinstance(comp, int):
            self.sum_comp = comp
        else:
            print('Вводить необходимо число')

    def get_name(self):
        for i in range(self.sum_user):
            name_user = input(f'Назовите имя пользователя {i+1}: ')
            self.name['User'].append(name_user)
        for i in range(self.sum_comp):
            self.name['Comp'].append(f'Компьютер {i+1}')

    def show_users(self):
        print(self.name)

u = User()
u.sum_gamers()
u.get_name()

if u.sum_user > 0:
    user_objs = [Card(name=u.name['User'][i]) for i in range(u.sum_user)]
    for i in range(len(user_objs)):
        user_objs[i].initialize_card()
if u.sum_comp > 0:
    comp_objs = [Card(name=u.name['Comp'][i]) for i in range(u.sum_comp)]
    for i in range(len(comp_objs)):
        comp_objs[i].initialize_card()  

bochonok = Bochonok()

games = True
while True:
    print()
    if bochonok.get_bochonok() and games:
        if u.sum_user:
            for i in user_objs:
                print(f'Новый бочонок: {bochonok.number} (осталось {bochonok.ostatok})')
                i.card_view_user(i.name)
                answer = input("Зачеркнуть цифру? (y/n) ")
                if answer == 'y':
                    if i.check_bochonok_user(bochonok.number, answer):
                        print(f'{i.name} проиграл!')
                        games = False
                        break
                        
                else:
                    if i.check_bochonok_user(bochonok.number, answer):
                        print(f'{i.name} проиграл!')
                        games = False
                        break

                if i.check_game_over():
                    print(f'Ты выграл: {i.name}')
                    games = False
                    break

        if u.sum_comp and games:   
            for i in comp_objs:
                print(f'Новый бочонок: {bochonok.number} (осталось {bochonok.ostatok})')
                i.card_view_comp(i.name)
                i.check_bochonok_comp(bochonok.number)
                if i.check_game_over():
                    print(f'{i.name} выграл!!!')
                    games = False
                    break
    else:
        break
    
