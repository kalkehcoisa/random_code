## Nuveo JSON/CSV ##

Projeto para o processo seletivo da Nuveo.com.br
Implementado usando go 1.6.2 para Linux 32bits.

- - -

### Especificação ###

1. Escrever uma função onde recebe uma URL (endereço HTTP) que seja um JSON ou CSV (precisa processar os dois tipos).
2. Colocar esse conteúdo do JSON ou CSV dentro de uma estrutura de dados que contém os seguintes campos:
 - nome
 - email
 - sexo
 - idade
 - OUTROS (dinamicamente precisa armazena outros campos que chegarem)
3. Escrever teste com todas as possibilidades, ou seja, cobertura de 100%
- - -

### Instruções de uso ###
É só executar o main.go passando uma url como parâmetro. Da seguinte forma:  
> go run main.go http://exemplo.com
> 

Se não for passada uma url
Se a url não contiver um JSON ou CSV, o programa vai retornar um erro.

### Testes ###
É só rodar `go test -cover -v -covermode=count -coverprofile=coverage.out` para executá-los.

* * *
