import json
from datetime import datetime
from unittest.mock import mock_open, patch
from main import parse_files, generate_avg_report


def test_parse_files_with_date_filter():
    mock_data = '\n'.join([
        json.dumps({
            "@timestamp": "2025-06-25T10:00:00+00:00",
            "url": "/api/test1",
            "response_time": 0.2
        }),
        json.dumps({"@timestamp": "2025-06-25T11:00:00+00:00",
                    "url": "/api/test1",
                    "response_time": 0.3
                    }),
        json.dumps({
            "@timestamp": "2025-06-24T11:00:00+00:00",
            "url": "/api/test2",
            "response_time": 0.4
        }),
    ])

    filter_date = datetime.strptime("2025-06-25", "%Y-%m-%d").date()

    with patch("builtins.open", mock_open(read_data=mock_data)):
        result = parse_files(["fakefile.log"], filter_date)

    assert "/api/test1" in result
    assert "/api/test2" not in result
    assert len(result["/api/test1"]) == 2


def test_parse_files_without_date_filter():
    mock_data = '\n'.join([
        json.dumps({
            "@timestamp": "2025-06-25T10:00:00+00:00",
            "url": "/api/test1",
            "response_time": 0.2
        }),
        json.dumps({"@timestamp": "2025-06-24T11:00:00+00:00",
                    "url": "/api/test2",
                    "response_time": 0.4
                    }),
    ])

    with patch("builtins.open", mock_open(read_data=mock_data)):
        result = parse_files(["fakefile.log"])  # filter_date = None

    assert "/api/test1" in result
    assert "/api/test2" in result
    assert len(result["/api/test1"]) == 1
    assert len(result["/api/test2"]) == 1


def test_generate_average_report():
    stats = {
        "/api/test1": [{"response_time": 0.2}, {"response_time": 0.4}],
        "/api/test2": [{"response_time": 0.6}],
    }

    rows = generate_avg_report(stats)

    assert len(rows) == 2
    assert ["/api/test1", 2, 0.3] in rows
    assert ["/api/test2", 1, 0.6] in rows


def test_parse_files_with_invalid_json():
    mock_data = '\n'.join([
        json.dumps({
            "@timestamp": "2025-06-25T10:00:00+00:00",
            "url": "/api/test1",
            "response_time": 0.2
        }),
        '{"@timestamp": "бракованоевремя",'
        '"url": "/api/test1"'
        ,
        json.dumps({
            "@timestamp": "2025-06-25T11:00:00+00:00",
            "url": "/api/test1",
            "response_time": 0.4
        }),
    ])

    filter_date = datetime.strptime("2025-06-25", "%Y-%m-%d").date()

    with patch("builtins.open", mock_open(read_data=mock_data)):
        result = parse_files(["badfile.log"], filter_date)

    assert "/api/test1" in result
    assert len(result["/api/test1"]) == 2

