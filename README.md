# Password Manager

## Overview

**Description**:  Enables users to save their accounts credentials in a secure way by encrypting the passwords.
The project provides additional features such as organizations, generating strong passwords and account categories.

Every user can create a user account and save his personal accounts. The user can create organization and add other
users which will give them the opportunity to share the accounts of the organization.

**Technology stack**: anaconda, python3.9

**Status**:  v1, in version 1 I have created a basic system for accounts and organizations management.

## Dependencies

In order to setup the project you need to create a google account and create a project in GCP.
After that you need to generate a service account key by following
these [steps](https://cloud.google.com/iam/docs/creating-managing-service-account-keys#iam-service-account-keys-create-console).
Finally, save the key as `credentials.json` in the parent directory of the project directory.

## Installation

I have created a `Makefile` with commands for easier installation of the app. 
The commands must be run in the terminal in the root folder of the project.

In order to use the `make` commands you need to install anaconda.
Unless you have it, you can check out this [link](https://docs.anaconda.com/anaconda/install/index.html) and install it.

### Setting up the venv
To setup the venv, please run
```bash
make set-venv
```

### Running the app
To run the app, please run 
```bash
make run
```

By default the file with the credentials to the datastore is in the parent directory of the project directory and its
name is `credentials.json`.
If you want to change the path to the file, you can change it in the `anaconda-project.yml`.

## Usage

When you run the `make run`, you will be able to write some commands for managing the accounts.
Please run `help` in order to receive more updated information about the available commands.

## How to test the software

### Unit tests

- To run the unit tests, please run

```bash
make test
```

### Configuring PyCharm

You can run the unit tests by creating new Python test run configuration with target `password_manager.test` and 
set the python interpreter to be the `pmenv`. 

### Unit tests coverage

To see the coverage of the tests, please run

```bash
make test-coverage
```

### Lint

To see the lint score of the code, please run

```bash
make lint
```

## Contributors

- [Lyudmil Stamenov](https://github.com/lyudmilstamenov)