import os
import folium
import json
import pandas as pd
import mapclassify as mc
from folium.plugins import MarkerCluster

carte = folium.Map(location=[63.0, 15.0], tiles='cartodbpositron', zoom_start=5)  

geom = os.path.join('./', 'sweden.geojson')
sweden = json.load(open(geom))

# Création d'un DataFrame
regions_data = pd.DataFrame([
    {"name": feature["properties"]["name"], "density": feature["properties"]["density"]}
    for feature in sweden["features"]
])

# Natural Breaks pour déviser la densité de population en trois classes
jenks_breaks = mc.NaturalBreaks(regions_data['density'], k=3)  
bins = jenks_breaks.bins.tolist()
bins = [regions_data['density'].min()] + bins

# Carte choroplèthe
folium.Choropleth(
    geo_data=sweden,
    name="Densité de population",
    data=regions_data,
    columns=["name", "density"],
    key_on="feature.properties.name",
    fill_color="Blues",  
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="Densité de population (hab./km²) - Natural Breaks (Jenks)", 
    bins=bins,
    control=False
).add_to(carte)

# Régions de la Suède interactives
folium.GeoJson(
    sweden,
    name="Régions de Suède",  
    style_function=lambda feature: {
        'fillColor': 'transparent', 
        'color': 'black',
        'weight': 0.5
    },
    highlight_function=lambda feature: {
        'fillColor': '#add8e6', 
        'color': 'black',       
        'weight': 0.5,            
        'fillOpacity': 0.3     
    },
    tooltip=folium.GeoJsonTooltip(
        fields=['name'],
        aliases=["Nom du région:"],  
        style=("background-color: white; color: black; font-weight: bold;")  
    ),
    show=False  
).add_to(carte)

marker_cluster = MarkerCluster(name="Objets économiquement significatifs").add_to(carte)
sites_industriels = [
    {"nom": "Kiruna (Minerai de fer)", "emplacement": [67.8558, 20.2253], "type": "Mine", "details": "La plus grande mine de minerai de fer"},
    {"nom": "Malmberget (Minerai de fer)", "emplacement": [67.1773, 20.6507], "type": "Mine", "details": "Deuxième plus grand gisement"},
    {"nom": "Luleå (Usine métallurgique)", "emplacement": [65.5848, 22.1567], "type": "Usine", "details": "Production d'acier"},
    {"nom": "Port de Göteborg", "emplacement": [57.7057, 11.9665], "type": "Port", "details": "Le plus grand port de Suède"},
    {"nom": "Skellefteå (Usine de traitement des métaux)", "emplacement": [64.7507, 20.9528], "type": "Usine", "details": "Traitement des terres rares"},
]

icon_map = {
    "Mine": "certificate",  
    "Usine": "industry",    
    "Port": "ship"          
}

for site in sites_industriels:
    icon_type = icon_map.get(site["type"], "info-sign")  
    
    popup_text = folium.Popup(
                    f"Bateau : {bateau}<br>Date : {ligne['Date']}<br>Heure : {ligne['Heure']}",
                    max_width=250
                )
    folium.Marker(
        location=site["emplacement"],
        popup=f"<strong>{site['nom']}</strong><br>{site['type']}<br>{site['details']}",
        icon=folium.Icon(color='blue', icon=icon_type, prefix='fa') 
    ).add_to(marker_cluster)


cities = [
    {"name": "Stockholm", "location": [59.3293, 18.0686], 
     "description": "La capitale et la plus grande ville de Suède.", "population": 975551},  
    
    {"name": "Göteborg", "location": [57.7089, 11.9746], 
     "description": "Ville portuaire importante sur la côte ouest.", "population": 570000},  
    
    {"name": "Malmö", "location": [55.6050, 13.0038], 
     "description": "Ville dynamique située au sud de la Suède.", "population": 344166}, 
    
    {"name": "Uppsala", "location": [59.8586, 17.6389], 
     "description": "Connue pour sa célèbre université, l'une des plus anciennes de Scandinavie.", "population": 233839},  
    
    {"name": "Västerås", "location": [59.6162, 16.5528], 
     "description": "Ville industrielle importante au cœur de la Suède.", "population": 128534}, 
    
    {"name": "Örebro", "location": [59.2741, 15.2066], 
     "description": "Ville historique célèbre pour son château médiéval.", "population": 124027}, 
    
    {"name": "Linköping", "location": [58.4108, 15.6214], 
     "description": "Ville universitaire et technologique.", "population": 165000}, 
    
    {"name": "Jönköping", "location": [57.7815, 14.1562], 
     "description": "Ville au bord du lac Vättern.", "population": 141081},  
    
    {"name": "Växjö", "location": [56.8777, 14.8091], 
     "description": "Centre écologique de la Suède.", "population": 93609},  
    
    {"name": "Karlstad", "location": [59.3793, 13.5036], 
     "description": "Ville ensoleillée au bord du lac Vänern.", "population": 93829}, 
    
    {"name": "Kalmar", "location": [56.6616, 16.3616], 
     "description": "Ville historique célèbre pour son château.", "population": 70285},
    
    {"name": "Sundsvall", "location": [62.3908, 17.3069], 
     "description": "Ville industrielle au bord de la mer Baltique.", "population": 98999},  
    
    {"name": "Gävle", "location": [60.6749, 17.1413], 
     "description": "Ville portuaire avec une longue histoire industrielle.", "population": 102904},  
    
    {"name": "Luleå", "location": [65.5848, 22.1567], 
     "description": "Ville côtière importante pour l'industrie minière.", "population": 77800},  
    
    {"name": "Halmstad", "location": [56.6745, 12.8572], 
     "description": "Ville côtière populaire pour ses plages.", "population": 99716},  
    
    {"name": "Karlskrona", "location": [56.1612, 15.5869], 
     "description": "Ville portuaire et base navale historique.", "population": 66275},  
    
    {"name": "Falun", "location": [60.6065, 15.6355], 
     "description": "Ville connue pour sa mine de cuivre historique.", "population": 58700},  
    
    {"name": "Östersund", "location": [63.1792, 14.6357], 
     "description": "Ville pittoresque au bord du lac Storsjön.", "population": 50000},  
    
    {"name": "Umeå", "location": [63.8258, 20.2630], 
     "description": "Centre culturel et universitaire du nord de la Suède.", "population": 130224},  
    
    {"name": "Eskilstuna", "location": [59.3666, 16.5077], 
     "description": "Centre industriel avec une riche histoire.", "population": 107478},  
    
    {"name": "Visby", "location": [57.6348, 18.2948], 
     "description": "Ville médiévale bien conservée sur l'île de Gotland.", "population": 23993}  
]

# Création la popup
for city in cities:
    popup_text = f"""
    <strong>{city['name']}</strong><br>
    {city['description']}<br>
    Population: {city['population']}
    """

# Définition des marqueurs en fonction de la population
    if city['population'] > 300000:
        radius = 10  
    elif 100000 <= city['population'] <= 300000:
        radius = 7   
    else:
        radius = 5   
        
    if city["name"] == "Stockholm":
        folium.CircleMarker(
            location=city["location"],
            popup=folium.Popup(popup_text, max_width=300),
            color="black",
            fill=True,
            fill_color="red",
            fill_opacity=1,
            weight=1
        ).add_to(carte)
    else:
        folium.CircleMarker(
            location=city["location"],
            radius=radius,
            popup=folium.Popup(popup_text, max_width=300),
            color="black",
            fill=True,
            fill_color="black",
            fill_opacity=0.7,
            weight=1
        ).add_to(carte)


from folium.plugins import MiniMap

minimap = MiniMap(toggle_display=True)
carte.add_child(minimap)

folium.LayerControl().add_to(carte)

d = "resultats"
output_dir = d  

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

output = os.path.join(d, "sweden_map.html")
carte.save(output)
