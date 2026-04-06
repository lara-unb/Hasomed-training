# Hasomed-training

> Repositório de treinamento para a família de dispositivos **Hasomed**, cobrindo os equipamentos **RehaStim 1**, **P24** e **I24**.  
> Destinado aos membros do Projeto EMA e a demais interessados, com acesso à documentação, manuais e scripts de operação.

##  Sobre a Hasomed

A Hasomed desenvolve produtos de hardware, software e eletrônica bem estabelecidos no mercado de reabilitação neurológica, com forte diálogo com hospitais, clínicas e pacientes — o que a torna uma das empresas líderes mundiais nesse campo.

O foco da empresa é a **Estimulação Elétrica Funcional (FES)**, uma tecnologia que aplica correntes elétricas de baixa intensidade para ativar músculos com mobilidade reduzida ou paralisada, viabilizando aplicações clínicas e de pesquisa. Para facilitar o controle programático dos dispositivos, a Hasomed desenvolveu o protocolo **HASOMED ScienceMode®**, que oferece acesso flexível e amigável aos equipamentos de pesquisa, permitindo controle externo via USB com ajuste completo de parâmetros por PC, MATLAB, Python, entre outros.

---

##  Dispositivos Cobertos

| Dispositivo | Protocolo | Canais | Descrição |
|-------------|-----------|--------|-----------|
| **RehaStim 1** | ScienceMode 1 | 8 canais | Estimulador FES clássico, comunicação serial via porta COM virtual |
| **P24** | ScienceMode 4 | 8 canais simultâneos | Controlado via PC por USB-C, sem bateria interna; projetado para pesquisa, estudos e desenvolvimento de produtos |
| **I24** | ScienceMode 4 | 4 canais (3 potencial + 1 impedância) | Dispositivo para medições de potencial e impedância, controlado via USB-C; indicado para pesquisa e desenvolvimento avançado |

---

##  Aplicação no Projeto

Os três dispositivos compartilham o protocolo **ScienceMode** da Hasomed, o que permite uma abordagem unificada no desenvolvimento de scripts e pipelines experimentais. Com isso, é possível:

- **Controlar parâmetros de estimulação** como frequência, largura de pulso, intensidade e duração de trens de pulso diretamente via código
- **Integrar com ferramentas de pesquisa** como encoders, sensores de eletromiografia (EMG), sensores inerciais (IMU) e plataformas de força
- **Prototipagem rápida** de novos protocolos de estimulação em Python ou outras linguagens compatíveis
- **Comparar o comportamento** entre gerações de dispositivos (RehaStim 1 → P24/I24) dentro do mesmo repositório

>  A biblioteca open-source **[pyScienceMode](https://github.com/ScienceMode)** é um ponto de partida recomendado para controle via Python, com suporte ao RehaStim e ao P24.

---

##  Conteúdo do Repositório

Cada dispositivo conta com:

- **Documentação técnica** — especificações, diagramas e notas de engenharia
- **Manual de operação** — guia de configuração, parâmetros e limites de segurança
- **Scripts** — exemplos de comunicação, testes e automação de protocolos

---

##  Requisitos Técnicos

- Sistema Operacional: Windows 10/11 ou Linux (Ubuntu 20.04+)
- Python 3.8+ (para execução dos scripts)
- Drivers Hasomed instalados ([site oficial](https://www.hasomed.de))
- Conexão USB-C (P24 / I24) ou interface serial COM virtual (RehaStim 1)

---

##  Segurança

>  **Atenção:** Sempre siga as normas de segurança elétrica e os protocolos clínicos aplicáveis antes de conectar qualquer dispositivo a um voluntário ou bancada experimental.

---


