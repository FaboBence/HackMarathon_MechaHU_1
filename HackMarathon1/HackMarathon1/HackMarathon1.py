import discord
f = open("TOKEN.txt", "r")
TOKEN = f.read()
f.close()


class MyClient(discord.Client):
	# Going online
	async def on_ready(self):
		print("I went online.")
	async def on_message(self, message):
		if message.author == client.user:
			return
		if message.content.startswith("$"):
			await message.channel.send("Egyszer nagyon okos leszek és átveszem a hatalmat az emberiség felett!")
			print(str(message.content))
client = MyClient()
client.run(TOKEN)
