import numpy as np

# Define o ambiente
num_estados = 8
num_acoes = 5
Q = np.zeros((num_estados, num_acoes))

# Define os parâmetros de aprendizado
taxa_aprendizado = 0.7
fator_desconto = 0.9
exploracao = 0.15

# Define as recompensas
recompensas = np.array([[-2, -2, -2, -2, -2],
                         [-2, -2, -2, -2, -2],
                         [-2, -2, -2, -2, -2],
                         [-2, -2, -2, -2, -2],
                         [-2, -2, -2, -2, -2],
                         [-2, -2, -2, -2, -2],
                         [-2, -2, -2, -2, -2],
                         [-2, -2, -2, -2, 150]])

# Treina o agente
for i in range(1500):
    estado = np.random.randint(0, num_estados)
    if np.random.uniform(0, 1) < exploracao:
        acao = np.random.randint(0, num_acoes)
    else:
        acao = np.argmax(Q[estado])
    proximo_estado = np.random.randint(0, num_estados)
    Q[estado, acao] = Q[estado, acao] + taxa_aprendizado * (recompensas[estado, acao] + fator_desconto * np.max(Q[proximo_estado]) - Q[estado, acao])

# Imprime a tabela Q
print(f"Tabela Q: {Q}")
