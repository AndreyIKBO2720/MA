import os
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.orm import Session

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


@app.get("/health", status_code=status.HTTP_200_OK)
async def service_alive():
    return {'message': 'service alive'}


@app.get("/purchases")
def get_purchases(db: db_dependency):
    purchases = db.query(Purchase).all()
    return purchases


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
