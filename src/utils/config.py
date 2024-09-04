import streamlit as st

import yaml

def load_yaml_config():
    with open('config.yaml') as file:
        config = yaml.load(file, Loader=yaml.SafeLoader)
    return config


def init_btn_session_state(key):
    if key not in st.session_state:
        st.session_state[key] = False


def toggle_btn_session_state(key):
    st.session_state[key] = not st.session_state[key]