
def pos_effect(clicks):
    pos_lst = list(clicks)
    sub = pos_lst[-1]
    for i in range(len(pos_lst)):
        pos_lst[i] -= sub
    div = float(pos_lst[0])
    for i in range(len(pos_lst)):
        pos_lst[i] = pos_lst[i]/div

    return pos_lst
