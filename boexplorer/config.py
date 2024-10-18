import tomli

def load_config():
    with open("boexplorer.toml", "rb") as config_file:
        return tomli.load(config_file)

app_config = load_config()
