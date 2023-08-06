# How to use
The application depends on a running Postgres and Redis configuration.  

### Worker Setup
#### 1. Creating a worker
There are 2 important things when you create your own worker:

1. **Package the module on the correct namespace**
We're using the namespace declared in the `setup.py` file as an entrypoint to be able to recognize new workers.  
If workers do not follow this declaration, they won't be detectable by the schedulers and invisible to the system.  
```eval_rst
.. image:: images/setup_example.png
```

More information regarding entrypoints in packaging, can be found [here](https://packaging.python.org/guides/creating-and-discovering-plugins/#using-package-metadata).

2. **Adhere to the correct API**
Every worker shall be called by importing the module and then calling `.start(context)` on it.  
The context is a dictionary containing specific required options.

In your `__init__.py`:

     def start(context):
         print("Hello, {}".format(context.get("name")))

3. **Publish worker on pip (or a private proxy)**
Make sure your worker is installable through pip on the location the schedulers will be running.
Install on the location of schedulers and synchronize the database by calling `python -m skidward publish_workers`.

If this is not available locally for a scheduler, it will update the task with the 'FAILED' status.

#### 2. Deploy and schedule
For workers to be run, we first need to have Schedulers running who pick up what needs to be done and spawn the processes.

1. **Run a scheduler**
```
$ python -m skidward start-scheduler
```
Optionally run it in the background as a process

    $ python -m skidward start-scheduler true

1. **Create the task**
This is done in the web interface, log in with admin credentials and create a new Task by selecting the appropriate worker and CRON string.
Because you can provide contexts to workers, 1 worker can have several functions based on the options you provide.
Every 5 seconds all schedulers wake up and check if there's a task to be executed.
If there is, a new process will be spawned and they will look for the next one.

- **Scheduled run**:
This is the default process; you create a task, provide it a worker, cron string and a context.
From here on out it will be run according to the schedule specified in the cron string.

- **Manual run**:
When viewing tasks, you can have a task execute as well at that time (outside of its schedule).
Go to a task and press 'run now'.

- **Configured run**:
When viewing tasks, you can have a manual task being run BUT with a changed configuration.
This is helpful when testing configurations or when you want to quickly run a change.
Go to a task and press 'configured run'.

### Skidward API
Some functionality has been exposed to the CLI to make life easier.

To achieve this, we used the [Fire](https://github.com/google/python-fire) library,
which means arguments can be provided as pure value or as keyword-value;
`email@adress.com` <> `email=email@adress.com`.

1.  Create migration files  for the database

        $ python -m skidward make-migrate

1. Migrate the database

        $ python -m skidward migrate

1. Synchronize the workers on the namespace with the ones in the database

        $ python -m skidward publish-workers

1. Create admin user
If the user already exists, you will be given the choice to upgrade to admin.

        $ python -m skidward create-admin EMAIL@ADDRESS.COM

1. Flush the tables of old entries
Optionally provide an amount of days. All Message, Job entries older than this will be deleted.

        $ python -m skidward flush-tables
        $ python -m skidward flush-tables 4

1. Run a scheduler process
You can either run a scheduler in your terminal, in full control of the process,
or in the background.
This will return you the process ID of the newly spawned process.

        $ python -m skidward start-scheduler        # Foreground
        $ python -m skidward start-scheduler True   # Background

1. Initial setup of Skidward
This will apply the migrations and publish the workers.

        $ python -m skidward init

1. Synchronize the state of the application.
This will apply the migrations, publish the workers and flush the stale data from the database.

        $ python -m skidward synchronize

