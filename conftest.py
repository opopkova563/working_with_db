import pytest
import pymysql
from faker import Faker


@pytest.fixture
def faker():
    return Faker()


@pytest.fixture
def customer_data(faker):
    return {
        "firstname": faker.first_name(),
        "lastname": faker.last_name(),
        "email": faker.email(),
    }



def pytest_addoption(parser):
    group = parser.getgroup("prestashop-db")
    parser.addoption("--host", action="store", default="localhost")
    parser.addoption("--port", action="store", type=int, default=3306)
    parser.addoption("--user", action="store", default="root")
    parser.addoption("--password", action="store", default="admin")
    parser.addoption("--database", action="store", default="prestashop")


@pytest.fixture(scope="session")
def connection(request):
    connection = pymysql.connect(
        host=request.config.getoption("--host"),
        port=request.config.getoption("--port"),
        user=request.config.getoption("--user"),
        password=request.config.getoption("--password"),
        database=request.config.getoption("--database"),
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False,
    )

    yield connection

    connection.close()
