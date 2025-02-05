#nome: Sergio Barboza dos Santos Júnior
# número USP: 12548751

import numpy as np
import matplotlib.pyplot as plt


def calcular_A(T):
    return 2.771 - 0.00523 * T


def gamma(A, x):
    return np.exp(A * (x ** 2))


def pressão_sat1(T):
    return np.exp(16.59158 - (3643.31 / (T - 33.424)))


def pressão_sat2(T):
    return np.exp(14.25326 - (2655.54 / (T - 53.424)))


def obter_temperatura_orvalho(P, x1, x2, tol=0.00001, T_min=250, T_max=400):
    while T_max - T_min > tol:
        temperatura = (T_min + T_max) / 2
        P1_sat = pressão_sat1(temperatura)
        P2_sat = pressão_sat2(temperatura)
        G1 = gamma(calcular_A(temperatura), x2)
        G2 = gamma(calcular_A(temperatura), x1)
        p_orvalho = 1 / ((x1 / (P1_sat * G1)) + (x2 / (P2_sat * G2)))

        if p_orvalho > P:
            T_max = temperatura
        else:
            T_min = temperatura

    return (T_min + T_max) / 2


def obter_temperatura_bolha(P, x1, x2, tol=0.00001, T_min=250, T_max=400):
    while T_max - T_min > tol:
        temperatura = (T_min + T_max) / 2
        P1_sat = pressão_sat1(temperatura)
        P2_sat = pressão_sat2(temperatura)
        G1 = gamma(calcular_A(temperatura), x2)
        G2 = gamma(calcular_A(temperatura), x1)
        p_bolha = P1_sat * G1 * x1 + P2_sat * G2 * x2

        if p_bolha > P:
            T_max = temperatura
        else:
            T_min = temperatura

    return (T_min + T_max) / 2


# Frações molares específicas para a tabela
frações_molares_tabela = [0, 0.2, 0.4, 0.6, 0.8, 1]
temperaturas_orvalho = []
temperaturas_bolha = []

# Pressão desejada
P = 202.66  # Exemplo de pressão desejada em kPa

# Cálculo das temperaturas para as frações molares específicas
for x1_i in frações_molares_tabela:
    x2_i = 1 - x1_i
    temperatura_orvalho = obter_temperatura_orvalho(P, x1_i, x2_i)
    temperatura_bolha = obter_temperatura_bolha(P, x1_i, x2_i)
    temperaturas_orvalho.append(temperatura_orvalho)
    temperaturas_bolha.append(temperatura_bolha)

# Exibir a tabela básica apenas para os pontos especificados
print("Fração Molar (x) | Temperatura de Orvalho (K) | Temperatura de Bolha (K)")
print("--------------------------------------------------------------")
for i in range(len(frações_molares_tabela)):
    print(f"{frações_molares_tabela[i]:<18} | {temperaturas_orvalho[i]:<25} | {temperaturas_bolha[i]:<25}")

# Criar uma gama de frações molares para o gráfico
frações_molares_grafico = np.arange(0, 1.01, 0.01)  # De 0 a 1 com passo de 0.01
temperaturas_orvalho_grafico = []
temperaturas_bolha_grafico = []

# Cálculo das temperaturas para o gráfico
for x1_i in frações_molares_grafico:
    x2_i = 1 - x1_i
    temperatura_orvalho = obter_temperatura_orvalho(P, x1_i, x2_i)
    temperatura_bolha = obter_temperatura_bolha(P, x1_i, x2_i)
    temperaturas_orvalho_grafico.append(temperatura_orvalho)
    temperaturas_bolha_grafico.append(temperatura_bolha)

# Plotar os resultados
plt.plot(frações_molares_grafico, temperaturas_orvalho_grafico, label='Curva de Orvalho', color='blue')
plt.plot(frações_molares_grafico, temperaturas_bolha_grafico, label='Curva de Bolha', color='red')

# Adicionar pontos específicos no gráfico
for x in frações_molares_tabela:
    y_orvalho = obter_temperatura_orvalho(P, x, 1 - x)
    y_bolha = obter_temperatura_bolha(P, x, 1 - x)
    plt.plot(x, y_orvalho, 'ro')  # Ponto para a curva de orvalho
    plt.plot(x, y_bolha, 'bo')  # Ponto para a curva de bolha
    plt.text(x, y_orvalho, f"{y_orvalho:.1f}", fontsize=8, verticalalignment='bottom', horizontalalignment='right')
    plt.text(x, y_bolha, f"{y_bolha:.1f}", fontsize=8, verticalalignment='top', horizontalalignment='right')

# Adicionar pontos de saturação T2 e T1
T2 = obter_temperatura_orvalho(P, 0, 1)  # Temperatura de saturação para x = 0
T1 = obter_temperatura_bolha(P, 1, 0)  # Temperatura de saturação para x = 1
P2_sat = pressão_sat2(T2)  # Pressão de saturação para x = 0
P1_sat = pressão_sat1(T1)  # Pressão de saturação para x = 1

plt.plot(0, T2, 'go', label='T2 (x=0)', markersize=8)  # Ponto T2
plt.plot(1, T1, 'mo', label='T1 (x=1)', markersize=8)  # Ponto T1
plt.text(0, T2, f"{T2:.1f}", fontsize=8, verticalalignment='bottom', horizontalalignment='right')
plt.text(1, T1, f"{T1:.1f}", fontsize=8, verticalalignment='bottom', horizontalalignment='right')

# Estilizando o gráfico
plt.xlabel('Frações molares')
plt.ylabel('Temperatura final (K)')
plt.title('Curva de Temperatura para Ponto de Orvalho e Bolha')
plt.legend()
plt.grid()
plt.show()
