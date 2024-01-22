# import pytest
# from aio_pika.abc import AbstractIncomingMessage
#
#
# @pytest.mark.asyncio
# async def test_status(rabbit_connection):
#     assert rabbit_connection.status() is True
#
# @pytest.mark.asyncio
# async def test_close(rabbit_connection):
#     await rabbit_connection._clear()
#     assert rabbit_connection.status() is False
#
# @pytest.mark.asyncio
# async def test_receive_processing_projects(rabbit_connection):
#     message = AbstractIncomingMessage()
#     message.headers = {"Name": "PROJECT", "Type": "CREATE"}
#     # assume a valid body format for `create_project` function
#     message.body = b'{"id": 1, "name": "Test Project"}'
#     await rabbit_connection.receive_processing_projects(message)