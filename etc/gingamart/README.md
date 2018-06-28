# README #

Este é um pequeno projeto para o processo seletivo da Ginga One implementado utilizando o framework Falcon em Python 3.4. Para mais detalhes de quais pacotes foram utilizados, consulte o arquivo `pip-requirements.txt` e `apt-requirements.txt`.

#### Entregando mercadorias ####

O Walmart está desenvolvendo um novo sistema de logística e sua ajuda é muito importante neste momento. Sua tarefa será desenvolver o novo sistema de entregas visando sempre o menor custo. Para popular sua base de dados o sistema precisa expor um Webservice que aceite o formato de malha logística (exemplo abaixo). Nesta mesma requisição o requisitante deverá informar um nome para este mapa. É importante que os mapas sejam persistidos para evitar que a cada nova requisição todas as informações desapareçam. O formato de malha logística é bastante simples, cada linha mostra uma rota: ponto de origem, ponto de destino e distância entre os pontos em quilômetros.

    A B 10
    B D 15
    A C 20
    C D 30
    B E 50
    D E 30

Com os mapas carregados o requisitante irá procurar o menor valor de entrega e seu caminho, para isso ele passará o mapa, nome do ponto de origem, nome do ponto de destino, autonomia do caminhão (km/l) e o valor do litro do combustível, agora sua tarefa é criar este Webservice. Um exemplo de entrada seria, mapa SP, origem A, destino D, autonomia 10, valor do litro 2,50; a resposta seria a rota A B D com custo de 6,25.

### Instalação ###

* Sistemas baseados em Debian:
 * Vá para o diretório raiz do projeto e execute:
 * `cat apt-requirements.txt | xargs sudo apt-get install -y`
 * `virtualenv -p /usr/bin/python3 .venv`
 * `source .venv/bin/activate`
 * `pip install -r pip-requirements.txt`

* Para os demais sistemas ou em caso da instalação acima não funcionar, siga as instruções na página do [scipy](http://www.scipy.org/install.html)

* Como executar o projeto
 * Dentro do diretório raiz do projeto, execute:
 * `source .venv/bin/activate`
 * `gunicorn gingamart:app -b 127.0.0.1:8000 --reload`

* Como executar os testes
* Os testes utilizam o nose e o webtests, basta executar na raiz do projeto:
 * `nosetests .`

### Como usar ###

* Após o projeto estar instalado, configurado e rodando, basta acessá-lo em http://127.0.0.1:8000/. Você terá um json como resposta se tudo tiver corrido bem.
* Para cadastrar um grafo envie `name` - nome do grafo - e `graph` - grafo mapeado como na especificação - via POST para http://127.0.0.1:8000/graph. Ele te retornará status=True se for bem sucedido.
* Tendo cadastrado e guardado o nome do grafo, envie os seguintes valores via GET para http://127.0.0.1:8000/ para fazer buscas em grafos cadastrados:
 * `name` - nome do grafo
 * `start` - ponto inicial do percurso
 * `target` - destino
 * `autonomy` - autonomia
 * `gas_price` - preço do combustível
