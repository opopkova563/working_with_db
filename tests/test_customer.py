from lib.db import create_customer, delete_customer, get_customer_data_by_id, update_customer_data


def test_create_customer(connection, customer_data):
    customer_id = create_customer(connection, customer_data)
    created_customer = get_customer_data_by_id(connection, customer_id)

    assert created_customer["id_customer"] == customer_id
    assert created_customer["firstname"] == customer_data["firstname"]
    assert created_customer["lastname"] == customer_data["lastname"]
    assert created_customer["email"] == customer_data["email"]


def test_update_existing_customer(connection, customer_data, faker):
    customer_id = create_customer(connection, customer_data)
    updated_data = {
        "firstname": faker.first_name(),
        "lastname": faker.last_name(),
        "email": faker.email(),
    }
    update_customer_data(connection, customer_id, updated_data)
    updated_customer = get_customer_data_by_id(connection, customer_id)

    assert updated_customer["firstname"] == updated_data["firstname"]
    assert updated_customer["lastname"] == updated_data["lastname"]
    assert updated_customer["email"] == updated_data["email"]

    delete_customer(connection, customer_id)


def test_update_not_existent_customer(connection, faker):
    not_existent_customer_id = 999999999

    updated_data = {
        "firstname": faker.first_name(),
        "lastname": faker.last_name(),
        "email": faker.email(),
    }

    is_updated = update_customer_data(connection, not_existent_customer_id, updated_data)

    assert is_updated is False


def test_delete_existing_customer(connection, customer_data):
    customer_id = create_customer(connection, customer_data)

    assert get_customer_data_by_id(connection, customer_id) is not None

    is_deleted = delete_customer(connection, customer_id)

    assert is_deleted is True
    assert get_customer_data_by_id(connection, customer_id) is None


def test_delete_not_existent_customer(connection):
    not_existent_customer_id = 999999999

    is_deleted = delete_customer(connection, not_existent_customer_id)

    assert is_deleted is False