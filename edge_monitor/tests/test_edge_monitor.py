# import pytest
# import asyncio
# from unittest.mock import MagicMock, patch
# from src.edge_monitor.edge_monitor import EdgeMonitor
# """Tests for `edge_monitor.edge_monitor` class."""

# def test_edge_monitor_init():
#     """
#         Test that EdgeMonitor initialization while passing explicit argument.
#     """
#     monitor = EdgeMonitor(
#         transport="http",
#         interval=5,
#         endpoint="http://example.com",
#         broker="localhost",
#         port=1883
#     )

#     assert monitor.transport == "http"
#     assert monitor.interval == 5
#     assert monitor.endpoint == "http://example.com"
#     assert monitor.broker == "localhost"
#     assert monitor.port == 1883


# @pytest.mark.asyncio
# async def test_edge_monitor_file_transfer(monkeypatch):
#     """
#         Test that EdgeMonitor calls file_transfer.send() for 'file' transport.
#     """
#     mock_file_transfer = MagicMock()
#     monkeypatch.setattr("src.edge_monitor.edge_monitor.file_transfer.send",mock_file_transfer)

#     my_edge_monitor = EdgeMonitor(transport="file", interval=0.1)
#     shutdown_event = asyncio.Event()

#     async def shut_after_delay():
#         await asyncio.sleep(0.3)
#         shutdown_event.set()
    
#     await asyncio.gather(my_edge_monitor.run(shutdown_event), shut_after_delay())

#     assert mock_file_transfer.called
#     assert mock_file_transfer.call_count >=1
