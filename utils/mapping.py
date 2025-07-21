# Generation of Folium Map of Norwegian Continental Shelf Oil and Gas Fields #
def generate_folium_map(lat=63.5, long=6.27, zoom_level=4):
    # Importing Necessary Libraries #
    import folium
    from folium.plugins import MiniMap
    from folium.plugins import Geocoder
    from folium.plugins import pattern
    from folium.plugins import Search
    from folium.plugins import Draw
    from folium.plugins import Fullscreen
    from branca.element import Template, MacroElement
    import json

    # Importing Maps for TileLayers of Folium #
    # Map Tiles #
    satelite_map = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'
    satelite_attribution = 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'

    nat_geo_map = 'https://server.arcgisonline.com/ArcGIS/rest/services/NatGeo_World_Map/MapServer/tile/{z}/{y}/{x}'
    nat_geo_attribution = 'Tiles &copy; Esri &mdash; National Geographic, Esri, DeLorme, NAVTEQ, UNEP-WCMC, USGS, NASA, ESA, METI, NRCAN, GEBCO, NOAA, iPC'

    dark_mode_map = 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png'
    dark_mode_attribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'

    relief_map = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Shaded_Relief/MapServer/tile/{z}/{y}/{x}'
    relief_attribution = 'Tiles &copy; Esri &mdash; Source: Esri'

    physical_map = 'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png'
    physical_attribution = 'Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)'

    map_names = [
        "Satelite Map",
        "Nat Geo Map",
        "Dark Mode Map",
        "Relief Map",
        "Physical Map"
    ]

    map_types = [
        satelite_map,
        nat_geo_map,
        dark_mode_map,
        relief_map,
        physical_map
    ]

    map_attributions = [
        satelite_attribution,
        nat_geo_attribution,
        dark_mode_attribution,
        relief_attribution,
        physical_attribution
    ]

    # Requesting All Country Borders #
    political_countries_url = (
        "http://geojson.xyz/naturalearth-3.3.0/ne_50m_admin_0_countries.geojson"
    )

    # Boundaries #
    with open(r"assets/geojson/boundaries/Shipping_Lanes.geojson") as shipping:
        shipping_lanes_json = json.load(shipping)

    with open(r"assets/geojson/boundaries/EEZ_Boundaries.json") as eez:
        eez_boundaries_json = json.load(eez)

    # NCS Fields #
    with open(r"assets/geojson/fields/myshpfile.geojson") as norway:
        norwegian_fields_json = json.load(norway)

    # Geological Features #
    with open(r"assets/geojson/geology/faults.json") as faults:
        faults_json = json.load(faults)

    with open(r"assets/geojson/geology/domer.json") as domer:
        domer_json = json.load(domer)

    # Creating a Legend for Norwegian Offshore Fields #
    # Define the legend
    template = """
    {% macro html(this, kwargs) %}

    <!doctype html>
    <html lang="en">
    <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>jQuery UI Draggable - Default functionality</title>
    <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">

    <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
    <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
    
    <script>
    $( function() {
        $( "#maplegend" ).draggable({
                        start: function (event, ui) {
                            $(this).css({
                                right: "auto",
                                top: "auto",
                                bottom: "auto"
                            });
                        }
                    });
    });
    </script>
    </head>
    <body>
    <div id='maplegend' class='maplegend' 
        style='position: absolute; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
        border-radius:6px; padding: 10px; font-size:14px; right: 20px; bottom: 40px;'>
        
        <div class='legend-title'>Legend</div>
        <div class='legend-scale'>
        <ul class='legend-labels'>
            <li><span style='background:teal;opacity:0.7;'></span>Oil</li>
            <li><span style='background:brown;opacity:0.7;'></span>Gas</li>
            <li><span style='background:repeating-linear-gradient(-45deg, brown 10%, white 15%, white 20%);opacity:0.7;'></span>Oil/Gas</li>
        </ul>
        </div>
    </div>
    </body>
    </html>

    <style type='text/css'>
    .maplegend .legend-title {
        text-align: left;
        margin-bottom: 5px;
        font-weight: bold;
        font-size: 90%;
        }
    .maplegend .legend-scale ul {
        margin: 0;
        margin-bottom: 5px;
        padding: 0;
        float: left;
        list-style: none;
        }
    .maplegend .legend-scale ul li {
        font-size: 80%;
        list-style: none;
        margin-left: 0;
        line-height: 18px;
        margin-bottom: 2px;
        }
    .maplegend ul.legend-labels li span {
        display: block;
        float: left;
        height: 16px;
        width: 30px;
        margin-right: 5px;
        margin-left: 0;
        border: 1px solid #999;
        }
    .maplegend .legend-source {
        font-size: 80%;
        color: #777;
        clear: both;
        }
    .maplegend a {
        color: #777;
        }
    </style>
    {% endmacro %}"""

    macro = MacroElement()
    macro._template = Template(template)

    # Generation of a Single Map #
    # Initiation of Map with Tiles #
    m = folium.Map(
        tiles="OpenStreetMap",
        location=(lat, long),
        zoom_start=zoom_level,
        zoom_control=False
    )

    for i in range (0, len(map_attributions), 1):
        folium.TileLayer(
            tiles=map_types[i],
            name=f"{map_names[i]}",
            attr=map_attributions[i]
        ).add_to(m)

    # Adding GeoJSON Data to the Map #
    folium.GeoJson(
        political_countries_url, 
        name="Country Borders",
        style_function=lambda feature: {
            "color": "white",
            "weight": 1
        },
        show=False
    ).add_to(m)

    # Adding Exclusive Economic Zone Boundaris Data to the Map #
    folium.GeoJson(
        eez_boundaries_json, 
        name="Exclusive Economic Zones", 
        style_function=lambda feature: {
            "fillColor": "#ffff00",
            "color": "black",
            "weight": 1,
        },
    ).add_to(m)

    # Adding Norwegian Offshore Fields as GeoJSON #
    popup = folium.GeoJsonPopup(
        fields=["fieldName", "Dctype", "OpLongName", "discYear", "curActStat"],
        aliases=["fieldName", "Dctype", "OpLongName", "discYear", "curActStat"],
        labels=True
    )

    norwegian_offshore_fields = folium.GeoJson(
        norwegian_fields_json, 
        name="Norwegian Fields", 
        style_function=lambda feature: {
            "fillColor": "teal" if feature["properties"]["Dctype"]=="OIL" else "brown",
            "fillPattern" : pattern.StripePattern(angle=-45, color="brown", space_color="black") if feature["properties"]["Dctype"]=="OIL/GAS" else None,
            "color": "black",
            "weight": 1,
            "fillOpacity": 0.9,
            "html": """
                <div style="font-size: 0.8em;">
                feature['properties']['fieldName']
                </div>
            """
        },
        popup=popup,
        popup_keep_highlighted=True
    ).add_to(m)

    folium.GeoJson(
        shipping_lanes_json, 
        name="Shipping Lanes",
        show=False
    ).add_to(m)

    # Adding Faults JSON Data to the Map #
    folium.GeoJson(
        faults_json, 
        name="Faults",
        style_function=lambda feature: {
            "color": "black",
            "weight": 1
        },
        show=False
    ).add_to(m)

    # Adding Structural Elements JSON Data to the Map #
    folium.GeoJson(
        domer_json, 
        name="Domer",
        style_function=lambda feature: {
            "color": "black",
            "weight": 1
        },
        show=False
    ).add_to(m)

    # Adding a Search Bar to the Map #
    Geocoder(
        position="topright"
    ).add_to(m)

    # Adding Mini Map to the Map #
    MiniMap(
        tile_layer="Esri.WorldPhysical",
        position="topleft", 
        width=200, 
        height=200,
        zoom_level_offset=-7
    ).add_to(m)

    # Adding Lat-Long by Clicking Class #
    m.add_child(
        folium.LatLngPopup()
    )

    # Add the legend to the map
    m.get_root().add_child(
        macro
    )

    # Adding Field Search Bar to the Map #
    Search(
        layer=norwegian_offshore_fields,
        geom_type="Polygon",
        placeholder="Search for an offshore field",
        collapsed=True,
        search_label="fieldName",
        position="topleft"
    ).add_to(m)

    # Adding Measurement and Drawing Tools to the Map #
    Draw(
        export=False
    ).add_to(m)

    # Adding Fullscreen Option to the Map #
    Fullscreen(
        position="topright",
        title="Expand me",
        title_cancel="Exit me",
        force_separate_button=True,
    ).add_to(m)

    # Adding Layers to the Map #
    folium.LayerControl().add_to(m)

    # Invoking the Map for to display #
    return m