import uuid
from datetime import datetime
import pymysql


def db_execute(connection, sql: str, params: tuple = ()):
    with connection.cursor() as cursor:
        cursor.execute(sql, params)

        if cursor.description:
            return cursor.fetchall()

        return []


def create_customer(connection, customer_data: dict) -> int:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    customer_data.setdefault("firstname", "Test")
    customer_data.setdefault("lastname", "User")
    customer_data.setdefault("email", f"test_{uuid.uuid4().hex[:10]}@example.com")
    customer_data.setdefault("password", "password_hash")
    customer_data.setdefault("date_added", now)

    sql = """
        INSERT INTO ps_customer
            (id_shop_group, id_shop, id_gender, id_default_group,
             firstname, lastname, email, passwd, birthday, newsletter,
             newsletter_date_add, ip_registration_newsletter, optin,
             website, company, siret, ape, outstanding_allow_amount,
             show_public_prices, max_payment_days,
             id_lang, id_risk, note, active, is_guest, deleted,
             date_add, date_upd)
        VALUES
            (1, 1, 0, 3, %s, %s, %s, %s, NULL, 0, NULL, '', 0,
             '', '', '', '', 0.000000, 0, 0,
             1, 0, '', 1, 0, 0,
             %s, %s)
    """

    params = (
        customer_data["firstname"],
        customer_data["lastname"],
        customer_data["email"],
        customer_data["password"],
        customer_data["date_added"],
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            customer_id = cursor.lastrowid

        connection.commit()
        return customer_id

    except pymysql.MySQLError as exc:
        connection.rollback()
        raise RuntimeError(f"Не удалось создать клиента: {exc}") from exc


def get_customer_data_by_id(connection, customer_id: int) -> dict | None:

    sql = """
        SELECT *
        FROM ps_customer
        WHERE id_customer = %s
    """

    try:
        rows = db_execute(connection, sql, (customer_id,))
        return rows[0] if rows else None

    except pymysql.MySQLError as exc:
        raise RuntimeError(
            f"Не удалось получить клиента {customer_id}: {exc}"
        ) from exc


def get_customers(connection, limit: int = 50) -> list[dict]:

    sql = """
        SELECT *
        FROM ps_customer
        ORDER BY id_customer
        LIMIT %s
    """

    try:
        return db_execute(connection, sql, (limit,))

    except pymysql.MySQLError as exc:
        raise RuntimeError(f"Не удалось получить клиентов: {exc}") from exc


def update_customer_data(connection, customer_id: int, customer_data: dict) -> bool:
    sql = """
        UPDATE ps_customer
        SET firstname = %s,
            lastname = %s,
            email = %s,
            date_upd = NOW()
        WHERE id_customer = %s
    """

    params = (customer_data.get("firstname"), customer_data.get("lastname"), customer_data.get("email"), customer_id)

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            affected_rows = cursor.rowcount

        connection.commit()
        return affected_rows > 0

    except pymysql.MySQLError as exc:
        connection.rollback()
        raise RuntimeError(
            f"Не удалось обновить клиента {customer_id}: {exc}"
        ) from exc


def delete_customer(connection, customer_id: int) -> bool:
    sql = """
        DELETE FROM ps_customer
        WHERE id_customer = %s
    """

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, (customer_id,))
            affected_rows = cursor.rowcount

        connection.commit()
        return affected_rows > 0

    except pymysql.MySQLError as exc:
        connection.rollback()
        raise RuntimeError(
            f"Не удалось удалить клиента {customer_id}: {exc}"
        ) from exc