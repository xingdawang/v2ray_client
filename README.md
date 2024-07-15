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
