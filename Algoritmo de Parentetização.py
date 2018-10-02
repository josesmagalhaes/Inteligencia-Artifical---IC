def produto_de_matrizes(p):
    """
    Retornar m e s.

     m [i] [j] é o número mínimo de multiplicações escalares necessárias para calcular o
     produto das matrizes A (i), A (i + 1), ..., A (j).

     s [i] [j] é o índice da matriz após o qual o produto é dividido em um
     parêntese ideal do produto da matriz.

     p [0 ... n] é uma lista tal que a matriz A (i) tem dimensões p [i - 1] x p [i].
    """
    tamanho = len(p)  # len(p) = número de matrizes + 1

    # m [i] [j] é o número mínimo de multiplicações necessárias para calcular o
    # produto das matrizes A (i), A (i + 1), ..., A (j)
    # s [i] [j] é a matriz após a qual o produto é dividido no mínimo
    # Número de multiplicações necessárias
    m = [[-1] * tamanho for _ in range(tamanho)]
    s = [[-1] * tamanho for _ in range(tamanho)]

    produto_de_matrizes_auxiliar(p, 1, tamanho - 1, m, s)

    return m, s


def produto_de_matrizes_auxiliar(p, inicio, fim, m, s):
    """
    Retorna o número mínimo de multiplicações escalares necessárias para calcular o
     produto das matrizes A (inicio), A (inicio + 1), ..., A (fim).

     O número mínimo de multiplicações escalares necessárias para calcular o
     produto das matrizes A (i), A (i + 1), ..., A (j) é armazenado em m [i] [j].

     O índice da matriz após o qual o produto acima é dividido em um valor de ótima
     patentetizaçao é armazenado em s [i] [j].

     p [0 ... n] é uma lista tal que a matriz A (i) tem dimensões p [i - 1] x p [i].
    """
    if m[inicio][fim] >= 0:
        return m[inicio][fim]

    if inicio == fim:
        q = 0
    else:
        q = float('inf')
        for k in range(inicio, fim):
            temp = produto_de_matrizes_auxiliar(p, inicio, k, m, s) \
                   + produto_de_matrizes_auxiliar(p, k + 1, fim, m, s) \
                   + p[inicio - 1] * p[k] * p[fim]
            if q > temp:
                q = temp
                s[inicio][fim] = k

    m[inicio][fim] = q
    return q


def imprimir_parentetizcao(s, inicio, fim):
    """
    Imprime o parêntese ótimo do produto de matriz A (inicio) x
     A (inicio + 1) x ... x A (fim).

     s [i] [j] é o índice da matriz após o qual o produto é dividido em uma
     parentetizaçao ideal do produto matriz.
    """
    if inicio == fim:
        print('M[{}]'.format(inicio), end='')
        return

    k = s[inicio][fim]

    print('(', end='')
    imprimir_parentetizcao(s, inicio, k)
    imprimir_parentetizcao(s, k + 1, fim)
    print(')', end='')


n = int(input('Digite o numero de matrizes: '))
p = []
for i in range(n):
    temp = int(input('Digite o numero de linhas da matriz {}: '.format(i + 1)))
    p.append(temp)
temp = int(input('Digite o numero de colunas da matriz {}: '.format(n)))
p.append(temp)

m, s = produto_de_matrizes(p)
print('O numero de multiplicações necessárias é:', m[1][n])
print('A parententização ótima para o caso é: ', end='')
imprimir_parentetizcao(s, 1, n)

#Codigo desenvolvido com carinho e noites de sono perdidas por:
#José de Sousa Magalhaes
#Acadêmico do curso de Sistemas de Informaçao da UFPI.