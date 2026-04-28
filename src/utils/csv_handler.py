import csv

class CSVHandler:
    @staticmethod
    def read_student_ids(file_path):
        students = []
        with open(file_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if row and row[0].strip():
                    students.append(row[0].strip())
        return students
    
    @staticmethod
    def write_responses(file_path, results, num_questions):
        results_by_student = {}
        
        for result in results:
            cedula = result['cedula']
            if cedula not in results_by_student:
                results_by_student[cedula] = []
            results_by_student[cedula].extend(result['responses'])
        
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            header = ['Cedula'] + [f'P{i}' for i in range(1, num_questions + 1)]
            writer.writerow(header)
            
            for cedula, responses in results_by_student.items():
                row = [cedula] + responses[:num_questions]
                writer.writerow(row)
