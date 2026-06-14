5.1 Decisões de Design Justificadas
Para cada decisão abaixo, você deve ser capaz de explicar o porquê:
1.	Por que modelou os relacionamentos dessa forma e não de outra?
A relação foi projetada utilizando chaves estrangeiras, garantindo a integridade referencial e permitindo consultas eficientes.

2.	Por que escolheu colocar determinada regra no validator do Pydantic versus na camada de serviço?
Coloquei validações como datas obrigatórias e tipos de dados no Pydantic para garantir que dados inválidos não cheguem nem ao banco de dados, nem à lógica de negócio. Isso previne erros de integridade desde o início. A regra de negócio fica na camada de serviço para separar responsabilidades.

3.	Por que a migration 2 foi necessária? O que mudou no entendimento do domínio?
A Migration 1 criou apenas as entidades cadastrais de infraestrutura. No entanto, ao aprofundarmos no fluxo de negócio da oficina, identificamos um risco operacional: um técnico poderia, por erro de digitação no sistema, adicionar o mesmo produto em duas linhas separadas dentro da mesma Ordem de Serviço, gerando redundância de dados e inconsistência no controle de inventário.

A Migration 2 foi necessária para introduzir as tabelas dinâmicas (OS e os_itens) e aplicar uma restrição de integridade rígida a nível de banco. Com isso, o entendimento do domínio evoluiu para garantir que cada insumo seja exclusivo por Ordem de Serviço, forçando o sistema a incrementar a quantidade em uma linha existente em vez de duplicar registros.

4.	Qual seria o comportamento correto se dois usuários tentassem modificar o mesmo recurso simultaneamente? (race condition — implementar ou argumentar)
Para o cenário onde o Usuário 1 acessa uma Ordem de Serviço/Venda e a mantém aberta em tela de edição, adotariamos o modelo de Bloqueio de alteração da OS. O comportamento do sistema impederia que o Usuário 2 abra a mesma OS em modo de edição, permitindo a ele apenas a visualização dos dados até que o Usuário 1 libere o recurso

5.	Quais estados são terminais? Por que não faz sentido retornar de um estado terminal?
Os estados terminais são `Cancelado` e `Concluído`. Uma vez que uma Ordem de Serviço é cancelada (por desistência) ou concluída (serviço finalizado e pago), não faz sentido permitir alterações como adicionar peças ou mudar o status para aberto novamente, pois isso violaria a integridade histórica e lógica do fluxo de trabalho.

5.2 Consistência em Cenários de Borda
Você deve identificar e tratar pelo menos 3 cenários de borda específicos do seu domínio. Exemplos do que pode ser relevante dependendo do domínio escolhido:
•	O que acontece quando uma entidade pai é deletada e possui filhos ativos?
Não é permitido deletar um Cliente ou Equipamento (entidades pais) que possua Ordens de Serviço ativas (entidades filhas) vinculadas a eles. Adicionalmente, restrições do banco de dados (RESTRICT) impedem a remoção de clientes/equipamentos se houver qualquer OS associada.

•	O que acontece quando um recurso limitado (vagas, estoque, saldo) chega a zero?
Não é permitido adicionar um item (produto) a uma OS se a quantidade desejada for superior à disponível no estoque (quantidade_estoque). O sistema permite criar uma OS vazia, mas bloqueia a inclusão de itens sem estoque suficiente.

•	O que acontece quando se tenta modificar uma entidade em estado terminal?
Não é permitido modificar uma OS que esteja em estado de "Cancelado" ou "Concluído".

#   B r u n o - I n f o r m a t i c a 

 
                                                                