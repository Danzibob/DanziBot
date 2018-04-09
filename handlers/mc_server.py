from mcstatus import MinecraftServer
import asyncio
import subprocess
import discord
import logging

server = -1

async def startServer(location="~/Plebingtons"):
	command = "tmux new-session -d -n MCServer {}/startServer.sh".format(location)
	print(command)
	completed = subprocess.run(command, shell=True, stdout=subprocess.PIPE)
	print('returncode:', completed.returncode)
	print("output:", str(completed.stdout))


async def sendCommand(msg, client):
	command = " ".join(msg.content.split(" ")[1:])
	if ping() == -1:
		return -1
	subprocess.run("tmux send-keys -t MCServer \"{}\r\"".format(command) ,shell=True)
	await client.send_message(msg.channel, "Sent command `{}`".format(command))


def ping():
	try:
		return server.ping()
	except ConnectionRefusedError:
		return -1

async def getOnlinePlayers(msg, client):
	try:
		query = server.query()
		players = query.players.names
		reply = "Currently {} players online".format(len(players))
		if len(players) > 0:
			reply += ":\n```" + "\n".join(players) + "```"
		await client.send_message(msg.channel, reply)

	except Exception as e:
		logging.error(e)
		return -1

async def getServer(ip="localhost", port=25565):
	global server
	server = MinecraftServer(ip, port)
	if ping() == -1:
		print("Failed to connect to server, checking the screen is active")
		screens = subprocess.run('tmux list-windows', shell=True, stdout=subprocess.PIPE)
		# If the server's screen is up
		if "MCServer" in str(screens.stdout):
			print("Screen is active, awaiting server start for 2 minutes")
			timeout = 120
			while timeout > 0:
				await asyncio.sleep(20)
				timeout -= 20
			if timeout <= 0:
				print("Server is failing to start. Please attempt to start manually")
				return -1
		# If the server's screen is not up
		else:
			print("No screen found. Starting server...")
			await startServer()
			print("Server started, connecting...")
			server = MinecraftServer(ip, port)
	# If we can connect to the server
	else:
		print("Found server!")
		return 1

loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(getServer())
except:
	logging.error("Minecraft server couldn't be grabbed!")