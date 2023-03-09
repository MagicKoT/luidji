from database import db


class GuildMember:
    def __init__(self, id=None, member_id=None, guild_id=None):
        self.id = id
        self.member_id = member_id
        self.guild_id = guild_id
        
        if self.id is not None:
            self.statement = f"WHERE id = '{self.id}'"
        elif self.member_id is not None and self.guild_id is not None:
            self.statement = f"WHERE member.member_id = '{self.member_id}' AND member.guild_id = '{self.guild_id}'"
        else:
            print("Ошибка! Недостаточно аргументов для получения пользователя")
            return

        query_string = f"""SELECT
                member.*,
                eco.bank,
                exp.chat_level,
                exp.chat_experience,
                exp.chat_next_level_experience_cap,
                exp.voice_level,
                exp.voice_experience,
                exp.voice_next_level_experience_cap
            FROM member
            LEFT JOIN eco ON eco.member_id = member.member_id AND eco.guild_id = member.guild_id
            LEFT JOIN experience as exp ON exp.member_id = member.member_id AND exp.guild_id = member.guild_id
            {self.statement}
            LIMIT 1
        """

        guild_member_data = db.query(query_string)

        if len(guild_member_data) == 0:
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
    
    def save_eco(self):
        db.query(f"UPDATE eco SET bank = '{self.guild_member['bank']}' {self.statement}")

    def save_experience(self):
        db.query(f"""UPDATE experience
            SET
                chat_level = '{self.guild_member['chat_level']}' AND
                chat_experience = '{self.guild_member['chat_experience']}' AND 
                chat_next_level_experience_cap = '{self.guild_member['chat_next_level_experience_cap']}' AND
                voice_level = '{self.guild_member['voice_level']}' AND
                voice_experience = '{self.guild_member['voice_experience']}' AND
                voice_next_level_experience_cap = '{self.guild_member['voice_next_level_experience_cap']}'
        """)

    def save(self):
        self.save_eco()
        self.save_experience()
