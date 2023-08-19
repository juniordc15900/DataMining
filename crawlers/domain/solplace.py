from dataclasses import dataclass
from datetime import datetime


@dataclass
class Solplace:
    produto: str
    preco: float
    inversor: str
    modulo: str    
    data: datetime