class Student:
    def __init__(self, id_number):
        self.id_number = str(id_number).strip()
    
    def __repr__(self):
        return f"Student(ID: {self.id_number})"
