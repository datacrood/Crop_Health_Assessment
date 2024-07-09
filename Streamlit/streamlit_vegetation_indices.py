import streamlit as st
import folium
from streamlit_folium import folium_static
import rasterio
from rasterio.plot import show

def load_geotiff(tif_path):
    data = rasterio.open(tif_path)
    return data

def display_map(geo_data):
    # Calculate the center of the map
    lon, lat = (geo_data.bounds.left + geo_data.bounds.right) / 2, (geo_data.bounds.bottom + geo_data.bounds.top) / 2
    m = folium.Map(location=[lat, lon], zoom_start=12)

    # Add TIFF
    folium.raster_layers.ImageOverlay(
        image=show(geo_data, show=False),
        bounds=[[geo_data.bounds.bottom, geo_data.bounds.left], [geo_data.bounds.top, geo_data.bounds.right]],
        mercator_project=True
    ).add_to(m)

    folium_static(m)

def main():
    st.title('GeoTIFF Overlay and Image Selection')
    tif_path = st.text_input('Enter the path to your TIFF file:', '')

    if tif_path:
        geo_data = load_geotiff(tif_path)
        display_map(geo_data)

        st.title("Select the index you want to view")
        options1 = ['Vikram Farm Block 26A']
        options2 = ['22-June-2023']
        options3 = ['75m']
        options4 = ['None','Orthomosaic', 'BNDVI', 'GNDVI', 'LCI', 'MCARI', 'NDRE', 'NDVI', 'SIPI2', 'TGI', 'VARI']
        options5 = ['None','Surface Model']

        col1, col2, col3, col4, col5 = st.columns(5) 

        with col1:
            selected_option1 = st.selectbox("Select Name", options1)

        with col2:
            selected_option2 = st.selectbox("Select Date", options2)

        with col3:
            selected_option3 = st.selectbox("Select Resolution", options3)

        with col4:
            selected_option4 = st.selectbox("Select VIs", options4)

        with col5:
            selected_option5 = st.selectbox("Select DSM", options5)

        if st.button("Apply"):
            if selected_option4 != 'None':
                image_path = f"/Users/punit/Downloads/{selected_option4}.jpg"
                st.image(image_path)

            if selected_option5 != 'None':
                image_path = f"/Users/punit/Downloads/{selected_option5}.jpg"
                st.image(image_path)

if __name__ == "__main__":
    main()
