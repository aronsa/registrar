import time
import os
import main

students = 100
classes = 10
type = "classes" # type is "students" or "classes"

# def time_analysis(init, type):
filename1 = "time_analysis_" + type + ".txt"
file1 = open(filename1, "w")
filename2 = "solution_analysis_" + type + ".txt"
file2 = open(filename2, "w")

for i in range(50):
    students += 50
    classes += 6
    # remove old constraints and prefs files
    os.remove("demo_constraints.txt")
    os.remove("demo_studentprefs.txt")
    # generate new constraints and prefs files
    if type == "students":
        arg = "perl make_random_input.pl 50 260 8 " + str(students) + " demo_constraints.txt demo_studentprefs.txt"
    elif type == "classes":
        arg = "perl make_random_input.pl 40 " + str(classes) + " 8 2000 demo_constraints.txt demo_studentprefs.txt"
    os.system(arg)
    # time analysis
    start_time = time.time()
    exec(open('main.py').read())
    file1.write(str(time.time() - start_time) + "\n")
    # solution quality analysis
    if type == "students":
        opt_student_value = students * 4
        real_student_value = main.student_value()
        frac = float(real_student_value)/float(opt_student_value)
        file2.write(str(frac) + "\n")
    if type == "classes":
        opt_student_value = 2000 * 4
        real_student_value = main.student_value()
        frac = float(real_student_value)/float(opt_student_value)
        file2.write(str(frac) + "\n")

file1.close()
file2.close()
