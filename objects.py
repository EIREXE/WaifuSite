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

class User(Document):
    @property
    def is_authenticated(self):
        return True
    @property
    def is_active(self):
        return True
    @property
    def is_anonymous(self):
        return False
    @property
    def is_admin(self):
        if self.google_id == "113163643206165149631":
            return True
        else:
            return False
    @property
    def is_banned(self):
        if(self.banned):
            return True
        else:
            return False
    def get_id(self):
        return self.pk
    pass
