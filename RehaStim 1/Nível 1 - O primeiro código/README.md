# Nível 1 — O Primeiro Código: `stim_node.py`

## Contexto e Objetivo

Este código foi o ponto de partida prático do aprendizado com o RehaStim 1. É uma versão simplificada do sistema original do **Projeto EMA**, adaptada para remover as dependências do **ROS** (*Robot Operating System*), mantendo a funcionalidade de comunicação serial via ScienceMode.

---

## Importações e Dependências

```python
import time
import numpy as np
import sys
import serial
import struct
```

- `time` — delays e controle temporal
- `numpy` — computação numérica (importada, não usada no código base)
- `sys` — funcionalidades do sistema (importada, não usada no código base)
- `serial` — comunicação serial com o RehaStim
- `struct` — empacotamento e desempacotamento de dados binários

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

---

## Dicionário de Comandos

| Comando | ID (Ident) | Descrição |
|---------|-----------|-----------|
| `channelListModeInitialization` | 00 | Inicializa CCL |
| `channelListModeUpdate` | 01 | Atualiza PW e corrente |
| `channelListModeStop` | 10 | Para estimulação |
| `singlePulseGeneration` | 11 | Pulso único por canal |

---

## Métodos Principais

### `write_read_command` — Comunicação Serial

```python
def write_read_command(self, command_bytes):
    self.serial_port.write(command_bytes)
    while(self.serial_port.in_waiting < 1): pass
    ack = struct.unpack('B', self.serial_port.read(1))[0]
    error_code = ack & 1
    return {0: False, 1: True}[error_code]
```

O bit 0 do ACK indica: `True` = OK, `False` = erro (conforme protocolo ScienceMode, Seção 5.7 do manual).

---

### `initialize_ccl` — Inicialização

Calcula `Main_Time` a partir da frequência e monta o pacote de 6 bytes de inicialização. O checksum tem módulo 8.

---

### `update_ccl` — Atualização de Parâmetros

Atualiza largura de pulso e corrente para cada canal ativo. O checksum acumulativo tem módulo 32.

---

### `stop_ccl` — Parada

Envia o pacote de 1 byte de parada (checksum = 0). Sempre chamar ao final de uma sessão.

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
