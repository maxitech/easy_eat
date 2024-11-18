import streamlit as st

import os
import yaml


def load_yaml_config():
    possible_paths = [
        os.path.abspath(os.path.join(os.path.dirname(__file__), "config.yaml")),
        os.path.abspath(os.path.join(os.path.dirname(__file__), "../../config.yaml")),
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            with open(path, "r") as file:
                return yaml.load(file, Loader=yaml.SafeLoader)

    raise FileNotFoundError("Config file not found. Please check the paths.")


def init_btn_session_state(key):
    if key not in st.session_state:
        st.session_state[key] = False


def toggle_btn_session_state(key):
    st.session_state[key] = not st.session_state[key]