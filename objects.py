from flask import current_app
from blitzdb import Document, queryset

class Waifu(Document):
    def get_waifu_position(self):
        waifus = current_app.dbbackend.filter(Waifu, {"type":"Waifu"}).sort(key="votes", order=queryset.QuerySet.DESCENDING)
        waifu_position = 0
        for waifu in waifus:
            print(waifu)
            waifu_position = waifu_position + 1
            if waifu == self:
                break
        return waifu_position
    pass
