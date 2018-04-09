from asyncio import iscoroutinefunction as isCoro
import logging

PREFIX = "#"

class Handler:
	def __init__(self, func, channels, perms):
		self.func = func
		self.channels = channels
		self.perms = perms
		self.isAsync = isCoro(self.func)

class Delegator:
	def __init__(self):
		self.handlers = {}

	def addNewHandler(self, command, handler, channels=[], permissions=[]):
		if command in self.handlers:
			logging.warning("Handler {} already exists!".format(command))
		self.handlers[command] = Handler(handler,channels,permissions)

	def addHandler(self, command, handler):
		if command in self.handlers:
			logging.warning("Handler {} already exists!".format(command))
		self.handlers[command] = handler

	async def handle(self, msg, dc_client):
		# Ensure the message has the prefix
		if msg.content[0] != PREFIX:
			#If not, ignore this message
			return

		# Get the command string for the message
		cmd = msg.content.split(" ")[0][1:]
		if cmd not in self.handlers:
			logging.info("Unrecognised command: " + cmd)
			# TODO: Unrecognised command message
			return

		h = self.handlers[cmd]

		# TODO: Check permissions and channels
		
		if h.isAsync:
			await h.func(msg, dc_client)
		else:
			h.func(msg, dc_client)