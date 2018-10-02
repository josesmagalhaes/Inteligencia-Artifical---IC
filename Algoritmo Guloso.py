moedas=[]#lista para armazenar as moedas.
num=int(input("Quantas moedas voce possui: "))#Variavel que recebe a quantidade de moedas.
for i in range(num):#laço para preencher o vetor com as moedas digitadas pelo usuário.
   moe = int(input("Digite a primeira moeda: "))#moedas digitadas pelo usuario.
   moedas.append(moe)
total = 0#total de moedas usadas, iniciando com zero.
troco = int(input("Qual troco voce deseja passar: "))#troco a ser passado com a quantidade de moedas.

for i in range(len(moedas)):#laço para verificar com metodo guloso a quantidade de minima de moedas.
    num_moedas = troco // moedas[i]#necessario fazer divisao inteira para garantir precisão.
    troco -= num_moedas * moedas[i]
    total+=num_moedas

print("O total de moedas usadas foram",total)#impressao das moedas.

#Codigo desenvolvido com carinho e noites de sono perdidas por:
#José de Sousa Magalhaes
#Acadêmico do curso de Sistemas de Informaçao da UFPI.
