# Exporting Map as a PNG File #
def export_folium_map_to_png(map, filename):
    import io
    from PIL import Image

    img_data = map._to_png(5)
    img = Image.open(io.BytesIO(img_data))
    img.save(f'{filename}.png')