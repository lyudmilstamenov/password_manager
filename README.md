# password_manager

## How to run the app?
In order to use the `make` commands you need to have installed anaconda. Unless you have it, check out this [link](https://docs.anaconda.com/anaconda/install/index.html) and install it.


Enter `make set-venv` to initialize the venv.

To run the app enter `make run`.
By default the file with the credentials to the datastore is in the parent directory of the project directory.
If you want to change the path to the file, you can change it in the `anaconda-project.yml` or run `make set-path PATH=path/to/service/account/creds`.