from random import randint

class Level():
    def __init__(self):
        pass

    def add_exp(self, exp: int, give_exp: any):
        give_exp: int = give_exp if type(give_exp) is int else randint(give_exp[0], give_exp[-1])
        return exp + give_exp
