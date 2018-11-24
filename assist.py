# assist.py contains functions for assist mode

# prints possible melds from highlighted melds
def isMeld(data):
    melds = logic.checkMelds(data.highlighted)
    if melds != []:
        print(melds)


L = [3,4,5, 4]
L.remove(4)
print(L)