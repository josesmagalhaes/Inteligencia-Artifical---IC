# USO:
# alphabeta (entrada, início, superior, inferior)
#
# Onde:
# "entrada" é uma árvore de entrada do formulário de lista.
# "início" é o número do nó raiz. Então, 0 ou 1 (0 se raiz for MAX, 1 se raiz for MIN)
# "lim_superiorBeta" é o limite superior para beta. Configure isso para algo maior que qualquer valor em sua árvore
# "lim_inferiorBeta" é o limite inferior para beta. Defina isto como algo menor que qualquer valor em sua árvore
#
# A função retorna os valores alfa e beta raiz, bem como o resultado e o número de
# 'podas' que ocorreram.

# This is the arvore we are working with
arvore = [[[8, 7, 3], [9, 1, 6]], [[9, 4, 1], [1, 3, 5], [3, 9, 2], [6, 5, 2], [1, 2, 3], [9, 7, 2], [16, 5, 4]]]
raiz = 8
poda = 0


def filhas(ramo, profundidade, alpha, beta):
    global arvore
    global raiz
    global poda
    i = 0
    for filha in ramo:
        if type(filha) is list:
            (nalpha, nbeta) = filhas(filha, profundidade + 1, alpha, beta)
            if profundidade % 2 == 1:
                beta = nalpha if nalpha < beta else beta
            else:
                alpha = nbeta if nbeta > alpha else alpha
            ramo[i] = alpha if profundidade % 2 == 0 else beta
            i += 1
        else:
            if profundidade % 2 == 0 and alpha < filha:
                alpha = filha
            if profundidade % 2 == 1 and beta > filha:
                beta = filha
            if alpha >= beta:
                poda += 1
                break
    if profundidade == raiz:
        arvore = alpha if raiz == 0 else beta
    return (alpha, beta)


def alphabeta(em_arvore=arvore, inicio=raiz, lim_superiorBeta=16, lim_inferiorBeta=1):
    global arvore
    global poda
    global raiz

    (alpha, beta) = filhas(arvore, inicio, lim_superiorBeta, lim_inferiorBeta)

    if __name__ == "__main__":
        print("Valores minimax (alpha, beta): ", alpha, beta)
        print("Avaliações necessárias: : ", poda)

    return (alpha, beta, arvore, poda)


if __name__ == "__main__":
    alphabeta(None)