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
choose_food_type = "Choose which kind of food you want to eat! \n :pizza:: Pizza\n :hamburger:: Hamburger\n :sandwich:: Sandwich\n :salad:: Salad\n :chicken:: Chicken\n :cow2:: Beef\n :pig2:: Pork\n :flag_us:: American food\n :flag_cn:: Chinese food\n :flag_mx:: Mexican food\n :flag_jp:: Japanese food\n(You can choose multiple categories!)"
choose_price_range = "Which price category is the most suitable for you? \n :coin:: Cheap\n :dollar:: Medium priced\n :moneybag:: Reasonably priced\n :gem:: Expensive\n(You can choose multiple categories!)"
choose_delivery_time = "How long are you willing to wait after ordering a meal? \n :one:: <10min\n :two:: <20min\n :three:: <30min\n :four:: <40min\n :five:: <50min\n :six:: <60min \n(If it doesn't matter, don't choose anything.)"

class MyClient(discord.Client):
	# Going online
	async def on_ready(self):
		print("I went online.")

	async def on_message(self, message):
		if message.author == client.user:
			# Choices for Food type
			if message.content == choose_food_type:
				await message.add_reaction("🍕")
				await message.add_reaction("\N{hamburger}")
				await message.add_reaction("\N{sandwich}")
				await message.add_reaction("\N{green salad}")
				await message.add_reaction("\N{chicken}")
				await message.add_reaction("\N{cow}")
				await message.add_reaction("\N{pig}")
				await message.add_reaction(u"\U0001F1FA\U0001F1F8") # American flag
				await message.add_reaction(u"\U0001F1E8\U0001F1F3") # Chinese flag
				await message.add_reaction(u"\U0001F1F2\U0001F1FD") # Mexican flag
				await message.add_reaction(u"\U0001F1EF\U0001F1F5") # Japanese flag
			# Choices for Price range
			elif message.content == choose_price_range:
				await message.add_reaction(u"\U0001FA99") # coin
				await message.add_reaction("💵") # dollar banknote
				await message.add_reaction("\N{money bag}")
				await message.add_reaction("\N{gem stone}")
			# Choices for Delivery time
			elif message.content == choose_delivery_time:
				await message.add_reaction("1️⃣")
				await message.add_reaction("2️⃣")
				await message.add_reaction("3️⃣")
				await message.add_reaction("4️⃣")
				await message.add_reaction("5️⃣")
				await message.add_reaction("6️⃣")
			return

		# Command: $order
		if message.content.startswith("$order"):
			print(str(message.content))
			# Food type message
			await message.channel.send(choose_food_type)
			# Price preference
			await message.channel.send(choose_price_range)
			# Delivery time
			await message.channel.send(choose_delivery_time)
	
	async def on_raw_reaction_add(self, payload):
		user = await client.fetch_user(payload.user_id)
		channel = await client.fetch_channel(payload.channel_id)
		message = await channel.fetch_message(payload.message_id)

		if user == client.user:
			return
		await message.channel.send(str(user) + " chose " + str(payload.emoji))

	#async def on_reaction_add(self, reaction, user):
	#	if user == client.user:
	#		return
	#	print("on_reaction_add")
	#	await reaction.message.channel.send(str(user) + " chose " + str(reaction.emoji))
	#	await user.send(str(user) + " chose " + str(reaction.emoji))

client = MyClient()
client.run(TOKEN)
