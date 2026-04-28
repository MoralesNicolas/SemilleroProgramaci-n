from .student import Student

class BubbleSheet:
    def __init__(self, student, num_questions):
        self.student = student
        self.num_questions = num_questions
        self.responses = {}
    
    def set_response(self, question_num, answer):
        if answer in ['A', 'B', 'C', 'D']:
            self.responses[question_num] = answer
    
    def get_response(self, question_num):
        return self.responses.get(question_num, '')
    
    def get_all_responses(self):
        return [self.get_response(i) for i in range(1, self.num_questions + 1)]
