# Licença GNU GPL v3
# Autor: Nilo Menezes
# https://www.nilo.pro.br
# GitHub: https://github.com/lskbr/desenhador

import socket
import pygame
import select

from pygame.locals import MOUSEBUTTONDOWN, KEYDOWN, K_s, QUIT
from enum import Enum

#
# Globais
#
ENDERECO = '127.0.0.1', 8800
SERV_BACKLOG = 10
COR = (255, 0, 0)

# Cores
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
CINZA = (128, 128, 128)

# Tamanho da grade: tgrade x tgrade
TGRADE = 16

# Tamanho da Janela
XTAM = 800
YTAM = 800


class Posição:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def tuple(self):
        return (self.x, self.y)

    def __str__(self):
        return(f"(x={self.x}, y={self.y})")


class Modo(Enum):
    RETANGULO = 1
    OVAL = 2


class Servidor:
    def __init__(self, cor=COR, endereco=ENDERECO, serv_backlog=SERV_BACKLOG,
                 tgrade_x=TGRADE, tgrade_y=TGRADE, xtam=XTAM, ytam=YTAM):
        self.xtam = xtam
        self.ytam = ytam
        self.conexoes = []
        self.recebido = {}
        self.endereco = endereco
        self.backlog = serv_backlog
        self.tgrade = Posição(tgrade_x, tgrade_y)
        self.cor = cor
        self.modo = Modo.RETANGULO
        self.desenha_grid = True
        self.margem = 0  # Desenha os quadrados dentro do grid
        self.inicialize()
        self.inicialize_servidor()
        self.atualiza_grid()
        self.grade()
        print(f"Tamanho = {self.tamanho}\n"
              f"Largura = {self.largura} Altura = {self.altura}\n")

    def inicialize(self):
        pygame.init()
        pygame.display.set_mode((self.xtam, self.ytam), 0)
        pygame.display.set_caption("Desenho")
        self.superficie = pygame.display.get_surface()
        tamanho = self.superficie.get_size()
        self.tamanho = Posição(tamanho[0], tamanho[1])

    def atualiza_grid(self):
        self.largura = self.xtam / self.tgrade.x
        self.altura = self.ytam / self.tgrade.y

    def inicialize_servidor(self):
        self.servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servidor.bind(self.endereco)
        self.servidor.settimeout(0.0)
        self.servidor.listen(self.backlog)

    def corrija(self, posicao):
        posicao.x *= self.largura
        posicao.y *= self.altura
        return posicao

    def tela_para_grid(self, posicao):
        return Posição(posicao[0] // self.largura, posicao[1] // self.altura)

    def calcule_limites(self, p):
        return (p.x + self.margem, p.y + self.margem,
                self.largura - self.margem, self.altura - self.margem)

    def crie_rect_com_limites(self, p):
        return pygame.Rect(*self.calcule_limites(p))

    def ponto(self, posicao, cor):
        p1 = self.corrija(Posição(posicao.x, posicao.y))
        if self.modo == Modo.RETANGULO:
            pygame.draw.rect(self.superficie, cor,
                             self.crie_rect_com_limites(p1))
        elif self.mode == Modo.OVAL:
            pygame.draw.ellipse(self.superficie, cor,
                                self.crie_rect_com_limites(p1))

        print(f"Ponto: {posicao} Cor: {cor}")
        pygame.display.update()

    def linha(self, inicio, fim, cor):
        pass

    def coordenadas(self, dimensao):
        pass

    def grade(self):
        if self.desenha_grid:
            for pedaco in range(self.tgrade.x):
                pygame.draw.line(self.superficie, AZUL,
                                 (pedaco * self.largura, 0),
                                 (pedaco * self.largura, self.tamanho.y))
            for pedaco in range(self.tgrade.y):
                pygame.draw.line(self.superficie, AZUL,
                                 (0, pedaco * self.altura),
                                 (self.tamanho.y, pedaco * self.altura))
        pygame.display.update()

    def limpa(self):
        self.superficie.fill(PRETO)
        self.atualiza_grid()
        self.grade()

    def processa_comando(self, comando, parametros):
        comando = comando.decode("utf-8")
        # print(f"> COMANDO {comando}")
        if comando == "PO":
            self.ponto(Posição(int(parametros[0]), int(parametros[1])),
                       self.cor)
            # print(f"> PONTO {comando} {parametros}")
        elif comando == "PC":
            self.ponto(Posição(int(parametros[0]), int(parametros[1])),
                       parametros[2])
        elif comando == "CL":
            self.tgrade = Posição(int(parametros[0]), int(parametros[1]))
            self.limpa()
        elif comando == "CO":
            self.cor = (int(parametros[0]), int(parametros[1]), int(parametros[2]))
            # print(self.cor)
        elif comando == "GD":
            self.desenha_grid = int(parametros[0]) == 1
            self.margem = int(parametros[1])

    def remove_conexao(self, conexao):
        remova = []
        for c in self.conexoes:
            if c[0].fileno == conexao.fileno:
                remova.append(c)
        for r in remova:
            self.conexoes.remove(r)
            if conexao.fileno in self.recebido:
                del self.recebido[conexao.fileno]

    def verifica_dados(self):
        try:
            rc = [x[0] for x in self.conexoes]
            r, _, ex = select.select(rc, [], rc, 0)

            for x in ex:
                self.remove_conexao(x)

            for cc in r:
                n = cc.recv(1024)
                if len(n) == 0:
                    self.remove_conexao(cc)
                    cc.close()
                    continue
                self.recebido[cc.fileno] += n
                print(f"Recebi: {n}")
                while True:
                    c = self.recebido[cc.fileno].find(b'\n')
                    if c != -1:
                        linha = self.recebido[cc.fileno][:c]
                        comando = linha[0:2]
                        parametros = linha[3:].split(b",")
                        self.processa_comando(comando, parametros)
                        self.recebido[cc.fileno] = self.recebido[cc.fileno][c + 1:]
                    else:
                        break
        except socket.error as erro:
            numero, nome = erro
            print(f"Erro: {numero} - {nome}")

    def verifica_conexoes(self):
        try:
            r, w, x = select.select([self.servidor],
                                    [self.servidor],
                                    [self.servidor], 0)
            if r:
                conexao, endereço = self.servidor.accept()
                print("Accept OK!")
                self.conexoes += [[conexao, endereço]]
                self.recebido[conexao.fileno] = b""
                print(self.conexoes)
            if x:
                print("Erro no servidor")
        except Exception:
            raise

    def loop(self):
        try:
            relogio = pygame.time.Clock()
            while True:
                e = pygame.event.peek()
                if e:
                    e = pygame.event.poll()
                    if e.type == MOUSEBUTTONDOWN:
                        # self.ponto(self.tela_para_grid(e.pos), AZUL)
                        ptela = self.tela_para_grid(e.pos)
                        pygame.display.set_caption(f"Desenho: {ptela.x}, {ptela.y}")
                    elif e.type == KEYDOWN and e.key == K_s:
                        pygame.image.save(self.superficie, 'tela.png')
                    elif e.type == QUIT:
                        raise SystemExit
                self.verifica_conexoes()
                if self.conexoes:
                    self.verifica_dados()
                # print(relogio.get_fps())
                relogio.tick(60)
        finally:
            pygame.display.quit()


g = Servidor()
g.loop()
