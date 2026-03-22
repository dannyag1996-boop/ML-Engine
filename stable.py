import os
import tarfile

print("🔄 Extracting archived folders from GitHub...")
for filename in os.listdir("."):
    if filename.endswith(".tar.gz"):
        print(f"Extracting {filename}...")
        with tarfile.open(filename, "r:gz") as tar:
            tar.extractall(path=".")
        print(f"✅ Successfully extracted {filename}")
import discord
from discord.ext import commands
import traceback

bot = commands.Bot(
    command_prefix=None,
    intents=discord.Intents.all(),
    help_command=None
)

async def setup_hook():
    from command_handler import CommandHandler
    await bot.add_cog(CommandHandler(bot))
    try:
        synced = await bot.tree.sync()
        print(f"✅ Slash commands synced! Total: {len(synced)}")
    except Exception as e:
        print(f"⚠️ Slash sync failed: {e}")

bot.setup_hook = setup_hook

@bot.event
async def on_ready():
    print(f"✅ Bot is fully online as {bot.user}")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ **Command doesn't exist.** Use `/help`.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ **Missing arguments for `{ctx.command}`.**")
    else:
        traceback.print_exc()
        await ctx.send("❌ Unexpected error occurred.")

bot.run("MTQ4Mjg5NjM0NDY5NDY1NzEyNA.GtTTPG.WKIVt_1jUJECWkoHlheFComhR5AWeGEIAhILt4")
