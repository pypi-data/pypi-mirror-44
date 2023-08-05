# Configurations
To allow for maximum flexibility, most settings will be open to configure.  

We use [dotenv](https://github.com/theskumar/python-dotenv) in combination with a `.env` file, to set environment variables.
These are set when initially loading the application and don't overwrite any pre-existing variables.

Underneath is our .env.default file, with an overview of all available options.
```eval_rst
    .. include:: ../../.env.default
       :literal:
```