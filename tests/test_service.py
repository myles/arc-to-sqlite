from io import BytesIO

from arc_to_sqlite import service


def test_build_database(mock_db):
    service.build_database(mock_db)

    assert mock_db["arc_export_files"].exists() is True
    assert mock_db["timeline_items"].exists() is True
    assert mock_db["samples"].exists() is True
    assert mock_db["places"].exists() is True


def test_update_or_insert(mock_db):
    table = mock_db.create_table(
        name="test_update_or_insert",
        columns={
            "id": int,
            "title": str,
            "body": str,
            "tags": str,
        },
        pk="id",
    )

    table = service.update_or_insert(
        table,
        title="Hello, World!",
        defaults={"body": "I'm testing the update_or_insert service function."},
        create_defaults={"tags": "mock_db, test"},
    )
    assert table.count == 1
    row = table.get(table.last_rowid)
    assert row == {
        "id": table.last_rowid,
        "title": "Hello, World!",
        "body": "I'm testing the update_or_insert service function.",
        "tags": "mock_db, test",
    }

    table = service.update_or_insert(
        table,
        title="Hello, World!",
        defaults={"body": "Testing running the function again!"},
        create_defaults={"tags": "test"},
    )
    assert table.count == 1
    row = table.get(table.last_rowid)
    assert row == {
        "id": table.last_rowid,
        "title": "Hello, World!",
        "body": "Testing running the function again!",
        "tags": "mock_db, test",
    }


def test_calculate_file_obj_checksum():
    file_obj = BytesIO(b"test")

    result = service.calculate_file_obj_checksum(file_obj)
    assert (
        result
        == "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08"
    )


def test_get_arc_export_file_row(mock_db):
    service.build_database(mock_db)
    table = mock_db["arc_export_files"]

    result = service.get_arc_export_file_row("2024-01-01.json.gz", table)
    assert result is None

    row = {
        "file_name": "2024-01-01.json.gz",
        "file_checksum": "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08",
    }
    table = table.insert(row)
    pk = table.last_rowid

    result = service.get_arc_export_file_row("2024-01-01.json.gz", table)
    assert result[0] == pk
    assert result[1]["file_name"] == "2024-01-01.json.gz"
