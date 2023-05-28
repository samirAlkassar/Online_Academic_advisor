from Subject_Data import *
from Program import GradeAnalyzer

output = ["['Computer architecture\n','Computer graphics ','Artificial intelligence','Algorithms','Internet technology','Information and Computer Networks Security']"]
# print("Plan:", output)


class Pre_request:
    def __init__(self, subjects, data, outputlist):
        self.subjects = subjects
        self.data = data
        self.outputlist = outputlist

    def convert_to_list(self):
        new_list = self.outputlist[0].replace("'", "").replace(
            "\n", "").replace("[", "").replace("]", "").split(",")
        new_list = [s.strip() for s in new_list]

        return new_list

    def associate_grades_with_courses(self):
        course_code = list(self.subjects.keys())
        course_grades = []
        for x, i in zip(course_code, range(4, len(self.data))):
            course_grade = self.data[i]
            course_grades.append(
                (x, course_grade))
        return course_grades

    def get_passed_courses(self):
        codes_list = []
        for grades in self.associate_grades_with_courses():
            if grades[1] == None:
                continue
            elif grades[1] == 'pc' or (grades[1] >= 60):
                codes_list.append((grades[0]))

        return codes_list

    def get_prerequest(self):
        course_names = []
        pre_req = []
        for code, subject in self.subjects.items():
            if subject['name'] in self.convert_to_list():
                course_names.append(subject['name'])
                pre_req.append(subject['pre_req'])
        prerequisite_list = [pre_req[self.convert_to_list().index(
            course_name)] for course_name in course_names]
        return prerequisite_list

    def check_prerequest(self):

        prereq_list = self.get_prerequest()
        passed_courses = self.get_passed_courses()
        prereq_status = []

        # courses = ['HU111', 'HU113', 'HU121', 'MT441', 'IT281', 'CS311', 'IS341'] list of courses that student passed, large
        # prereq_list = ['prereques to the plan'] small
        for course in prereq_list:  # plan prerequest codes
            if course == None:
                STATE = "Prerequest!"
                prereq_status.append((course, STATE))
            elif course == 'Pass 3 levels':

                grades = GradeAnalyzer.associate_grades_with_courses()
                credit = GradeAnalyzer.credit_hourse(grades)
                if credit >= 109:
                    STATE = "Yes"
                    prereq_status.append((course, STATE))
                else:
                    STATE = "No"
                    prereq_status.append((course, STATE))
            elif course not in passed_courses:
                STATE = "No"
                prereq_status.append((course, STATE))
            else:
                STATE = "Yes"
                prereq_status.append((course, STATE))
        print(prereq_status)
        return prereq_status

    def remove_failed_courses(self):
        prereq_status = self.check_prerequest()
        plan = self.convert_to_list()
        new_plan = []
        Yes = ['Yes', 'Prerequest!']
        for i, j in zip(prereq_status, plan):
            if i[1] in Yes:
                new_plan.append(j)
        return new_plan


# pre_req = Pre_request(subjects, Data_7, output)
# new_plan = pre_req.remove_failed_courses()
# print("the new plan", new_plan)


class CoursePlanner:
    def __init__(self, subjects, data, new_plan):
        self.subjects = subjects
        self.data = data
        self.new_plan = new_plan
        self.associate_grades_with_courses = self._associate_grades_with_courses()
        self.Plan_credits = self._Plan_credits()
        self.newplan_credits = self._newplan_credits()

        self.compute_loss = self._compute_loss()

    def _associate_grades_with_courses(self):
        course_code = list(self.subjects.keys())
        course_grades = []
        for x, i in zip(course_code, range(4, len(self.data))):
            course_name = self.subjects.get(x, {}).get('name')
            course_program = self.subjects.get(x, {}).get('program')
            course_credits = self.subjects.get(x, {}).get('credits')
            course_prereq = self.subjects.get(x, {}).get('pre_req')
            course_grade = self.data[i]
            course_grades.append(
                (course_name, [course_grade, course_program, course_credits, course_prereq]))
        return course_grades

    def _Plan_credits(self):
        newplan_credits = []
        for code, subjects in self.subjects.items():
            if subjects['name'] in self.new_plan:
                newplan_credits.append((subjects['name'], subjects['credits']))
        return newplan_credits

    def _newplan_credits(self):
        sum_credits = 0
        for i in range(0, len(self.Plan_credits)):
            sum_credits += self.Plan_credits[i][1]
        print(f"newplan_credits: {sum_credits} hourse")
        return sum_credits

    def _compute_loss(self):
        if self.data[2] >= 2.0:
            student_hours = 18
        elif self.data[2] == 0:
            student_hours = 18
        else:
            student_hours = 12
        loss = student_hours - self.newplan_credits
        if loss < -1:
            print("student registered one more hour")
        elif loss > 0:
            print(
                f"you need to register {loss} more hourse\n consult your academic advisor.")
        return loss


# cp = CoursePlanner(subjects, Data_7, new_plan)
# loss = cp.compute_loss
# print(f"Loss: {loss} hours")
