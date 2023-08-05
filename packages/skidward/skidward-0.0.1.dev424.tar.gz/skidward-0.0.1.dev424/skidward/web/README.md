# Skidward-Web UI

### Web Interface to manage, run and schedule Python Scripts

The User Interface is created in Flask by Integrating functionality of
**Flask-admin** and **Flask-security**.

By using Flask-admin and Flask-security together, we can provide custom
security for admin user and other users.

**Flask-admin** provides ready to use Admin Interface, easy to manage 
template functionality for login, logout, register and related pages. 

By default, there is no security/authentication for admin page, anyone
can access that. So in order to restrict the access of admin page so that 
only users with *administrative access* can manage all sorts of database tables,
creating users and permissions, we need to employ **Flask-Security** here.


### DATABASE:
**Skidward** uses `SQLAlchemy` as an ORM on top of the `Postgresql` Relational Database.
`Redis` is used as a replacement for handling message streams.

In order for this Application to run, Postgres and Redis should be running.
         
#### Setting DB connection string
The application is designed to load all the configuration parameters from environment variables.
The `.env` file you must provide, initially writes all env variables that do not exist yet on your system, nothing is overwritten.
Connection to the database is the most essential and its connection string is constructed like so:

    SQLALCHEMY_DATABASE_URI='postgresql://admin:123@localhost/skidwardDB'

  where you can replace 'admin' with '_yourusername_', 123' with '_yourpassword_'
  and 'skidwardDB' with '_yourDatabaseName_'


## RUN THE APPLICATION
1. To run the application, we need to point Flask to the location of the web application

       $ export FLASK_APP=skidward.web
      
2. Then, optionally we can set DEBUG=true, so the application gets updated real-time
      
       $ export DEBUG=true
      
     (OR change flask environment to development, serves similar purpose)
      
       $ export FLASK_ENV=development
        
3. Superuser Creation 
**Note:** Only necessary if you don't have an admin set up yet.
   
       $ python -m skidward create-admin USER_EMAIL
   
4. Run Application with following command

       $ flask run
   
5. Navigate to the application in your browser (by default on `localhost:5000`) and login with your admin credentials

