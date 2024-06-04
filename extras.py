
from fastapi import HTTPException
from starlette import requests
def validate_ids(list_: str):
    list_ = list_.replace('[', '')
    list_ = list_.replace(']', '')
    list_ = list_.replace('{', '')
    list_ = list_.replace('}', '')
    list_ = list_.replace('\"', '')
    list_ = list_.replace('\'', '')
    list_ = list_.split(',')
    list_ = [id.strip() for id in list_]
    for id in list_:
        if not id.isdigit():
            raise HTTPException(status_code=400, detail=f"The id {id} is not valid, every ID must be a number")
        if not len(id) == 10 and id.isdigit():
            raise HTTPException(status_code=400, detail=f"The id {id} is not valid, every ID must be a 10-digit number.")
    return list_