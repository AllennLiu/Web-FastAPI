#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('../app')

from os import chdir

chdir('../app')

from main import app
from re import search
from pytest import mark, skip, fixture
from fastapi.testclient import TestClient

client = TestClient(app)

@fixture(name='variable_manager', scope='class')
def variable_manager_fixture():
    class VariableManager:
        def __init__(self):
            self.timestamp_criteria = 0
            self.timestamp_compare  = 0
    return VariableManager()

class TestMongodb:

    @mark.order(1)
    def test_db_create(self, variable_manager):
        response = client.post('/api/v1/test',
                               headers={
                                   "Content-Type": "application/x-www-form-urlencoded"
                               })
        assert response.status_code == 200, response.text
        data = response.json()
        uuid_regexp = '^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-4[0-9A-Fa-f]{3}-[89ABab][0-9A-Fa-f]{3}-[0-9A-Fa-f]{12}$'
        assert search(uuid_regexp, data["uuid"]) != None
        assert "timestamp" in data
        variable_manager.timestamp_criteria = data["timestamp"]

    @mark.order(2)
    def test_db_search(self, variable_manager):
        response = client.get(f'/api/v1/test/{variable_manager.timestamp_criteria}')
        assert response.status_code == 200, response.text
        data = response.json()
        assert "timestamp" in data
        assert data["timestamp"] == variable_manager.timestamp_criteria

    @mark.order(3)
    def test_db_update(self, variable_manager):
        response = client.put(f'/api/v1/test/{variable_manager.timestamp_criteria}')
        assert response.status_code == 200, response.text
        data = response.json()
        assert "timestamp" in data
        variable_manager.timestamp_compare = variable_manager.timestamp_criteria + 1
        assert data["timestamp"] == variable_manager.timestamp_compare

    @mark.order(4)
    def test_db_delete(self, variable_manager):
        response = client.delete(f'/api/v1/test/{variable_manager.timestamp_compare}')
        assert response.status_code == 200, response.text
