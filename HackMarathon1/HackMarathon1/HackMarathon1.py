import discord
from Ranking_algorithm import *
import numpy as np

# Reading requisite files
with open("TOKEN.txt", "r") as f:
	TOKEN = f.read() # Token for bot

# Bot communication
order_text = ["✋","Who would like to order a meal? (Press like, and the Bot will contact you.)"]
ready_message = ["✅","Let others know you are done!"]
choose_food_type = "Choose which kind of food you want to eat! (You can choose multiple categories!)"
food_li = [["🍕",":pizza:","Pizza"],
		  ["\N{hamburger}",":hamburger:","Hamburger"],
		  ["\N{sandwich}",":sandwich:","Sandwich"],
		  ["\N{green salad}",":salad:","Salad"],
		  ["\N{chicken}",":chicken:","Chicken"],
		  ["\N{cow}",":cow2","Beef"],
		  ["\N{pig}",":pig2:","Pork"],
		  ["🐟",":fish:","Fish"],
		  [u"\U0001F1FA\U0001F1F8",":flag_us:","American food"],
		  [u"\U0001F1E8\U0001F1F3",":flag_cn:","Chinese food"],
		  [u"\U0001F1F2\U0001F1FD",":flag_mx","Mexican food"],
		  [u"\U0001F1EF\U0001F1F5",":flag_jp","Japanese food"]]
choose_price_range = "Which price category is the most suitable for you? (You can choose multiple categories!)"
price_li = [[u"\U0001FA99",":coin:","Cheap"],
		["💵",":dollar:","Medium priced"],
		["\N{money bag}",":moneybag:","Reasonably priced"],
		["\N{gem stone}",":gem:","Expensive"]]
choose_delivery_time = "By what time do you want to have lunch together? (If it doesn't matter, don't choose anything.)"
time_li = [["🕛",":clock12:","12:00",12],
		["🕧",":clock1230:","12:30",12.5],
		["🕐",":clock1:","13:00",13],
		["🕜",":clock130:","13:30",13.5],
		["🕑",":clock2:","14:00",14],
		["🕝",":clock230:","14:30",14.5],
		["🕒",":clock3:","15:00",15]]

time_list = np.array(time_li)
values_array = time_list[:,3].astype(np.float).tolist()

# Creating messages from Bot communication data
for t in food_li:
	choose_food_type += ("\n " + t[1] + ": "+ t[2])
for t in price_li:
	choose_price_range += ("\n " + t[1] + ": "+ t[2])
for t in time_li:
	choose_delivery_time += ("\n " + t[1] + ": "+ t[2])


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
		self.deleteable_messages = []

	# Going online
	async def on_ready(self):
		print("I went online.")

	async def on_message(self, message):
		if message.author == client.user:
			# Choices for Food type
			if message.content == choose_food_type:
				for t in food_li:
					await message.add_reaction(t[0])
			# Choices for Price range
			elif message.content == choose_price_range:
				for t in price_li:
					await message.add_reaction(t[0])
			# Choices for Delivery time
			elif message.content == choose_delivery_time:
				for t in time_li:
					await message.add_reaction(t[0])
			return

		# Command: $order
		if message.content.startswith("$order") and self.ordering == False:
			self.participants.clear()
			self.ordering = True
			self.order_msg = await message.channel.send(order_text[1])
			await self.order_msg.add_reaction(order_text[0]) # Only those get messages who react to this
		elif message.content.startswith("$order") and self.ordering == True:
			await message.channel.send("An ordering process is already running! If you want to end it and see the results type: $close")

		# Command: $close
		elif message.content.startswith("$close") and self.ordering == True:
			self.ordering = False
			if self.participants: # It runs only when at least someone participated
				self.deleteable_messages.append(await message.channel.send("The suitable restaurants will appear shortly..."))
				# We go through every message of the participants and list out their reactions
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
				# List of reactions appended together in the form of a matrix
				price_matrix = []
				food_matrix = []
				time_matrix = []
				for participant in self.participants:
					price_matrix.append(participant.price_reactions)
					food_matrix.append(participant.food_reactions)
					time_matrix.append(participant.time_reactions)
#### Running the ranking algorithm ####
			
				lunch_time_idx = voting(time_matrix, values_array)
				ranked_restaurants = ranking_algorithm(price_matrix,food_matrix)
				ranked_rest_list = "We found these restaurants for you:\n"
				for i in range(3):
					ranked_rest_list += str(i+1) + ". " + str(ranked_restaurants[i]) + "\n"
				ranked_rest_list += "Based on the votes, the best time for lunch is " + time_li[lunch_time_idx][2]
				await self.order_msg.channel.send(ranked_rest_list)
			else:
				await self.order_msg.channel.send("Nobody participated!")

			# Deleting dispensable data
			self.deleteable_messages.append(self.order_msg)
			for i in self.deleteable_messages:
				await i.delete()
				self.deleteable_messages.pop(-1)
			self.participants.clear()

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
			# Ready
			tmp = await user.send(ready_message[1])
			p.messages.append(tmp)
			await tmp.add_reaction(ready_message[0])
			# We save each participant in the list
			self.participants.append(p)
		elif message.content == ready_message[1]:
			self.deleteable_messages.append(await self.order_msg.channel.send(str(user.display_name)+" has voted!"))

client = MyClient()
client.run(TOKEN)
