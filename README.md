# desenhador

Utilitário simples de desenho para ensino de lógica de programação.

O objetivo deste programa é facilitar exercícios visuais de lógica de programação.


# Instalação

- Testado com Python 3.9, Pygame 2.0 no Windows 10
- Pode funcionar com Python 3.8


```
pip install -r requirements.txt
```

# Rodando o exemplo

```
python tela.py
```

e em outra janela:

```
python graficos.py
```

Exemplo:

![Tela de exemplo](https://static.nilo.pro.br/outros/desenhador/desenho.png)

# Como funciona

Este programa permite desenhar a partir da linha de comando ou do IDLE.
Como o programa que faz o desenho roda em outro processo, este não trava o editor e permite debugar o cliente.

O programa tela.py deve estar rodando antes que graficos.py seja ativado.

# Modo de uso

## Tela.py

Clique <kbd>s</kbd> para salvar o desenho como tela.png. 
Cuidado para não sobrescrever arquivos anteriores.

Para sair, simplesmente feche a janela.

O servidor suporta vários clientes e caso o cliente desconecte, não é necessário reinicializar tela.py.


## Graficos.py

Simplesmente execute graficos.py para que uma imagem aleatória seja gerada.

Lembre de executar tela.py antes de graficos.py, caso contrário a conexão não será realizada.


# Desenhando

```
from graficos import Graficos

g = Graficos()
g.limpa()
g.grid(False, 2)
g.ponto(10, 5)
g.cor(255, 0, 0)
g.ponto(5, 6)
```

## Limpa

Apaga o desenho e redesenha o grid. Você pode opcionalmente passar o tamanho do novo grid.

Exemplo:

```
g.limpa(16, 16)
```

ou 

```
g.limpa()
```

O valor padrão é 16.

## Grid

Reconfigura o grid. O primeiro parâmetro indica se o grid deve ser desenhado ou não.
O valor padrão é True, ou seja, o grid deve ser desenhado.

O segundo parâmetro é a margem. A margem é um número inteiro que reduz o desenho dentro do grid.
Um valor de 1, faz com que o retângulo seja desenhando dentro da célula do grid. 
O valor de margem é subtraído de cada canto.

Estas alterações só são visíveis após limpar o desenho.

Exemplo:

```
g.grid(True, 0)  # Desenha o grid com margem 0
g.limpa()
```

## Ponto

Desenha um ponto nas cordenadas x, y usando a cor atual.

Exemplo:

```
g.ponto(10, 10)
```

## Cor

Muda a cor atual do desenho.

Exemplo:

```
g.cor(255, 0, 0)  # Vermelho
g.ponto(1, 1)
g.cor(0, 255, 0)  # Verde
g.ponto(2, 2)
g.cor(0, 0, 255)  # Azul
g.ponto(3, 3)
```
