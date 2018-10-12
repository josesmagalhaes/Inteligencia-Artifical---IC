
dist = {
	'Bucharest': 		0,
	'Giurgiu': 			77,
	'Urziceni': 		80,
	'Pitesti': 			98,
	'Craiova': 			160,
	'Fagaras': 			178,
	'Rimnicu Vilcea': 	193,
	'Mehadia': 			241,
	'Dobreta': 			242,
	'Lugoj': 			244,
	'Sibiu': 			253,
	'Timisoara': 		329,
	'Arad': 			366,
	'Zerind': 			374,
	'Oradea': 			380
}



vizinhancas = {
	'Giurgiu': 			['Bucharest'	],
	'Fagaras':			['Bucharest', 	'Sibiu'		],
	'Lugoj': 			['Timisoara', 	'Mehadia'	],
	'Mehadia': 			['Dobreta', 	'Lugoj'		],
	'Oradea': 			['Zerind', 		'Sibiu'		],
	'Timisoara': 		['Arad', 		'Lugoj'		],
	'Zerind':			['Arad', 		'Oradea'	],
	'Arad': 			['Zerind', 		'Timisoara', 		'Sibiu'		],
	'Craiova': 			['Dobreta', 	'Rimnicu Vilcea', 	'Pitesti'	],
	'Pitesti': 			['Bucharest', 	'Rimnicu Vilcea', 	'Craiova'	],
	'Dobreta': 			['Mehadia', 			'Craiova'	],
	'Rimnicu Vilcea': 	['Pitesti', 	'Craiova', 			'Sibiu'		],
	'Bucharest': 		['Urziceni', 	'Giurgiu', 			'Pitesti', 		'Fagaras'			],
	'Sibiu': 			['Oradea', 		'Fagaras', 			'Arad', 		'Rimnicu Vilcea'	]
}

vizinhancas_ = {
	'Giurgiu': 		    {'Bucharest':90},
	'Fagaras':			{'Bucharest':211,'Sibiu':99},
	'Lugoj': 			{'Timisoara':111,'Mehadia':70},
	'Mehadia': 			{'Dobreta':75,'Lugoj':70},
	'Oradea': 			{'Zerind':71,'Sibiu':151},
	'Timisoara': 		{'Arad':118,'Lugoj':111},
	'Zerind':			{'Arad':75,'Oradea':71},
	'Arad': 			{'Zerind':75,'Timisoara':118,'Sibiu':140},
	'Craiova': 			{'Dobreta':120,'Rimnicu Vilcea':146,'Pitesti':138},
	'Pitesti': 			{'Bucharest':101,'Rimnicu Vilcea':97,'Craiova':138},
	'Dobreta': 			{'Mehadia':75,'Craiova':120},
	'Rimnicu Vilcea': 	{'Pitesti':97,'Craiova':146,'Sibiu':80},
	'Bucharest': 		{'Urziceni':85,'Giurgiu':90,'Pitesti':101,'Fagaras':211},
	'Sibiu': 			{'Oradea':151,'Fagaras':99,'Arad':140,'Rimnicu Vilcea':80}
}

global cidade_previa

def obter_melhor_vizinhanca(cidade):
	menor_distancia = 99999
	melhor_vizinhanca = None
	for cidade in vizinhancas[cidade]:
		if dist[cidade] < menor_distancia:
			menor_distancia = dist[cidade]
			melhor_vizinhanca = cidade
	return melhor_vizinhanca

def obter_melhor_vizinhanca_(cidade):
	global cidade_previa
	menor_distancia = 99999
	melhor_vizinhanca = None
	for cidade_local in vizinhancas[cidade]:
		if cidade_local == cidade_previa:
			continue
		distancia_do_destino = dist[cidade_local]
		tamanho_do_percurso = vizinhancas_[cidade][cidade_local]
		if menor_distancia > (distancia_do_destino/tamanho_do_percurso):
			menor_distancia = distancia_do_destino/tamanho_do_percurso
			melhor_vizinhanca = cidade_local
	return melhor_vizinhanca


def encontrar_melhor_caminho(iniciando_cidade, finalizando_cidade, ):

	cidade_atual = iniciando_cidade
	if cidade_atual == finalizando_cidade:
		print("Destino atingido!")
	else:
		proxima_cidade = obter_melhor_vizinhanca_(cidade_atual)
		print("\t", proxima_cidade)
		previous_city = proxima_cidade
		encontrar_melhor_caminho(proxima_cidade, finalizando_cidade)


def main():
	global cidade_previa
	cidade_inicio = "Zerind"
	cidade_previa = cidade_inicio
	cidade_final = "Bucharest"

	print("Saindo da cidade", cidade_inicio)
	encontrar_melhor_caminho(cidade_inicio, cidade_final)
	print(cidade_final)


if __name__ == "__main__":
	main()