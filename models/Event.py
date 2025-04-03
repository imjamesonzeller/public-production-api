class Event():
    def __init__(self, name, date, trueStart):
        self.name: str = name
        self.date: str = date
        self.trueStart: str = trueStart

    def to_dict(self) -> dict[str, str]:
        return {
            "name": self.name,
            "date": self.date,
        }
    
    def __lt__(self, obj):
        return ((self.trueStart) < (obj.trueStart))

    def __gt__(self, obj):
        return ((self.trueStart) > (obj.trueStart))

    def __le__(self, obj):
        return ((self.trueStart) <= (obj.trueStart))

    def __ge__(self, obj):
        return ((self.trueStart) >= (obj.trueStart))

    def __eq__(self, obj):
        return (self.trueStart == obj.trueStart)