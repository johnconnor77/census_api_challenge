# Challenge: API for census-income data base

## Set up

In this repo you can find:

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
uvicorn app:app --reload --port 8000
```

### 4. Go to localhost
http://127.0.0.1:8000/docs

### 5. Stop the server
```
ctrl + c
```

## Usage (example)

Perform the following query in [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs):
```
{
  "age": 31,
  "class_of_worker": " Private",
  "industry_code": 43,
  "occupation_code": 7,
  "marital_status": " Never married",
  "major_industry_code": " Education",
  "major_occupation_code": " Professional specialty",
  "hispanic_origin": " Mexican (Mexicano)",
  "sex": " Female"
}
```

You should obtain the following response:

```
[
  {
    "mean_wage": 0,
    "mean_weeks_worked": 46.666666666666664,
    "min_wage": 0,
    "min_weeks_worked": 12,
    "max_wage": 0,
    "max_weeks_worked": 52,
    "person_50k_plus": 4,
    "num_person": 12
  }
]
```