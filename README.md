# VENDEPASS: Venda de Passagens

## Introdução

No mundo atual, faz-se necessário - em muitos casos - a fragmentação de uma estrutura monolítica e rígida em partes menores, esse é o caso do setor de aviação de baixo custo, que através dessa divisão criou uma estrutura barata e muito mais acessível para voos. Essa fragmentação foi usada tanto na logística operacional interna da empresa, quanto na ideia de um servidor central que possa ser acessado por clientes de forma autônoma. Para isso, entretanto, faz-se necessário o estabelecimento de um servidor robusto que possa conseguir responder a diversos clientes, de uma maneira eficaz e segura, e que exponha um conjunto de métodos de comunicação servidor-cliente. Do lado dos clientes, é necessário também a criação de uma entidade instanciável para escolha e compra de passagens, que usará dos métodos do servidor para atualização de informações relevantes. Além disso, um formato de dados que seja comumente compreensível entre servidor e cliente deve ser usado. Foi escolhido o formato JSON (JavaScript Object Notation) para o propósito de armazenamento de informações dos voos. 

Para a implementação, foi usado o subsistema de rede TCP/IP, usando uma API socket básica para comunicação. O projeto em sua completude foi feito usando a linguagem de programação Python, que oferecia recursos diversos como Mutexes e Threads, que foram de vital importância para o problema, principalmente no tocante ao acesso simultâneo. Além disso, foi usado uma biblioteca de grafos para organização de rotas, por distância e disponibilidade. Por fim, para uma melhor confiabilidade no uso e teste, foi adotado o uso de conteinerização com o Docker, promovendo estabilidade nos mais variados ambientes de utilização.

Como resultado, criou-se uma estrutura servidor-cliente onde um servidor pode aceitar diversos clientes simultaneamente de forma que um cliente não interfira com a compra do outro. Existe ainda estabilidade em relação a conexão, no sentido que ela ocorre num período pequeno - somente no intervalo de envio e recebimento de dados - já ocorrendo a desconexão. No geral o sistema é ”stateless”, por não guardar informações relevantes entre requisições e pela estrutura supracitada.

## Metodologia e Resultados

Arquitetura: O sistema apresenta uma estrutura onde um servidor dispõe de um conjunto de métodos para troca de informações com os clientes. Esse servidor é apoiado por dois arquivos no formato JSON. O primeiro para armazenamento de informações de passagens (que registrará informações como distância, trajeto, valor e outros, para uma pessoa) e o segundo, será um arquivo que conterá em si os trechos e assentos disponíveis para aquele trecho, além de também salvar informações sobre os passageiros, como o CPF. 

Os módulos do cliente são apoiados por sub-módulos:
* O primeiro está relacionado a utilidades, como cálculo de distâncias e limpeza de terminais (utils_cliente).
* O segundo é chamado ‘’interface’’. Que é um sub-módulo responsável por toda interatividade por parte do cliente. Contém métodos que mostram menus, seleção de cidades de origem, destino e caminho (conjunto de trechos) escolhido. É um “módulo meio” responsável por coletar ‘’inputs’’ e passar para a parte de processamento.
*O último, comum também ao servidor, é o ‘’connection’’, ele é o responsável por implementar toda lógica de comunicação. De funções usadas pelo cliente deste módulo estão: conectar cliente com o servidor, enviar e receber mensagens (para o servidor), e desconexão (encerrar conexão) com servidor, além de funções de teste de conexão, usadas para casos onde a queda ocorre.

