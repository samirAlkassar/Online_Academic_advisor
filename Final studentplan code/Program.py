from Subject_Data import *
import matplotlib.pyplot as plt
# student_status = [1, 1, 2.5, 1, 70, 40, 0, 0, 90,  0, 0, 'pc', 'pc', 'pc', 'pc', 'pc', 'pc', 'pc', 60, 60, 60, 60, 60, 60, 60, 60, 66, 66, 66, 66, 66, 0, 0, 0, 0,
#                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


class GradeAnalyzer:
    def __init__(self, data, subjects):
        self.data = data
        self.subjects = subjects

    def associate_grades_with_courses(self):
        course_code = list(self.subjects.keys())
        course_grades = []
        for x, i in zip(course_code, range(4, len(self.data))):
            course_name = self.subjects.get(x, {}).get('name')
            course_program = self.subjects.get(x, {}).get('program')
            course_credits = self.subjects.get(x, {}).get('credits')
            course_grade = self.data[i]
            course_grades.append(
                (course_name, [course_grade, course_program, course_credits]))

        return course_grades

    def credit_hourse(self, grades):
        sum_credits = 0
        exclude = [0, None]
        for i in range(0, len(grades)):
            if (grades[i][1][0]) not in exclude:
                sum_credits += grades[i][1][2]

        return sum_credits

    def programs_percentage(self):
        course_grades = self.associate_grades_with_courses()
        programs = ['cs', 'it', 'is', 0,  2, 3]
        credit_hourse = self.credit_hourse(course_grades)
        if credit_hourse < 66:
            print("the student didn't pass 66 credit hourse yet !!")
            return
        elif self.data[3] in programs:
            print("student is already in a program !!")
            return
        sum_cs = 0
        count_cs = 0
        sum_it = 0
        count_it = 0
        sum_is = 0
        count_is = 0
        exclude = [None, 'pc', 'general', 'cs', 'it', 'is', 0]
        for i in range(0, len(course_grades)):
            if (course_grades[i][1][0]) not in exclude and course_grades[i][1][1] == 'Computer Science':
                sum_cs += course_grades[i][1][0]
                count_cs += 1
            if (course_grades[i][1][0]) not in exclude and course_grades[i][1][1] == 'Information Technology':
                sum_it += course_grades[i][1][0]
                count_it += 1
            if (course_grades[i][1][0]) not in exclude and course_grades[i][1][1] == 'Information Systems':
                sum_is += course_grades[i][1][0]
                count_is += 1

        avg_cs = sum_cs / count_cs if count_cs > 0 else 0
        avg_it = sum_it / count_it if count_it > 0 else 0
        avg_is = sum_is / count_is if count_is > 0 else 0
        total_percentage = avg_cs+avg_it+avg_is
        cs_percentage = (avg_cs / total_percentage) * 100
        it_percentage = (avg_it / total_percentage) * 100
        is_percentage = (avg_is / total_percentage) * 100
        # Define the data
        program_percentage = {'Computer Science': round(cs_percentage),
                              'Information Technology': round(it_percentage), 'Information Systems': round(is_percentage)}
        programs = list(program_percentage.keys())
        percentages = list(program_percentage.values())
        fig, ax = plt.subplots()
        ax.pie(percentages, labels=programs, autopct='%1.1f%%')
        ax.set_title('Program Percentages')
        plt.show()
        avg_dict = {'Computer Science': round(cs_percentage), 'Information Technology': round(
            it_percentage), 'Information Systems': round(is_percentage)}
        print("credit hourse sum :", credit_hourse)
        print("The average is:", avg_dict, "%")
        max_program = (max(avg_dict['Computer Science'],
                       avg_dict['Information Technology'], avg_dict['Information Systems']))
        for key, value in avg_dict.items():
            if value == max_program:
                print(key, ':', value, "%")
                break


analyzer = GradeAnalyzer(Data_7, subjects)
analyzer.programs_percentage()
