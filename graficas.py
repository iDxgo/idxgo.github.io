import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

#Preprocesamiento
df_global = pd.read_csv("Data/data_global_promedio.csv")

df_mexico = pd.read_csv("Data/data_mexico.csv")

df_mexico["PERIODO"] = pd.to_datetime(df_mexico["PERIODO"])
df_mexico["Año"] = df_mexico["PERIODO"].dt.year
df_mexico["Mes"] = df_mexico["PERIODO"].dt.month_name()

df_mexico = df_mexico[df_mexico["Año"] <= 2025]

df_nacional = df_mexico[df_mexico["CVE_ENT"] == 0].copy()
df_estados = df_mexico[df_mexico["CVE_ENT"] != 0].copy()

df_anual_media = df_estados.groupby(["Año", "ENTIDAD"])[["MEDIA"]].mean().reset_index()
df_anual_maxima = df_estados.groupby(["Año", "ENTIDAD"])[["MAXIMA"]].max().reset_index()
df_nacional_media = df_nacional.groupby("Año")["MEDIA"].mean().reset_index()

min_temp_media = df_anual_media["MEDIA"].min()
max_temp_media = df_anual_media["MEDIA"].max()

min_temp_maxima = df_anual_maxima["MAXIMA"].min()
max_temp_maxima = df_anual_maxima["MAXIMA"].max()

meses_orden = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

#Evolución temperatura promedio (México)
frames = []
for i in range(1, len(df_nacional_media) + 1):
    temp_df = df_nacional_media.iloc[:i].copy()
    temp_df["Frame"] = df_nacional_media.iloc[i-1]["Año"]
    frames.append(temp_df)

df_anim = pd.concat(frames)

fig = px.line(
    df_anim,
    x="Año",
    y="MEDIA",
    animation_frame="Frame",
    title="Evolución Histórica de la Temperatura Media Nacional",
    labels={"MEDIA": "Temperatura Media (°C)", "Año": "Año"},
    markers=True,
    color_discrete_sequence=["red"]
)

fig.update_traces(line_color="red", line_width=3,hovertemplate="<b>Año:</b> %{x}<br><b>Temperatura:</b> %{y:.2f}°C<extra></extra>")

y_min = df_nacional_media["MEDIA"].min() - 0.5
y_max = df_nacional_media["MEDIA"].max() + 0.5
x_min = df_nacional_media["Año"].min()
x_max = df_nacional_media["Año"].max()

fig.update_layout(
    xaxis=dict(range=[x_min, x_max], title="Año", gridcolor="lightgrey"),
    yaxis=dict(range=[y_min, y_max], title="Temperatura (°C)", gridcolor="lightgrey"),
    template="plotly_white",
    height=550
)
inicio = df_nacional_media.iloc[0]["MEDIA"]
final = df_nacional_media.iloc[-1]["MEDIA"]
diff = final - inicio

fig.add_annotation(
    xref="paper", yref="paper",
    x=0.01, y=0.95,
    text=f"Incremento total: {diff:.2f}°C",    
    showarrow=False,
    font=dict(size=12, color="red"),
    align="left"
)

#fig.show()

#Ranking temperatura Máxima (México)
fig = px.bar(
    df_anual_maxima,
    x="MAXIMA",
    y="ENTIDAD",
    animation_frame="Año",
    orientation="h",
    color="MAXIMA",
    color_continuous_scale="YlOrRd",
    range_x=[0, max_temp_maxima + 2],
    title="Ranking de Temperatura Máxima por Estado en México",
    labels={"MAXIMA": "Temperatura Máxima (°C)", "ENTIDAD": "Estado", "Año": "Año"}
)

fig.update_layout(
    xaxis=dict(
        title="Temperatura (°C)",
        fixedrange=True
    ),
    yaxis={"categoryorder": "total ascending"},
    
    coloraxis=dict(
        cmin=min_temp_maxima-2, 
        cmax=max_temp_maxima+2,
        colorbar=dict(title="Temp (°C)")
    ),
    height=750,
    template="plotly_white",
    margin={"l": 150}
)

#fig.show()


#Matriz Térmica Nacional (México)
fig = px.imshow(
    df_nacional.pivot(index="Año", columns="Mes", values="MEDIA")[meses_orden],
    labels=dict(x="Mes", y="Año", color="Temp (°C)"),
    x=meses_orden,
    color_continuous_scale="YlOrRd",
    title="Matriz Térmica Histórica de México (Nacional)"
)

fig.update_layout(height=600, template="plotly_white")

#fig.show()

#Promedio Temperatura (Mundial)
fig = px.choropleth(
    df_global,
    locations="iso_code",
    color="mean_temperature",
    hover_name="country",
    animation_frame="year",
    color_continuous_scale="RdYlBu_r",
    range_color=[df_global["mean_temperature"].min(), df_global["mean_temperature"].max()],
    title="Evolución de la Temperatura Media Global por País",
    labels={"mean_temperature": "Temp. Media (°C)", "year": "Año", "iso_code": "Código ISO"}
)

fig.update_layout(
    margin={"r":0,"t":50,"l":0,"b":0},
    coloraxis_colorbar=dict(title="Temp (°C)"),
    template="plotly_white"
)

fig.update_geos(
    showcountries=True, 
    countrycolor="LightGrey",
    showcoastlines=True,
    projection_type="natural earth"
)

#fig.show()
