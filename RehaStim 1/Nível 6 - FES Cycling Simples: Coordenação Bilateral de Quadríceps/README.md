# Nível 6 — FES Cycling Simples: Coordenação Bilateral de Quadríceps

## 1. Visão Geral
O Nível 6 eleva a neuroprótese ao patamar de um sistema de reabilitação funcional complexo, o FES Cycling. O objetivo é automatizar a pedalada em umma Trike utilizando o estímulo sincronizado dos músculos do quadríceps de ambas as pernas. 

O sistema utiliza a leitura de ângulo da IMU (posicionada em um dos pé de vela, normalmente no esquerdo) para mapear o ciclo de 360° e disparar os pulsos de corrente elétrica nos momentos biomecanicamente eficientes para gerar torque.

---

## 2. Do Controle de Ângulo ao Ciclo de Pedalada

| Recurso | Nível 5 (Neuroprótese Simples) | Nível 6 (FES Cycling) |
| :--- | :--- | :--- |
| **Canais ativos** | 1 Canal (Unilateral) | **2 Canais** (Bilateral: Direita e Esquerda) |
| **Lógica de Disparo** | Função Degrau (ON/OFF por ângulo) | **Janelas de Ativação** (Mapeamento de 0° a 360°) |
| **Aplicação** | Extensão de joelho/cotovelo | Propulsão rítmica na Trike |
| **Complexidade** | Estímulo reativo | Estímulo coordenado e alternado |

---

## 3. Lógica de Controle: Janelas de Ativação

Para que o ciclismo ocorra, o estímulo não pode ser contínuo. Ele deve respeitar a biomecânica da pedalada, onde cada músculo atua em uma "janela" específica do giro. No código `fescycling_main.py`, as janelas são definidas da seguinte forma:

### Mapeamento do Ciclo (Exemplo usado Projeto)
* Considerando a IMU fixada no pé de vela esquerdo da trike, temos as sequintes angulações:
  * **Perna Direita (Canal 1):** Ativação entre **120° e 235°**. É a fase de descida, onde o quadríceps gera potência.
  * **Perna Esquerda (Canal 2):** Ativação entre **300° e 55°** (atravessando o ponto zero). Corresponde à fase de descida do pedal esquerdo.
  * **Zonas Mortas:** Intervalos onde nenhum canal é estimulado.


---

## 4. Modelagem Matemática Aplicada

### A. Sincronização Angular
Diferente do Nível 5, aqui precisamos tratar o ângulo como um ciclo contínuo. Se $\theta$ é o ângulo lido pela IMU, garantimos que ele esteja sempre no intervalo $[0, 360)$ para a lógica de decisão:
$$\theta_{\text{ciclo}} = \theta \pmod{360}$$

### B. Função de Controle Bilateral
A saída para os dois canais ($u_1, u_2$) é regida por funções de intervalo:

$$
u_1(\theta) =
\begin{cases}
\mathrm{ON} & 120^\circ \leq \theta \leq 235^\circ \\
\mathrm{OFF} & \mathrm{otherwise}
\end{cases}
$$

$$
u_2(\theta) =
\begin{cases}
\mathrm{ON} & \theta \geq 300^\circ \ \mathrm{or} \ \theta \leq 55^\circ \\
\mathrm{OFF} & \mathrm{otherwise}
\end{cases}
$$

---

## 5. Implementação no Código

### Módulo `fescycling_main.py`
Neste nível, o `main` gerencia listas de parâmetros para dois canais simultaneamente:
* `CHANNELS = [1, 2]`
* `PULSE_WIDTH_ON = [100, 100]` (µs)
* `PULSE_CURRENT_ON = [30, 30]` (mA) 

### Otimização de Performance
Para evitar atrasos na comunicação serial que poderiam desfigurar o ritmo da pedalada, o código utiliza:
* **`serial_port.reset_input_buffer()`**: Limpa dados antigos da IMU antes de cada leitura.
* **`stim.update_ccl(...)`**: Atualiza ambos os canais em um único pacote binário, reduzindo o tráfego na porta COM.

---

## 6. Perspectivas e Próximos Passos (Evolução do Sistema)

O Nível 6 consolidou a automação da pedalada assistida. Para os próximos estágios de desenvolvimento, o foco será o refinamento da eficiência motora e a complexidade do recrutamento muscular.

### A. Compensação Dinâmica de Atraso (Shift de Velocidade)
Atualmente, as janelas de ativação são fixas em relação ao ângulo lido. No entanto, devido à latência intrínseca da comunicação serial e à constante de tempo da contração muscular, em velocidades de pedalada mais altas, a força pode ser gerada fora do ponto ideal.
* **Objetivo:** Implementar um algoritmo de *shift* angular que antecipe o disparo da estimulação proporcionalmente à velocidade angular ($\omega$), garantindo que o pico de torque ocorra sempre na fase de descida do pedal.

### B. Recrutamento de Músculos Antagonistas (Isquiotibiais)
Para uma pedalada mais fluida e próxima da fisiológica, o sistema evoluirá de 2 para 4 canais de estimulação.
* **Objetivo:** Replicar a lógica de janelas para incluir os músculos **isquiotibiais** em conjunto com os quadríceps. Enquanto o quadríceps atua na fase de extensão (descida), os isquiotibiais serão ativados na fase de flexão (subida), aumentando a potência total gerada e melhorando a estabilidade da articulação do joelho.

### C. Controle Proporcional de Intensidade
Em vez de rajadas de corrente fixa, o sistema passará a modular a intensidade ($mA$) ou a largura de pulso ($\mu s$) dentro das janelas, suavizando o início da contração e reduzindo o impacto súbito no sistema musculoesquelético do usuário.

---
