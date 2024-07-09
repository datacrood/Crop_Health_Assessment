import streamlit as st
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from PIL import Image

def extract_chips(image, chip_size, overlap):
    height, width = image.shape[:2]
    stride_y = max(1, int(chip_size[0] * (1 - overlap)))
    stride_x = max(1, int(chip_size[1] * (1 - overlap)))

    chips = []
    for r in range(0, height - chip_size[0] + stride_y, stride_y):
        for c in range(0, width - chip_size[1] + stride_x, stride_x):
            chip = image[r:r + chip_size[0], c:c + chip_size[1]]
            chips.append(chip)

    return chips

def main():
    st.title("TIFF Chips Extractor V2.0")

    uploaded_file = st.file_uploader("Upload a TIFF image", type=["tif", "tiff"])
    if uploaded_file is not None:
        image = np.array(Image.open(uploaded_file))

        # User input for chip size
        chip_width = st.number_input("Enter chip width:", min_value=10, value=100)
        chip_height = st.number_input("Enter chip height:", min_value=10, value=100)
        chip_size = (chip_height, chip_width)

        # User input for overlap percentage
        overlap = st.slider("Select overlap percentage:", min_value=0, max_value=90, value=50) / 100.0

        chips_list = extract_chips(image, chip_size, overlap)
        st.write(f"Extracted {len(chips_list)} chips.")

        num_samples = 20
        if len(chips_list) < num_samples:
            num_samples = len(chips_list)
        sample_indices = np.random.choice(len(chips_list), num_samples, replace=False)
        sample_chips = [chips_list[i] for i in sample_indices]

        st.write("Sample of Chips:")
        fig, axes = plt.subplots((num_samples + 4) // 5, 5, figsize=(10, 8))
        for i, ax in enumerate(axes.flat):
            if i < num_samples:
                ax.imshow(sample_chips[i])
                ax.axis('off')
            else:
                ax.set_visible(False)
        st.pyplot(fig)

        save_dir = 'saved_chips'
        os.makedirs(save_dir, exist_ok=True)
        num_to_save = 5
        for i in range(min(num_to_save, len(chips_list))):
            chip_name = os.path.join(save_dir, f"chip_{i}.png")
            cv2.imwrite(chip_name, cv2.cvtColor(chips_list[i], cv2.COLOR_RGB2BGR))

        st.success(f"Saved {num_to_save} chips to '{save_dir}'.")

if __name__ == "__main__":
    main()
