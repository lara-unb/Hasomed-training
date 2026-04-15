# Nível 4 — Máquina de Estados: Loop com Parada e Reinicialização

## Introdução e Objetivos
No nível anterior, o sistema permitia uma única interrupção que encerrava completamente o programa. No **Nível 4**, elevamos a lógica de controle para uma **Máquina de Estados Finitos (FSM)**. O objetivo é permitir que o experimentador alterne entre diferentes modos de operação (Estimulação Ativa, Pausa e Standby) sem precisar reiniciar o script Python ou o hardware.

Esta arquitetura é fundamental para protocolos de reabilitação que exigem ciclos de contração e repouso (ON/OFF) ou intervenções manuais para ajustes de eletrodos durante a sessão.

---

## Conceitos Fundamentais para Estudo

Para compreender a evolução deste nível, revisaremos os seguintes conceitos de engenharia de software:

* **Máquina de Estados (State Machine):** Um modelo de comportamento que consiste em um número finito de estados, transições entre esses estados e ações. No nosso caso, o programa "se comporta" de forma diferente dependendo se o estado atual é de pausa ou de estimulação.
* **Controle de Fluxo Não-Bloqueante:** Diferente do `input()`, utilizamos aqui o `keyboard.is_pressed()`. Isso permite que o loop principal continue rodando (mantendo a comunicação com o RehaStim) enquanto verifica rapidamente se alguma tecla foi acionada.
* **Debounce (Software):** O uso de `time.sleep(0.3)` após detectar o pressionamento de uma tecla. Isso evita que um único toque rápido seja registrado como múltiplos comandos pelo processador.

---

## Arquitetura do Sistema: Estados de Operação

O programa agora é organizado em torno de quatro estados lógicos:

| Estado | Descrição Técnica | Ação no RehaStim |
| :--- | :--- | :--- |
| `STATE_WAITING` | Aguardando o início da sessão pelo operador. | Nenhum comando enviado. |
| `STATE_STIM_ON` | Estimulação ativa com os parâmetros definidos. | Envia `update_ccl` com `PULSE_WIDTH_ON`. |
| `STATE_STIM_OFF` | Estado de pausa (estimulação zerada, mas conexão ativa). | Envia `update_ccl` com valores zerados (`OFF`). |
| `STATE_EXIT` | Encerramento seguro da sessão e saída do loop. | Executa `stop_ccl()` e encerra o script. |



---

## Implementação: Por que esta estrutura é superior?

A principal vantagem desta abordagem é a **estabilidade da comunicação**. No Nível 1, para "pausar", era necessário encerrar o programa. No Nível 4, o RehaStim permanece em modo CCL (Channel List Mode) o tempo todo, apenas recebendo comandos de corrente zero quando pausado. 

Isso elimina o *delay* de reinicialização do hardware e garante que, ao retomar a estimulação (tecla 'L'), a resposta muscular seja imediata e sincronizada.

---

## Guia de Operação e Comandos

O controle da sessão agora é feito inteiramente via teclado, seguindo a lógica abaixo:

1.  **Início (`S`):** Sai do modo de espera e inicia a contração muscular.
2.  **Pausa (`P`):** Zera a corrente nos canais, mas mantém o programa rodando. Ideal para descanso do paciente.
3.  **Retomar (`L`):** Volta ao estado de estimulação ativa após uma pausa.
4.  **Sair (`ESC`):** O comando definitivo de segurança que interrompe o CCL e fecha o programa.

---

## Protocolo de Segurança e Verificação

* **Verificação de Estado:** O terminal agora atua como um monitor de estado em tempo real, exibindo mensagens como `[PAUSADO]` ou `[STIM ON]`. Sempre verifique o console antes de tocar nos eletrodos.
* **Prioridade do ESC:** A tecla `ESC` está programada em todos os estados críticos. Em caso de qualquer comportamento inesperado, ela é o seu "Kill Switch" via software.
* **Persistência do Driver:** O arquivo `stim_node.py` permanece idêntico aos níveis anteriores, provando que uma boa abstração de hardware (driver) não precisa mudar quando a lógica de aplicação (interface) evolui.

> **Dica de Estudo:** Tente observar como a variável `state` controla qual bloco do `match/case` (ou `if/elif`) é executado. Este é o padrão ouro para programação de sistemas embarcados e robótica industrial.
