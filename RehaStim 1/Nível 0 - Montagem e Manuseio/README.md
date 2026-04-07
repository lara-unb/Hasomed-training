# Nível 0 — Montagem e Manuseio do RehaStim 1

Antes de testar e programar o Hasomed RehaStim, é fundamental aprender a montar, conectar e desmontar o equipamento corretamente. O mau manuseio dos cabos e conectores é uma das causas mais comuns de falhas de comunicação e de danos ao equipamento.

![WhatsApp Image 2026-04-06 at 12 47 06](https://github.com/user-attachments/assets/27cccd70-25ef-4d7f-bf46-93801ba796d2)


---

## Montagem e Conexão

1. Posicione o RehaStim em uma superfície plana e estável, longe de líquidos
2. Verifique visualmente o estado dos cabos e conectores antes de qualquer conexão
3. Conecte o cabo USB ao computador antes de ligar o dispositivo
4. Ligue o RehaStim pelo painel frontal e aguarde a inicialização completa
5. Ative o modo ScienceMode pelo painel touchscreen
6. Conecte os cabos dos eletrodos aos canais desejados — encaixe firme, sem forçar
7. Posicione e fixe os eletrodos na pele antes de iniciar qualquer estimulação

---

## Cuidados com os Conectores e Canais

Os conectores dos canais de estimulação são a parte mais sensível do equipamento. Danos nos pinos ou no encaixe podem comprometer um canal inteiro.

>  **Aviso:**
> 1. **Nunca force um conector!** Se sentir resistência ao encaixar, verifique a orientação antes de aplicar pressão. Conectores tortos ou com pinos dobrados devem ser reportados imediatamente a um mestrando ou ao professor Roberto.
> 2. **Nunca posicione os eletrodos/terminais de um mesmo canal em lados diferentes do corpo!** Os eletrodos devem estar nas extremidades do mesmo músculo ou grupo muscular — jamais um em cada braço, por exemplo, pois a corrente entra por um eletrodo e sai pelo outro, estimulando tudo que há entre eles (nesse exemplo, o coração).

- Sempre segure o conector ao encaixar ou remover — **nunca puxe pelo cabo**
- Verifique o alinhamento dos pinos antes de encaixar
- Após o uso, remova os cabos dos canais com movimento reto, sem torção
- Inspecione visualmente os pinos a cada uso — pinos dobrados indicam mau uso

---

## Cuidados com os Cabos

Os cabos de estimulação são flexíveis, mas possuem vida útil limitada se manuseados incorretamente. Dobras bruscas, especialmente próximas aos conectores, causam ruptura interna das fibras condutoras.

- **Não dobre os cabos em ângulos agudos**, especialmente na região próxima ao conector
- **Não enrole os cabos com força** — o enrolamento deve ser suave, em círculos amplos
- Mantenha os cabos afastados de bordas de mesa ou de regiões com movimento e fricção (ex.: não deixe os conectores perto das pernas durante o FES Cycling)
- Se um cabo apresentar estimulação intermitente, verifique se há dobras ou "kinks" ao longo do cabo

---

## Teste em bancada 
>  Antes de testar qualquer eletroestimulador na própria pele, é recomendado realizar um teste em bancada para verificar se o equipamento está fornecendo a corrente e a forma de onda esperadas.

![WhatsApp Image 2026-04-07 at 14 22 23](https://github.com/user-attachments/assets/f0177582-d491-49c7-896e-c04e06a4116a)

### Materiais Necessários

- Eletroestimulador e cabo do canal a ser verificado;
- Resistor de potência — para suportar os pulsos de energia, deve ser dimensionado para aguentar a potência dissipada durante a estimulação;
- Terminais adaptados para conexão ao resistor;
- Osciloscópio e cabos de prova.

### Por que usar um resistor?
 
O resistor substitui a pele e o tecido muscular no circuito, simulando a impedância da interface eletrodo-pele. Isso permite observar a forma de onda real da estimulação antes de qualquer contato com o participante.

![WhatsApp Image 2026-04-07 at 14 22 20](https://github.com/user-attachments/assets/758621e2-09ba-4719-8c60-68e001694eea)

No exemplo da imagem a cima, foi utilizado um resistor de **1 kΩ / 5 W**. A escolha do valor segue a Lei de Ohm — com uma corrente de teste de, por exemplo, 10 mA, a tensão esperada nos terminais do resistor será:
 
```
V = R × I  →  V = 1000 × 0,010 = 10 V
```
 
A potência dissipada pelo resistor durante um pulso pode ser estimada por:
 
```
P = I² × R  →  P = (0,010)² × 1000 = 0,1 W
```
 
Como a estimulação é pulsada (não contínua), a potência média real é muito menor que o pico — por isso um resistor de 5 W oferece margem de segurança adequada para esse tipo de teste.
 
### O que observar no osciloscópio
 
- **Forma de onda bifásica** — confirma que o pulso está sendo gerado corretamente
- **Largura de pulso (PW)** — deve corresponder ao valor configurado no código
- **Amplitude de tensão** — dividindo pela resistência, você obtém a corrente real entregue: `I = V / R`
- **Frequência** — deve bater com o parâmetro `FREQ` configurado



---

## Desmontagem e Guarda do Equipamento

1. Encerre a estimulação pelo software (`stop_ccl()`) antes de qualquer desconexão
2. Desligue o RehaStim pelo painel — aguarde o desligamento completo
3. Remova os eletrodos da pele com cuidado, sem arrancar
4. Desconecte os cabos dos canais segurando sempre pelo conector
5. Enrole cada cabo individualmente em círculos suaves e guarde no local apropriado
6. Desconecte o cabo USB do computador
7. Guarde o RehaStim e os cabos na maleta de transporte original
