import codecs
import json
import os.path

__CONFIG = []

def init_config():
    config_file = os.path.join(
        os.path.expanduser('~'),
        '.redispy-cli.json'
    )
    with codecs.open(config_file) as fp:
        config_data = json.load(fp)
        id = 0
        for conn in config_data['conn']:
            info = [str(id)]
            info.append(conn['name'])
            info.append(conn['host'])
            info.append(conn['port'])
            for db,desc in conn['db'].iteritems():
                detail = list(info)
                detail[0] = str(id)
                detail.append(db)
                detail.append(desc)
                __CONFIG.append(detail)
                id += 1

def get_conn(id):
    if len(__CONFIG)==0:
        init_config()
    conn = __CONFIG[id]
    return (conn[2],conn[3],int(conn[4]))

def list_conns():
    if len(__CONFIG)==0:
        init_config()
    return __CONFIG

if __name__ == '__main__':
    print get_conn(0)