import discord
import pandas as pd

# Reading requisite files + Global variables
with open("TOKEN.txt", "r") as f:
	TOKEN = f.read() # Token for bot
database = pd.read_csv('Database.csv', index_col = 0, sep=';') # Restaurant data

# adatok filterezésének próbálgatása
#print(database)
#filter_hamburger = database['Hamburger'] == 1
#print(database[filter_hamburger])
#print(database[filter_hamburger].Name.to_string(index=False))
#for i in database[filter_hamburger]['Name']:
	#print(i)

# Bot communication
order_text = "Who would like to order a meal? (Press like, and the Bot will contact you.)"
choose_food_type = "Choose which kind of food you want to eat! \n :pizza:: Pizza\n :hamburger:: Hamburger\n :sandwich:: Sandwich\n :salad:: Salad\n :chicken:: Chicken\n :cow2:: Beef\n :pig2:: Pork\n :fish:: Fish\n :flag_us:: American food\n :flag_cn:: Chinese food\n :flag_mx:: Mexican food\n :flag_jp:: Japanese food\n(You can choose multiple categories!)"
choose_price_range = "Which price category is the most suitable for you? \n :coin:: Cheap\n :dollar:: Medium priced\n :moneybag:: Reasonably priced\n :gem:: Expensive\n(You can choose multiple categories!)"
choose_delivery_time = "By what time do you want to recieve your ordered meal? \n :clock12:: 12:00\n :clock1230:: 12:30\n :clock1:: 13:00\n :clock130:: 13:30\n :clock2:: 14:00\n :clock230:: 14:30\n :clock3:: 15:00 \n(If it doesn't matter, don't choose anything.)"


class Participant():
	def __init__(self, id):
		self.id = id
		self.messages = []
		self.food_reactions = []
		self.price_reactions = []
		self.time_reactions = []

class MyClient(discord.Client):
	def __init__(self):
		super().__init__()
		self.ordering = False # Is an ordering process already running
		self.order_msg = None
		self.participants = [] # List of participants

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
				await message.add_reaction("🐟")
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
				await message.add_reaction("🕛")
				await message.add_reaction("🕧")
				await message.add_reaction("🕐")
				await message.add_reaction("🕜")
				await message.add_reaction("🕑")
				await message.add_reaction("🕝")
				await message.add_reaction("🕒")
			return

		# Command: $order
		if message.content.startswith("$order") and self.ordering == False:
			self.ordering = True
			self.order_msg = await message.channel.send(order_text)
			await self.order_msg.add_reaction("✋")
			#channel = await client.fetch_channel(self.order_msg.channel.id)
			#order_message = await channel.fetch_message(self.order_msg.id)
			#await order_message.add_reaction("✋")
		elif message.content.startswith("$order") and self.ordering == True:
			await message.channel.send("An ordering process is already running! If you want to end it and see the results type: $close")

		# Command: $close
		elif message.content.startswith("$close") and self.ordering == True: # Here the answers should be evaluated
			self.ordering = False
			await message.channel.send("The suitable restaurants will appear shortly...")
			for participant in self.participants:
				for i,tmp in enumerate(participant.messages):
					msg = await tmp.channel.fetch_message(tmp.id)
					if i==0:
						for reaction in msg.reactions:
							participant.food_reactions.append(reaction.count - 1)
						print(participant.food_reactions)
					elif i==1:
						for reaction in msg.reactions:
							participant.price_reactions.append(reaction.count - 1)
						print(participant.price_reactions)
					elif i==2:
						for reaction in msg.reactions:
							participant.time_reactions.append(reaction.count - 1)
						print(participant.time_reactions)
					await tmp.delete()
		elif message.content.startswith("$close") and self.ordering == False:
			await message.channel.send("There isn't an ordering process to close! If you want to start one type: $order")

	async def on_raw_reaction_add(self, payload):
		user = await client.fetch_user(payload.user_id)
		channel = await client.fetch_channel(payload.channel_id)
		message = await channel.fetch_message(payload.message_id)

		if user == client.user:
			return
		if message.id == self.order_msg.id: # If people want to order
			p = Participant(user.id)
			# Food type message
			tmp = await user.send(choose_food_type)
			p.messages.append(tmp)
			# Price preference
			tmp = await user.send(choose_price_range)
			p.messages.append(tmp)
			# Delivery time
			tmp = await user.send(choose_delivery_time)
			p.messages.append(tmp)
			# We save each participant in the list
			self.participants.append(p)
		#await message.channel.send(str(user) + " chose " + str(payload.emoji))
		#message1 = await tmp.channel.fetch_message(tmp.id)

	#async def on_reaction_add(self, reaction, user):
	#	if user == client.user:
	#		return
	#	print("on_reaction_add")
	#	await reaction.message.channel.send(str(user) + " chose " + str(reaction.emoji))
	#	await user.send(str(user) + " chose " + str(reaction.emoji))

client = MyClient()
client.run(TOKEN)
