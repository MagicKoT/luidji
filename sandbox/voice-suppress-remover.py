"""
guild = get(client.guilds, id=772577481919430656)
target_member = None
target_channel = None

for member in guild.members:
    if member.name == "johntheco":
        target_member = member

for channel in guild.channels:
    if channel.name == "Канал для MAGIC":
        target_channel = channel

print(target_member)
print(target_channel)

print(target_channel.permissions_for(target_member))
permissions = target_channel.overwrites_for(member)
permissions.speak = True
await target_channel.set_permissions(target_member, overwrite=permissions)
"""
