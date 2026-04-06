
# **REFERÊNCIA E SOLUÇÃO DE PROBLEMAS**


## Diagnóstico e Resolução de Problemas

### Problemas de Comunicação

| **Sintoma**           | **Causa Provável**        | **Solução** |
|----------------------|---------------------------|-------------|
| Sem ACK              | Porta COM errada          | `mode` (Windows) ou `ls /dev/tty*` (Linux) |
| Timeout              | Baudrate incorreto        | Confirmar 115200 bps |
| Desconexão aleatória | Cabo USB com defeito      | Trocar cabo |
| Erro de checksum     | Interferência elétrica    | Blindagem, separar cabos de força |
| Sem resposta alguma  | ScienceMode não ativado   | Ativar pelo painel do RehaStim |

---

### Problemas de Estimulação

| **Sintoma**            | **Causa Provável**                  | **Solução** |
|------------------------|------------------------------------|-------------|
| ACK OK mas sem pulso   | Resistência de pele fora do range   | Reposicionar/umedecer eletrodos |
| Sem resposta motora    | Eletrodo solto ou seco             | Reposicionar eletrodo |
| Resposta assimétrica   | Eletrodos mal posicionados         | Remarcar posição anatômica |
| Queimação na pele      | Alta densidade de carga            | Reduzir `I` ou aumentar área |
| Fadiga rápida          | Frequência muito alta              | Fazer pausa ou reduzir a frequência |

---

### Problemas com Python / pyserial

| **Erro** | **Solução** |
|----------|------------|
| `ModuleNotFoundError: No module named 'serial'` | `pip install pyserial` |
| `AttributeError: module 'serial' has no attribute 'Serial'` | `pip uninstall serial && pip install pyserial` |
| `PermissionError` na porta serial | Linux: `sudo usermod -aG dialout $USER` |
| `time.delay` não existe | Usar `time.sleep()` |

---

