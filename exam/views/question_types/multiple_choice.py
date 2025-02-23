class MultipleChoice:
    @property
    def answer(self):
        self.result = {"answer": []}
        
        for answer in self.answers:
            if answer.startswith("answer_"):
                answer_splitted = answer.split("_")
                self.result["answer"].append(answer_splitted[1])

        return self.result


    def __init__(self, answers):
        self.answers = answers
    
    def __call__(self):
        return self.answer
