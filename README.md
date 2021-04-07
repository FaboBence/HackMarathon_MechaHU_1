# Hack Kosice Marathon 1b: Discord Bot order assistant


## Team

**MechaHU**

### Team members

- Bence Fabó, Budapest University of Technology and Economics
- Mihály Makovsky, Budapest University of Technology and Economics
- Gellért Csapodi, Budapest University of Technology and Economics

## Description

**We all know the struggle** when it comes to ordering food together: whether it's your family, your colleagues or your friends, it's always hard to agree on where to order from.

In our project, we came up with an **innovative, convenient and easily customizable** solution to make the process of ordering food faster!

To help you, we've created a **Discord bot** which collects everyone's preferences via direct messages, and with a special ranking algorithm it finds the optimal compromise and lists you the restaurants which meet your expectations the most.

You can name your food, price and meal time preferences simply by **reacting with emojis** onto the bot's questions. This way, settling on a restaurant to order from together won't take longer than a minute!

*Our solution makes the process very fast and convenient, and with some modifications you can customize and boost the bot to meet your expectations perfectly!*
## Prototype

When it comes to ordering food, someone from the group should type **$order** to a channel in your Discord server.
The bot recognizes the message and asks you on the channel who wants to order today. If you react with a ✋ on the message, the bot sends you a direct message where it asks you 3 questions:

- Choose which kind of food you want to eat! 🍕 🍔 🥪 🥗 🐔 🐄 🐖 🐟 🇺🇸 🇲🇽 🇨🇳 🇯🇵
- What price category is the most suitable for you?  🟡 💵 💎 💰
- By what time do you want to have lunch together? 🕛 🕧 🕜 🕜 🕑 🕝 🕒

You can answer the queastions simply by **reacting with the given emojis** to the questions!

If everyone finished ordering, someone has to type **$close** into the channel. 
The bot will start to gather all the reactions and evaluate them with the method described below.

The core of the project is the **Latent Factor Collaborative Filtering algorithm**, which uses **matrix multipilication** to rank the restaurants in the database. We have two matrices (one for the restaurants and one for the participants) with the same columns of attributes like cheap, expensive, american food, fish, pork, etc., where each restaurant and participant has a value of 1 or 0 assigned to these fields, depending on whether the feature is true or false. Then we **normalize** the participant matrix with the number of votes given to **prevent various problematic phenomena**, like reacting with no or with all emojis to a message, which could distort the voting results. Finally, the participant and restaurant matrices are multiplied, then the achieved points of each restaurant are summed up to create the final ranking. The algorithm can be fine tuned by adding some **coefficients or factors**.

After finishing with the evaluation, the bot is going to list the most suitable restaurants and also reveal the best time to have lunch together, based on the average of incoming votes. "All you have to do now is simply grab your phones and order your meal!"
This prototype uses a database created by us to select the restaurants, if you want to get relevant results you'll have to manually add your nearby restaurants to the database!
All emojis and questions can be customized in the *"HackMarathon1.py"* file.
## How to try

*List any URLs relevant to demonstrating your prototype, e.g. a live url where judges can preview your app. Note that judges won't be able to setup anything in their computers.*

## Presentation

*List any links to your presentation or additional materials that you want to share with the judges.*

## Challenges and accomplishments

During working on the project, we learnt many important skills which we'll be able to use in our future projects as well:

- We figured out how we can program Discord bots with Python or any other programming language, which is very useful, especially as Discord is rapidly growing in popularity
- We implemented an interesting ranking algorithm which can be used for solving other problems as well.
- We found optimal ways to work together as a team, to break down the project into smaller subtasks and to distribute these among the members of the team.

## Next steps

Of course, the project needs further steps to make it work even better!

The features we are planning to add:
- Collecting **order history** and giving **personalized options** for the users according to their preferences during the last orders.
- Communication with **Google Places API** to list near restaurants from Google's database.
- Making **customization** easier, adding bot commands to insert new emojis or add new questions to the votings.

We hope that with these additional steps, our bot's going to become your daily **order-assistant**!
