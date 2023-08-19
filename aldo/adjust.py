import pandas as pd
from datetime import datetime
import sys
sys.path.append(".")

def adjust():
    df = pd.read_excel("aldo/aldo_produtos.xlsx")
    df.Preço = df.Preço*0.7
    data = datetime.today().strftime('%Y-%m-%d')
    df['Data'] = data
    df.to_excel(f"resultados-crawler/aldo/aldo_produtos_{data}.xlsx")
    print(df)