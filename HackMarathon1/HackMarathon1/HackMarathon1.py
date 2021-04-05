import discord
import pandas as pd

# Reading requisite files
f = open("TOKEN.txt", "r")
TOKEN = f.read()
f.close()

database = pd.read_csv('Database.csv', index_col = 0, sep=';')
print(database)
# adatok filterezésének próbálgatása
filter_hamburger = database['Hamburger'] == 1
print(database[filter_hamburger])
#print(database[filter_hamburger].Name.to_string(index=False))
for i in database[filter_hamburger]['Name']:
	print(i)

# Bot communication
choose_food_type = "Choose which kind of food you want to eat!"

class MyClient(discord.Client):
	# Going online
	async def on_ready(self):
		print("I went online.")
	async def on_message(self, message):
		if message.author == client.user:
			if message.content == choose_food_type:
				await message.add_reaction("🍕")
				await message.add_reaction("\N{hamburger}")
				await message.add_reaction("\N{sandwich}")
				await message.add_reaction("\N{green salad}")
				await message.add_reaction("\N{chicken}")
				await message.add_reaction("\N{cow}")
				await message.add_reaction("\N{pig}")
				await message.add_reaction("🍣")
			else:
				pass
		if message.content.startswith("$order"):
			print(str(message.content))
			# First step: What kind of food do you want to eat?
			await message.channel.send(choose_food_type)

	#async def on_reaction_add(self, reaction, user):
	#	if user == client.user:
	#		return
	#	print("on_reaction_add")
	#	await reaction.message.channel.send(str(user) + " chose " + str(reaction.emoji))
	#	await user.send(str(user) + " chose " + str(reaction.emoji))
	
	async def on_raw_reaction_add(self, payload):
		channel = await client.fetch_channel(payload.channel_id)
		user = await client.fetch_user(payload.user_id)
		message = await channel.fetch_message(payload.message_id)
		if user == client.user:
			return
		await message.channel.send(str(user) + " chose " + str(payload.emoji))

client = MyClient()
client.run(TOKEN)
