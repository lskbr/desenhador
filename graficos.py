# Licença GNU GPL v3
# Autor: Nilo Menezes
# https://www.nilo.pro.br
# GitHub: https://github.com/lskbr/desenhador

import socket

IP_TELA = "127.0.0.1"
PORTA_TELA = 8800
TGRADE = 16


class Graficos:
    def __init__(self, ip=IP_TELA, porta=PORTA_TELA):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.connect((ip, porta))
        except socket.error as erro:
            numero, nome = erro
            print(f"Erro: {numero} - {nome}")
        else:
            print("OK! Inicializado.")

    def ponto(self, x, y):
        comando = f'PO {x},{y}\n'
        self.send_comando(comando)

    def cor(self, vermelho, verde, azul):
        comando = f'CO {vermelho},{verde},{azul}\n'
        self.send_comando(comando)

    def limpa(self, colunas=TGRADE, linhas=TGRADE):
        comando = f'CL {colunas},{linhas}\n'
        self.send_comando(comando)

    def grid(self, desenha_grid: bool, margem: int):
        grid_flag = 1 if desenha_grid else 0
        comando = f'GD {grid_flag},{margem}\n'
        self.send_comando(comando)

    def send_comando(self, comando):
        self.s.send(comando.encode("utf-8"))

    def finaliza(self):
        self.s.close()


if __name__ == "__main__":
    import random
    g = Graficos()
    linhas = colunas = 32
    g.grid(False, 8)
    g.limpa(colunas, linhas)
    g.cor(255, 255, 255)
    while True:
        g.ponto(random.randint(0, colunas - 1),
                random.randint(0, linhas - 1))
        g.cor(random.randint(0, 255),
              random.randint(0, 255),
              random.randint(0, 255))
