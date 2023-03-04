from database import db

class GuildMember:
    def __init__(self, id, member_id, guild_id):
        self.id = id
        self.member_id = member_id
        self.guild_id = guild_id
        
        if self.id:
            query = f"WHERE id = '{self.id}'"
        elif self.member_id and self.guild_id:
            query = f"WHERE member.id = '{self.member_id}' and member.guild_id = '{self.guild_id}'"
        else:
            print("Ошибка! Недостаточно аргументов для получения пользователя")
            return

        guild_member_data = db.query(f"""
            SELECT * member
            LEFT JOIN bank ON bank.member_id = member.id and bank.guild_id = member.guild_id
            WHERE {query}
            LIMIT 1
        """)

        print(guild_member_data)

        if len(guild_member) is None:
            print("Ошибка! Пользователь не найден!")
            return

        self.guild_member = guild_member_data[0]

    def id(self):
        return self.guild_member['id']

    def member_id(self):
        return self.member_id

    def guild_id(self):
        return self.guild_id

    def balance(self):
        return self.guild_member['bank']
