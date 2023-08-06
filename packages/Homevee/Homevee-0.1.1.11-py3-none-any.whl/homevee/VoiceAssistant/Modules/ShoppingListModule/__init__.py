from homevee.VoiceAssistant.Modules import VoiceModule

class VoiceShoppingListModule(VoiceModule):
    def find_items(self, text, db):
        items = []

        with db:
            cur = db.cursor()

            cur.execute("SELECT * FROM SHOPPING_LIST")

            for item in cur.fetchall():
                position = text.find(item['ITEM'].lower())
                if position is not -1:
                    items.append({'item': item['ITEM'], 'amount': item['AMOUNT'], 'id': item['ID']})

        return items