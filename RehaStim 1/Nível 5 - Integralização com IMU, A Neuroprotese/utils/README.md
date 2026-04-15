# Pasta `utils` — Módulos de Suporte e Processamento

## Visão Geral
Esta pasta contém os módulos utilitários responsáveis pela abstração da comunicação com o hardware e pelo processamento matemático dos dados sensoriais. A separação nestes arquivos permite que a lógica de manipulação de ângulos e comunicação serial seja reaproveitada em diferentes níveis do projeto, sem sobrecarregar os scripts principais de estimulação.

## Estrutura de Arquivos

| Arquivo | Responsabilidade Principal |
| :--- | :--- |
| `serial_operations.py` | Gerenciamento da porta serial, configuração de *dongles* e sensores IMU (Yost Labs). |
| `quaternion_operations.py` | Cálculos espaciais utilizando Quatérnios, incluindo conversão para matrizes de rotação e ângulos de Euler. |
| `euler_angle_operations.py` | Operações trigonométricas com ângulos de Euler e cálculo de diferença angular entre vetores. |
| `imu_yostlabs_lara.py` | Interface de alto nível para inicialização, configuração de *streaming* e extração de dados das IMUs. |

---

## Detalhamento dos Módulos

### 1. `serial_operations.py`
Este é o "motor" de comunicação. Ele lida com o protocolo de baixo nível dos sensores Yost Labs, utilizando comandos formatados em strings (`>ID,Command,Arguments\n`).
* **Principais Funções:**
    * `get_dongle_object()`: Localiza automaticamente o PID do dongle e abre a conexão.
    * `set_streaming_slots()`: Define quais dados (Quatérnios, Euler, Accel) o sensor deve enviar em tempo real.
    * `manual_flush()`: Limpa o buffer da serial para evitar o processamento de dados "atrasados".

### 2. `quaternion_operations.py`
Para evitar o problema de *Gimbal Lock* (travamento de eixos), o sistema prioriza o uso de quatérnios para representar orientações no espaço.
* **Destaque:** O método `calculate_angle_between_quaternions` permite calcular a distância angular entre dois sensores, essencial para medir a amplitude de movimento (ROM) de uma articulação.


### 3. `imu_yostlabs_lara.py`
Funciona como um *wrapper* (embrulho) que simplifica o uso das IMUs para o usuário final. 
* **Configuração Dinâmica:** Através do `configure_imu`, você pode habilitar ou desabilitar sensores internos (Giroscópio, Bússola, Acelerômetro) e definir quais slots de dados serão transmitidos.
* **Estratégias de Extração:** Utiliza um dicionário de estratégias (`data_strategies`) para interpretar os bytes recebidos da serial e transformá-los em tipos de dados Python (listas ou arrays NumPy).

---

## Fluxo de Dados Sensoriais
O processamento segue a seguinte hierarquia:
1.  **Captura:** `serial_operations` lê os bytes brutos da porta COM.
2.  **Tratamento:** `imu_yostlabs_lara` identifica a origem (ID do sensor) e o tipo de dado.
3.  **Matemática:** `quaternion_operations` ou `euler_angle_operations` transformam esses dados em informações úteis (ex: "O joelho está flexionado em 45°").

---

## Requisitos de Estudo
Para colaborar com esta pasta, recomenda-se o estudo de:
* **Álgebra Linear:** Rotações em 3D e matrizes de transformação.
* **Protocolos Seriais:** Entendimento de *Baudrate*, *Buffer* e *Streaming*.
* **PySerial e NumPy:** Bibliotecas base para a manipulação dos dados no Python.

---
