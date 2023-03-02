# Tickets Plus

A Discord bot that adds extensions to the [Tickets](https://github.com/TicketsBot) discord bot.
Works as a supplimentary, separate bot.
When a feature is added to the main bot it will be removed from here.

Note: This setup assumes you have the main bot added to the server and configured, Support will not be provided to those who do not assume a likewise configuraton.

## Feature 1 - Staff Notes

Private threads are free!

This creates a private thread in a channel and adds the staff roles to it.
You can now disable pings, just use /settings staffpings to toggle.
The 'open message' is adjustable via /settings openmsg. $channels is replaced with the channel mention.

## Feature 2 - Staff Response

You can now respond as the staff team using /respond.
The command is limited to users with roles added to staff.
The 'name' of the team is adjustable via /settings staffname.

## Feature 3 - Strip Buttons

Due to the main Tickets bot not facilitating permissions check withthe 'Close' and 'Close with Reason' buttons this bot will strip the buttons enabling the use of / command perms to limit access.
Toggle with /setting stripbuttons.

### Minor Feature 1 - Message Discovery

The bot will display previews of discord message links.
Requires message content intent.

### Minor Feature 2 - Community Support

Automatically adds roles to the channels created by the tracked users.

## Setup

 Here are the steps to host your copy of this bot:

1. Clone or Download the repo to your machine of choice.
2. Run `python -m venv 'virt environment name'` to create an enviroment to avoid dependency conflicts.
3. Invoke `/'venv name here'/scripts/activate` to enter into the enviroment for use.
4. Run (Assuming pip and python are already on the machine) `pip install -r requirements.txt`
5. Create the bot on [Discord Developers](https://discord.com/developers/applications).
    1. Create application however you want.
    2. Create a bot. No Privilaged intents are necessary (Unless you want features that use it). Probably disable 'Public Bot'.
    3. Input your bot token to secret.json. (Refer to example_secret.json)
    4. Use `https://discord.com/api/oauth2/authorize?client_id=<APP_ID>&permissions=397284478096&scope=bot%20applications.commands` to invite the bot. replace `<APP_ID>` with the numbers from your apps `https://discord.com/developers/applications/<APP_ID>/`.
6. Fill out config.json based on the information about your server. (Refer to example_config.json)
7. Start your bot!
    1. Probably add a background service that will restart the bot on boot. I use systemctl for my bots.
