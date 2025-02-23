class ShortAnswer:
    @property
    def answer(self):
        return {"answer": self.answers["answer"]}
    
    def __init__(self, answers):
        self.answers = answers
    
    def __call__(self):
        return self.answer