import toml
with open("config.toml","r") as file:
	data = toml.loads(file.read())

discord = data["discord"]