from fastapi import APIRouter
# from models.signin import SigninRequest
import psycopg2

router = APIRouter(prefix="/auth")

@router.get("/signin")
async def signin():
    return {"message": "Hello World!"}
    # try:
    #     conn = psycopg2.connect("dbname='lan' user='master' host='localhost'")
    # except:
    #     print("I am unable to connect to the database")
    #     return 500
    # with conn.cursor() as curs:
    #     try:
    #         curs.
    #         new_signin = SigninRequest(**request.model_dump())
    #         new_signin.
    #         return new_signin
