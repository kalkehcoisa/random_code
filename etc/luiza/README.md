# Desafio Luiza Labs #

Esta é uma resolução do desafio do Luzia Labs realizada usando basicamente Bottle, SqlAlchemy e sqlite para gerar uma API REST para manusear dados de usuários do Facebook através do graph API.


### Instalação ###

Para instalar basta executar os comandos a seguir:  
`git clone https://bitbucket.org/kalkehcoisa/luiza/ luiza`  
`cd luiza`  
`pip install -r requirements.txt`  

Para rodar, é só executar:  
`python api.py`


### Testes ###

Os testes foram feitos usando nose e webtest com nose-cov para gerar os relatório de cobertura dos testes.

Para executar e gerar os arquivos de informação de cobertura:  
`nosetests --with-cov --cov-report html --cover-package=luiza` 

Se quiser executar somente executar os testes:  
`nosetests .`

Ao terminar de executar os testes, para ver os dados de cobertura é só abrir o arquivo `index.html` dentro do diretório `htmlcov/index.html` - criado após rodar os testes com a primeira linha de comandos.


### Materias utilizados ###

* [Tutorial de bottle-sqlalchemy](https://github.com/iurisilvio/bottle-sqlalchemy)
* [RFC 2661](http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html)
* [Código fonte do bottle](https://github.com/bottlepy/bottle/tree/master/test)
* [StackOverflow (nose-cov)](http://stackoverflow.com/a/24828596)
* [Github do webtest](https://github.com/Pylons/webtest/blob/master/docs/testapp.rst)


### Melhorias ###

* Os testes funcionais feitos com webtest não estão gerando dados de cobertura. Não sei se é uma limitação da biblioteca ou se foi alguma falha de configuração minha. Poderia mudar para selenium, mas creio que seja um exagero para o caso - além de ter que instalar JVM, configurar o ambiente, montar novos casos de teste, etc, etc.
