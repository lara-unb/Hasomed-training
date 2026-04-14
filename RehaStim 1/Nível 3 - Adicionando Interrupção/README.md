# Nível 3 - Adicionando Interrupção
 
## Introdução e Objetivos
No estágio anterior, o sistema operava em malha aberta com tempo fixo, o que limitava a intervenção do usuário durante a sessão de estimulação. O **Nível 3** introduz a capacidade de interrupção manual assistida por **Multithreading**. O objetivo principal é permitir que o experimentador monitore a resposta muscular em tempo real e encerre a estimulação de forma imediata e segura através de um comando de teclado.

Neste guia, focaremos em como gerenciar duas tarefas simultâneas: a manutenção da comunicação serial com o RehaStim 1 e a escuta ativa de eventos do sistema operacional.

---

## Conceitos Fundamentais para Estudo

Para a compreensão deste nível, é necessário dominar os seguintes termos técnicos:

* **Thread (Linha de Execução):** Diferente de um programa sequencial comum, uma thread permite que o processador execute múltiplas tarefas em paralelo dentro do mesmo programa.
* **Flags de Estado:** Variáveis booleanas (como `stop_flag`) utilizadas para sinalizar mudanças de condição entre diferentes threads.
* **Input Bloqueante:** Funções que suspendem a execução de uma thread até que uma entrada específica ocorra (ex: `input()` ou `keyboard.wait()`).
* **Polling de Eventos:** A técnica de verificar repetidamente uma condição dentro de um loop (como o `while not stop_flag`) para decidir o próximo passo do software.

---

## Arquitetura do Sistema: O Uso de Threads

A implementação atual separa as responsabilidades do software em dois fluxos distintos que rodam simultaneamente:

1.  **Thread Principal (Main Thread):** Responsável por instanciar a classe `StimNode`, configurar os parâmetros de corrente e largura de pulso, e executar o loop de atualização do CCL (`update_ccl`).
2.  **Thread de Interrupção (Monitor Thread):** Uma thread secundária criada exclusivamente para aguardar a interação do usuário. Ela permanece em estado de espera (bloqueada) até que a tecla definida seja pressionada.

### Por que o `input()` bloqueante é utilizado?
Ao contrário de sistemas puramente automáticos, a escolha de uma entrada bloqueante neste projeto é **estratégica e proposital**. Em contextos de pesquisa em neuroengenharia e reabilitação, o controle total do operador sobre o hardware é uma camada de segurança crítica. O bloqueio da thread de monitoramento garante que o programa não prossiga para etapas subsequentes sem que o pesquisador tenha validado visualmente a segurança da contração muscular produzida pelo RehaStim.

---

## Referência Técnica de Implementação

Abaixo estão os novos componentes introduzidos na lógica do `main.py`:

| Componente | Tipo | Função Técnica |
| :--- | :--- | :--- |
| `threading.Thread` | Classe | Instancia o fluxo paralelo para o monitoramento do teclado. |
| `stop_flag` | Booleano | Variável compartilhada que interrompe o loop de estimulação ao se tornar `True`. |
| `keyboard.wait('space')` | Função | Comando bloqueante que captura o evento da tecla "espaço" em nível de sistema. |
| `stim.stop_ccl()` | Método | Chamado obrigatoriamente após a interrupção para zerar os canais do RehaStim. |

---

## Guia de Execução e Segurança

O fluxo de operação deve seguir rigorosamente os passos abaixo para garantir a integridade do equipamento e do sujeito de teste:

1.  **Preparação de Hardware:** Certifique-se de que o RehaStim 1 está em modo *ScienceMode* e os eletrodos estão devidamente posicionados.
2.  **Inicialização:** Ao rodar o `python main.py`, a thread de monitoramento será disparada imediatamente.
3.  **Monitoramento:** O loop de estimulação enviará pulsos continuamente conforme a `FREQ` definida.
4.  **Interrupção Manual:** Ao pressionar a tecla de espaço, a thread secundária altera a `stop_flag`, forçando a saída do loop principal e a execução do comando de parada (`stop_ccl`).
5.  **Verificação de Saída:** Confirme no terminal se a mensagem de encerramento foi exibida e se os LEDs do RehaStim indicam o fim da transmissão de dados.

> **Aviso de Segurança:** Caso a tecla de interrupção não responda devido a falhas no driver de teclado ou sobrecarga do sistema, o desligamento manual através do botão físico do RehaStim deve ser realizado imediatamente para cessar a corrente elétrica.
