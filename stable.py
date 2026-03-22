import os
import tarfile
import discord
from discord.ext import commands
import traceback

print("🔄 Setting up persistent storage...")

data_dir = "/data"
os.makedirs(data_dir, exist_ok=True)

# === ONLY extract the first time the folders don't exist yet ===
key_folders = ["local", "cache"]
folders_already_exist = all(os.path.exists(os.path.join(data_dir, f)) for f in key_folders)

if not folders_already_exist:
    print("📦 First-time migration: Extracting .tar.gz archives into Volume...")
    for filename in os.listdir("."):
        if filename.endswith(".tar.gz"):
            print(f"Extracting {filename}...")
            with tarfile.open(filename, "r:gz") as tar:
                tar.extractall(path=data_dir, filter="data")
            print(f"✅ Successfully extracted {filename}")
else:
    print("✅ Data already exists in persistent volume. Skipping extraction.")

# === ALWAYS create symlinks on every boot (this part is required forever) ===
print("🔗 Creating symlinks to persistent storage...")
for folder in key_folders:
    src = os.path.join(data_dir, folder)
    dst = f"./{folder}"
    if os.path.exists(src):
        # Remove old symlink if it exists
        if os.path.exists(dst) and os.path.islink(dst):
            os.unlink(dst)
        try:
            os.symlink(src, dst, target_is_directory=True)
            print(f"✅ Symlink created for {folder}/")
        except Exception as e:
            print(f"Symlink for {folder} already good or skipped.")

print("✅ Persistent storage setup complete!")

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

bot.run(os.getenv("DISCORD_TOKEN"))
