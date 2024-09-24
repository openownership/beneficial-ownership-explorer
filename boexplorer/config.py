import tomllib

def load_config():
    with open("boexplorer.toml", "rb") as config_file:
        return tomllib.load(config_file)

app_config = load_config()
