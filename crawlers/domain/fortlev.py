from dataclasses import dataclass
from datetime import datetime


@dataclass
class Fortlev:
    potencia: str
    preco: float
    modulo: str    
    qtd_modulo: str
    inversor: str
    qtd_inversor: str
    estrutura: str
    data: datetime