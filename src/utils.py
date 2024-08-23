import yaml

def update_config(config):
    with open('../config.yaml', 'w') as file:
        yaml.dump(config, file, default_flow_style=False)