# Copied from https://www.postgresqltutorial.com/postgresql-python/connect/
#!/usr/bin/python
from configparser import ConfigParser
import os


def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    if os.path.isfile(filename):
        # get section, default to postgresql
        db = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))

        return db
    else:
        print(f"{filename} not found")
        return None


def app_token(filename='database.ini', section='app_token'):
    print(f"from app token, section is {section}")
    token = config(filename, section)
    return token['token']

def datasource_info(filename='datasources.ini', section='la'):
    return config(filename, section)
