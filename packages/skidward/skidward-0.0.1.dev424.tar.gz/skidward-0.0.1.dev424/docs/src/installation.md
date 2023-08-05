# Installation

## Prerequisites
The project was built with Python 3.6.7 and requires a working Postgres and Redis setup.  

* Python 3.6.7
* Postgres (tested on 11 and up)
* Redis (tested on 5 and up)

#### Installing Postgres
**Note:** Look at your operating system's specific install instructions, steps may vary!

1. **On Mac OSX**

  - Install, confirm status and autostart on boot
   
        $ brew install postgres
        $ postgres -V
        $ pg_ctl -D /usr/local/var/postgres start && brew services start postgresql

2. **On Linux/Ubuntu**

  - Install Postgres, check if it is installed correctly and autostart on boot
  
        $ sudo apt-get install postgresql
        $ postgres -V
        $ sudo systemctl enable postgresql.service


#### Installing Redis
**Note:** Look at your operating system's specific install instructions, steps may vary!

1. **On Mac OSX**
  - Install and run in terminal
  
        $ brew install redis
        $ redis-server

2. **On Linux/Ubuntu**
  - Install
    
        $ sudo apt-get install redis server
        
  - Allow Redis to be controlled by `systemd`
  
     In `/etc/redis/redis.conf` change the line 
        > supervised no      - no supervision interaction
     To
        > supervised systemd - no supervision interaction
     
  - Restart service and check status
  
        $ sudo systemctl restart redis.service
        $ sudo systemctl status redis
    
## Skidward
- Install the requirements

        $ pip install -r requirements.txt

- Create user (called a 'role') in postgres and give it ownership over the new db
**Note:** It is recommended to create a user with a password, even for development purposes.

        $ createuser skidwarduser
        $ createdb skidwarddb -O skidwarduser

The application uses environment variables to offer flexible configuration options.  
Before using the application, review the configuration in the `.env` file to match your desired setup.  
A typical connectionstring looks like this:
    `SQLALCHEMY_DATABASE_URI='postgresql://USER:PASSWORD@localhost/DATABASENAME'` 

- Copy the `.env.default` file to the skidward module and rename to `.env`.  

        $ cp .env.default skidward/.env

- Publish available workers on the namespace in the database

        $ python -m skidward publish-workers

- Create an admin user for use in the application

        $ python -m skidward create-admin USER_EMAIL

### Development
- Create a new virtual environment to isolate the dependencies:  

        $ python -m venv .skidward_venv  # Create
        $ source .skidward_venv/bin/activate  # Activate
    
- Install the appropriate [requirements](installation__requirements.md)

        $ pip install -r requirements.txt
        $ pip install -r requirements-dev.txt

- Create a .env file based on the [provided defaults](configuration.md) and configure appropriately

        $ cp .env.default .env

    
- Set up the git pre-commit hook required for development

        $ pre-commit install
    
*Optional:* If you want to install demo-workers from a proxy,
navigate to the root of your virtual environment and create a `pip.conf` file.

        $ touch pip.conf
        $ echo "[global]" >> pip.conf
        $ echo "extra-index-url = URL_TO_PROXY" >> pip.conf
