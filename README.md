# V2ray Web Client

V2ray Web Client with admin backend to distribute ISP and x-ui configurations.

## Table of Contents
- [Environment](#environment)
- [Installation](#installation)
- [Running](#running)

## Environment

1. Install, enable and check status of Crontab in AWS Linux

    ```bash
    sudo yum install cronie
    sudo systemctl enable crond.service
    sudo systemctl start crond.service
    sudo systemctl status crond.service
    ```
2. Install Python, pip and create soft links

    ```bash
    sudo yum install python3.11 python3.11-pip

    # setup soft link on Python and pip forcely on Python 3.11
    sudo ln -sf /usr/bin/python3.11 /usr/bin/python
    sudo ln -sf /usr/bin/pip3.11 /usr/bin/pip

    # revert back default Python 3.9
    sudo ln -sf /usr/bin/python3.9 /usr/bin/python
    sudo ln -sf /usr/bin/pip3.9 /usr/bin/pip

    # check Python verison
    python --version
    pip --version
    ```

3. Trouble shooting

    `No module named 'dnf' when running yum or dnf`
    
    replace default `#!/usr/bin/python3` shebang in `/usr/bin/dnf` Python script with a specific one `#!/usr/bin/python3.9`.

    `$ head -1 /usr/bin/dnf`
    
    #!/usr/bin/python3.9
    
    it works fine:

    `$ dnf --version`
    
    4.14.0

## Installation

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/xingdawang/v2ray_client.git
    ```

2. Navigate to the project directory:

    ```bash
    cd v2ray_client 
    ```

3. Install the project dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Apply the database migrations:

    ```bash
    python manage.py migrate
    ```

5. Create a superuser:

    ```bash
    python manage.py createsuperuser
    ```

6. Run the server backend and no hug up

    Inside the project root folder, run: 
    
    ```bash
    nohup python manage.py runserver 0.0.0.0:8000 &
    ```

    This let the website runs background, and you can see the website from the browser, in the mean time, you will notice there is a nohup.out file generated automatically.



7. Install and config Nginx

    As the website has run already, we need to bind 8000 to 80 with Nginx.

    7.1 Installation
    ```bash
    sudo yum install nginx
    ```
    
    Nginx config location: `/etc/nginx/config.d/`, any configuration end with `.conf`

    Create a configuration file for server, e.g. `/etc/nginx/config.d/dango_link2globe.com.conf`, the content inside:

    ```bash
    server {
        listen 80;
        server_name 34.214.109.145;  # replace with your server IP or public dns

        location / {
            proxy_pass http://127.0.0.1:8000;  # local address and port
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

            proxy_connect_timeout 600;
            proxy_send_timeout 600;
            proxy_read_timeout 600;
            send_timeout 600;

            client_max_body_size 20M;  # maximum upload file zie
        }

        location /static/ {
            alias /var/www/link2globe.com/static/;  # static file location
        }
    }
    ```

    Note: the above `static` folder should match the project settings.py (e.g. `v2ray_client/client/settings.py`) folder.

    Inside `v2ray_client/client/settings.py`, make sure this line match above `static` location.
    
    ```bash
    STATIC_ROOT = '/var/www/link2globe.com/static'
    ```
    7.2 Config project

    After installed nginx, go back to the project folder (e.g. `v2ray_client/client`), and push the static files to the `static` folder

    ```bash
    python manage.py collectstatic
    ```

    Be noticed that the `static` folder may need 777 permission.
    ```bash
    sudo chmod 777 -R /var/www/link2globe.com/static
    ```

    7.3 restart nginx server and check

    ```bash
    sudo systemctl restart nginx
    sudo systemctl status nginx
    ```



## Running

1. Add, remove and check Crontab

   ```bash
   python manage.py crontab add
   python manage.py crontab remove
   python manage.py crontab show
   ```

2. Import AWS pem files

   In the project root folder, create a pem folder with necessary pem file inside, and update `client/settings.py` `SERVER_CONFIG` section.
   
3. Add server ip to the `client/settings.py` `ALLOWED_HOSTS` section.

4. Create a `.env` file in the root folder, and record credentials inside.

5. Start the Django development server:

```bash
python manage.py runserver 0.0.0.0:8000
```
