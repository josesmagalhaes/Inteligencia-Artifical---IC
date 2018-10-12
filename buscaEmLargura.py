def dfs_recursiva(grafo, start, caminho=[]):
  '''profundidade recursiva da primeira pesquisa do início'''
  caminho= caminho + [start]
  for no in grafo[start]:
    if not no in caminho:
      caminho=dfs_recursiva(grafo, no, caminho)
  return caminho

def busca_em_profundidade(grafo, inicio, caminho=[]):
  '''profundidade iterativa da primeira busca de casa'''
  q=[inicio]
  while q:
    v=q.pop(0)
    if v not in caminho:
      caminho= caminho + [v]
      q= grafo[v] + q
  return caminho

def busca_em_largura(grafo, inicio, caminho=[]):
  '''largura iterativa da primeiro pesquisa de inicio'''
  q=[inicio]
  while q:
    v=q.pop(0)
    if not v in caminho:
      caminho= caminho + [v]
      q= q + grafo[v]
  return caminho

'''
   +---- A
   |   /   \
   |  B--D--C
   |   \ | /
   +---- E
'''
graph = {'A':['B','C'],'B':['D','E'],'C':['D','E'],'D':['E'],'E':['A']}
print ('Busca em profundidade: ', busca_em_profundidade(graph, 'A'))
print ('Busca em largura: ', busca_em_largura(graph, 'A'))