# Nível 1 — O Primeiro Código: `stim_node.py`

## Contexto e Objetivo

Este código foi o ponto de partida prático do aprendizado com o RehaStim 1. É uma versão simplificada do sistema original do **Projeto EMA**, adaptada para remover as dependências do **ROS** (*Robot Operating System*), mantendo a funcionalidade de comunicação serial via ScienceMode.

O script implementa uma classe `StimNode` que encapsula toda a comunicação com o RehaStim. Ao rodar, ele:

1. Abre uma conexão serial com o dispositivo
2. Inicializa o modo de lista de canais (CCL — *Channel List Mode*)
3. Envia parâmetros de estimulação (largura de pulso e corrente)
4. Mantém a estimulação por um tempo definido
5. Encerra a estimulação com segurança
 
> **Aviso:** Certifique-se de que o modo ScienceMode está ativo no painel do RehaStim **antes** de rodar o script. Sem isso, nenhum comando será processado pelo dispositivo.



---

## Importações e Dependências

```python
import time
import numpy as np
import sys
import serial
import struct
```
 
| Biblioteca | Uso |
|-----------|-----|
| `time` | Delays e controle temporal (ex.: `time.sleep()`) |
| `numpy` | Computação numérica — importada, não usada no código base |
| `sys` | Funcionalidades do sistema — importada, não usada no código base |
| `serial` | Comunicação serial com o RehaStim via porta COM/USB |
| `struct` | Empacotamento e desempacotamento de dados binários para montagem dos pacotes ScienceMode |

---

## Atributos de Classe

```python
class StimNode:
    PORT = "COM5"       # Windows; Linux: "/dev/ttyUSB0"
    CHANNEL_LF = []
    FREQ = 50           # Hz
    N_FACTOR = 0
    GROUP_TIME = 0
    STIM_MODE = 0       # 0 = single pulse
```

| Atributo | Descrição |
|----------|-----------|
| `PORT` | Porta serial onde o RehaStim está conectado |
| `CHANNEL_LF` | Lista de canais ativos — preenchida em `initialize_ccl()` |
| `FREQ` | Frequência de estimulação em Hz — usada para calcular o `Main_Time` do pacote de inicialização |
| `N_FACTOR` | Fator multiplicador do `Main_Time` — usado para frequências muito baixas; vale `0` na maioria dos casos |
| `GROUP_TIME` | Tempo de grupo entre módulos A e B — deixar em `0` para comportamento padrão |
| `STIM_MODE` | Modo de estimulação: `0` = pulso único (*single pulse*) |

>  **Nota:** Para descobrir a porta no **Windows**: digitar `mode` no terminal após conectar o RehaStim. No **Linux/macOS**: `ls /dev/tty*`.

---

## Construtor — Conexão Serial

```python
def __init__(self):
    self.serial_port = serial.Serial(
        port=self.PORT,
        baudrate=115200,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_TWO,
        rtscts=True
    )
    print("[INFO] StimNode inicializado")
```
 
Os parâmetros de comunicação serial são **obrigatórios e definidos pelo protocolo ScienceMode** — não devem ser alterados:
 
| Parâmetro | Valor | Motivo |
|-----------|-------|--------|
| `baudrate` | 115200 | Taxa de comunicação exigida pelo firmware do RehaStim |
| `bytesize` | 8 bits | Padrão do protocolo |
| `parity` | None | Sem bit de paridade |
| `stopbits` | 2 | Dois bits de parada — exigido pelo RehaStim |
| `rtscts` | True | Controle de fluxo por hardware (RTS/CTS) — necessário para sincronização |

---

## Dicionário de Comandos

O protocolo ScienceMode identifica cada tipo de mensagem por um byte de identificação (`Ident`). Os comandos utilizados neste código são:

| Comando | ID (Ident) | Descrição |
|---------|-----------|-----------|
| `channelListModeInitialization` | 00 | Inicializa CCL com frequência e canais ativos |
| `channelListModeUpdate` | 01 | Atualiza PW (largura de pulso) e corrente por canal |
| `channelListModeStop` | 10 | Para estimulação e libera os canais |
| `singlePulseGeneration` | 11 | Gera um pulso único por canal |

---

## Métodos Principais

### Fluxo de Chamada Obrigatório
 
```
initialize_ccl()  →  update_ccl()  →  [estimulação ativa]  →  stop_ccl()
```
 
>  **Aviso:** Nunca chame `update_ccl()` sem antes ter chamado `initialize_ccl()`. O dispositivo não reconhecerá os parâmetros e pode se comportar de forma inesperada.


### `write_read_command` — Comunicação Serial

```python
def write_read_command(self, command_bytes):
    self.serial_port.write(command_bytes)
    while(self.serial_port.in_waiting < 1): pass
    ack = struct.unpack('B', self.serial_port.read(1))[0]
    error_code = ack & 1
    return {0: False, 1: True}[error_code]
```

Método base de comunicação — todos os outros métodos passam por ele. Envia um pacote de bytes ao RehaStim e aguarda o byte de confirmação (ACK).

O bit 0 do ACK indica: `True` = comando aceito, `False` = erro. Os demais bits do ACK carregam informações adicionais de status (conforme protocolo ScienceMode, Seção 5.7 do manual).

---

### `initialize_ccl` — Inicialização

**Argumentos:** lista de canais a ativar (ex.: `[1]`, `[1, 2, 3]`)

Calcula `Main_Time` a partir da frequência definida em `FREQ` e monta o pacote de 6 bytes de inicialização do CCL. O checksum é calculado com módulo 8. Deve ser chamado uma única vez antes de iniciar a estimulação.

---

### `update_ccl` — Atualização de Parâmetros

**Argumentos:** lista de larguras de pulso (µs) e lista de correntes (mA) — uma entrada por canal ativo, na mesma ordem da inicialização.

Monta e envia o pacote de atualização com os novos parâmetros de estimulação. O checksum acumulativo tem módulo 32. Pode ser chamado repetidamente durante uma sessão para alterar os parâmetros em tempo real.

---

### `stop_ccl` — Parada

Envia o pacote de 1 byte de parada (checksum = 0), encerrando imediatamente a estimulação em todos os canais. **Sempre deve ser chamado ao final de uma sessão**, inclusive em situações de erro ou interrupção pelo usuário.

---

## Exemplo de Uso — Função `main()`

```python
def main():
    stim_object = StimNode()
    channels = [1]

    stim_object.initialize_ccl(channels)

    pulse_width   = [180]   # us  (braco: a partir de 180 us)
    pulse_current = [8]     # mA  (braco: entre 5 mA e 10 mA)

    stim_object.update_ccl(pulse_width, pulse_current)
    time.sleep(5)
    stim_object.stop_ccl()

if __name__ == '__main__':
    main()
```
Os valores `pulse_width = [180]` e `pulse_current = [8]` foram escolhidos como **ponto de partida seguro para membro superior** — são valores baixos o suficiente para não causar desconforto em um primeiro teste, mas já suficientes para observar contração muscular em indivíduos com boa condutividade de pele. Ajuste conforme o músculo-alvo e a resposta observada.
