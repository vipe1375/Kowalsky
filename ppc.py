def play():
    liste_coups = []

def choix_coup(prob_feuille, prob_pierre, prob_ciseaux):
    l = [prob_feuille, prob_pierre, prob_ciseaux]
    m = l.index(max(l))
    if m == 0:
        coup = 'ciseaux'
    elif m==1:
        coup = 'feuille'
    else:
        coup = 'pierre'
    return coup