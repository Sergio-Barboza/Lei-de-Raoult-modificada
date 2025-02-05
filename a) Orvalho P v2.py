#nome: Sergio Barboza dos Santos Júnior
# número USP: 12548751

import numpy as np
import matplotlib.pyplot as plt

# Função para calcular o parâmetro A
def calcular_A(T):
    return 2.771 - 0.00523 * T

# Função para calcular o fator de atividade gamma
def gamma(A, y):
    return np.exp(A * (y ** 2))

# Funções para calcular a pressão de saturação
def pressão_sat1(T):
    return np.exp(16.59158 - (3643.31 / (T - 33.424)))

def pressão_sat2(T):
    return np.exp(14.25326 - (2655.54 / (T - 53.424)))

# Função para calcular a pressão pelo método de Raoult
def Orvalho(y1, y2, P1, P2, G1, G2):
    return 1 / ((y1 / (P1 * G1)) + (y2 / (P2 * G2)))

# Função para calcular a bolha pelo método de Raoult
def Bolha(x1, x2, P1, P2, G1, G2):
    return x1 * P1 * G1 + x2 * P2 * G2

# Temperatura fixa
T = 330  # Kelvin (K)

# Fracções molares (x1 para bolha, y1 para orvalho)
x1 = np.linspace(0, 1, 1000)
y1 = np.linspace(0, 1, 1000)
x2 = 1 - x1
y2 = 1 - y1

# Lista para armazenar as pressões
pressões_bolha = []
pressões_orvalho = []

# Iteração sobre as frações molares para calcular a pressão de bolha e orvalho
for x1_i, x2_i, y1_i, y2_i in zip(x1, x2, y1, y2):
    A = calcular_A(T)

    # Calcular fator de atividade
    G1_bolha = gamma(A, x2_i)
    G2_bolha = gamma(A, x1_i)
    G1_orvalho = gamma(A, y2_i)
    G2_orvalho = gamma(A, y1_i)

    # Calcular pressões de saturação
    P1_sat = pressão_sat1(T)
    P2_sat = pressão_sat2(T)

    # Calcular pressão de bolha e orvalho
    P_bolha = Bolha(x1_i, x2_i, P1_sat, P2_sat, G1_bolha, G2_bolha)
    P_orvalho = Orvalho(y1_i, y2_i, P1_sat, P2_sat, G1_orvalho, G2_orvalho)

    # Armazenar os valores
    pressões_bolha.append(P_bolha)
    pressões_orvalho.append(P_orvalho)

# Criar o gráfico das curvas de Bolha e Orvalho
plt.plot(x1, pressões_bolha, label='Curva de Bolha', color='blue')
plt.plot(y1, pressões_orvalho, label='Curva de Orvalho', color='red')

# Adicionar pontos de pressão de saturação
P1_sat = pressão_sat1(T)  # Pressão de saturação do componente 1
P2_sat = pressão_sat2(T)  # Pressão de saturação do componente 2

# Plotar P2_sat quando x = 0 e P1_sat quando x = 1
plt.scatter([0], [P2_sat], color='green', label='P2_sat (x=0)', zorder=5)
plt.scatter([1], [P1_sat], color='orange', label='P1_sat (x=1)', zorder=5)

# Configurações do gráfico
plt.title('Diagrama de Pressão de Bolha e Orvalho')
plt.xlabel('Fração Molar')
plt.ylabel('Pressão (kPa)')
plt.grid(True)
plt.legend()

# Adicionar valores de pressão nos pontos específicos
pontos_especificos = [0, 0.2, 0.4, 0.6, 0.8, 1]
for ponto in pontos_especificos:
    # Calcular pressão de bolha
    A = calcular_A(T)
    G1_bolha = gamma(A, 1 - ponto)  # Complemento de ponto
    G2_bolha = gamma(A, ponto)
    P1_sat = pressão_sat1(T)
    P2_sat = pressão_sat2(T)
    P_bolha = Bolha(ponto, 1 - ponto, P1_sat, P2_sat, G1_bolha, G2_bolha)

    # Calcular pressão de orvalho
    G1_orvalho = gamma(A, 1 - ponto)
    G2_orvalho = gamma(A, ponto)
    P_orvalho = Orvalho(ponto, 1 - ponto, P1_sat, P2_sat, G1_orvalho, G2_orvalho)

    # Adicionar valores de pressão no gráfico
    plt.text(ponto, P_bolha, f'P={P_bolha:.2f} kPa', fontsize=8, verticalalignment='bottom',
             horizontalalignment='right', color='blue')
    plt.text(ponto, P_orvalho, f'P={P_orvalho:.2f} kPa', fontsize=8, verticalalignment='top',
             horizontalalignment='right', color='red')

# Mostrar a tabela de resultados
print("x/y | Pressão de Orvalho (K) | Pressão de Bolha (K)")
print("--------------------------------------------------------------")
for ponto in pontos_especificos:
    # Calcular pressão de bolha
    A = calcular_A(T)
    G1_bolha = gamma(A, 1 - ponto)  # Complemento de ponto
    G2_bolha = gamma(A, ponto)
    P1_sat = pressão_sat1(T)
    P2_sat = pressão_sat2(T)
    P_bolha = Bolha(ponto, 1 - ponto, P1_sat, P2_sat, G1_bolha, G2_bolha)

    # Calcular pressão de orvalho
    G1_orvalho = gamma(A, 1 - ponto)
    G2_orvalho = gamma(A, ponto)
    P_orvalho = Orvalho(ponto, 1 - ponto, P1_sat, P2_sat, G1_orvalho, G2_orvalho)

    # Imprimir valores para cada ponto específico
    print(f"{ponto:<5} {P_bolha:<25.6f} {P_orvalho:<25.6f}")

# Pausar brevemente para garantir que a tabela apareça antes do gráfico
plt.pause(0.001)

# Mostrar o gráfico
plt.show()
