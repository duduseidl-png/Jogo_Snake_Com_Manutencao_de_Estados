import pygame

from pygame.locals import *
from menu import Menu


class MenuPausa(Menu):
    #"""Tela de pausa (ESC durante o jogo): Continuar ou Voltar ao Menu.

    #executar() devolve:
        #'continuar' -> voltar a jogar
        #'menu'      -> o jogador quer voltar ao menu principal
        #'fechar'    -> o jogador fechou a janela durante a pausa
    #O game.py decide o que fazer com cada resposta (por exemplo, salvar o jogo).
    #"""

    TRANSPARENCIA = 215     # 0 = película invisível, 255 = branco total

    def __init__(self, tela, relogio):
        super().__init__(tela, relogio, ['Continuar', 'Voltar ao Menu'])
        self.fundo = None

    def executar(self):
        self.selecionada = 0
        self.fundo = self.tirar_foto_do_jogo()
        return super().executar()

    def tirar_foto_do_jogo(self):
        #"""Copia o que está na tela agora (o jogo congelado) e cobre com uma película branca."""
        foto = self.tela.copy()
        pelicula = pygame.Surface(self.tela.get_size())
        pelicula.fill(self.BRANCO)
        pelicula.set_alpha(self.TRANSPARENCIA)
        foto.blit(pelicula, (0, 0))
        return foto

    def ao_apertar_tecla(self, tecla):
        if tecla == K_ESCAPE:               # ESC de novo = continuar jogando
            return 'continuar'
        return super().ao_apertar_tecla(tecla)

    def confirmar(self, indice):
        return 'continuar' if indice == 0 else 'menu'

    def ao_fechar_janela(self):
        return 'fechar'                     # quem chamou decide (o game.py salva e encerra)

    def desenhar(self):
        self.tela.blit(self.fundo, (0, 0))
        self.escrever_centralizado('Pausado', self.fonte_titulo, self.VERDE, 130)
        self.desenhar_opcoes(240)
        self.escrever_centralizado('Voltar ao Menu salva o jogo automaticamente',
                                   self.fonte_dica, self.CINZA, 400)
        self.escrever_centralizado('ENTER: escolher    ESC: continuar',
                                   self.fonte_dica, self.CINZA, 450)
