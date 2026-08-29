class Person:
    def __init__ (self, Id, name):
        self.name = name
        self.Id = Id

class Student(Person):
    def __init__(self, Id, student_id, name):
        super().__init__(Id, name)
        self.student_id = student_id


class Staff(Person):
    def __init__(self, Id, name, staff_id, tax_num):
        super().__init__(Id, name)
        self.staff_id = staff_id
        self.tax_num = tax_num

class General(Staff):
    def __init__(self, Id, name, staff_id, tax_num, rate_of_pay):
        super().__init__(Id, name, staff_id, tax_num)
        self.rate_of_pay = rate_of_pay

class Academics(Staff):
    def __init__(self, Id, name, staff_id, tax_num, id, publications):
        super().__init__(Id, name, staff_id, tax_num)
        self.id = id
        self.publications = publications



        