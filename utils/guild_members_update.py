from database import db


def guild_members_update(client):
    for guild in client.guilds:
        members_count_left = len(guild.members)
        member_counter = 0
        member_insert = []

        for member in guild.members:
            member_counter = member_counter + 1
            member_insert.append(f"('{member.id}', '{guild.id}')")
            
            # TODO: Transactions + Multiple insert maximum (research why mysql is so fucking disgustingly slow)
            if member_counter == 200 or member_counter == members_count_left:
                db.query(f"INSERT IGNORE INTO member (`member_id`, `guild_id`) VALUES " + ", ".join(member_insert))
                members_count_left = members_count_left - member_counter
                member_counter = 0
                member_insert = []
