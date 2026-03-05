import discord
from discord.ext import commands
from discord import Permissions
from discord.ui import Button, View
import os
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()

# --- НАСТРОЙКИ ---
TOKEN = os.getenv('DISCORD_TOKEN')  # ⚠️ Токен берётся из .env
if not TOKEN:
    print("❌ Error: DISCORD_TOKEN not found in environment variables!")
    print("💡 Please create a .env file with DISCORD_TOKEN=your_token_here")
    exit(1)

INTENTS = discord.Intents.default()
INTENTS.message_content = True
INTENTS.members = True  # Нужно для on_member_join

# Отключаем стандартную команду help, чтобы использовать свою
bot = commands.Bot(command_prefix='!', intents=INTENTS, help_command=None)

# --- ID КАНАЛОВ (для кликабельных ссылок) ---
CHANNEL_IDS = {
    "rules": "1479178350823211068",
    "roles": "1479178355701186695",
    "general": "1479178361535201513",
    "lfg-pve": "1479178383601434675"
}

# --- ID АВТО-РОЛИ ПРИ ВХОДЕ ---
AUTO_ROLE_ID = "1479178344976089179"  # New-Agent role

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

# --- РОЛИ ДЛЯ САМОВЫДАЧИ (через кнопки) ---
SELF_ASSIGNABLE_ROLES = {
    "PC": "🖥️ PC Gamer",
    "PlayStation": "🎮 PlayStation",
    "Xbox": "🕹️ Xbox",
    "PvE-Hardcore": "⚔️ PvE Hardcore",
    "PvE-Casual": "🌿 PvE Casual",
    "BattlePass-Grind": "🏆 Battle Pass Grind",
    "Ping-Events": "📢 Event Notifications",
    "Ping-LFG": "🔍 LFG Notifications"
}

# --- ОПИСАНИЯ РОЛЕЙ (для !roles команды) ---
ROLE_DESCRIPTIONS = {
    "Leader": "👑 Server Owner - Full control over server",
    "Officer": "🛡️ Server Moderator - Manage members and channels",
    "Veteran": "⭐ Trusted Member - Long-time active player",
    "Raid-Leader": "⚔️ Raid Organizer - Leads raid operations",
    "PC": "💻 PC Platform - Play on PC (Steam/Ubisoft)",
    "PlayStation": "🎮 PlayStation Platform - Play on PS4/PS5",
    "Xbox": "🕹️ Xbox Platform - Play on Xbox One/Series",
    "PvE-Hardcore": "🔥 Hardcore PvE - Raids, Heroic, Optimized builds",
    "PvE-Casual": "🌿 Casual PvE - Missions, Farming, relaxed gameplay",
    "BattlePass-Grind": "🏆 BP Farmer - Focus on Battle Pass progression",
    "Ping-Events": "📢 Event Pings - Get notified about clan events",
    "Ping-LFG": "🔍 LFG Pings - Get notified about group finding",
    "New-Agent": "🔰 New Member - Just joined the server",
    "Muted": "🔇 Muted - Temporary restriction"
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

# --- КЛАСС ДЛЯ КНОПОК РОЛЕЙ ---
class RoleSelectView(View):
    def __init__(self):
        super().__init__(timeout=None)
        
        # Создаем кнопки для каждой самовыдаваемой роли
        for role_name, description in SELF_ASSIGNABLE_ROLES.items():
            emoji = description.split(" ")[0]  # Берём эмодзи из описания
            
            # Определяем цвет кнопки
            if role_name in ["PC", "PlayStation", "Xbox"]:
                style = discord.ButtonStyle.blurple
            elif role_name in ["Ping-Events", "Ping-LFG"]:
                style = discord.ButtonStyle.green
            else:
                style = discord.ButtonStyle.gray
            
            button = RoleButton(role_name, emoji, style)
            self.add_item(button)

class RoleButton(Button):
    def __init__(self, role_name, emoji, style):
        super().__init__(style=style, label=role_name, emoji=emoji)
        self.role_name = role_name
    
    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        member = interaction.user
        
        # Ищем роль по имени
        role = discord.utils.get(guild.roles, name=self.role_name)
        
        if not role:
            await interaction.response.send_message(
                f"❌ Role **{self.role_name}** not found!",
                ephemeral=True
            )
            return
        
        # Проверяем, есть ли уже роль
        if role in member.roles:
            # Удаляем роль
            await member.remove_roles(role)
            await interaction.response.send_message(
                f"❌ Removed **{self.role_name}** role!",
                ephemeral=True
            )
        else:
            # Добавляем роль
            await member.add_roles(role)
            await interaction.response.send_message(
                f"✅ Added **{self.role_name}** role!",
                ephemeral=True
            )

# --- СОБЫТИЯ ---
@bot.event
async def on_ready():
    print(f'✅ Bot Online: {bot.user.name}')
    print(f'🔗 Server ID: {bot.guilds[0].id if bot.guilds else "N/A"}')
    await bot.change_presence(activity=discord.Game(name="The Division 2 | !help"))
    
    # Синхронизация кнопок (нужно для persistent views)
    bot.add_view(RoleSelectView())

@bot.event
async def on_member_join(member):
    """
    🎉 Авто-выдача роли при входе на сервер
    """
    try:
        auto_role = discord.utils.get(member.guild.roles, id=int(AUTO_ROLE_ID))
        if auto_role:
            await member.add_roles(auto_role)
            print(f"✅ Auto-role assigned to {member.name}")
            
            # Отправляем приветственное ЛС
            try:
                await member.send(
                    f"🧡 **Welcome to CoopFamily, {member.name}!**\n\n"
                    f"You've been assigned the **New-Agent** role.\n\n"
                    f"📋 **Next steps:**\n"
                    f"• Read rules in <#{CHANNEL_IDS['rules']}>\n"
                    f"• Get your roles in <#{CHANNEL_IDS['roles']}>\n"
                    f"• Introduce yourself in <#{CHANNEL_IDS['general']}>\n\n"
                    f"*United We Stand, Divided We Fall*"
                )
            except discord.Forbidden:
                print(f"⚠️ Cannot send DM to {member.name} (DMs disabled)")
    except Exception as e:
        print(f"❌ Error assigning auto-role: {e}")

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
    await ctx.send("💡 **Tip:** Use `!welcome` in #👋・welcome and `!roles` in #🎁・roles")

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
        value=f"1️⃣ Read rules in <#{CHANNEL_IDS['rules']}>\n2️⃣ Pick your platform in <#{CHANNEL_IDS['roles']}>\n3️⃣ Introduce yourself in <#{CHANNEL_IDS['general']}>\n4️⃣ Find a group in <#{CHANNEL_IDS['lfg-pve']}>",
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

@bot.command(name='roles')
@commands.has_permissions(manage_messages=True)
async def send_roles(ctx):
    """
    🎁 Sends role selection embed with buttons.
    """
    embed = discord.Embed(
        title="🎁 Select Your Roles",
        description="Click the buttons below to get your roles! You can remove them by clicking again.",
        color=0x3498DB
    )
    
    # Разделяем роли по категориям
    platforms = "**🎮 Platforms**\n"
    playstyle = "**⚔️ Playstyle**\n"
    notifications = "**🔔 Notifications**\n"
    
    for role_name, description in SELF_ASSIGNABLE_ROLES.items():
        emoji = description.split(" ")[0]
        if role_name in ["PC", "PlayStation", "Xbox"]:
            platforms += f"{emoji} `{role_name}` - Platform selection\n"
        elif role_name in ["Ping-Events", "Ping-LFG"]:
            notifications += f"{emoji} `{role_name}` - Get pinged for events\n"
        else:
            playstyle += f"{emoji} `{role_name}` - Your gameplay style\n"
    
    embed.add_field(name="🎮 Platforms", value=platforms, inline=False)
    embed.add_field(name="⚔️ Playstyle", value=playstyle, inline=False)
    embed.add_field(name="🔔 Notifications", value=notifications, inline=False)
    
    embed.add_field(
        name="⚠️ Restricted Roles",
        value="`Leader`, `Officer`, `Veteran` - Assigned by administrators only",
        inline=False
    )
    
    embed.set_footer(text="CoopFamily • Click buttons to self-assign roles")
    
    await ctx.send(embed=embed, view=RoleSelectView())

@bot.command(name='help')
async def help_command(ctx):
    """
    ❓ Shows list of available commands (Custom Help).
    """
    embed = discord.Embed(
        title="🤖 CoopFamily Bot Commands",
        description="Here are all available commands for the server.",
        color=0x3498DB
    )
    embed.add_field(
        name="🛠️ Server Setup",
        value="`!setup` - Create all roles and channels (Admin only)",
        inline=False
    )
    embed.add_field(
        name="📢 Messages",
        value="`!welcome` - Send welcome message (Mod+)\n`!roles` - Send role selection panel (Mod+)\n`!help` - Show this help menu",
        inline=False
    )
    embed.add_field(
        name="🏓 Utilities",
        value="`!ping` - Check bot latency",
        inline=False
    )
    embed.set_footer(text="CoopFamily Bot v1.1 • Type !command for more info")
    await ctx.send(embed=embed)

@bot.command(name='ping')
async def ping_command(ctx):
    """
    🏓 Check bot latency.
    """
    latency = round(bot.latency * 1000)
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"Bot latency: **{latency}ms**",
        color=0x2ECC71
    )
    await ctx.send(embed=embed)

# --- ОБРАБОТКА ОШИБОК ---
@setup_server.error
async def setup_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You need **Administrator** permissions to use this command!")
    else:
        await ctx.send(f"❌ Error: {error}")

@send_welcome.error
async def welcome_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You need **Manage Messages** permissions to use this command!")
    else:
        await ctx.send(f"❌ Error: {error}")

@send_roles.error
async def roles_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You need **Manage Messages** permissions to use this command!")
    else:
        await ctx.send(f"❌ Error: {error}")

@help_command.error
async def help_error(ctx, error):
    await ctx.send(f"❌ Error: {error}")

@ping_command.error
async def ping_error(ctx, error):
    await ctx.send(f"❌ Error: {error}")

# --- ЗАПУСК ---
if __name__ == "__main__":
    try:
        print("🚀 Starting CoopFamily Bot v1.1...")
        bot.run(TOKEN)
    except discord.LoginFailure:
        print("❌ Invalid token! Please check your DISCORD_TOKEN.")
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
