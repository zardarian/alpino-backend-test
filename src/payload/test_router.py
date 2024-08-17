import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from main import app
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, ANY
from src.payload import models, schemas, router

client = TestClient(app)

def test_create_payload_with_cache_hit():
    payload = {
        "list_1": ["a", "b"],
        "list_2": ["1", "2"]
    }

    # Mock get_cached_payload_by_list1_list2
    with patch("src.cached_payload.queries.get_cached_payload_by_list1_list2") as mock_get_cache:
        mock_get_cache.return_value = MagicMock(result="a, 1, b, 2")

        # Mock create_payload
        with patch("src.payload.queries.create_payload") as mock_create_payload:
            # Set the return value to match queries.create_payload returns
            mock_create_payload.return_value = models.Payload(
                id = 1,
                data = str(payload),
                result = "a, 1, b, 2"
            )

            response = client.post("/payload/", json=payload)
            
            assert response.status_code == 200
            assert response.json()["result"] == "a, 1, b, 2"
            mock_get_cache.assert_called_once()
            mock_create_payload.assert_called_once()

def test_create_payload_without_cache_hit():
    payload = {
        "list_1": ["a", "b"],
        "list_2": ["1", "2"]
    }

    # Mock get_cached_payload_by_list1_list2
    with patch("src.cached_payload.queries.get_cached_payload_by_list1_list2") as mock_get_cache:
        mock_get_cache.return_value = None

        # Mock create_cached_payload
        with patch("src.cached_payload.queries.create_cached_payload") as mock_create_cached_payload:

            # Mock create_payload
            with patch("src.payload.queries.create_payload") as mock_create_payload:
                # Set the return value to match queries.create_payload returns
                mock_create_payload.return_value = models.Payload(
                    id = 2,
                    data = str(payload),
                    result = "A, 1, B, 2"
                )
            
                response = client.post("/payload/", json=payload)
                
                assert response.status_code == 200
                assert response.json()["result"] == "A, 1, B, 2"
                mock_get_cache.assert_called_once()
                mock_create_payload.assert_called_once()
                mock_create_cached_payload.assert_called_once()

def test_read_payload_found():
    payload_id = 1

    # Mock get_payload
    with patch("src.payload.queries.get_payload") as mock_get_payload:
        mock_get_payload.return_value = models.Payload(
            id=payload_id,
            data="{'list_1': ['a', 'b'], 'list_2': ['1', '2']}",
            result="a, 1, b, 2"
        )

        response = client.get(f"/payload/{payload_id}")
        
        assert response.status_code == 200
        assert response.json()["id"] == payload_id
        assert response.json()["result"] == "a, 1, b, 2"
        mock_get_payload.assert_called_once_with(db=ANY, payload_id=payload_id)

def test_read_payload_not_found():
    payload_id = 2

    # Mock get_payload
    with patch("src.payload.queries.get_payload") as mock_get_payload:
        mock_get_payload.return_value = None

        response = client.get(f"/payload/{payload_id}")

        assert response.status_code == 404
        assert response.json()["detail"] == "Payload not found"
        mock_get_payload.assert_called_once_with(db=ANY, payload_id=payload_id)
