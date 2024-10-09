class Person:
    def __init__(self, first_name, last_name, email):
        self.__id = None  # id سيتم تعيينه من قبل قاعدة البيانات
        self.__Fname = first_name  
        self.__Lname = last_name    
        self.__email = email        

    @property
    def id(self):
        return self.__id
    
    @property
    def Fname(self):
        return self.__Fname

    @property
    def Lname(self):
        return self.__Lname

    @property
    def email(self):
        return self.__email

    @id.setter
    def id (self,value):
        if isinstance(value, int):
            self.__id = value
        else:
            pass
        
    @Fname.setter
    def Fname(self, value):
        if isinstance(value, str) and value.isalpha():
            self.__Fname = value
        else:
            pass

    @Lname.setter
    def Lname(self, value):
        if isinstance(value, str) and value.isalpha():
            self.__Lname = value
        else:
            pass

    @email.setter
    def email(self, value):
        if isinstance(value, str) and value.isalpha():
            self.__email = value
        else:
            pass

    def printo(self):
        print(f"Name: {self.Fname} {self.Lname}, Email: {self.email}")