import pandas as pd

df = pd.read_csv('sir.csv',  skiprows=3, usecols=[1, 4, 6], encoding="shift-jis")
