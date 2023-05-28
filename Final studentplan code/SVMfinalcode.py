from sklearn.ensemble import RandomForestClassifier as rfc
from sklearn.model_selection import train_test_split
from Pre_request import *
from sklearn import preprocessing
import matplotlib.pyplot as plt
from Subject_Data import *
import Program as pp
import pandas as pd
import numpy as np
data = pd.read_csv(
    r'C:\Users\East-Sound\Desktop\Student ML\Final studentplan code\students_data.csv')


def Randomforest(data):
    data1 = data.fillna(0)
    le = preprocessing.LabelEncoder()
    data1['Program'] = le.fit_transform(data1['Program'])
    for column in data1.columns[11:18]:

        mask = data1[column] == 'pc'
        data1.loc[mask, column] = 50
    # features
    x = data1.iloc[:, :-1].values
    y = data1.iloc[:, [-1]].values
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=5)
    random_forest = rfc(n_estimators=95)
    random_forest.fit(x_train, y_train.ravel())
    print('Accuracy :', random_forest.score(x_test, y_test), '%')
    return random_forest


def Input(features, random_forest):
    new_list = [0 if x == None else x for x in features]
    new_list = [50 if x == 'pc' else x for x in new_list]
    if len(new_list) != 74:
        print("ERROR:: features length should be 74")
    else:
        output = random_forest.predict([new_list])
    return output


#general ==1
#it == 3
# is == 2
#cs == 0

class GradeAnalyzer:
    def __init__(self, features, subjects):
        self.features = features
        self.subjects = subjects

    def associate_grades_with_courses(self):
        course_code = list(self.subjects.keys())
        course_grades = []
        for x, i in zip(course_code, range(4, len(self.features))):
            course_name = self.subjects.get(x, {}).get('name')
            course_program = self.subjects.get(x, {}).get('program')
            course_credits = self.subjects.get(x, {}).get('credits')
            course_grade = self.features[i]
            course_grades.append(
                (course_name, [course_grade, course_program, course_credits]))

        return course_grades

    def credit_hours(self, grades):
        sum_credits = 0
        exclude = [0, None]
        for i in range(0, len(grades)):
            if (grades[i][1][0]) not in exclude:
                sum_credits += grades[i][1][2]

        return sum_credits

    def program(self):
        general = [1, 'general']
        if self.features[3] in general:
            state = 'general'
        else:
            state = 'not_general'
        return state

    def course_planning(self):
        support_vector_machine = Randomforest(data)
        associate_grades_with_courses = self.associate_grades_with_courses()
        credit_hours = self.credit_hours(associate_grades_with_courses)
        _program = self.program()

        if _program == "general" and (credit_hours > 66):
            return
        else:
            INPUT = Input(self.features, support_vector_machine)
            print("model plan:", INPUT)
            pre_req = Pre_request(self.subjects, self.features, INPUT)
            new_plan = pre_req.remove_failed_courses()
            print("Updated Plan:\n", new_plan)
            cp = CoursePlanner(self.subjects, self.features, new_plan)
            loss = cp.compute_loss
            print(f"Loss: {loss} hours")
            return new_plan


def course(features):
    analyzer = GradeAnalyzer(features, subjects)
    plan = analyzer.course_planning()
    return plan


course = course(Data_1)
