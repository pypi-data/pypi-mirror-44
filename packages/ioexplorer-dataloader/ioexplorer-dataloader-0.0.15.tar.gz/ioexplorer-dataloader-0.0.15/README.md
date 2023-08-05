# ioexplorer-dataloader

_This repository contains the code for a command line tool to manage and ingest datasets into a Postgres database, for later use by the IOExplorer web application._

## Pre-Requisites
This CLI has three main depencies: `docker` and `node`, and `python` (specifically Python 3).

Installation instructions for each can be found below:
- `docker`: https://docs.docker.com/install/
- `node`: https://nodejs.org/en/
- `python`: https://www.python.org/downloads/

Once `node` is installed, you will also need to globally install some packages which are used to interact with the database.
```
npm i -g sequelize sequelize-cli pg
```

With some environments, you will get a permission error when you attempt to install these packages. There is a [good article](https://docs.npmjs.com/getting-started/fixing-npm-permissions) on how to fix your environment to avoid these errors.

To do a final check to make sure all software is installed, run the following:
```
docker --version
node --version
npm --version
sequelize --version
python --version
```
Note that `python --version` should return something starting with `3`.
## Installing the CLI
 Installing the CLI:
 simply,
 ```
 pip install ioexplorer-dataloader
 iodl --help
 ```

 Make sure you have the most up to date version!
 Run the following if you have downloaded in the past:
 ```
 pip install ioexplorer-dataloader --upgrade
 ```
 ## Example Workflows
 ### 1. Basics
 _A workflow to help you get familiar with the basics of the dataloader._

##### Setting environment variables
To start, we need to set environment variables so that we can interact with a database.
For example, to set up a development database, we can create a file called `development.env` with the following contents:
```
NODE_ENV=development
IOEXPLORER_MODE=development
IOEXPLORER_DEVELOPMENT_DATABASE_NAME=ioexplorerdb
IOEXPLORER_DEVELOPMENT_DATABASE_HOST=127.0.0.1
IOEXPLORER_DEVELOPMENT_DATABASE_PORT=5432
IOEXPLORER_DEVELOPMENT_DATABASE_USERNAME=root
IOEXPLORER_DEVELOPMENT_DATABASE_PASSWORD=password

```
Then call `set -a && source development.env`.
_Note: `set -a` will cause all bash variables which are modified to be exported. This is the equivalent of calling `export <line>` for each `<line>` in `development.env`._

In order to use a production database, you would instead work with a file called `production.env` which would look slightly different
```
NODE_ENV=production
IOEXPLORER_MODE=production
IOEXPLORER_PRODUCTION_DATABASE_NAME=ioexplorerdb
IOEXPLORER_PRODUCTION_DATABASE_HOST=127.0.0.1
IOEXPLORER_PRODUCTION_DATABASE_PORT=5432
IOEXPLORER_PRODUCTION_DATABASE_USERNAME=root
IOEXPLORER_PRODUCTION_DATABASE_PASSWORD=password
IOEXPLORER_GRAPHQL_URL=http://api:4000/graphql

```
_Note: The differences here are that `DEVELOPMENT` is replaced with `PRODUCTION` for many of the environment variables. This is so you can have production and development variables loaded at the same time and easily toggle between the two contexts by setting `IOEXPLORER_MODE` and `NODE_ENV`. Also, the environment variable `IOEXPLORER_GRAPHQL_URL` is added in production, since the processes will be interconnected via a docker network in production rather than via localhost in development. Be sure to `unset IOEXPLORER_GRAPHQL_URL` in development, or else your graphql client will attempt to connet to the graphql api at the wrong url._
##### Starting a database.

Note that the database is not live yet, we only set our environment properly to connect to the database. Start the database by running
```
$ iodl database start
```

The database should now be started. The database just a docker container running the [postgres](https://hub.docker.com/_/postgres/) image, so you can see it being run with `docker ps`.

##### Opening a `psql` shell into a database.
Now lets open a `psql` shell connected to our newly created database:
```
$ iodl database shell
psql (11.0 (Debian 11.0-1.pgdg90+2))
Type "help" for help.

ioexplorerdb=# \dt
Did not find any relations.
```

The message `Did not find any relations.` lets us know that this database is completely empty and schemaless.

##### Applying migrations to our database.
The `iodl` CLI has a copy of all migrations used to produce the current production version of the IOExplorer database schema. To apply all these migrations run:
```
$ iodl database migrate
```

Now if you open another `psql` shell and list the relations, you get the expected:
```
$ iodl database shell
psql (11.0 (Debian 11.0-1.pgdg90+2))
Type "help" for help.

ioepxlorerdb=# \dt
           List of relations
 Schema |     Name      | Type  | Owner
--------+---------------+-------+-------
 public | SequelizeMeta | table | root
 public | cnas          | table | root
 public | datasets      | table | root
 public | fusions       | table | root
 public | mutations     | table | root
 public | samples       | table | root
 public | subjects      | table | root
 public | svs           | table | root
 public | timelines     | table | root
(9 rows)
```

Now our database is ready to get some data.


##### Initializing a dataset

`cd` into a dataset to upload. Ask Ryan for one if you do not have any.
**TODO**: upload example dataset.

The dataset should have the following directory structure:
```
.
├── data_clinical_patient.txt   (R)
├── data_clinical_sample.txt    (R)
├── data_CNA.txt
├── data_fusions.txt
├── data_expression.fpkm.txt
├── data_expression.rld.txt
├── data_expression.raw.txt
├── data_mutations_extended.txt
├── data_SV.txt
└── data_timeline.txt
```
Note: _Only the files denoted with an (R) are actually required_.

We now want to _initialize_ the dataset. This step will
1. Run some quick validations to make sure the data structure is correct.
2. Collect some meta-information from the user.
3. Write a `config.yaml` file which stores information about this dataset and helps with ingestion.

Run:
```
(dataloader) ryan@galliumos:~/MSK/data/Hugo$ iodl dataset init
INFO: Initializing new dataset!

...
 Some success messages will appear here, or a prompt will ask you if you would like to continue with missing data.
...

? What is the dataset name?  my-dataset
? What is a description of the dataset?  this is a test dataset...
? Enter link to paper.  http://google.com
? Who are you (person uploading data)?  Ryan
SUCCESS: Thanks! I made a file called `config.yaml` in this directory! Check it out and make sure everything looks OK!
```

##### Ingesting a dataset
With the `config.yaml` file already formed, ingesting the database is very simple.
```
$ iodl dataset ingest
```

If there are any problems during ingestion, an error will be thrown and the data that already made it into the database (before the error) will be deleted. This will let you diagnose any problems with the data ingestion and re-attempt ingestion without messing with the state of the database.

### 2. Production on AWS
There are some subtle differences in the above when running on the production AWS server:

1. Instead of `pip`, you should use `pip-3.6`.
2. The environment variables are located in `~/ioexplorer/production.env`.
3. `iodl database shell` will no longer work since the production database is running in a docker swarm. If you would like to shell into the datbase, you can find the id of the database container with
`docker container ls`.
Look for the line where the `IMAGE` is `postgres:latest` and the `NAMES` is something starting with `ioexplorer_database`. Copy the name string, which should look like `ioexplorer_database.1.<a bunch of random characters>`. Then, execute `docker container exec -it ioexplorer_database.1.<a bunch of random characters> psql -d $IOEXPLORER_PRODUCTION_DATABASE_NAME`