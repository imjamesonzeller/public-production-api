class Task():
    def __init__(self, name, due_date, priority):
        self.name: str = name
        self.due_date: str = due_date
        self.priority: str = priority

    def to_dict(self) -> dict[str, str]:
        return {
            "name": self.name,
            "due_date": self.due_date,
            "priority": self.priority,
        }