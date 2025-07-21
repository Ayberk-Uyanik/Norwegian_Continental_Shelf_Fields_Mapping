# Conversion of the zmap files into JSON #
def convert_zmap_to_json(zmap_path, output_json_path):
    from zmapio import ZMAPGrid
    
    # Sample code #
    ZMAPGrid (zmap_path).to_geojson(output_json_path)

def convert_zmap_to_csv(zmap_path, output_csv_path):
    from zmapio import ZMAPGrid
    
    ZMAPGrid (zmap_path).to_csv(output_csv_path)

def convert_zmap_to_dataframe(zmap_path):
    from zmapio import ZMAPGrid
    
    dataframe = ZMAPGrid (zmap_path).to_dataframe()

    return dataframe

def fetch_csv_dataframe(csv_path):
    import geopandas as gpd
    
    dataframe = gpd.read_file(csv_path)
    dataframe = dataframe.set_crs("EPSG:900913", inplace=True)
    # dataframe = dataframe.drop ("geometry", 1)

    return dataframe

def convert_zmap_coordinates(dataframe):
    from geopandas import GeoDataFrame
    from shapely.geometry import Point

    geometry = [Point(xy) for xy in zip(dataframe["X"].astype(float), dataframe["Y"].astype(float))]
    gdf = GeoDataFrame(dataframe, geometry=geometry, crs="EPSG:23032")
    gdf = gdf.to_crs("EPSG:4326")
    gdf["lat"] = gdf["geometry"].apply(lambda p: p.y)
    gdf["long"] = gdf["geometry"].apply(lambda p: p.x)

    return gdf

def drop_columns (dataframe):
    dataframe = dataframe.dropna(ignore_index=True)
    dataframe = dataframe.drop (["Unnamed: 0", "field_1", "field_2", "geometry"], axis=1)
    dataframe = dataframe.drop("field_3", axis=1)

    return dataframe

def arrange_columns (dataframe):
    dataframe = dataframe.dropna(ignore_index=True)
    dataframe = dataframe[["lat", "long", "Z"]]
    dataframe["Z"] = [i*-1 for i in dataframe["Z"]]

    return dataframe

def display_map (dataframe, faults_file, title):
    import plotly.graph_objects as go

    fig = go.Figure()

    fig.add_trace(go.Densitymapbox(
            lat=dataframe["lat"], 
            lon=dataframe["long"], 
            z=dataframe["Z"], 
            colorscale="Viridis", 
            radius=1, 
            opacity=0.65, 
            name="Depth (m.)", 
            customdata=dataframe["Z"], 
            hovertemplate="Depth: %{customdata}", 
            reversescale=True, 
            colorbar=dict(
                title="Depth (m.)", 
                thickness=18
            )
        )
    )


    fig.update_layout(
        title=dict(
            text=f"{title} Depth Map",
            x= 0.5
        ), 
        mapbox_style="open-street-map", 
        mapbox=dict(center=dict(lat=58.5, lon=5.27), 
                    zoom=4.2, 
                    layers=[
                        {
                            'sourcetype': 'geojson',
                            'source': faults_file,
                            'type': 'line',
                            'color': 'black'
                        }
                    ]
                ),
        legend=dict (
            x=0,
            y=1,
            traceorder="reversed",
            title_font_family="Arial",
            font=dict(
                family="Arial",
                size=14,
                color="black"
            ),
            bgcolor="LightSteelBlue",
            bordercolor="Black",
            borderwidth=1
        ),
        margin=dict(
            l=0, 
            r=0, 
            b=0, 
            t=50
        )
    )

    config = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'custom_image',
            'scale':6 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }
    
    fig.show(config=config)