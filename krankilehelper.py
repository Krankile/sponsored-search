#Returns a number between 0,1 inclusive for each weigthing of position
# , based on last round history
def pos_effect(clicks):
    pos_lst = list(clicks)
    sub = pos_lst[-1]
    #make all values -= last postion clicks, makes all values weakly greater than 0
    for i in range(len(pos_lst)):
        pos_lst[i] -= sub
    div = float(pos_lst[0])
    #Normalize all numbers, make all numbers weakly smaller than 1
    for i in range(len(pos_lst)):
        pos_lst[i] = pos_lst[i]/div

    return pos_lst
