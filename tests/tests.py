import pytest
from unittest.mock import patch, MagicMock
from chia_py_rpc.wallet import SharedMethods

# Test data
test_data = [
    # open_connection
    ("test1", "127.0.0.1", 8555, {"result": "success"}, None),
    ("test2", "192.168.1.1", 8555, {"result": "success"}, None),
    (
        "test3",
        "localhost",
        8555,
        {"error": "Connection failed"},
        Exception("Connection failed"),
    ),
    # close_connection
    ("test4", "node1", {"result": "success"}, None),
    ("test5", "node2", {"result": "success"}, None),
    (
        "test6",
        "node3",
        {"error": "Failed to close connection"},
        Exception("Failed to close connection"),
    ),
    # get_connections
    ("test7", {"connections": ["node1", "node2", "node3"]}, None),
    ("test8", {"connections": []}, None),
    (
        "test9",
        {"error": "Failed to get connections"},
        Exception("Failed to get connections"),
    ),
    # get_routes
    ("test10", {"routes": ["/route1", "/route2", "/route3"]}, None),
    ("test11", {"routes": []}, None),
    ("test12", {"error": "Failed to get routes"}, Exception("Failed to get routes")),
    # check_healthz
    ("test13", {"status": "healthy"}, None),
    ("test14", {"status": "unhealthy"}, None),
    ("test15", {"error": "Health check failed"}, Exception("Health check failed")),
    # stop_node
    ("test16", {"result": "success"}, None),
    ("test17", {"result": "failure"}, None),
    ("test18", {"error": "Failed to stop node"}, Exception("Failed to stop node")),
]


@pytest.mark.parametrize("test_id,*args,expected_result,side_effect", test_data)
def test_shared_methods(test_id, args, expected_result, side_effect):
    # Arrange
    with patch("chia_py_rpc.wallet.WalletRPC") as MockWalletRPC:
        instance = MockWalletRPC.return_value
        instance.submit.side_effect = side_effect
        shared_methods = SharedMethods()

    # Act
    result = getattr(shared_methods, test_id)(*args)

    # Assert
    assert result == expected_result
