from person_class import Person

class Student(Person):
    def __init__(self, first_name, last_name, email, date_of_birth, date_of_enroll):
        super().__init__(first_name, last_name, email)
        self.__DateOfBirth = date_of_birth  
        self.__DateOfEnroll = date_of_enroll  

    @property
    def DateOfBirth(self):
        return self.__DateOfBirth

    @property
    def DateOfEnroll(self):
        return self.__DateOfEnroll

    @DateOfBirth.setter
    def DateOfBirth(self, value):
        self.__DateOfBirth = value

    @DateOfEnroll.setter
    def DateOfEnroll(self, value):
        self.__DateOfEnroll = value

    def printo(self):
        super().printo()
        print(f"Date of Birth: {self.DateOfBirth}, Date of Enroll: {self.DateOfEnroll}")
