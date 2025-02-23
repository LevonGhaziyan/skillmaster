class ShortAnswer:
    @property
    def question_info(self):
        return {"answer": self.question_property}
    
    def __init__(self, question_property):
        self.question_property = question_property
    
    def __call__(self):
        return self.question_info