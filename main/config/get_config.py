import configparser


def get_config():
    config = configparser.ConfigParser()
    config.read('main/config/config.ini')
    config.sections()
    db_path = config['DATABASE']['path']
    return db_path
