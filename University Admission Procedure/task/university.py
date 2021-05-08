
class UniversityAdmissionProcedure:
    """Class for processing student admissions."""
    def __init__(self):
        self.applicants_list = []
        self.accepted_applicants = None
        self.departments = {'Engineering': [], 'Chemistry': [],
                            'Biotech': [], 'Physics': [],
                            'Mathematics': []}

        self.score_positions = {'Engineering': lambda x: (x[4] + x[5]) / 2,
                                'Chemistry': lambda x: (x[3]),
                                'Biotech': lambda x: (x[2] + x[3]) / 2,
                                'Physics': lambda x: (x[2] + x[4]) / 2,
                                'Mathematics': lambda x: (x[4])
                                }
        self.remaining_positions = None
        self.accepted = {'Engineering': [], 'Chemistry': [],
                         'Biotech': [], 'Physics': [],
                         'Mathematics': []}

    def get_criterion(self, department):
        """Get lambda for sorting student lists."""
        return lambda student: (-(self.get_final_score(department, student)), student[0], student[1])


    def get_final_score(self, department, x):
        """Compare exam results according to department."""
        return max(self.score_positions[department](x), x[6])


    def input_data(self, filename):
        """Read data from file."""
        self.accepted_applicants = int(input())
        self.remaining_positions = {'Engineering': self.accepted_applicants, 'Chemistry': self.accepted_applicants,
                                    'Biotech': self.accepted_applicants, 'Physics': self.accepted_applicants,
                                    'Mathematics': self.accepted_applicants}
        with open(filename, 'r') as file:
            for line in file:
                self.applicants_list.append(line.split())
                for i in [2, 3, 4, 5, 6]:
                    self.applicants_list[-1][i] = float(self.applicants_list[-1][i])

    def accept_students(self):
        """Accept students via exam results."""
        for priority in [7, 8, 9]:
            for student in self.applicants_list:
                self.departments[student[priority]].append(student)
            for department, value in self.departments.items():
                value.sort(key=self.get_criterion(department))
                while self.remaining_positions[department] > 0:
                    if len(value) == 0:
                        break
                    student = value.pop(0)
                    self.accepted[department].append(student)
                    self.applicants_list.remove(student)
                    self.remaining_positions[department] -= 1
                value.clear()

    def save_to_file(self):
        """Save result to files."""
        for department, students in self.accepted.items():
            with open(f'{department}.txt', 'w') as file:
                for student in sorted(students, key=self.get_criterion(department)):
                    print(f'{student[0]} {student[1]} {self.get_final_score(department, student)}', file=file)

    def main(self, filename):
        """Starting point of a program."""
        self.input_data(filename)
        self.accept_students()
        self.save_to_file()
        # for department, value in sorted(self.accepted.items(), key=lambda x: x[0]):
        #     print(f'{department}')
        #     for student in sorted(value, key=lambda x: (-(self.score_positions[department](x)), x[0], x[1])):
        #         print(f'{student[0]} {student[1]} {self.score_positions[department](student)}')
        #     print('\n')


if __name__ == '__main__':
    test = UniversityAdmissionProcedure()
    test.main('applicants_list_7.txt')
