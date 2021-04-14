from fastapi import FastAPI
from schemas import UserRequestModel
from fastapi.responses import JSONResponse
from databases import Database
import uvicorn
# import summary

database = Database("sqlite:///censusdb.db")

app = FastAPI(title='Census data Summary',
              description='',
              version='0.0.1')

@app.on_event("startup")
async def database_connect():
    await database.connect()


@app.on_event("shutdown")
async def database_disconnect():
    await database.disconnect() 

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
    age = str(age)
    det_ind_code = str(det_ind_code)
    det_occ_code = str(det_occ_code)
    filter_query = """
    WITH filter AS (
    WITH data AS (
        WITH data_occ AS (
            WITH data_class AS(
                WITH person_total AS (
                    WITH person_edu AS (
                        WITH person_sex AS (
                            WITH person_race AS (
                                WITH person_hisp AS (
                                    SELECT p1.id_person, p1.age, p1.year, p1.marital_stat, p1.race, 
                                    p1.education, p1.sex, hsp.hisp_origin FROM person_tbl as p1
                                    INNER JOIN hisp_origin_tbl as hsp ON hsp.id = p1.hisp_origin
                                )
                                SELECT r.race, p2.id_person, p2.age, p2.year, p2.marital_stat,
                                        p2.education, p2.hisp_origin, p2.sex FROM race_tbl as r 
                                INNER JOIN person_hisp as p2 ON p2.race = r.id
                                )
                            SELECT p3.id_person, p3.race, p3.age, p3.year, p3.education, p3.hisp_origin,
                                    p3.sex, ms.marital_stat FROM person_race AS p3
                            INNER JOIN  martial_status_tbl as ms ON ms.id = p3.marital_stat
                            )
                        SELECT p4.id_person, p4.race, p4.age, p4.year, p4.marital_stat, p4.education, 
                                p4.hisp_origin, sex_tbl.sex FROM person_sex AS p4
                        INNER JOIN sex_tbl ON sex_tbl.id = p4.sex
                    )
                    SELECT p5.id_person, p5.race, p5.age, p5.year, p5.marital_stat, edu.education,
                            p5.hisp_origin, p5.sex FROM person_edu as p5
                    INNER JOIN education_tbl as edu ON edu.id = p5.education
                )
                SELECT p.id_person, p.race, p.age, p.year, p.marital_stat, p.education, p.hisp_origin, 
                        p.sex, e.det_occ_code, e.wage_per_hour, e.union_member, e.unemp_reason,
                        e.own_or_self, e.weeks_worked, e.income_50k, e.class_worker FROM person_total AS p
                INNER JOIN employee_tbl as e ON e.id_person=p.id_person
            )
            SELECT dcl.id_person, dcl.race, dcl.age, dcl.year, dcl.marital_stat, dcl.education, dcl.hisp_origin,
                   dcl.sex, dcl.wage_per_hour, dcl.union_member, dcl.unemp_reason, dcl.own_or_self,
                   dcl.weeks_worked, dcl.income_50k, dcl.det_occ_code, cw.class_worker FROM data_class as dcl
            INNER JOIN class_worker_tbl as cw ON cw.id = dcl.class_worker
        )
        SELECT docc.id_person, docc.race, docc.age, docc.year, docc.marital_stat, docc.education, docc.hisp_origin,
               docc.sex, docc.wage_per_hour, docc.union_member, docc.unemp_reason, docc.own_or_self,
               docc.weeks_worked, docc.income_50k, mo.major_occ_code, mo.det_ind_code, docc.class_worker,
               docc.det_occ_code FROM data_occ as docc
        INNER JOIN det_occ_code_tbl as mo ON mo.det_occ_code = docc.det_occ_code
    )
    SELECT data.id_person, data.race, data.age, data.year, data.marital_stat, data.education, data.hisp_origin,
       data.sex, data.wage_per_hour, data.union_member, data.unemp_reason, data.own_or_self, data.class_worker,
       data.weeks_worked, data.income_50k, data.major_occ_code, mi.major_ind_code, 
       data.det_ind_code, data.det_occ_code FROM data
    INNER JOIN det_ind_code_tbl as mi ON mi.det_ind_code = data.det_ind_code
    WHERE age = '{}'""".format(age)
    filter_query = filter_query + " AND class_worker = '{}'".format(class_of_worker)
    filter_query = filter_query + " AND data.det_ind_code = '{}'".format(det_ind_code)
    filter_query = filter_query + " AND data.det_occ_code = '{}'".format(det_occ_code)
    final_block = """)
       SELECT avg(wage_per_hour) as mean_wage, avg(weeks_worked) as mean_weeks_worked,
              min(wage_per_hour) as min_wage, min(weeks_worked) as min_weeks_worked,
              max(wage_per_hour) as max_wage, max(weeks_worked) as max_weeks_worked,
              sum(income_50k) as person_50k_plus, count(id_person) as num_person
              FROM filter;"""                            

    if None in [marital_stat, major_ind_code, major_occ_code, hisp_origin, sex]:
           if marital_stat is not None:
                  filter_query = filter_query + " AND marital_stat = '{}'".format(marital_stat)
           if major_ind_code is not None:
                  filter_query = filter_query + " AND major_ind_code = '{}'".format(major_ind_code)
           if major_occ_code is not None:
                  filter_query = filter_query + " AND major_occ_code = '{}'".format(major_occ_code)
           if hisp_origin is not None:
                  filter_query = filter_query + " AND hisp_origin = '{}'".format(hisp_origin)
           if sex is not None:
                  filter_query = filter_query + " AND sex = '{}'".format(sex)                                         
    
    filter_query = filter_query + final_block
    results = await database.fetch_all(query=filter_query)

    return results

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info")         