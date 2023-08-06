from homevee.VoiceAssistant import VoiceAssistant

def user_is_at_home(username, db):
    with db:
        cur = db.cursor()
        cur.execute("SELECT * FROM USERDATA WHERE USERNAME = :username", {'username': username})

        user = cur.fetchone()

        return user['AT_HOME']

def do_voice_command(username, text, user_last_location, location, db, language):
    return VoiceAssistant().do_voice_command(username, text, user_last_location, location, db, language)