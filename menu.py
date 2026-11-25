import pygame

from pygame.locals import *
from sys import exit


class Menu:
    #"""Classe base de todos os menus do jogo.

    #Cuida do que é igual em qualquer menu: guardar as opções, mover a seleção
    #com W/S ou setas, desenhar as opções e rodar o laço de repetição do menu.
    #As classes filhas (MenuPrincipal, MenuPausa) só definem o que acontece ao
    #confirmar uma opção e como a tela é desenhada.
    #"""

    BRANCO = (255, 255, 255)
    PRETO = (0, 0, 0)
    VERDE = (0, 150, 0)
    CINZA = (130, 130, 130)
    VERMELHO = (200, 0, 0)

    def __init__(self, tela, relogio, opcoes):
        self.tela = tela
        self.relogio = relogio
        self.largura, self.altura = tela.get_size()
        self.opcoes = opcoes
        self.selecionada = 0    # índice da opção destacada

        self.fonte_titulo = pygame.font.SysFont('arial', 80, True)
        self.fonte_opcao = pygame.font.SysFont('arial', 36, True)
        self.fonte_dica = pygame.font.SysFont('arial', 20, True, True)

    # ---------------- desenho ----------------
    def escrever_centralizado(self, texto, fonte, cor, y):
        imagem = fonte.render(texto, True, cor)
        self.tela.blit(imagem, imagem.get_rect(center=(self.largura // 2, y)))

    def desenhar_opcoes(self, y_inicial, desativadas=()):
        #"""Desenha as opções uma embaixo da outra. 'desativadas' = índices que ficam cinza."""
        for i, opcao in enumerate(self.opcoes):
            if i in desativadas:
                cor = self.CINZA
            elif i == self.selecionada:
                cor = self.VERDE
            else:
                cor = self.PRETO
            texto = f'> {opcao} <' if i == self.selecionada else opcao
            self.escrever_centralizado(texto, self.fonte_opcao, cor, y_inicial + i * 60)

    def desenhar(self):
        #"""Cada menu desenha a sua própria tela."""
        raise NotImplementedError

    # ---------------- comportamento ----------------
    def ao_apertar_tecla(self, tecla):
        #"""Navega pelas opções. Devolve o resultado do menu quando o jogador confirma, senão None."""
        if tecla in (K_w, K_UP):
            self.selecionada = (self.selecionada - 1) % len(self.opcoes)
        elif tecla in (K_s, K_DOWN):
            self.selecionada = (self.selecionada + 1) % len(self.opcoes)
        elif tecla in (K_RETURN, K_KP_ENTER):
            return self.confirmar(self.selecionada)
        return None

    def confirmar(self, indice):
        #"""O que fazer quando o jogador aperta ENTER numa opção. Cada menu define o seu."""
        raise NotImplementedError

    def ao_fechar_janela(self):
        #"""Por padrão, fechar a janela encerra o programa (como no seu jogo original)."""
        pygame.quit()
        exit()

    def executar(self):
        #"""Mostra o menu e só volta quando o jogador escolhe algo. Devolve o resultado da escolha."""
        while True:
            self.relogio.tick(30)

            for event in pygame.event.get():
                if event.type == QUIT:
                    resultado = self.ao_fechar_janela()
                    if resultado is not None:
                        return resultado
                if event.type == KEYDOWN:
                    resultado = self.ao_apertar_tecla(event.key)
                    if resultado is not None:
                        return resultado

            self.desenhar()
            pygame.display.update()


class MenuPrincipal(Menu):
    #"""Menu inicial: Novo Jogo, Carregar Jogo e Sair.

    #executar() devolve uma tupla (acao, estado):
        #('novo', None)          -> começar um jogo do zero
        #('carregar', dicionario) -> continuar o jogo salvo
    #"""

    def __init__(self, tela, relogio, save):
        super().__init__(tela, relogio, ['Novo Jogo', 'Carregar Jogo', 'Sair'])
        self.save = save        # objeto SaveGame, usado para checar/ler o arquivo
        self.aviso = ''

    def executar(self):
        self.selecionada = 0
        self.aviso = ''
        return super().executar()

    def ao_apertar_tecla(self, tecla):
        self.aviso = ''         # qualquer tecla apaga o aviso anterior
        return super().ao_apertar_tecla(tecla)

    def confirmar(self, indice):
        if indice == 0:                     # Novo Jogo
            return ('novo', None)

        if indice == 1:                     # Carregar Jogo
            estado = self.save.carregar()
            if estado is not None:
                return ('carregar', estado)
            self.aviso = 'Nenhum jogo salvo encontrado!'
            return None                     # continua no menu

        return self.ao_fechar_janela()      # Sair

    def desenhar(self):
        self.tela.fill(self.BRANCO)
        self.escrever_centralizado('Snake', self.fonte_titulo, self.VERDE, 100)

        # "Carregar Jogo" (índice 1) fica cinza se ainda não existe save
        self.desenhar_opcoes(220, desativadas=() if self.save.existe() else (1,))

        if self.aviso:
            self.escrever_centralizado(self.aviso, self.fonte_dica, self.VERMELHO, 410)
        self.escrever_centralizado('W/S ou setas: navegar    ENTER: escolher',
                                   self.fonte_dica, self.CINZA, 450)
