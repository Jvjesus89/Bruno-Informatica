5.1 Decisões de Design Justificadas
Para cada decisão abaixo, você deve ser capaz de explicar o porquê:
1.	Por que modelou os relacionamentos dessa forma e não de outra?

2.	Por que escolheu colocar determinada regra no validator do Pydantic versus na camada de serviço?

3.	Por que a migration 2 foi necessária? O que mudou no entendimento do domínio?

4.	Qual seria o comportamento correto se dois usuários tentassem modificar o mesmo recurso simultaneamente? (race condition — implementar ou argumentar)

5.	Quais estados são terminais? Por que não faz sentido retornar de um estado terminal?

5.2 Consistência em Cenários de Borda
Você deve identificar e tratar pelo menos 3 cenários de borda específicos do seu domínio. Exemplos do que pode ser relevante dependendo do domínio escolhido:
•	O que acontece quando uma entidade pai é deletada e possui filhos ativos?

•	O que acontece quando um recurso limitado (vagas, estoque, saldo) chega a zero?

•	O que acontece quando se tenta modificar uma entidade em estado terminal?

•	O que acontece quando datas/horários se sobrepõem?

•	O que acontece quando um cálculo derivado ficaria negativo ou inválido?
#   B r u n o - I n f o r m a t i c a 

 
                                                                