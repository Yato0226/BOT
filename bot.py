import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
import os  # Import os to access environment variables

intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent

# Retrieve the Discord bot token and Steam API key from environment variables
TOKEN = os.getenv('HELLO')  # Get the Discord bot token from environment variables
STEAM_API_KEY = os.getenv('Hi')  # Get the Steam API key from environment variables

if TOKEN is None:
    print("Error: DISCORD_BOT_TOKEN is not set.")
    exit(1)

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def steam_login(ctx, username, password):
    """
    Logs in to Steam (simplified for demonstration).
    This is a basic implementation and may not be secure.
    Consider using a more robust authentication method.
    """
    try:
        # Attempt to log in to Steam (replace with actual login logic)
        session = requests.Session()
        login_url = "https://steamcommunity.com/login/" 
        login_data = {
            "username": username,
            "password": password,
            "remember_login": "true"
        }
        response = session.post(login_url, data=login_data)
        
        # Check for successful login (replace with actual login verification)
        if "You have successfully logged on to Steam" in response.text:
            await ctx.send("Steam login successful!")
            ctx.author.steam_session = session 
        else:
            await ctx.send("Steam login failed.")
    except Exception as e:
        await ctx.send(f"An error occurred during login: {e}")

@bot.command()
async def add_workshop_items(ctx):
    try:
        if not hasattr(ctx.author, 'steam_session'):
            await ctx.send("Please login to Steam first using the `!steam_login` command.")
            return

        session = ctx.author.steam_session 

        # Get user's Steam profile URL (replace with actual logic)
        profile_url = f"https://steamcommunity.com/id/{ctx.author.name}/myworkshopfiles/" 
        response = session.get(profile_url)
        soup = BeautifulSoup(response.content, "html.parser")

        # Find workshop items (adjust selectors as needed)
        workshop_items = soup.find_all("a", class_="workshopItemTitle")

        for item in workshop_items:
            workshop_item_url = item['href']
            workshop_item_name = item.text.strip()

            # Create a thread in your Discord server (replace with actual thread creation logic)
            category = discord.utils.get(ctx.guild.categories, name="Steam Workshop") 
            if not category:
                category = await ctx.guild.create_category("Steam Workshop")
            channel = await ctx.guild.create_text_channel(workshop_item_name, category=category)

            # Send initial message to the thread
            await channel.send(f"**{workshop_item_name}**\n{workshop_item_url}")

            await ctx.send(f"Thread created for: {workshop_item_name}")

    except Exception as e:
        await ctx.send(f"An error occurred while adding workshop items: {e}")

# Run the bot
bot.run(TOKEN)