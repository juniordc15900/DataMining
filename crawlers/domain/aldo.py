from dataclasses import dataclass
from datetime import datetime



class Aldo():
    def __init__(self,nome,descricao,preco,data):
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.data = data