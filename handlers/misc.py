async def ping(msg, client):
	await client.send_message(msg.channel, "pong")