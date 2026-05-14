import json
import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df_uzorci = pd.read_csv('data/mars_uzorci.csv', sep = ';', decimal = ',')
df_lokacija = pd.read_csv('data/mars_lokacije.csv', sep = ';', decimal = ',')

df_spojeno = pd.merge(
        df_lokacija,
        df_uzorci,
        on='ID_Uzorka'
)
df_filtrirano = df_spojeno[df_spojeno['Temp_Tla_C'] < 150]
ukupna_temp = 0
for i in range(0,len(df_filtrirano)):
  
