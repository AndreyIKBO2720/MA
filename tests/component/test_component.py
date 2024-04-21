import requests

admin_url = 'http://localhost:8001'
get_purchases_url = f'{admin_url}/purchases'
get_purchase_by_id_url = f'{admin_url}/get_purchase_by_id'
add_purchase_url = f'{admin_url}/create_purchase'
delete_purchase_url = f'{admin_url}/delete_purchase'

new_purchase = {
    "id": 0,
    "date": "2023-04-01",
    "text": "Finalize and submit the quarterly report",
    "price": 200.00
}

def test_1_add_purchase():
    res = requests.post(f"{add_purchase_url}", json=new_purchase)
    assert res.status_code == 200

def test_2_get_purchases():
    res = requests.get(f"{get_purchases_url}").json()
    # Проверяем, что в ответе есть покупка с нужными параметрами
    assert any(p['id'] == new_purchase['id'] and
               p['text'] == new_purchase['text'] and
               p['date'] == new_purchase['date'] and
               p['price'] == new_purchase['price'] for p in res)

def test_3_get_purchase_by_id():
    res = requests.get(f"{get_purchase_by_id_url}?purchase_id=0").json()
    assert res['id'] == new_purchase['id'] and \
           res['text'] == new_purchase['text'] and \
           res['date'] == new_purchase['date'] and \
           res['price'] == new_purchase['price']

def test_4_delete_purchase():
    res = requests.delete(f"{delete_purchase_url}?purchase_id=0").json()
    assert res == {"message": "Purchase deleted successfully"}

