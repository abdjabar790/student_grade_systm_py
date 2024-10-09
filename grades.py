class Grade:
    def __init__(self, grade, assignmentId, studentId):
        self.__id = None  
        self.__grade = grade
        self.__assignmentId = assignmentId
        self.__studentId = studentId

    @property
    def id(self):
        return self.__id

    @property
    def grade(self):
        return self.__grade

    @property
    def assignmentId(self):
        return self.__assignmentId

    @property
    def studentId(self):
        return self.__studentId