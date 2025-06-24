import requests
import random
import pytest
import json
import jsonschema
from jsonschema import validate
from selenium import webdriver
driver = webdriver.Chrome() 

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
tests_get_order_by_id(4)

#Напишите тест для удаления заказа (DELETE /store/order/{orderId})
#Название тест-кейса: Функция для тестирования удаления заказа по его номеру
# Описание: Тест проверяет возможность получения заказа путем отправки delete-запроса на API PetStore Swagger по указанному адресу
def testsDeleteOrder(orderId):

# Шаги выполнения: Проверяем что заказ есть в базе. Отправляем DELETE-запрос для удаления заказа по заданному ID

  positiveResponse = requests.get(f'https://petstore.swagger.io/v2/store/order/{orderId}') 
  response = requests.delete(f'https://petstore.swagger.io/v2/store/order/{orderId}')

#Ожидаемый результат: HTTP-статус ответа 200 OK, совпадение возвращённого номера заказа с исходным значением
  assert positiveResponse.status_code == 200,f"Заказа не существует, статус: {response.status_code}, сообщение: {response.text}"

  assert response.status_code == 200,f"Ошибка удаления заказа, статус: {response.status_code}, сообщение: {response.text}"
  
  infoId = response.json()   
  if infoId["message"] == str(orderId): 
   print("Номер заказа для удаления совпадает") 
  else:     
    print("Данные некорректны")  

testsDeleteOrder(4)
#______________________________________________________________________________________________________

# . Добавьте негативные тесты (некорректные ID, неверные форматы данных)

# Функция для негативного тестирования метода получения заказа по неверному ID
# Цель теста: проверить поведение API при попытке получить заказ с неверным/некорректным ID. 

invalidId = ["aaa", -1, 0, 99, 1.3]
def negativeTests_get_order():
  idOrder = random.choice(invalidId)
  # Выполняем GET-запрос на получение заказа с неправильным ID
  response = requests.get(f'https://petstore.swagger.io/v2/store/order/{idOrder}')
  # Убеждаемся, что сервер вернул соответствующий код ошибки (HTTP 400 Bad Request)
  assert response.status_code == 400,f"Код ошибки{response.status_code}, текст ошибки{response.text}"

negativeTests_get_order()

# Цель теста: Проверить ситуацию, когда передаваемые данные некорректны или неполны, что должно привести к ошибкам со стороны API 
# Создание недействительного заказа (отсутствует поле petId и quantity)
InvalidOrder = {
      "id": 1,
      "shipDate": "2023-07-08T12:00:00Z",
      "status": "placed",
      "complete": "true"
    }

def negative_tests_create_invalid_order():
    # Шаги выполнения: Отправляем POST-запрос на API PetStore Swagger по указанному адресу
    url = "https://petstore.swagger.io/v2/store/order"

    # Ожидаемый результат: Статус код НЕ равен 200 (обычно это 400 — bad request)
    response = requests.post(url, data=json.dumps(InvalidOrder), headers={'Content-Type': 'application/json'})
    assert response.status_code == 400, f"Ожидалась ошибка создания заказа, статус: {response.status_code}, сообщение: {response.text}"

negative_tests_create_invalid_order()
order2 = {
      "id": 2,
      "petId": 102,
      "quantity": 1,
      "shipDate": "2023-07-10T10:00:00Z",
      "status": "approved",
      "complete": "true"
    }

# Цель теста: Проверка запроса без необходимого заголовка 'Content-Type'
def negative_tests_create_without_headers(ValidOrder):
    # Шаги выполнения: Отправляем POST-запрос на API PetStore Swagger по указанному адресу
    url = "https://petstore.swagger.io/v2/store/order"

    # Ожидаемый результат: Статус код 400 — bad request или 415 - Unsupported Media Type
    response = requests.post(url, data=json.dumps(ValidOrder))  # Заголовок 'Content-Type' отсутствует!
    assert response.status_code == 400 or response.status_code == 415, \
        f"Ожидался статус 400 (Bad Request) или 415 (Unsupported Media Type), полученный статус: {response.status_code}, сообщение: {response.text}"


negative_tests_create_without_headers(order2)

# Цель теста: проверить поведение API при попытке удалить заказ с неверным/некорректным ID. 

invalidId = ["aaa", -1, 0, 99, 1.3]

def negativeTests_delete_order():
  idOrder = random.choice(invalidId)
  # Выполняем GET-запрос на получение заказа с неправильным ID
  response = requests.delete(f'https://petstore.swagger.io/v2/store/order/{idOrder}')
  # Убеждаемся, что сервер вернул соответствующий код ошибки (HTTP 400 Bad Request)
  assert response.status_code == 400,f"Код ошибки{response.status_code}, текст ошибки{response.text}"
negativeTests_delete_order()
