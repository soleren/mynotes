class StackItem:
    def __init__(self, item_id, prev_id, text, next, type, level,cat_prev_id=None, search=None):
        self.item_id = item_id
        self.prev_id = prev_id
        self.text = text
        self.next = next
        self.type = type
        self.level = level
        self.cat_prev_id = cat_prev_id
        self.search = search


    def __repr__(self):
        return str({"item_id": self.item_id, "prev_id": self.prev_id, "text": self.text,
                "next": self.next, "type": self.type, "level": self.level, "cat_prev_id": self.cat_prev_id})
