from person_class import Person

class Lecturer (Person):
    def __init__(self, first_name, last_name, email, HierDate, department):
        super().__init__(first_name, last_name, email)
        self.__hierDate = HierDate
        self.__department = department

    @property
    def hierDate(self):
        return self.__hierDate

    @property
    def department(self):
        return self.__department

    @hierDate.setter
    def hierDate(self, value):
        self.__hierDate = value

    @department.setter
    def department(self, value):
        self.__department = value

    def printo(self):
        super().printo()
        print(f"Hier Date: {self.hierDate}, Department: {self.department}")