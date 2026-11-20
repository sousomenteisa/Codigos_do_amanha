import matplotlib.pyplot as plt
#1. Dados simples do cotidiano
dias = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta']
cafes_tomados = [2, 4, 3, 5, 1]
#2. Criando o gráfico
plt.plot(dias, cafes_tomados, marker='o')
#3. Nomeando cada pedaço que você explicou
plt.title('Consumo de Café Durante a Semana') #Manchete
plt.xlabel('Dias da Semana') #Eixo horizonta(x)
plt.ylabel('Quantidade de Xícaras') #Eixo vertical(y)
#4. Exibindo o gráfico
plt.show()