class MultipleChoice:
    @property
    def question_info(self):
        results = self.question_property.split(",")

        final_results = list(map(str.strip, results))

        return {"answer": final_results}
    
    def __init__(self, question_property: str):
        self.question_property = question_property
    
    def __call__(self):
        return self.question_info