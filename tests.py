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
