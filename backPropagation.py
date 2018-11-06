import random
import math

#
# Forma abreviada:
# "dp_" como um prefixo variável significa "derivada parcial"
# "d_" como um prefixo variável significa "derivado"
# "_wrt_" é uma abreviação de "with respect to" ou seja com pespeito a
# "w_ho" e "w_ih" são o índice de pesos dos neurônios ocultos
# para os neurônios da camada de saída e de entrada para os neurônios da camada oculta, respectivamente
#
# Referências de comentário:


class RedeNeural:
    TAXA_DE_APRENDIZAGEM = 0.5

    def __init__(self, numero_entrada, numero_escondido, numero_saida, peso_camada_escondida = None, vies_camada_oculta = None, peso_camada_saida = None, vies_camada_saida = None):
        self.num_inputs = numero_entrada

        self.hidden_layer = Camada_de_Neuronio(numero_escondido, vies_camada_oculta)
        self.output_layer = Camada_de_Neuronio(numero_saida, vies_camada_saida)

        self.peso_inicial_de_entrada_neuronios_de_camada_oculta(peso_camada_escondida)
        self.pesos_iniciais_de_neuronios_da_camada_oculta_para_neuronios_da_camada_de_saida(peso_camada_saida)

    def peso_inicial_de_entrada_neuronios_de_camada_oculta(self, camada_peso_oculta):
        numero_pesos = 0
        for h in range(len(self.hidden_layer.neurons)):
            for i in range(self.num_inputs):
                if not camada_peso_oculta:
                    self.hidden_layer.neurons[h].weights.append(random.random())
                else:
                    self.hidden_layer.neurons[h].weights.append(camada_peso_oculta[numero_pesos])
                numero_pesos += 1

    def pesos_iniciais_de_neuronios_da_camada_oculta_para_neuronios_da_camada_de_saida(self, camada_peso_saida):
        numero_pesos = 0
        for o in range(len(self.output_layer.neurons)):
            for h in range(len(self.hidden_layer.neurons)):
                if not camada_peso_saida:
                    self.output_layer.neurons[o].weights.append(random.random())
                else:
                    self.output_layer.neurons[o].weights.append(camada_peso_saida[numero_pesos])
                numero_pesos += 1

    def inspecionar(self):
        print('------')
        print('* Entradas: {}'.format(self.num_inputs))
        print('------')
        print('Camada oculta')
        self.hidden_layer.inspecionar()
        print('------')
        print('* Camada saida')
        self.output_layer.inspecionar()
        print('------')

    def alimentar_adiante(self, entradas):
        saida_camada_oculta = self.hidden_layer.seguir_adiante(entradas)
        return self.output_layer.seguir_adiante(saida_camada_oculta)

        # Usa aprendizado on-line, ou seja, atualiza os pesos após cada caso de treinamento
    def ensinar(self, entrada_ensino, saida_ensino):
        self.alimentar_adiante(entrada_ensino)

        # 1. Saída de deltas de neurônios
        erros_de_pd_pesos_escondidos_neuronios_total_entradas = [0] * len(self.output_layer.neurons)
        for o in range(len(self.output_layer.neurons)):

            # ∂E/∂zⱼ
            erros_de_pd_pesos_escondidos_neuronios_total_entradas[o] = self.output_layer.neurons[o].erro_calculo_dp_total_de_entradas(saida_ensino[o])

        # 2. Os deltas do neurônio oculto
        erros_de_pd_pesos_escondidos_neuronios_total_entradas = [0] * len(self.hidden_layer.neurons)
        for h in range(len(self.hidden_layer.neurons)):

            # Precisamos calcular a derivada do erro em relação à saída de cada neurônio de camada oculta
            # dE/dyⱼ = Σ ∂E/∂zⱼ * ∂z/∂yⱼ = Σ ∂E/∂zⱼ * wᵢⱼ
            erro_d_peso_oculto_neuronio_saida = 0
            for o in range(len(self.output_layer.neurons)):
                erro_d_peso_oculto_neuronio_saida += erros_de_pd_pesos_escondidos_neuronios_total_entradas[o] * self.output_layer.neurons[o].weights[h]

            # ∂E/∂zⱼ = dE/dyⱼ * ∂zⱼ/∂
            erros_de_pd_pesos_escondidos_neuronios_total_entradas[h] = erro_d_peso_oculto_neuronio_saida * self.hidden_layer.neurons[h].calculate_pd_total_entradas_com_entradas()

            # 3. Atualizar pesos de neurônios de saída
        for o in range(len(self.output_layer.neurons)):
            for w_ho in range(len(self.output_layer.neurons[o].weights)):

                # ∂Eⱼ/∂wᵢⱼ = ∂E/∂zⱼ * ∂zⱼ/∂wᵢⱼ
                pd_erro_peso = erros_de_pd_pesos_escondidos_neuronios_total_entradas[o] * self.output_layer.neurons[o].calculate_pd_total_entrada_com_pesos(w_ho)

                # Δw = α * ∂Eⱼ/∂wᵢ
                self.output_layer.neurons[o].weights[w_ho] -= self.TAXA_DE_APRENDIZAGEM * pd_erro_peso

            # 4. Atualizar pesos de neurônios ocultos
        for h in range(len(self.hidden_layer.neurons)):
            for w_ih in range(len(self.hidden_layer.neurons[h].weights)):

                # ∂Eⱼ/∂wᵢ = ∂E/∂zⱼ * ∂zⱼ/∂wᵢ
                pd_erro_peso = erros_de_pd_pesos_escondidos_neuronios_total_entradas[h] * self.hidden_layer.neurons[h].calculate_pd_total_entrada_com_pesos(w_ih)

                # Δw = α * ∂Eⱼ/∂wᵢ
                self.hidden_layer.neurons[h].weights[w_ih] -= self.TAXA_DE_APRENDIZAGEM * pd_erro_peso

    def calculo_erro_total(self, passos_ensino):
        total_de_erros = 0
        for t in range(len(passos_ensino)):
            entradas_de_ensino, saidas_de_ensino = passos_ensino[t]
            self.alimentar_adiante(entradas_de_ensino)
            for o in range(len(saidas_de_ensino)):
                total_de_erros += self.output_layer.neurons[o].calculo_de_erro(saidas_de_ensino[o])
        return total_de_erros

class Camada_de_Neuronio:
    def __init__(self, numero_de_neuronios, vies):

        # Cada neurônio em uma camada compartilha os mesmos vies
        self.bias = vies if vies else random.random()

        self.neurons = []
        for i in range(numero_de_neuronios):
            self.neurons.append(Neuronio(self.bias))

    def inspecionar(self):
        print('Neuronios:', len(self.neurons))
        for n in range(len(self.neurons)):
            print(' Neuronio', n)
            for w in range(len(self.neurons[n].weights)):
                print('  Peso:', self.neurons[n].weights[w])
            print('  Vies:', self.bias)

    def seguir_adiante(self, inputs):
        saidas = []
        for neuron in self.neurons:
            saidas.append(neuron.calculo_de_saidas(inputs))
        return saidas

    def obter_saida(self):
        saidas = []
        for neuron in self.neurons:
            saidas.append(neuron.output)
        return saidas

class Neuronio:
    def __init__(self, vies):
        self.bias = vies
        self.weights = []

    def calculo_de_saidas(self, saidas):
        self.inputs = saidas
        self.output = self.esmagar(self.calculo_total_de_entradas())
        return self.output

    def calculo_total_de_entradas(self):
        total = 0
        for i in range(len(self.inputs)):
            total += self.inputs[i] * self.weights[i]
        return total + self.bias

    # Aplique a função logística para esmagar a saída do neurônio
    # O resultado é por vezes referido como 'net' [2] ou 'net' [1]
    def esmagar(self, total_entradas):
        return 1 / (1 + math.exp(-total_entradas))

    #
    # Determine quanto a entrada total do neurônio precisa mudar para se aproximar da saída esperada
    # Agora que temos a derivada parcial do erro em relação à saída (∂E / ∂yⱼ) e
    # a derivada da saída em relação à entrada líquida total (dyⱼ / dzⱼ) podemos calcular
    # a derivada parcial do erro em relação à entrada líquida total.
    # Esse valor também é conhecido como o delta (δ) [1]
    # δ = ∂E/∂zⱼ = ∂E/∂yⱼ * dyⱼ/dzⱼ
    #
    def erro_calculo_dp_total_de_entradas(self, alvo_saida):
        return self.erro_calculo_dp_saida(alvo_saida) * self.calculate_pd_total_entradas_com_entradas();

    # O erro de cada neurônio é calculado pelo método do Erro Quadrático Médio:
    def calculo_de_erro(self, alvo_saida):
        return 0.5 * (alvo_saida - self.output) ** 2

    # A derivada parcial do erro em relação à saída real é calculada por:
    # = 2 * 0.5 * (saída de destino - saída real) ^ (2 - 1) * -1
    # = - (saída de destino - saída real)
    #
    # O artigo da Wikipédia sobre retropropagação [1] simplifica para o seguinte, mas a maioria dos outros materiais de aprendizagem não [2]
    # = saída real - saída de destino
    #
    # Alternativa, você pode usar (target-output), mas então precisa adicioná-la durante a retropropagação [3]
    #
    # Observe que a saída real do neurônio de saída é geralmente escrita como yⱼ e a saída de destino como tⱼ então:
    # = ∂E/∂yⱼ = -(tⱼ - yⱼ)

    def erro_calculo_dp_saida(self, alvo_saida):
        return -(alvo_saida - self.output)

    # A entrada líquida total no neurônio é esmagada usando a função logística para calcular a saída do neurônio:
    # yⱼ = φ = 1 / (1 + e ^ (- zⱼ))
    # Observe que onde ⱼ representa a saída dos neurônios em qualquer camada que estamos olhando e ᵢ representa a camada abaixo dela
    #
    # A derivada (não derivada parcial, uma vez que existe apenas uma variável) da saída é:
    # dyⱼ/dzⱼ = yⱼ * (1 - yⱼ)

    def calculate_pd_total_entradas_com_entradas(self):
        return self.output * (1 - self.output)

    # A entrada líquida total é a soma ponderada de todas as entradas para o neurônio e seus respectivos pesos:
    # = zⱼ = netⱼ = x₁w₁ + x₂w₂ ...
    #
    # A derivada parcial da entrada líquida total com o respectivo peso (com todo o resto mantido constante) e então:
    # = ∂zⱼ/∂wᵢ = alguma constante + 1 * xᵢw₁^(1-0) + alguma constante ... = xᵢ

    def calculate_pd_total_entrada_com_pesos(self, index):
        return self.inputs[index]

###

nn = RedeNeural(2, 2, 2, peso_camada_escondida=[0.15, 0.2, 0.25, 0.3], vies_camada_oculta=0.35, peso_camada_saida=[0.4, 0.45, 0.5, 0.55], vies_camada_saida=0.6)
for i in range(10000):
    nn.ensinar([0.05, 0.1], [0.01, 0.99])
    print(i, round(nn.calculo_erro_total([[[0.05, 0.1], [0.01, 0.99]]]), 9))

# EXEMPLO:

# passos_de_ensino = [
#     [[0, 0], [0]],
#     [[0, 1], [1]],
#     [[1, 0], [1]],
#     [[1, 1], [0]]
# ]

# nn = redeNeural(len(passos_de_ensino[0][0]), 5, len(passos_de_ensino[0][1]))
# for i in range(10000):
#     entradas_ensino, saidas_ensino = random.choice(passos_de_ensino)
#     nn.ensinar(entradas_ensino, saidas_ensino)
#     print(i, nn.calculo_erro_total(passos_de_ensino))