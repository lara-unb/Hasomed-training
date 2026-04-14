# Nível 2 - Parametrizando o Primeiro Código

## Contexto e Objetivo

No Nível 1, o `StimNode` era independente: os parâmetros de porta, frequência, modo e canais ficavam hardcoded como atributos de classe dentro do próprio arquivo. Isso funcionava para um primeiro teste, mas tornava a configuração trabalhosa — para mudar a porta serial era preciso editar o código da classe.

Neste nível de aprendizado, duas mudanças estruturais foram feitas:

1. **`StimNode` foi parametrizado** — os atributos de classe fixos foram substituídos por argumentos do construtor `__init__`, tornando a classe reutilizável sem modificação.
2. **`main.py` foi separado** — toda a lógica de execução e configuração saiu do `stim_node.py` e foi para um arquivo dedicado. O `stim_node.py` agora é puramente uma biblioteca.

A estrutura da pasta ficou assim:

```
nivel2/
├── stim_node.py   # classe StimNode — sem lógica de execução
└── main.py        # configurações e chamada do fluxo de estimulação
```

---

## O que mudou no `stim_node.py`

### Antes (Nível 1) — atributos de classe fixos

```python
class StimNode:
    PORT = "COM5"
    FREQ = 50
    N_FACTOR = 0
    GROUP_TIME = 0
    STIM_MODE = 0
    CHANNEL_LF = []

    def __init__(self):
        self.serial_port = serial.Serial(port=self.PORT, ...)
```

### Agora (Nível 2) — parâmetros no construtor

```python
class StimNode:

    def __init__(self, port, freq, n_factor, group_time, stim_mode, channel_lf):
        self.PORT       = port
        self.FREQ       = freq
        self.N_FACTOR   = n_factor
        self.GROUP_TIME = group_time
        self.STIM_MODE  = stim_mode
        self.CHANNEL_LF = channel_lf

        self.serial_port = serial.Serial(port=self.PORT, ...)
```

A classe em si não tem mais nenhum comando sobre qual porta usar ou qual frequência aplicar. Quem instanciar `StimNode` é responsável por passar todos os parâmetros. Isso é importante porque o mesmo `stim_node.py` pode agora ser importado por qualquer script sem precisar ser editado.

> **Nota:** O `command_dict` e `channel_stim` permanecem como atributos de classe, pois são constantes do protocolo ScienceMode e não variam entre sessões.

---

## O `main.py` — separação de responsabilidades

Todo o bloco de configuração e a função `main()` agora vivem em `main.py`. A seção de configuração foi destacada com comentários para facilitar edição:

```python
# ──────────────────────────────────────────
#  CONFIGURAÇÕES — edite aqui
# ──────────────────────────────────────────

PORT       = "COM5"
FREQ       = 50      # Hz
N_FACTOR   = 0
GROUP_TIME = 0
STIM_MODE  = 0       # 0 = single
CHANNEL_LF = []

CHANNELS       = [1]   # canais ativos (1–8)
PULSE_WIDTH    = [100]  # µs
PULSE_CURRENT  = [4]   # mA

STIM_DURATION  = 5     # segundos de estimulação
```

Toda configuração de uma sessão acontece aqui, sem tocar na classe. A função `main()` instancia `StimNode` com esses valores e executa o fluxo já conhecido do Nível 1:

```python
def main():
    stim = StimNode(
        port=PORT,
        freq=FREQ,
        n_factor=N_FACTOR,
        group_time=GROUP_TIME,
        stim_mode=STIM_MODE,
        channel_lf=CHANNEL_LF,
    )

    stim.initialize_ccl(CHANNELS)
    stim.update_ccl(PULSE_WIDTH, PULSE_CURRENT)

    time.sleep(STIM_DURATION)

    stim.stop_ccl()
```

O fluxo `initialize_ccl → update_ccl → stop_ccl` é idêntico ao do Nível 1. O que mudou é apenas onde a configuração está localizada e como chegar até a classe.

---

## Referência dos Parâmetros de Configuração

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `PORT` | `str` | Porta serial do RehaStim. Windows: `"COM5"`. Linux: `"/dev/ttyUSB0"` |
| `FREQ` | `int` | Frequência de estimulação em Hz. Valor típico: `50` |
| `N_FACTOR` | `int` | Fator multiplicador do `Main_Time` para frequências muito baixas. Deixar `0` na maioria dos casos |
| `GROUP_TIME` | `int` | Tempo de grupo entre módulos A e B. Deixar `0` para comportamento padrão |
| `STIM_MODE` | `int` | Modo de estimulação: `0` = pulso único (*single*) |
| `CHANNEL_LF` | `list` | Canais em modo de baixa frequência. Deixar `[]` para não usar |
| `CHANNELS` | `list[int]` | Canais a ativar, de `1` a `8`. Ex.: `[1]`, `[1, 3]` |
| `PULSE_WIDTH` | `list[int]` | Largura de pulso em µs para cada canal em `CHANNELS`, na mesma ordem |
| `PULSE_CURRENT` | `list[int]` | Corrente em mA para cada canal em `CHANNELS`, na mesma ordem |
| `STIM_DURATION` | `int/float` | Duração da estimulação em segundos antes de chamar `stop_ccl()` |


---

## Executando

```bash
python main.py
```

O script abre a porta serial, inicializa o CCL, aplica estimulação pelo tempo definido em `STIM_DURATION` e encerra com `stop_ccl()`.

> **Lembre-se:** O modo ScienceMode deve estar ativo no painel do RehaStim antes de rodar o script, conforme descrito no Nível 1.
