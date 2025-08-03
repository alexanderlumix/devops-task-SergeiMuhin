# init_mongo_servers.py
import pymongo
import yaml
import sys

CONFIG_FILE = 'mongo_servers.yml'

def load_config(config_file):
    with open(config_file, 'r') as f:
        return yaml.safe_load(f)

def test_connection(server):
    host = server['host']
    port = server.get('port', 27017)
    user = server['user']
    password = server['password']
    uri = f"mongodb://{user}:{password}@{host}:{port}/admin?directConnection=true"
    try:
        client = pymongo.MongoClient(uri, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        print(f"Connected to {host}:{port} as {user} successfully.")
    except Exception as e:
        print(f"Error connecting to {host}:{port} as {user}: {e}")
    finally:
        client.close()

def init_primary(server):
    host = server['host']
    port = server.get('port', 27017)
    user = server['user']
    password = server['password']
    uri = f"mongodb://{user}:{password}@{host}:{port}/admin?directConnection=true"
    try:
        client = pymongo.MongoClient(uri, serverSelectionTimeoutMS=5000)
        rs_config = {
            '_id': 'rs0',
            'members': [
                {'_id': 0, 'host': '127.0.0.1:27030'},
                {'_id': 1, 'host': '127.0.0.1:27031'},
                {'_id': 2, 'host': '127.0.0.1:27032'},
            ]
        }
        try:
            client.admin.command('replSetGetStatus')
            print(f"Replica set already initiated on {host}:{port}")
        except pymongo.errors.OperationFailure as e:
            if e.code == 94:  # NotYetInitialized
                print("Replica set not yet initiated. Initiating now...")
                client.admin.command('replSetInitiate', rs_config)
                print(f"Replica set initiated on {host}:{port}.")
            else:
                print(f"Replica set status check failed: {e}")
    except Exception as e:
        print(f"Error connecting to {host}:{port} as {user}: {e}")
        exit(1)
    finally:
        client.close()

def main():
    config = load_config(CONFIG_FILE)
    for idx, server in enumerate(config['servers']):
        test_connection(server)
    init_primary(config['servers'][0])

if __name__ == '__main__':
    main()
