import random
import math

objetivo = [[1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]]


def index(item, seq):
    """Função auxiliar que retorna -1 para o valor de índice não encontrado de uma seq"""
    try:
        return seq.index(item)
    except:
        return -1


class OitoPuzzle:
    def __init__(self):
        # valor heurístico
        self._hval = 0
        # profundidade de pesquisa da instância atual
        self._depth = 0
        # nó pai no caminho de pesquisa
        self._parent = None
        self.adj_matrix = []
        for i in range(3):
            self.adj_matrix.append(objetivo[i][:])

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        else:
            return self.adj_matrix == other.adj_matrix

    def __str__(self):
        res = ''
        for row in range(3):
            res += ' '.join(map(str, self.adj_matrix[row]))
            res += '\r\n'
        return res

    def _clone(self):
        p = OitoPuzzle()
        for i in range(3):
            p.adj_matrix[i] = self.adj_matrix[i][:]
        return p

    def obter_movimentos_legais(self):
        """Retorna a lista de tuplas com as quais o espaço livre pode
         ser trocado"""
        # obtem linha e coluna da peça vazia
        row, col = self.encontrar(0)
        free = []

        # descobrir quais peças podem se mover
        if row > 0:
            free.append((row - 1, col))
        if col > 0:
            free.append((row, col - 1))
        if row < 2:
            free.append((row + 1, col))
        if col < 2:
            free.append((row, col + 1))

        return free

    def gerar_movimentos(self):
        free = self.obter_movimentos_legais()
        zero = self.encontrar(0)

        def trocar_e_clonar(a, b):
            p = self._clone()
            p.troca(a, b)
            p._depth = self._depth + 1
            p._parent = self
            return p

        return map(lambda pair: trocar_e_clonar(zero, pair), free)

    def gerar_caminho_solucao(self, path):
        if self._parent == None:
            return path
        else:
            path.append(self)
            return self._parent.gerar_caminho_solucao(path)

    def resolve(self, h):
        """Executa uma pesquisa * para o estado da meta.
         h (puzzle) - função heurística, retorna um inteiro
        """

        def resolvido(puzzle):
            return puzzle.adj_matrix == objetivo

        openl = [self]
        closedl = []
        move_count = 0
        while len(openl) > 0:
            x = openl.pop(0)
            move_count += 1
            if (resolvido(x)):
                if len(closedl) > 0:
                    return x.gerar_caminho_solucao([]), move_count
                else:
                    return [x]

            succ = x.gerar_movimentos()
            idx_open = idx_closed = -1
            for move in succ:
                # Já vimos este nó?
                idx_open = index(move, openl)
                idx_closed = index(move, closedl)
                hval = h(move)
                fval = hval + move._depth

                if idx_closed == -1 and idx_open == -1:
                    move._hval = hval
                    openl.append(move)
                elif idx_open > -1:
                    copy = openl[idx_open]
                    if fval < copy._hval + copy._depth:
                        # copiar os valores dos movimentos sobre os existentes
                        copy._hval = hval
                        copy._parent = move._parent
                        copy._depth = move._depth
                elif idx_closed > -1:
                    copy = closedl[idx_closed]
                    if fval < copy._hval + copy._depth:
                        move._hval = hval
                        closedl.remove(copy)
                        openl.append(move)

            closedl.append(x)
            openl = sorted(openl, key=lambda p: p._hval + p._depth)

        # se o estado acabado não foi encontrado, retorna uma falha
        return [], 0

    def embaralhar(self, step_count):
        for i in range(step_count):
            row, col = self.encontrar(0)
            free = self.obter_movimentos_legais()
            target = random.choice(free)
            self.troca((row, col), target)
            row, col = target

    def encontrar(self, value):
        """retorna a linha, coordenadas da coluna do valor especificado
            no gráfico"""
        if value < 0 or value > 8:
            raise Exception("Valor fora do alcance.")

        for row in range(3):
            for col in range(3):
                if self.adj_matrix[row][col] == value:
                    return row, col

    def espreita(self, row, col):
        """retorna o valor na linha e coluna especificadas"""
        return self.adj_matrix[row][col]

    def chuta(self, row, col, value):
        """define o valor na linha e coluna especificadas"""
        self.adj_matrix[row][col] = value

    def troca(self, pos_a, pos_b):
        """troca valores nas coordenadas especificadas"""
        temp = self.espreita(*pos_a)
        self.chuta(pos_a[0], pos_a[1], self.espreita(*pos_b))
        self.chuta(pos_b[0], pos_b[1], temp)


def heuristico(puzzle, item_total_calc, total_calc):
    """
     Modelo heurístico que fornece a posição atual e de destino para cada número e
     função total.

     Parâmetros:
     puzze - puzze
     item_total_calc - recebe 4 parâmetros: linha atual, linha de destino, col atual, col.
     Retorna int.
     total_calc - recebe 1 parâmetro, a soma de item_total_calc sobre todas as entradas e retorna int.
     Este é o valor da função heurística
    """
    t = 0
    for row in range(3):
        for col in range(3):
            val = puzzle.espreita(row, col) - 1
            target_col = val % 3
            target_row = val / 3

            # account for 0 as blank
            if target_row < 0:
                target_row = 2

            t += item_total_calc(row, target_row, col, target_col)

    return total_calc(t)


# algumas funções heurísticas, sendo o melhor a distância manhattan padrão neste caso, como se trata
# mais próximo de maximizar a distância estimada enquanto ainda é admissível.

def h_manhattan(puzzle):
    return heuristico(puzzle,
                      lambda r, tr, c, tc: abs(tr - r) + abs(tc - c),
                      lambda t: t)


def h_manhattan_lsq(puzzle):
    return heuristico(puzzle,
                      lambda r, tr, c, tc: (abs(tr - r) + abs(tc - c)) ** 2,
                      lambda t: math.sqrt(t))


def h_linear(puzzle):
    return heuristico(puzzle,
                      lambda r, tr, c, tc: math.sqrt(math.sqrt((tr - r) ** 2 + (tc - c) ** 2)),
                      lambda t: t)


def h_linear_lsq(puzzle):
    return heuristico(puzzle,
                      lambda r, tr, c, tc: (tr - r) ** 2 + (tc - c) ** 2,
                      lambda t: math.sqrt(t))


def h_default(puzzle):
    return 0

def main():
    p = OitoPuzzle()
    p.embaralhar(20)
    print
    p

    path, count = p.resolve(h_manhattan)
    path.reverse()
    for i in path:
        print
        i

    print ("Resolvido com a distância de Manhattan explorando", count, "estágios")
    path, count = p.resolve(h_manhattan_lsq)
    print ("Resolvido com Manhattan por mínimos quadrados explorando", count, "estágios")
    path, count = p.resolve(h_linear)
    print("Resolvido com a distância linear explorando", count, "estágios")
    path, count = p.resolve(h_linear_lsq)
    print("Resolvido com mínimos quadrados lineares explorando", count, "estágios")
    print("Resultado final atingido!")
    for i in range(len(objetivo)):
        for j in range(len(objetivo[i])):
            print(objetivo[i][j], end=' ')
        print()

if __name__ == "__main__":
    main()

    # Codigo desenvolvido com carinho e noites de sono perdidas por:
    # José de Sousa Magalhaes
    # Acadêmico do curso de Sistemas de Informaçao da UFPI.
