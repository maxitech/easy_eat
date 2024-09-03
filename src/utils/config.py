import yaml

def load_yaml_config():
    with open('config.yaml') as file:
        config = yaml.load(file, Loader=yaml.SafeLoader)
    return config