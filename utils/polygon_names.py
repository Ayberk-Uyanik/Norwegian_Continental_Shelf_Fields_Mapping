# Add Polygon Names to the Folium Map with Markers in a Separate Layer #
def add_polygon_with_label(feature):
    # Importing Necessary Libraries #
    import folium
    from shapely.geometry import shape

    # Add Polygon Names to the Folium Map with Markers in a Separate Layer #
    fields = folium.FeatureGroup(
        name="Offshore Field Names",
        control=True,
        show=True
    )

    # Extract polygon geometry and Field Name #
    polygon = shape(feature['geometry'])
    name = feature['properties'].get('fieldName')
    
    # Calculate centroid and add a marker with the name at the centroid #
    centroid = polygon.centroid
    
    # Adding Markers to the Feature Layer #
    folium.Marker(
        location=[
            centroid.y, 
            centroid.x
        ],
        icon=folium.DivIcon(
            html=f"""
                <div style="font-size: 10pt; color: black;">
                    {name}
                </div>
            """
        ),
        draggable=True
    ).add_to(fields)