## Challenge: API for census-income data base

In this repo you can find

- `documentation/census_BD.pdf`: the entity-raletion diagram.
- `EDA_census.ipnb`: Jupyter notebook cwith EDA (Exploratory Data Analysis).
- `RDB_creation.ipynb`: Jupyter notebook for data base creation.

For using this app, please:

### 1. Install requirements
```
pip install -r requirements.txt --no-cache-dir
```

### 2. Change to app folder
```
cd census_api_challenge
```

### 3. Run de app
* Use --reload only in dev environment
```
uvicorn app:app --reload --port 5000
```

### 4. Go to localhost
http://127.0.0.1:5000/docs

### 5. Stop the server
```
ctrl + c
```