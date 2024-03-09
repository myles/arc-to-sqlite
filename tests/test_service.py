from io import BytesIO

from arc_to_sqlite import service


def test_build_database(mock_db):
    service.build_database(mock_db)

    assert mock_db["arc_export_files"].exists() is True
    assert mock_db["timeline_items"].exists() is True
    assert mock_db["samples"].exists() is True
    assert mock_db["places"].exists() is True


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
