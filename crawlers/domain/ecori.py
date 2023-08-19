from dataclasses import dataclass
from datetime import datetime


@dataclass
class Ecori:
    model_modulo: str
    port_modulo: str    
    model_inversor: str
    port_inversor: str
    estrutura: str
    preco: float
    data: datetime