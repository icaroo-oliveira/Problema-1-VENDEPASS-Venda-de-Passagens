<h1 align="center"> VENDEPASS: Venda de Passagens</h1>

## Introdução
<div align="justify"> 

No mundo atual, faz-se necessário - em muitos casos - a fragmentação de uma estrutura monolítica e rígida em partes menores, esse é o caso do setor de aviação de baixo custo, que através dessa divisão criou uma estrutura barata e muito mais acessível para voos. Essa fragmentação foi usada tanto na logística operacional interna da empresa, quanto na ideia de um servidor central que possa ser acessado por clientes de forma autônoma. 

Para isso, entretanto, faz-se necessário o estabelecimento de um servidor robusto que possa conseguir responder a diversos clientes, de uma maneira eficaz e segura, e que exponha um conjunto de métodos de comunicação servidor-cliente. Do lado dos clientes, é necessário também a criação de uma entidade instanciável para escolha e compra de passagens, que usará dos métodos do servidor para atualização de informações relevantes. Além disso, um formato de dados que seja comumente compreensível entre servidor e cliente deve ser usado. Foi escolhido o formato JSON (JavaScript Object Notation) para o propósito de armazenamento de informações dos voos. 

Para a implementação, foi usado o subsistema de rede TCP/IP, usando uma API socket básica para comunicação. O uso do TCP/IP se deu pelo fato de ser um padrão, escalável, flexível e seguro/confiável, já que ele garante a entrega dos pacotes de dados (IBM,2024). O projeto em sua completude foi feito usando a linguagem de programação Python, que oferecia recursos diversos como Mutexes, Threads e Queues, que foram de vital importância para o desenvolvimento do problema, principalmente no tocante ao acesso simultâneo. Além disso, foi usado uma biblioteca de grafos para organização de rotas, por distância e disponibilidade. Por fim, para uma melhor confiabilidade no uso e testes, foi adotado o uso de conteinerização com o Docker, promovendo estabilidade nos mais variados ambientes de utilização.

Como resultado, criou-se uma estrutura servidor-cliente onde um servidor pode aceitar diversos clientes simultaneamente de forma que um cliente não interfira com a compra do outro. Existe ainda estabilidade em relação a conexão, no sentido que ela ocorre num período pequeno - somente no intervalo de envio e recebimento de dados - já ocorrendo a desconexão. No geral o sistema é *stateless* (OSSAMA,2023), por não guardar informações relevantes entre requisições e pela estrutura supracitada.

## Metodologia e Resultados

**Arquitetura**: 

O sistema apresenta uma estrutura onde um servidor dispõe de um conjunto de métodos para troca de informações com os clientes. Esse servidor é apoiado por dois arquivos no formato JSON. O primeiro para armazenamento de informações de passagens (que registrará informações das compras de uma pessoa/cpf como distância, número do assento, trajeto e valor) e o segundo, será um arquivo que conterá em si os trechos entre cidades, a distância entre essas cidades e os assentos disponíveis para cada trecho, além de também salvar informações do comprador de um assento de determinado trecho, como o CPF. 

Os módulos do cliente são apoiados por sub-módulos:
* O primeiro está relacionado a utilidades, como cálculo do valor de um caminho por quilômetro e limpeza de terminais (utils_cliente).
* O segundo é chamado *interface*. Que é um sub-módulo responsável por toda interatividade por parte do cliente. Contém métodos que mostram menus, seleção de cidades de origem, destino e caminho (conjunto de trechos) escolhido. É um “módulo meio” responsável por coletar ‘’inputs’’ e passar para a parte de processamento.
* O último, comum também ao servidor, é o *connection*. Ele é o responsável por implementar toda lógica de comunicação. De funções usadas pelo cliente deste módulo estão: configurar socket e conectar cliente com o servidor, enviar e receber mensagens (para o servidor), e desconexão (encerrar conexão) com servidor, além de funções de teste de conexão, usadas para casos onde a queda ocorre.

Já o módulo do servidor é apoiado por dois sub-módulos:
* O primeiro é relacionado a utilidades do servidor, como a criação do grafo de trechos (já predefinido), carregar o grafo (trechos de viagem), carregar as passagens já compradas, salvar grafos e passagens, encontrar caminhos e verificações de compras em um CPF ou caminhos válidos. Ademais, possui também funções para adicionar e retirar threads da fila de acesso a região crítica do sistema, que será melhor abordada em tópicos posteriores.
* O último é o *connection*. Nele está contido funções de configuração de servidor (criação e configuração do socket, associação a uma endereço/porta e estabelecer o número máximo de conexão da fila), receber dados e enviar dados de um cliente, encerrar conexão e testar conexão (usado quando é necessário saber se ainda existe conexão).

**Paradigma de Comunicação**: 

O paradigma aplicado foi o *Stateless* (OSSAMA,2023), visto que cada nova requisição é tratada de forma independente e separada de outras pelo servidor, de forma que o servidor não mantém informações do cliente entre as requisições. Foi escolhido esse paradigma tanto pela escalabilidade - podendo replicar o servidor - de modo que as mais diversas solicitações, nos mais diversos ‘’estágios de compra’’ pudessem ser tratado por qualquer instância desse ‘’server’’, mesmo se uma instância caísse - e até se essa instância caísse e retornasse - a outra poderia continuar, visto que o servidor não mantém informações. Além disso, existe a redução de complexidade, no sentido de ficar salvando estados. Por fim, para a ideia proposta de conexão somente para envio e recebimento de dados e uso de flags, esse foi o melhor modelo para o servidor.

**Protocolo de comunicação**: 

Em relação ao formato das mensagens, o protocolo adota uma estrutura de mensagem como uma ‘’string’’, onde cada campo é separado por vírgulas. Após a formatação da string a ser enviada, a mesma é codificada para bytes e enviada via rede. No recebimento, esses bytes são decodificados novamente para string e a aplicação consegue tratar da forma necessária essa informação. Abaixo as mensagem para uma comunicação Cliente → Servidor (cliente enviando mensagem), sempre de tamanho 5, como mostra a Figura 1:


<p align="center">
  <img src="Imagens/mensagem_cliente.png" width = "600" />
</p>
<p align="center"><strong> Figura 1. Mensagem Cliente -> Servidor </strong></p>
</strong></p>



De outro modo, Servidor → Cliente (servidor enviando mensagem), sempre tamanho 2, como mostra a Figura 2:



<p align="center">
  <img src="Imagens/mensagem_servidor.png" width = "300" />
</p>
<p align="center"><strong> Figura 2. Mensagem Servidor -> Cliente </strong></p>
</strong></p>

Independente de quem envie a informação, o outro lado sempre tem uma forma de recebê-la. O último campo da ‘’string’’ acima é flexível, podendo retornar as passagens compradas por um CPF também. Pelo fato dos campos *Caminho* (cliente -> servidor) e *Caminhos** (servidor -> cliente), serem listas/tuplas, é necessário a conversão das mesmas para *strings json* antes da formatação da mensagem. 

A estrutura das mensagens sempre são respeitadas, mesmo que alguns campos possam ter valor vazio. Todos os campos são autoexplicativos, exceto a “Flag”. Na tabela abaixo, as “Flags” na linha “Cliente” indicam uma comunicação do tipo Cliente → Servidor, de modo que quem cria a “Flag” e envia é o cliente. Na linha “Servidor”, o contrário acontece.

* Flag → indica o tipo de solicitação e como o outro lado deve respondê-la, na Figura 3 as possíveis ‘’flags’’:


<p align="center">
  <img src="Imagens/flags.png" width = "600" />
</p>
<p align="center"><strong> Figura 3. Tipos de Flag por entidade </strong></p>
</strong></p>


As mensagens possíveis por parte do cliente são: 



<div align="center">


| Mensagem (Cliente)                        | Significado                                                |
|-------------------------------------------|------------------------------------------------------------|
| "Caminhos, [Origem], [Destino], ,”        | Solicitando caminhos entre [Origem] e [Destino].            |
| ”Comprar, , ,[Cpf],[Caminho]”             | Comprando uma passagem para o [Caminho].                    |
| “Passagens_Compradas, , ,[Cpf]”           | Solicitando passagens compradas por [Cpf].                  |

</div>


Por parte do servidor:




<div align="center">
  
| Mensagem (Servidor)                        | Significado                                                |
|--------------------------------------------|------------------------------------------------------------|
| “Caminhos_Encontrados, [Caminhos]”         | Retornando caminhos entre Origem-Destino.                  |
| “Novos_Caminhos_Encontrados, [Caminhos]”   | Se o caminho escolhido não existe mais, retorna novos.      |
| “Compra_Feita, ”                           | Confirmando a compra de uma passagem pelo [Caminho].        |
| “Passagens_Encontradas, [Passagens]”       | Passagens compradas por [Cpf].                             |
| “Flag_Invalida, ”                          | Operação não identificada.                                 |


</div>

A Figura 4, exemplifica o fluxo de mensagens para uma compra bem sucedida:


<p align="center">
  <img src="Imagens/fluxo_compra.jpg" width = "600" />
</p>
<p align="center"><strong> Figura 4. Fluxo de mensagens para uma compra bem sucedida </strong></p>
</strong></p>


**Formatação e tratamento de dados**: 

Para formatação de dados foi usado o sistema JSON (Website JSON, 2024), que é um sistema de arquivo baseado em dicionários e listas. Com o JSON foram criados dois tipos de arquivos como já citado anteriormente, um para passagens e outro para trechos. A estrutura do arquivo para passagens é um dicionário que tem como chaves o CPF e valor uma lista que contém todas as compras desse CPF. Cada compra é um dicionário com os caminhos, assentos, distância e valor da viagem como chaves.
Já o arquivo de trechos, são os diversos trechos que ligam as cidades disponíveis no sistema. Tem a estrutura de um dicionário onde as chaves são tuplas que contém um “trecho” (ex: “São paulo”, “Rio de Janeiro”) e valor um dicionário que contém como chaves distância, assentos e CPFs das pessoas que viajarão por aquele trecho.

O grafo da Figura 5 foi usado como base para composição de trechos. A sigla do estado é usada para referenciar as capitais dos estados. É válido salientar, que a união de trechos formam um caminho e pelo fato de que, por exemplo, o voo de Cuiabá -> Goiânia não ser o mesmo que Goiânia -> Cuiabá, o grafo é bidirecional, mesmo a distância sendo as mesma.

<p align="center">
  <img src="Imagens/grafo.png" width = "600" />
</p>
<p align="center"><strong> Figura 5. Grafo de rotas </strong></p>
</strong></p>


**Tratamento de conexões simultâneas e Tratamento de Concorrência**: 

O sistema não permite a compra de forma 100% paralela. Apesar de ser possível diversos clientes estarem comprando - com múltiplas threads sendo disparadas  - (cada thread sendo um cliente), quando uma requisição acontece, é usado um Mutex para travar aquela região de acesso aos dados dos arquivos, isso é feito para que não exista erros de disponibilidade de passagens durante a compra, além da possibilidade de erros inesperados envolvendo condições de corrida. 

Enquanto a região está travada, ou seja, processando uma requisição do cliente, uma outra solicitação de acesso ao arquivo é adicionada em uma fila FIFO, aguardando que a região seja liberada e sua vez na fila chegue. Dessa forma além de garantir a integridade dos dados manipulados, o conceito de concorrência é sanado, visto que o cliente que enviar primeiro a requisição de compra de um trecho terá prioridade ante os demais. 


**Documentação do código**: 

O código está completamente comentado e documentado.


**Emprego do Docker**: 

O código faz uso da conteinerização com Docker, para, como mencionado anteriormente, proporcionar uma ambiente seguro e confiável para testes (RED HAT, 2024). Foi criado um Docker para o servidor, com uma imagem 3.12-slim, instalando as bibliotecas necessárias para grafo e sub-módulos além do ‘’EXPOSE’’ na porta usada. Para o Docker do cliente, foi a mesma imagem python e foi carregado os sub-módulos. Por fim, criou-se um Docker Compose, para orquestrar e criar uma rede que ligasse o Docker do servidor com o do cliente.


**Desempenho e avaliação**: 

O sistema faz uso de Threads (linhas de execuções), sendo que cada uma é disparada para cada solicitação do cliente, isso faz com que exista uma redução no tempo entre solicitações dos mais diversos clientes. Além disso, a fila de solicitação para requisições foi ajustada para 50. Deste modo, é possível armazenar 50 requisições enquanto uma está sendo passada para uma thread. O desempenho do sistema foi satisfatório. Foi feito um script que criou 50 terminais solicitando os mesmos dados, onde o servidor conseguiu processar todas solicitações, sequencialmente, não deixando que uma mesma passagem fosse comprada quando não estivesse mais disponível e garantindo que cliente 1 comprasse antes que cliente 2, graças a fila FIFO para acesso das threads à região crítica (arquivos). 


**Confiabilidade da solução**: 

Foi adicionado tanto para cliente quanto para o servidor um tempo de espera para enviar, receber e se conectar (entre si), usada em casos onde após um tempo excedido (10 segundos) é retornado um erro de temporização. Além disso, excedido esse tempo, o cliente volta sempre para o início do estágio onde estava.

Além disto, foram feitos diversos testes em relação à desconexão, de modo que o sistema continuou funcionando.
* O primeiro foi quando uma conexão cliente/servidor é estabelecida, porém antes de o servidor receber os dados do cliente, o servidor perde rede. Dessa forma, o cliente é informado que o servidor não está mais disponível (não recebeu a resposta da requisição) e ele pode tentar enviar uma requisição novamente, porém como se trata de uma nova conexão, o cliente nem ao menos consegue conectar, visto que o servidor está sem rede. Ao servidor estabelecer rede novamente, é possível prosseguir a compra a partir daquele momento, a base disso é o fato do servidor ser *stateless*.
* O segundo teste é parecido com o primeiro, mas agora se o cliente perde conexão, antes de receber a resposta de uma requisição enviada ao servidor. Como o servidor já recebeu a requisição do cliente, a compra já foi processada em sistema, porém como o cliente caiu, o cliente não chega a receber a confirmação.

Outros testes foram realizados como: Enviando flags inválidas ao servidor, forçando ocorrências de timeout através de "sleep's", cliente conectando no endereço de servidor inválido, cliente conectando ao servidor que não está operando, entre outros. Para todos estes, a aplicação conseguiu identificar e se possível solucionar, mostando a eficiência do sistema.

# Conclusão

Por fim, foi possível criar um sistema servidor-cliente robusto e resistente a falhas, com forma maleável e eficaz. O fato de não haver registro de estados por parte do servidor, bem como as conexão só ocorrerem no momento de envio da mensagem, faz desse sistema bastante seguro. O servidor aceita múltiplas linhas de execução (Threads) e possuí segurança no que diz respeito a acesso e segurança dos dados, evitando problemas como compras de uma passagem não mais disponível. De melhoras para o sistema, um sistema de cache para maior velocidade de processamento seria uma adição bem-vinda para o sistema, de forma adicionar ainda mais eficácia do servidor no processamento de requisições. No mais foi possível criar contêiner para o servidor e cliente, proporcionando um ambiente de testagem seguro.

# Referências

OSSAMA, Ahmed. Stateless vs Stateful Servers (With Examples). Medium. Disponível em: https://medium.com/@ahmedossama22/stateless-vs-stateful-servers-with-examples-6e37223c028f. Acesso em: 23 set. 2024.

JSON. Introducing JSON. Disponível em: https://www.json.org/json-en.html. Acesso em: 23 set. 2024.

RED HAT. O que é Docker?. Disponível em: https://www.redhat.com/pt-br/topics/containers/what-is-docker. Acesso em: 23 set. 2024.

IBM. Protocolos TCP/IP. Disponível em: https://www.ibm.com/docs/pt-br/aix/7.3?topic=protocol-tcpip-protocols. Acesso em: 23 set. 2024.
