import discord
from discord.ext import commands
from discord import Permissions

# --- НАСТРОЙКИ ---
TOKEN = 'YOUR_BOT_TOKEN'  # ⚠️ Вставьте токен вашего бота
INTENTS = discord.Intents.default()
INTENTS.message_content = True

bot = commands.Bot(command_prefix='!', intents=INTENTS)

# --- ЦВЕТА РОЛЕЙ (HEX) ---
ROLE_COLORS = {
    "Leader": 0xFF6B35,        # SHD Orange
    "Officer": 0xFFD700,       # Gold
    "Veteran": 0xC0C0C0,       # Silver
    "Raid-Leader": 0xE74C3C,   # Red
    "PC": 0x3498DB,            # Blue
    "PlayStation": 0x0070D1,   # PS Blue
    "Xbox": 0x107C10,          # Xbox Green
    "PvE-Hardcore": 0x8E44AD,  # Purple
    "PvE-Casual": 0x27AE60,    # Green
    "BattlePass-Grind": 0xF1C40F, # Yellow
    "Ping-Events": 0xE91E63,   # Pink
    "Ping-LFG": 0x1ABC9C,      # Teal
    "New-Agent": 0x7F8C8D,     # Grey
    "Muted": 0x2C3E50          # Dark
}

# --- СТРУКТУРА КАНАЛОВ ---
CATEGORIES = {
    "🏠 WELCOME & INFO": [
        ("👋・welcome", "text"),
        ("📜・rules", "text"),
        ("📢・announcements", "text"),
        ("🎁・roles", "text"),
        ("🔗・useful-links", "text")
    ],
    "💬 GENERAL CHAT": [
        ("💬・general", "text"),
        ("🎮・gaming-chat", "text"),
        ("📸・screenshots", "text"),
        ("🤖・bot-commands", "text"),
        ("💡・suggestions", "text")
    ],
    "🎯 THE DIVISION 2: GAME HUB": [
        ("📰・td2-news", "text"),
        ("⚙️・builds-theory", "text"),
        ("🗺️・missions-help", "text"),
        ("👾・boss-strats", "text"),
        ("🛠️・tech-support", "text")
    ],
    "🔍 LFG / ACTIVITIES": [
        ("🔍・lfg-pve", "text"),
        ("🔥・lfg-raids", "text"),
        ("🏆・lfg-battlepass", "text"),
        ("🕐・scheduled-runs", "text"),
        ("🌍・lfg-global", "text")
    ],
    "🔊 VOICE CHANNELS": [
        ("🔊・Lobby", "voice"),
        ("🔊・Squad-1", "voice"),
        ("🔊・Squad-2", "voice"),
        ("🔊・Raid-Command", "voice"),
        ("🔊・AFK / Chill", "voice")
    ],
    "🛠️ STAFF & ADMIN": [
        ("🔐・staff-chat", "text"),
        ("📋・applications", "text"),
        ("🗑️・mod-logs", "text"),
        ("⚙️・server-setup", "text")
    ]
}

# --- СОБЫТИЯ ---
@bot.event
async def on_ready():
    print(f'✅ Bot Online: {bot.user.name}')
    print(f'🔗 Server ID: {bot.guilds[0].id if bot.guilds else "N/A"}')
    await bot.change_presence(activity=discord.Game(name="The Division 2 | !help"))

# --- КОМАНДЫ ---

@bot.command(name='setup')
@commands.has_permissions(administrator=True)
async def setup_server(ctx):
    """
    🛠️ Creates all roles, categories, and channels for CoopFamily server.
    Requires Administrator permissions.
    """
    guild = ctx.guild
    await ctx.send("🚀 **Starting CoopFamily Server Setup...** This may take a minute.")

    # 1. Создание ролей
    created_roles = {}
    for role_name, color in ROLE_COLORS.items():
        try:
            role = await guild.create_role(name=role_name, color=discord.Color(color), reason="CoopFamily Setup")
            created_roles[role_name] = role
            print(f"✅ Role created: {role_name}")
        except Exception as e:
            print(f"❌ Error creating role {role_name}: {e}")
    
    await ctx.send(f"🎨 **Created {len(created_roles)} roles.**")

    # 2. Создание категорий и каналов
    for cat_name, channels in CATEGORIES.items():
        try:
            category = await guild.create_category_channel(cat_name)
            
            # Скрываем категорию Staff от всех, кроме админов
            if "STAFF" in cat_name:
                await category.set_permissions(guild.default_role, view_channel=False)
                if "Leader" in created_roles:
                    await category.set_permissions(created_roles["Leader"], view_channel=True)
                if "Officer" in created_roles:
                    await category.set_permissions(created_roles["Officer"], view_channel=True)

            # Создаем каналы внутри категории
            for ch_name, ch_type in channels:
                if ch_type == "text":
                    await guild.create_text_channel(ch_name, category=category)
                elif ch_type == "voice":
                    await guild.create_voice_channel(ch_name, category=category)
            
            print(f"✅ Category created: {cat_name}")
        except Exception as e:
            print(f"❌ Error in category {cat_name}: {e}")

    await ctx.send("✅ **Server Setup Complete!** Check your channels and roles.")
    await ctx.send("💡 **Tip:** Use `!welcome` in #👋・welcome to send the welcome message.")

@bot.command(name='welcome')
@commands.has_permissions(manage_messages=True)
async def send_welcome(ctx):
    """
    📢 Sends a beautiful welcome embed message (English version).
    """
    embed = discord.Embed(
        title="🧡 Welcome to CoopFamily",
        description='"United We Stand, Divided We Fall" — Our motto in Washington.',
        color=0xFF6B35
    )
    embed.add_field(
        name="🎯 What to Expect?",
        value="• 🤝 Friendly PvE Community\n• 🔍 24/7 LFG for Missions & Farming\n• 📚 Guides, Builds & Newbie Help\n• 🏆 Joint Battlepass & Exotic Farming\n• 🎙️ Active Voice Chats (No Toxicity)",
        inline=False
    )
    embed.add_field(
        name="📋 First Steps:",
        value="1️⃣ Read rules in <#📜・rules>\n2️⃣ Pick your platform in <#🎁・roles>\n3️⃣ Introduce yourself in <#💬・general>\n4️⃣ Find a group in <#🔍・lfg-pve>",
        inline=False
    )
    embed.add_field(
        name="🔗 Useful Links",
        value="[📖 Official Wiki](https://division.fandom.com)\n[🧮 Build Calculator](https://d2calc.com)\n[🎮 Clan Name: CoopFamily]",
        inline=False
    )
    embed.set_footer(text="CoopFamily • SHD Network Active • Est. 2026")
    embed.timestamp = discord.utils.utcnow()

    await ctx.send(embed=embed)

@bot.command(name='help')
async def help_command(ctx):
    """
    ❓ Shows list of available commands.
    """
    embed = discord.Embed(title="🤖 CoopFamily Bot Commands", color=0x3498DB)
    embed.add_field(name="!setup", value="Setup server (roles + channels). Admin only.", inline=False)
    embed.add_field(name="!welcome", value="Send welcome message.", inline=False)
    embed.add_field(name="!help", value="Show this help message.", inline=False)
    embed.set_footer(text="CoopFamily Bot v1.0")
    await ctx.send(embed=embed)

@bot.command(name='ping')
async def ping_command(ctx):
    """
    🏓 Check bot latency.
    """
    latency = round(bot.latency * 1000)
    embed = discord.Embed(title="🏓 Pong!", description=f"Bot latency: **{latency}ms**", color=0x2ECC71)
    await ctx.send(embed=embed)

# --- ОБРАБОТКА ОШИБОК ---
@setup_server.error
async def setup_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You need **Administrator** permissions to use this command!")
    else:
        await ctx.send(f"❌ Error: {error}")

@welcome.error
async def welcome_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You need **Manage Messages** permissions to use this command!")

# --- ЗАПУСК ---
bot.run(TOKEN)

