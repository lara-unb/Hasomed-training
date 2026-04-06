# O RehaStim — Hardware e Arquitetura

## Visão Geral do Sistema

<img width="838" height="507" alt="image" src="https://github.com/user-attachments/assets/6837cad6-4148-4e50-9310-37250b7cd14b" />


O **RehaStim** é um estimulador de corrente controlada de 8 canais desenvolvido pela **Hasomed GmbH** (Alemanha). É um produto controlado pelo protocolo **ScienceMode** via interface USB (padrão USB 1.1 com isolação galvânica). O processador principal é um microcontrolador de 16 bits de ultra-baixo consumo (MSP430 da Texas Instruments).

>  **Nota:** O RehaStim possui dois módulos de estimulação independentes: o Módulo A controla os canais 1 a 4 e o Módulo B controla os canais 5 a 8. Cada módulo tem sua própria fonte de corrente e microprocessador dedicado ao timing dos pulsos. Isso permite geração simultânea de pulsos nos dois módulos, com um offset fixo de 0,6 ms entre eles.

---

## Especificações Técnicas

| Parâmetro | Valor / Descrição |
|-----------|-------------------|
| **Corrente** | 0 a 126 mA, passos de 2 mA |
| **Largura de pulso** | 0, 20 a 500 µs, passos de 1 µs |
| **Forma de onda** | Bifásica |
| **Canais** | 8 (2 módulos de 4 canais) |
| **Interface serial** | USB com isolação galvânica |
| **Protocolo** | ScienceMode |
| **Operação** | Painel touchscreen com iluminação |

>  **Aviso:** Os valores de corrente do RehaStim vão até 126 mA em passos de 2 mA (portanto apenas valores pares). A largura de pulso começa em 20 µs (não há valores entre 1 e 19 µs).

---

## Pulso Bifásico e Verificação de Resistência de Pele

O RehaStim gera pulsos bifásicos com uma pausa fixa de 100 µs entre as duas fases. Ao final do pulso, a carga residual nos eletrodos e na pele é removida por um curto-circuito ativo (inversão de polaridade por 1 µs).

Antes de cada pulso de estimulação, o dispositivo realiza uma verificação de resistência de pele por meio de um impulso de teste. Se a resistência estiver fora dos limites normais, o pulso de estimulação não será gerado, isso pode ser observado na bancada de teste

>  **Nota:** A verificação automática de resistência é um mecanismo de segurança importante. Eletrodos mal posicionados, secos ou danificados podem fazer com que o estimulador não gere pulso sem emitir qualquer aviso explícito ao código.

---

## Módulos de Estimulação A e B

| Módulo | Canais | Offset de início |
|--------|--------|-----------------|
| **A** | CH1, CH2, CH3, CH4 | 0 ms |
| **B** | CH5, CH6, CH7, CH8 | 0,6 ms após Módulo A |

Cada canal selecionado ocupa um **slot de tempo de 1,5 ms**, mesmo que corrente e largura de pulso sejam zero. O intervalo mínimo entre canais do mesmo módulo é de 1,5 ms.

---

# Segurança e Protocolos de Proteção

>  **Aviso:** Leia esta seção integralmente antes de qualquer sessão. O uso inadequado pode causar queimaduras, dor, arritmias cardíacas ou lesões neuromusculares.

## Contraindicações Absolutas

- Marcapassos ou dispositivos cardíacos implantados
- Estimuladores espinhais implantados
- Gravidez
- Infecções, feridas abertas ou lesões de pele na área de estimulação
- Epilepsia

---

## Limites de Segurança dos Parâmetros

| Parâmetro | Limite |
|-----------|--------|
| **Corrente máxima** | 126 mA (apenas valores pares: 0, 2, 4, …, 126 mA) |
| **Largura de pulso** | 0 ou 20–500 µs (passos de 1 µs) |
| **Carga por fase** | Q = I × PW — manter abaixo de 600 µC |
| **Densidade de carga** | ≤ 40 µC/cm² por fase |
| **Amplitude inicial recomendada** | ≤ 20 mA — aumentar gradualmente |
| **Frequência recomendada** | 50 Hz para minimizar fadiga |

---

## Checklist de Segurança pré-Sessão

- [ ] Confirmar consentimento do participante
- [ ] Verificar integridade dos cabos e eletrodos
- [ ] Confirmar que corrente e largura de pulso estão em zero antes de conectar
- [ ] Verificar posicionamento dos eletrodos (sem dobras, boa adesão)
- [ ] Ter modo de parada de estimulação acessível (comando de parada mapeado e/ou botão de emergência)
- [ ] Verificar ativação do modo ScienceMode no painel do dispositivo
- [ ] Registrar parâmetros iniciais para estudo posterior

---

## Procedimento em caso de Emergência

1. Caso o botão de emergência estiver conectado e configurado, apertar imediatamente para a interrupção.
2. Caso o botão de emergência não estiver disponível, no código deve ter um comando para zerar corrente e largura de pulso (chamar `update_ccl` com zeros) ou chamar `stop_ccl` com alguma tecla configurada.
3. Desconectar os eletrodos.
4. Inspecionar a pele na área de estimulação.
5. Registrar o incidente com data, hora e parâmetros ativos.

---

# Parâmetros de Estimulação — Guia de Referência

## Tabela de Parâmetros Iniciais por Músculo

### Membro Inferior

| Músculo | Canal | I (mA) | PW (µs) | f (Hz) | Obs. |
|---------|-------|--------|---------|--------|------|
| Quadríceps (D) | CH1 | — | — | 50 | Referência Estevão |
| Quadríceps (E) | CH2 | — | — | 50 | Referência Estevão |
| Isquiotibiais (D) | CH3 | — | — | 50 | Referência Estevão |
| Isquiotibiais (E) | CH4 | — | — | 50 | Referência Estevão |

### Membro Superior

| Músculo | Canal | I (mA) | PW (µs) | f (Hz) | Obs. |
|---------|-------|--------|---------|--------|------|
| Bíceps (D) | CH5 | — | — | 50 | Flexão do cotovelo |
| Bíceps (E) | CH6 | — | — | 50 | |
| Tríceps (D) | CH7 | — | — | 50 | Extensão do cotovelo |
| Tríceps (E) | CH8 | — | — | 50 | |


>  **Nota:** Todos os valores de corrente devem ser **pares** no RehaStim (0, 2, 4, …, 126 mA). Valores ímpares serão arredondados internamente pelo hardware.
