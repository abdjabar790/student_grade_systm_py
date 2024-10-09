class Assignment:
    def __init__(self, name, description, lectureId):
        self.__id = None  
        self.__name = name
        self.__description = description
        self.__lectureId = lectureId

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def description(self):
        return self.__description

    @property
    def lectureId(self):
        return self.__lectureId

    @id.setter
    def id(self, value):
        if isinstance(value, int):
            self.__id = value
        else:
            pass

    @name.setter
    def name(self, value):
        if isinstance(value, str) and value.isalpha():
            self.__name = value
        else:
            pass

    @description.setter
    def description(self, value):
        if isinstance(value, str) and value.isalpha():
            self.__description = value
        else:
            pass

    @lectureId.setter
    def lectureId(self, value):
        if isinstance(value, int):
            self.__lectureId = value
        else:
            pass