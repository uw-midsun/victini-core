# Mock database

This folder contains some scripts that allow you to mock a database for dev purposes. Make sure you have the following requirements before using the scripts.

- Docker (installed and running)
- Python (make sure you're in a virtual env as the scripts will be installing required modules)
- Bash or Zsh (needed to run the scripts)
- WSL (Only for Windows users, you must be _in_ your WSL machine)

Please remember to run the "stop" script when you're done working for the day as it will consume your computer's resources (RAM, CPU, etc). You will also need to manually exit Docker and WSL (if you're on Windows) when you're done.

## How the "start" script works

1. Checks that you're in a virtual env and installs/updates the required modules. Fails otherwise
2. Creates a MySQL database (using Docker) with the following credentials:
   - `MYSQL_DATABASE: midsun_dev_db_mock`
   - `PORT: 3306`
   - `MYSQL_USER: user`
   - `MYSQL_PASSWORD: password`
   - `MYSQL_ROOT_PASSWORD: root`
3. Seeds the database using the contents of `sample_data.csv`. Will attempt to do so for 3 times before failing. **If you only want to seed data, take a look at `seed_database.py` and use that as a standalone script**.
   - To change the contents of the data that is seeded, change the contents of `sample_data.csv`. Another option is to create a new `.csv` file and go into `seed_database.py` and have it load the content from your desired file
   - The script will seed the data into the `sample_data_table` database table (set as default). It will also overwrite the data in said table. To change the database table that the script seeds to, change the `DB_TABLE_NAME` variable in `seed_database.py`
   - **This step may fail if it's your first time running it (due to Docker setting everything up). Just run it again and it should work**

This script can be ran using:

```bash
sh mock-database-start.sh
```

## How the "stop" script works

1. Stops the database from running.

This script can be ran using:

```bash
sh mock-database-stop.sh
```
