from fabric import Connection
import logging
import paramiko
import os, time, json, base64
from .models import DbServer, ProtocalConfig
import sqlite3
import pandas as pd
from django.conf import settings

logger = logging.getLogger('users.tasks')

def delete_db_files_in_directory(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) and file_path.endswith('.db'):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                delete_db_files_in_directory(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

# download remote sqlite files
def request_remote_db():
    
    # logger.debug('*'*100)
    # logger.debug('Download remote aws sqlite db files')

    # connect to remote aws db servers
    # aws default user
    user = 'ec2-user'
    # download db file location
    local_path = os.path.join(os.path.dirname(__file__), 'static', 'db')

    # clear db folder before download
    delete_db_files_in_directory(local_path)

    # define aws pem file location, e.g. client/users/../pem/v2ray-california.pem
    pem_file_path = settings.SERVER_CONFIG['PEM_FILE_PATH']
    # logger.debug(f'pem_file_path: {pem_file_path}')

    # iterrate all servers
    servers = DbServer.objects.all()
    for server in servers:
        
        # logger.debug(f'server.server_ip: {server.server_ip}')
        server_ip_address = server.server_ip

        # define download location
        local_file_name = server_ip_address.replace('.', '_')+'.db'
        local_path = os.path.join(os.path.dirname(__file__), 'static', 'db', local_file_name)
    
        try:
            # Using Fabric to connect to the server
            conn = Connection(
                host=server_ip_address,
                user=user,
                connect_kwargs={
                    "key_filename": pem_file_path,
                },
            )
            
            # Define remote paths
            remote_path = "/etc/x-ui/x-ui.db"
            temp_path = "/tmp/x-ui.db"
       
            # Copy the file to a temporary location with sudo permissions
            conn.sudo(f"cp {remote_path} {temp_path}", hide=True, pty=True)
            # logger.debug('Done: Copy the file to a temporary location with sudo permissions')
       
            # Download the file from the temporary location to the local machine
            # logger.debug(f'temp_path: {temp_path}, local_path: {local_path}')
            conn.get(temp_path, local_path)
            # logger.debug('Done: Download the file from the temporary location to the local machine')
       
            # Clean up the temporary file on the remote server
            conn.sudo(f"rm {temp_path}", hide=True, pty=True)
            # logger.debug('Done: Clean up the temporary file on the remote server')
       
            # logger.debug(f"File downloaded successfully to {local_path}")
       
        except paramiko.ssh_exception.AuthenticationException as e:
            print(f"Authentication failed: {e}")
            # logger.debug(f"Authentication failed: {e}")
        except paramiko.ssh_exception.SSHException as e:
            print(f"SSH connection failed: {e}")
            # logger.debug(f"SSH connection failed: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
            # logger.debug(f"An error occurred: {e}")

# combine all sqlite file into one
def get_db(db_folder=os.path.join(os.path.dirname(__file__), 'static', 'db')):
    
    db_list = list()
    for file in os.listdir(db_folder):
        if '.db' in file:
            db_path = os.path.join(db_folder, file)

            # connect to sqlite db 
            connection = sqlite3.connect(db_path)
            temp_df = pd.read_sql_query("SELECT * FROM inbounds", connection)
            temp_df['server_ip'] = '.'.join(file.split('.db')[0].split('_'))
            connection.close()

            # concatenate database
            db_list.append(temp_df)
    db_inbounds = pd.concat(db_list)
    # logger.debug(f"db_inbounds.shape: {db_inbounds.shape}")
    return db_inbounds

# resemble url
def get_vmess_link(remark, server_ip, port, uuid, alter_id, network, network_type, protocal):
    # logger.debug(f'in get_vmess_link function')
    # assemble config dictionary
    config_dict = {
      "v": "2",
      "ps": str(remark),
      "add": str(server_ip),
      "port": int(port),
      "id": str(uuid),
      "aid": int(alter_id),
      "net": str(network),
      "type": str(network_type),
      "host": "",
      "path": "/",
      "tls": "none"
    }
   
    # use base64 to encode vmess import url
    raw_string = str(json.dumps(config_dict)).encode('utf-8')
    encoded_url = base64.b64encode(raw_string)
    vmess_url = protocal + '://' + str(encoded_url, encoding='utf-8')
    # logger.debug(f"vmess_url: {vmess_url}")
    return vmess_url

# save individual config items
def save_config():

    # logger.debug('in save_config function')
    # logger.debug('*'*100)

    db = get_db()

    for index, row in db.iterrows():

        # general information
        # remake / nickname
        remark = row['remark']
        port = row['port']
        up = row['up']
        down = row['down']
        total = row['total']
        enable = row['enable']
        expiry_time = row['expiry_time']
        protocal = row['protocol']
        server_ip = row['server_ip']

        # json load settings
        # settings
        settings = json.loads(row['settings'])
        uuid = settings['clients'][0]['id']
        alter_id = settings['clients'][0].get('alterId', 0)

        # stream_settings
        stream_settings = json.loads(row['stream_settings'])
        network = stream_settings['network']
        network_type = stream_settings['tcpSettings']['header']['type']

        vmess_url = get_vmess_link(remark, server_ip, port, uuid, alter_id, network, network_type, protocal)
        db.at[index, 'protocal_link'] = vmess_url
        # logger.debug(f"row: {row}")

        protocal_config, created = ProtocalConfig.objects.update_or_create(
            # search condition
            remark=remark,
            server_ip=server_ip,
            port=port,
            
            # update fields
            defaults={
                'up': up,
                'down': down,
                'total': total,
                'enable': enable,
                'expiry_time': expiry_time,
                'uuid': uuid,
                'alter_id': alter_id,
                'network': network,
                'network_type': network_type,
                'protocal': protocal,
                'config_url': vmess_url,
            }
        )
        if created:
            print(f"Added new protocal config: {remark}")
            logger.debug('*'*100)
            logger.debug(f"Added new protocal config: {remark}")
        else:
            print(f"Updated protocal config: {remark}")
            logger.debug(f"Updated protocal config: {remark}")

    # clean up discard configs
    
    # current db (remark, port) list
    current_db_remarks = ProtocalConfig.objects.values_list('remark', flat=True)
    current_db_ports = ProtocalConfig.objects.values_list('port', flat=True)
    current_db_pairs = set(zip(current_db_remarks, current_db_ports))

    # remote db remark list
    remote_db_remarks = db['remark'].to_list()
    remote_db_ports = db['port'].to_list()
    remote_db_pairs = set(zip(remote_db_remarks, remote_db_ports))

    # get discard (remark, port) list
    discard_remark_pairs = list(current_db_pairs - remote_db_pairs)
    
    # remove the config that deleted in the remote server
    if discard_remark_pairs:
        for discard_remark, discard_port in discard_remark_pairs:
            ProtocalConfig.objects.filter(remark=discard_remark, port=discard_port).delete()

    # logger.debug('-'*100)
    # logger.debug(f'current_db_pairs: {current_db_pairs}, \
    #     \remote_db_pairs: {remote_db_pairs}, \
    #     \ndiscard_remark_pairs: {discard_remark_pairs}')
    # logger.debug(f'2nd current_db_pairs: {current_db_pairs}, \n2nd remote_db_pairs: {remote_db_pairs}')


def download_and_save2db():
    request_remote_db()
    # wait 1 seconds to make sure file is ready
    time.sleep(1)
    save_config()
