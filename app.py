import streamlit as st
import numpy as np
import yaml
import os
from peakanalyzer.peakanalyzer import PeakAnalyzer
import time
from PIL import Image

# Constants
DATAFOLDER = "data/"
WITH_CURRENT_DIR = os.path.join(DATAFOLDER, "with_current")
WITHOUT_CURRENT_DIR = os.path.join(DATAFOLDER, "without_current")
WINDOW_LENGTH = 20
POLY_ORDER = 3
NUM_PEAKS_IN_CLUSTER = 3

# Ensure directories exist
os.makedirs(WITH_CURRENT_DIR, exist_ok=True)
os.makedirs(WITHOUT_CURRENT_DIR, exist_ok=True)


# Function to process files and display results
def process_files(numpy_file, yaml_file, dir_type):
    # Load numpy file
    data = np.load(numpy_file)

    # Load yaml file
    with open(yaml_file, 'r') as stream:
        yaml_data = yaml.safe_load(stream)

    pa_obj = PeakAnalyzer(DATAFOLDER)

    # (This is a placeholder. Replace with actual processing logic)
    # For example, process the data and generate a plot
    # Let's assume pa_obj has a method `generate_image` to create a plot image
    image_path = os.path.join(dir_type, "output.png")
    pa_obj.generate_image(data, yaml_data, image_path)

    # Display the generated image
    st.image(image_path, caption=f"Generated Image for {dir_type}", use_column_width=True)

    # Show some numbers (Placeholder for actual numbers)
    st.write(f"Processed {numpy_file} and {yaml_file} for {dir_type}")


# Streamlit app
def main():
    st.title("Peak Analyzer App")

    st.write("Upload numpy and yaml files for 'with current' and 'without current' categories.")

    with_current_numpy = st.file_uploader("Choose a numpy file for 'with current'", type=["npy"],
                                          key="with_current_numpy")
    with_current_yaml = st.file_uploader("Choose a yaml file for 'with current'", type=["yaml", "yml"],
                                         key="with_current_yaml")

    without_current_numpy = st.file_uploader("Choose a numpy file for 'without current'", type=["npy"],
                                             key="without_current_numpy")
    without_current_yaml = st.file_uploader("Choose a yaml file for 'without current'", type=["yaml", "yml"],
                                            key="without_current_yaml")

    if st.button("Detect Peaks"):
        if with_current_numpy and with_current_yaml:
            with_current_numpy_path = os.path.join(WITH_CURRENT_DIR, with_current_numpy.name)
            with_current_yaml_path = os.path.join(WITH_CURRENT_DIR, with_current_yaml.name)

            # Save uploaded files
            with open(with_current_numpy_path, "wb") as f:
                f.write(with_current_numpy.getbuffer())
            with open(with_current_yaml_path, "wb") as f:
                f.write(with_current_yaml.getbuffer())

            # Process and display results for 'with current'
            process_files(with_current_numpy_path, with_current_yaml_path, "with_current")

        if without_current_numpy and without_current_yaml:
            without_current_numpy_path = os.path.join(WITHOUT_CURRENT_DIR, without_current_numpy.name)
            without_current_yaml_path = os.path.join(WITHOUT_CURRENT_DIR, without_current_yaml.name)

            # Save uploaded files
            with open(without_current_numpy_path, "wb") as f:
                f.write(without_current_numpy.getbuffer())
            with open(without_current_yaml_path, "wb") as f:
                f.write(without_current_yaml.getbuffer())

            # Process and display results for 'without current'
            process_files(without_current_numpy_path, without_current_yaml_path, "without_current")




if __name__ == "__main__":
    main()