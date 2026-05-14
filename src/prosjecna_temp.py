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

# Izračun prosječne temperature
prosjecna_temp = df_filtrirano['Temp_Tla_C'].mean()
print(f"Prosječna temperatura: {prosjecna_temp:.2f}°C")
