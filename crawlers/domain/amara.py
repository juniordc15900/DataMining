from dataclasses import dataclass
from datetime import datetime


@dataclass
class Amara:
    tipo: str
    marca: str
    nome: str
    preco: float
    data: datetime