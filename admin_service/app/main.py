import os
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status, Form, Header
from typing import Annotated
from sqlalchemy.orm import Session
from keycloak import KeycloakOpenID

from database import database as database
from database.database import Purchase
from model.purchase import PurchaseModel

app = FastAPI()
database.Base.metadata.create_all(bind=database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

KEYCLOAK_URL = "http://keycloak:8080/"
KEYCLOAK_CLIENT_ID = "testClient"
KEYCLOAK_REALM = "testRealm"
KEYCLOAK_CLIENT_SECRET = "**********"

keycloak_openid = KeycloakOpenID(server_url=KEYCLOAK_URL,
                                 client_id=KEYCLOAK_CLIENT_ID,
                                 realm_name=KEYCLOAK_REALM,
                                 client_secret_key=KEYCLOAK_CLIENT_SECRET)

from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)


@app.post("/recieve_jwt_token")
async def login(username: str = Form(...), password: str = Form(...)):
    try:
        token = keycloak_openid.token(grant_type=["password"],
                                      username=username,
                                      password=password)
        return token
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Не удалось получить токен")


def chech_for_role_test(token):
    try:
        token_info = keycloak_openid.introspect(token)
        if "test" not in token_info["realm_access"]["roles"]:
            raise HTTPException(status_code=403, detail="Access denied")
        return token_info
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token or access denied")


@app.get("/health", status_code=status.HTTP_200_OK)
async def service_alive(token: str = Header()):
    if (chech_for_role_test(token)):
        return {'message': 'service alive'}
    else:
        return "Wrong JWT Token"


@app.get("/purchases")
def get_purchases(db: db_dependency, token: str = Header()):
    if (chech_for_role_test(token)):
        purchases = db.query(Purchase).all()
        return purchases
    else:
        return "Wrong JWT Token"


@app.get("/get_purchase_by_id")
def get_purchase_by_id(purchase_id: int, db: db_dependency):
    purchase = db.query(Purchase).filter(Purchase.id == purchase_id).first()
    if purchase is None:
        raise HTTPException(status_code=404, detail="Purchase not found")
    return purchase


@app.post("/create_purchase")
def create_purchase(purchase: PurchaseModel, db: db_dependency):
    db_purchase = Purchase(id=purchase.id, date=purchase.date, text=purchase.text, price=purchase.price)
    db.add(db_purchase)
    db.commit()
    db.refresh(db_purchase)
    return db_purchase


@app.delete("/delete_purchase")
def delete_purchase(purchase_id: int, db: db_dependency):
    db_purchase = db.query(Purchase).filter(Purchase.id == purchase_id).first()
    if not db_purchase:
        raise HTTPException(status_code=404, detail="Purchase not found")
    db.delete(db_purchase)
    db.commit()
    return {"message": "Purchase deleted successfully"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 80)))
