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
				#await message.add_reaction("🥩") # cut of meat
				await message.add_reaction("\N{cut of meat}")
				await message.add_reaction("🍕")
				await message.add_reaction("\N{hamburger}")
			else:
				pass
		if message.content.startswith("$order"):
			print(str(message.content))
			# First step: What kind of food do you want to eat?
			await message.channel.send(choose_food_type)
	async def on_reaction_add(self, reaction, user):
		if user == client.user:
			return
		await reaction.message.channel.send(str(user) + " chose " + str(reaction.emoji))

client = MyClient()
client.run(TOKEN)
