from fastapi import FastAPI
from fastapi.responses import JSONResponse
from schemas import UserRequestModel
from flask import jsonify
from database import chk_conn
import summary

app = FastAPI(title='Census data Summary',
              description='',
              version='0.0.1')

@app.on_event('startup')
def startup():
    pass

@app.on_event('shutdown')
def shutdown():
    pass

@app.post('/summary', summary="Summary of Census",
          description="Filter type of employee and computes some summary statitics of their wage per hour")
async def summary_census(myquery: UserRequestModel):
    """det_ind_code = industry_code
       det_occ_code = occupation_code
       marital_stat = marital_status
       major_ind_code = major_industry_code
       major_occ_code = major_occupation_code
       hisp_origin = hispanic_origin
    """
    age = myquery.age
    class_of_worker = myquery.class_of_worker
    det_ind_code = myquery.industry_code
    det_occ_code = myquery.occupation_code
    marital_stat = myquery.marital_status
    major_ind_code = myquery.major_industry_code
    major_occ_code = myquery.major_occupation_code
    hisp_origin = myquery.hispanic_origin
    sex = myquery.sex
    result = summary.summarise(age, class_of_worker, det_ind_code, det_occ_code, marital_stat,
              major_ind_code, major_occ_code, hisp_origin, sex)
    return jsonify(result)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info")         