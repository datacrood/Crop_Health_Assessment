import streamlit as st
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import tempfile
from PIL import Image
import rasterio

def extract_chips(image, chip_size):
    height, width = image.shape[:2]
    rows = height // chip_size[0]
    cols = width // chip_size[1]

    chips = []
    for r in range(rows):
        for c in range(cols):
            chip = image[r*chip_size[0]:(r+1)*chip_size[0], c*chip_size[1]:(c+1)*chip_size[1]]
            chips.append(chip)

    return chips

def main():
    st.title("TIFF Chips Extractor")

    uploaded_file = st.file_uploader("Upload a TIFF image", type=["tif", "tiff"])
    if uploaded_file is not None:
        # Save the uploaded file to a temporary file
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(uploaded_file.getvalue())

        # Use rasterio to extract metadata
        with rasterio.open(tfile.name) as src:
            meta = src.meta
            bounds = src.bounds
            width = src.width
            height = src.height
            count = src.count
            crs = src.crs
            dtype = src.dtypes

        st.write("### Image Metadata")
        st.write(f"Dimensions: {width} x {height}")
        st.write(f"Number of bands: {count}")
        st.write(f"Coordinate Reference System: {crs}")
        st.write(f"Bounds: {bounds}")
        st.write(f"Data types: {dtype}")

        # Close and delete the temporary file
        tfile.close()
        os.unlink(tfile.name)

        # Convert uploaded file to array for processing
        image = np.array(Image.open(uploaded_file).convert('RGB'))
        
        chip_size = (100, 100)
        chips_list = extract_chips(image, chip_size)
        st.write(f"Extracted {len(chips_list)} chips.")

        num_samples = 20
        sample_indices = np.random.choice(len(chips_list), num_samples, replace=False)
        sample_chips = [chips_list[i] for i in sample_indices]

        st.write("### Sample of 20 Chips:")
        fig, axes = plt.subplots(4, 5, figsize=(10, 6))
        for i, ax in enumerate(axes.flat):
            ax.imshow(sample_chips[i])
            ax.axis('off')
        st.pyplot(fig)

        save_dir = 'saved_chips'
        os.makedirs(save_dir, exist_ok=True)
        num_to_save = 5
        for i in range(num_to_save):
            chip_name = os.path.join(save_dir, f"chip_{i}.png")
            cv2.imwrite(chip_name, chips_list[i])

        st.success(f"Saved {num_to_save} chips to '{save_dir}'.")

if __name__ == "__main__":
    main()
