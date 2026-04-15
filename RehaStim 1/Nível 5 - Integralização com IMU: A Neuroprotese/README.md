# Nível 5 - Integralização com IMU: A Neuroprotese

## 1. Visão Geral e Evolução
Enquanto o Nível 4 introduziu uma máquina de estados controlada manualmente, o **Nível 5** marca a transição para uma **Neuroprótese Ativa**. O sistema deixa de depender exclusivamente de comandos humanos e passa a ser regido por **Feedback Biomecânico**.

Nesta arquitetura de **Malha Fechada**, o software monitora a cinemática do membro via sensores de inércia (IMU) e decide autonomamente quando disparar a estimulação. É o alicerce para o desenvolvimento de órteses inteligentes e tecnologias assistivas para reabilitação.

---

## 2. Comparativo Tecnológico: Nível 4 vs. Nível 5

| Recurso | Nível 4 (Máquina de Estados) | Nível 5 (Neuroprótese) |
| :--- | :--- | :--- |
| **Gatilho de Transição** | Manual (Teclas `S`, `P`, `L`) | **Automático** (Ângulo da IMU) |
| **Entrada de Dados** | Apenas Teclado | Teclado + Sensores IMU (Yost Labs) |
| **Tipo de Malha** | Malha Aberta (Operador no controle) | **Malha Fechada** (Feedback sensorial) |
| **Complexidade** | Lógica de estados estática | Lógica dinâmica baseada em limiares |



---

## 3. Arquitetura de Aquisição: Como a IMU Trabalha

A inteligência da neuroprótese depende de como ela traduz o movimento físico em sinais digitais através da fusão sensorial.

### A. Sensores Internos
A IMU Yost Labs combina três sensores fundamentais:
* **Acelerómetro:** Mede a inclinação em relação ao vetor da gravidade.
* **Giroscópio:** Mede a velocidade angular, essencial para a precisão em movimentos dinâmicos.
* **Magnetómetro:** Atua como referência magnética para evitar a deriva (*drift*) do sensor.

### B. Fluxo de Dados e Processamento
1.  **Amostragem:** Realizada em alta frequência interna para capturar micro-movimentos.
2.  **Fusão (Filtro Kalman/AHRS):** O hardware processa os dados brutos para gerar uma orientação estável.
3.  **Representação em Quatérnios:** O dado é enviado como um vetor de 4 dimensões ($q = [w, x, y, z]$), evitando o erro de *Gimbal Lock*.
4.  **Streaming:** Enviado via Serial a **100Hz**, garantindo latência mínima entre o movimento e a resposta elétrica.

---

## 4. Modelagem Matemática: Do Sensor ao Atuador

### A. Representação Espacial (Quatérnios)
Um quatérnio unitário é representado como:
$$q = w + xi + yj + zk$$
Onde a norma $\|q\| = \sqrt{w^2 + x^2 + y^2 + z^2} = 1$.

### B. Conversão para Ângulos de Euler
Para a lógica clínica, convertemos o quatérnio para o ângulo de inclinação (Roll - $\phi$):
$$\phi = \text{atan2}(2(wq + xy), 1 - 2(x^2 + y^2))$$


### C. Lógica de Controle (Trigger)
A ativação é baseada numa função degrau dependente do ângulo crítico ($\theta_c = 60^\circ$):
$$
f(\theta) = 
\begin{cases} 
\text{STIM\_ON} & \text{se } |\theta| > \theta_c \\
\text{STIM\_OFF} & \text{se } |\theta| \leq \theta_c 
\end{cases}
$$



---

## 5. Detalhes das Novas Funções (Módulos `utils`)

O `main.py` agora integra ferramentas avançadas de processamento:
* **`imu_yostlabs_lara.extract_data`**: Interpreta os pacotes binários da IMU e identifica o sensor de origem.
* **`quaternion_operations.euler_from_quaternion`**: Realiza a conversão trigonométrica para graus decimais.
* **`serial_operations.manual_flush`**: Limpa o buffer da porta COM, garantindo que a neuroprótese não tome decisões baseadas em dados "atrasados".

---

## 6. Lógica de Operação e Segurança

A Neuroprótese opera sob uma lógica de prioridade. Embora seja automática, as travas de segurança do Nível 4 foram mantidas:

1.  **Estado `waiting`**: O sistema aguarda o streaming estabilizar. A estimulação só inicia se o membro ultrapassar o `angulo_minimo`.
2.  **Estado `stim_on`**: A estimulação permanece ativa enquanto o ângulo for superior ao limiar. Se o usuário baixar o membro (fadiga ou fim do movimento) ou apertar `P`, o sistema corta a corrente.
3.  **Botão de Emergência (`ESC`)**: Interrompe instantaneamente o modo CCL do RehaStim e o streaming da IMU, garantindo um desligamento seguro em congressos ou feiras.


---

## 7. Destaques para Apresentações e Demonstrações
Ao demonstrar este trabalho, enfatize que este é um dos **alicerces para próteses inteligentes**:
* **Modularidade**: O `stim_node.py` (driver de potência) não precisou ser alterado, provando a robustez da abstração de hardware feita nos níveis anteriores.
* **Hibridismo**: É um sistema que une a autonomia da máquina com a supervisão humana (Controle Híbrido).
* **Escalabilidade**: A estrutura está pronta para receber múltiplos sensores (ex: um no braço e outro no antebraço) para calcular ângulos relativos de articulações complexas.
