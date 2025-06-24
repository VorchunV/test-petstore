import requests
import pytest
import json
import jsonschema
from jsonschema import validate

order1 = {
      "id": 1,
      "petId": 101,
      "quantity": 2,
      "shipDate": "2023-07-08T12:00:00Z",
      "status": "placed",
      "complete": "true"
    }
order2 = {
      "id": 2,
      "petId": 102,
      "quantity": 1,
      "shipDate": "2023-07-10T10:00:00Z",
      "status": "approved",
      "complete": "true"
    }

order3 = {
      "id": 3,
      "petId": 103,
      "quantity": 3,
      "shipDate": "2025-06-22T09:21:07.051Z",
      "status": "delivered",
      "complete": "true"
    }
order4 = {
      "id": 4,
      "petId": 104,
      "quantity": 1,
      "shipDate": "2023-07-12T14:00:00Z",
      "status": "placed",
      "complete": "false"
    }
# 1. Тесты для размещения нового заказa
# Название тест-кейса: Проверка размещения нового заказа

# Описание: Тест проверяет возможность для размещения нового заказа (POST /store/order) в PetStore


def tests_create_new_order(order):
  # Шаги выполнения:Отправляем POST-запрос на API PetStore Swagger по указанному адресу
  url = "https://petstore.swagger.io/v2/store/order"
  
  # Ожидаемый результат: Статус код 200, структура JSON-файла соответствует.
  response = requests.post(url, data=json.dumps(order), headers={'Content-Type': 'application/json'})
  assert response.status_code == 200,f"Ошибка создания заказа, статус: {response.status_code}, сообщение: {response.text}"

  response_json = response.json()
  print(response.json())

  schema =  {
  "id": "integer",
  "petId": "integer",
  "quantity"	: "integer",
  "shipDate" : 	"string",
  "status" :	"string",
  "complete" :"boolean"
   }

  try:
    validate(instance=order, schema=schema)
    print("Данные валидны")
  except jsonschema.exceptions.ValidationError as err:
    print(f"Ошибка валидации: {err.message}")

# Фактический результат: Новый заказ размещен, код статуса 200, jsonSchema соответствует.
tests_create_new_order(order4)

# Создание теста для получения заказа по ID (GET /store/order/{orderId})
#Название тест-кейса: создание тест-функции для проверки получения заказа по его id
# Описание: Тест проверяет возможность получения заказа путем отправки GET-запроса на API PetStore Swagger по указанному адресу
def tests_get_order_by_id(orderId):
# Шаги выполнения: Отправляем POST-запрос на API PetStore Swagger по указанному адресу передаем номер заказа
    response = requests.get(f'https://petstore.swagger.io/v2/store/order/{orderId}')
  
#Ожидаемый результат: HTTP-статус ответа 200,  совпадение номера полученного заказа с запрошенным номером
    assert response.status_code == 200, f"Ошибка получения заказа, статус: {response.status_code}, сообщение: {response.text}"

    receivedOrder = response.json()
    
    if receivedOrder['id'] == orderId:
        print(f"Номер заказа совпадает с запрашиваемым. Номер заказа {receivedOrder['id']}")
    else:
        print(f"Неверный ID заказа: ожидалось {orderId}, получено {receivedOrder['id']}")

# Фактический результат: HTTP-статус ответа 200, ID номера заказа совпадает.
tests_get_order_by_id(8)