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

df_filtrirano = df_spojeno[df_spojeno['Temp_Tla_C'] < 149]
df_anomalije = df_spojeno[df_spojeno['Temp_Tla_C'] > 149]

# Odnos temperature i vlaznosti tla


sns.scatterplot(
    data=df_filtrirano,
    x='Temp_Tla_C',
    y='H2O_Postotak',
    hue='Metan_Senzor',
    palette={"Negativno": "red", "Pozitivno": "blue"}
    )

plt.title('Odnos temperature i vlažnosti tla')
plt.xlabel('Temperatura tla (C)')
plt.ylabel('Vlaga (%)')

# Spremanje datoteke
plt.savefig('assets/graph1_temp_h2o.png')
plt.close()

# Prostorna raspodjela dubine bušenja

sns.scatterplot(
    data=df_filtrirano,
    x='GPS_LONG',
    y='GPS_LAT',
    hue='Dubina_Busenja_cm',
    palette = 'YlOrBr'
    )

plt.title('Prostorna raspodjela dubine bušenja')
plt.xlabel('Geografska dužina (Longitude)')
plt.ylabel('Geografska širina (Latitude)')

# Spremanje datoteke
plt.savefig('assets/graph2_heatmap_depth.png')
plt.close()

# Lokacije pozitivne detekcije metana

sns.scatterplot(
    data=df_filtrirano,
    x='GPS_LONG',
    y='GPS_LAT',
    hue='Metan_Senzor',
    palette={"Negativno": "blue", "Pozitivno": "red"}
    )

plt.title('Lokacije pozitivne detekcije metana')
plt.xlabel('Geografska dužina (Longitude)')
plt.ylabel('Geografska širina (Latitude)')

# Spremanje datoteke
plt.savefig('assets/graph3_methane_scatter.png')
plt.close()

# Geografska analiza uzoraka u krateru Jezero

sns.scatterplot(
    data=df_filtrirano,
    x='GPS_LONG',
    y='GPS_LAT',
    hue='H2O_Postotak',
    palette='viridis'
    )

kandidati = df_filtrirano[(df_filtrirano['Metan_Senzor'] == 'Pozitivno') &
                          (df_filtrirano['Organske_Molekule'] == 'Da')]

sns.scatterplot(
    x=kandidati['GPS_LONG'], y=kandidati['GPS_LAT'],
    marker='*', s=250, color='red', label='Kandidati za život'
    )


plt.title('Geografska analiza uzoraka u krateru Jezero')
plt.xlabel('Geografska dužina (Longitude)')
plt.ylabel('Geografska širina (Latitude)')

# Spremanje datoteke

plt.savefig('assets/graph4_scatter_plot.png')
plt.close()

# Završna mapa misije (Satelitski prikaz Jezero Kratera)

# 1. Priprema praznog platna
plt.figure(figsize=(12, 8))

# 2. Izračunavanje granica (extent) - tražimo minimum i maksimum GPS koordinata
# Format mora biti: [X_min, X_max, Y_min, Y_max]
extent_koordinate = [
    df_filtrirano['GPS_LONG'].min(), df_filtrirano['GPS_LONG'].max(),
    df_filtrirano['GPS_LAT'].min(), df_filtrirano['GPS_LAT'].max()
]

# 3. Učitavanje i prikaz slike
slika_kratera = plt.imread('jezero_crater_satellite_map.jpg')
# Argument aspect='auto' dozvoljava slici da se razvuče preko cijelog grafa
plt.imshow(slika_kratera, extent=extent_koordinate, aspect='auto', alpha=0.7)

# 4. Sada preko slike normalno crtaš svoje točkice (scatter)
sns.scatterplot(
    data=df_filtrirano,
    x='GPS_LONG',
    y='GPS_LAT',
    alpha=0.3,
    hue='H2O_Postotak',
    palette='viridis',
    legend=True
    )

plt.scatter(
    kandidati['GPS_LONG'], kandidati['GPS_LAT'],
    marker='*', s=250, color='yellow', label='Kritične zone bušenja'
)

plt.title('Završna mapa misije (Satelitski prikaz Jezero Kratera)')
plt.xlabel('Geografska dužina (Longitude)')
plt.ylabel('Geografska širina (Latitude)')

# Spremanje datoteke

plt.savefig('assets/graph5_jezero_mission_map(3).jpg')
plt.close()




misija = {
    "misija": "Nexus",
    "akcije": []
}

for index, red in kandidati.iterrows():

    akcija = {
        "ID_Uzorka": int(red['ID_Uzorka']),
        "lokacija": {
            "lat": float(red['GPS_LAT']),
            "lon": float(red['GPS_LONG'])
        },
        "naredbe": [
            {
                "tip": "NAVIGACIJA",
                "opis": "Robot se kreće do zadane lokacije"
            },
            {
                "tip": "SONDIRANJE",
                "dubina_cm": float(red['Dubina_Busenja_cm'])
            },
            {
                "tip": "SLANJE_PODATAKA",
                "parametri": {
                    "temperatura": float(red['Temp_Tla_C']),
                    "vlaga": float(red['H2O_Postotak']),
                    "metan": red['Metan_Senzor'],
                    "organske_molekule": bool(red['Organske_Molekule'])
                }
            }
        ]
    }

    misija["akcije"].append(akcija)

json_paket = json.dumps(misija, indent=4)

with open("misija_nexus.json", "w") as f:
    f.write(json_paket)

url = "https://webhook.site/#!/view/03f33f00-c3a0-4a66-8b06-63f1af147efa"

response = requests.post(url, json=misija)

if response.status_code == 200:
    print("uspješno poslano")
else:
    print(f"Greška pri slanju {response.status_code}")
