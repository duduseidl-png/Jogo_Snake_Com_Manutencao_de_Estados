import json
import os


class SaveGame:
    #"""Cuida do arquivo de jogo salvo (savegame.json).

   # Esta classe não conhece as regras do jogo: ela só grava e lê um dicionário
    #em formato JSON. Quem decide O QUE entra nesse dicionário é o game.py.
    #"""

    # Informações que precisam existir no arquivo para ele ser considerado válido
    CHAVES = (
        'x_cobra', 'y_cobra', 'x_controle', 'y_controle',
        'x_maca', 'y_maca', 'pontos', 'comprimento_inicial', 'lista_cobra',
    )

    def __init__(self, nome_arquivo='savegame.json'):
        pasta = os.path.dirname(os.path.abspath(__file__))   # pasta onde este arquivo está
        self.caminho = os.path.join(pasta, nome_arquivo)

    def existe(self):
       # """True se já existe um jogo salvo."""
        return os.path.exists(self.caminho)

    def salvar(self, estado):
        # """Grava o dicionário 'estado' no arquivo JSON."""
        with open(self.caminho, 'w', encoding='utf-8') as arquivo:
            json.dump(estado, arquivo, indent=4)

    def apagar(self):
        # """Apaga o arquivo de jogo salvo. Se ele não existir, não há o que apagar."""
        try:
            os.remove(self.caminho)
        except OSError:
            pass

    def carregar(self):
        # """Lê o arquivo e devolve o dicionário. Devolve None se não existir ou estiver inválido."""
        try:
            with open(self.caminho, 'r', encoding='utf-8') as arquivo:
                estado = json.load(arquivo)
        except (OSError, ValueError):       # arquivo ausente, ilegível ou com JSON quebrado
            return None

        if not isinstance(estado, dict):
            return None
        for chave in self.CHAVES:           # confere se tem todas as informações esperadas
            if chave not in estado:
                return None
        return estado
