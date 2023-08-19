from dataclasses import dataclass
from datetime import datetime


@dataclass
class Aldo:
    nome: str
    descricao: str
    preco: float
    data: datetime