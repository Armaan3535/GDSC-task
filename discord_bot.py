import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from typing import Final

import google.generativeai as genai
from google.generativeai import types





load_dotenv()
DISCORD_TOKEN:Final[str] = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)



generate_content_config = types.GenerationConfig(
        temperature=0.75,
        top_p=0.95,
        top_k=40,
        max_output_tokens=8192,
        response_mime_type="text/plain",
        
        
    )


genai.configure(api_key=os.getenv('GEMINI_API_TOKEN'))
model = genai.GenerativeModel(model_name="gemini-2.0-flash",generation_config=generate_content_config,system_instruction="You are a discord bot who is satirical,comical.Talk normally."
)



reminders = []

#bot login
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')
    check_reminders.start() 

#messaging
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    #bot mention
    if bot.user in message.mentions:
        content = message.content.replace(f'<@{bot.user.id}>', '').strip()


        max_content_length = 2000
        if len(content) > max_content_length:
            content = content[:max_content_length]
            await message.channel.send("Your message was too long and has been truncated")


        #basic greeting
        if content.lower() in ['hi', 'hello', 'hey']:
            await message.channel.send(f'Hey {message.author.mention}! 👋 I am Zen and I am here to help!')

        #api 
        else:
            try:
                response = model.generate_content(content)
                await message.channel.send(response.text)
            except Exception as e:
                print(f"Error during Gemini API CALL: {e}")
                await message.channel.send("Error Occured")

    await bot.process_commands(message)

    

#!remindme - set a reminder
@bot.command()
async def remindme(ctx, time, *, message):
    try:
        reminder_time = datetime.utcnow() + timedelta(seconds=int(time))
        reminders.append({
            'user': ctx.author,
            'channel': ctx.channel,
            'message': message,
            'time': reminder_time
        })
        await ctx.send(f"Got it! I'll remind you in {time} seconds.")
    except ValueError:
        await ctx.send("Please specify the time in seconds, like `!remindme 60 Take a break!`")

#!reminders_list - see the reminders
@bot.command()
async def reminders_list(ctx):
    user_reminders = [r for r in reminders if r['user'] == ctx.author]
    if user_reminders:
        msg = "**Your reminders:**\n"
        for idx, r in enumerate(user_reminders, start=1):
            time_left = (r['time'] - datetime.utcnow()).total_seconds()
            msg += f"{idx}. {r['message']} in {int(time_left)} seconds.\n"
        await ctx.send(msg)
    else:
        await ctx.send("You have no reminders set.")

#!cancelreminder - cancel reminder
@bot.command()
async def cancelreminder(ctx, index: int):
    user_reminders = [r for r in reminders if r['user'] == ctx.author]
    if 0 < index <= len(user_reminders):
        reminder_to_remove = user_reminders[index - 1]
        reminders.remove(reminder_to_remove)
        await ctx.send("Reminder cancelled!")
    else:
        await ctx.send("Invalid reminder number!")

#check & send reminders
@tasks.loop(seconds=5)
async def check_reminders():
    current_time = datetime.utcnow()
    to_remove = []
    for reminder in reminders:
        if reminder['time'] <= current_time:
            await reminder['channel'].send(f"⏰ Hey {reminder['user'].mention}, reminder: **{reminder['message']}**")
            to_remove.append(reminder)
    for r in to_remove:
        reminders.remove(r)

#!poll
@bot.command()
async def poll(ctx, *, question_and_options = None):

    if question_and_options is None:
        await ctx.send("Use the format: `!poll Question; Option 1; Option 2; ...`")
    parts = question_and_options.split(';')
    if len(parts) < 2:
        await ctx.send("Use the format: `!poll Question; Option 1; Option 2; ...`")
        return

    question = parts[0]
    options = parts[1:]

    if len(options) > 10:
        await ctx.send("You can only have up to 10 options.")
        return

    #create poll
    poll_message = f"📊 **{question}**\n"
    reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
    for i, option in enumerate(options):
        poll_message += f"{reactions[i]} {option}\n"

    poll_msg = await ctx.send(poll_message)

    #reactions for poll
    for i in range(len(options)):
        await poll_msg.add_reaction(reactions[i])

#member joim
@bot.event
async def on_member_join(member):
    welcome_channel = "welcome"
    channel = discord.utils.get(member.guild.text_channels,name= welcome_channel)
    
    if welcome_channel is not None:
        await channel.send(f"Welcome {member.mention} to the server!")
    else:
        print(f"Error:No channel named welcome")


bot.run(DISCORD_TOKEN)
