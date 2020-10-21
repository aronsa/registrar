import math
import operator

capacities = {} # capacities of rooms. e.g: room at index 0 has capacity 84
teacher_class = [] # the class number that each teacher teaches. e.g: teacher at index 0 teaches class no.5

text_file = open("demo_constraints.txt", "r")
class_time = text_file.readline()
rooms_num = int(text_file.readline().split("\t")[1])
for i in range(rooms_num):
    line = text_file.readline().split("\t")
    capacities[int(line[0])] = int(line[1])

capacities = sorted(capacities.items(), key=operator.itemgetter(1)) # a list of tuples. format: (room number, capacity)
print(capacities)


class_num = int(text_file.readline().split("\t")[1]) # total number of classes
teacher_num = int(text_file.readline().split("\t")[1]) # total number of teachers
for i in range(class_num):
    teacher_class.append(int(text_file.readline().split("\t")[1]))


student_prefs = [] # a list of list that contains student preferences

text_file = open("demo_studentprefs.txt", "r")
student_num = int(text_file.readline().split("\t")[1]) # number of students
for i in range(student_num):
    prefs = text_file.readline().split("\t")[1].split(' ')
    for index in range(4):
        prefs[index] = int(prefs[index])
    student_prefs.append(prefs)





#main portion of code
#eventually revise these values

#teachersAvailible is removed with a ranking in classConflicts
print("Class Num: ",class_num)
print("teacher_class: ",teacher_class)

classPopularity = [0] * class_num
classScheduled = [False] * class_num
classConflicts = [[0]*class_num for _ in range(class_num)]

#assuming class capacities exist.

for p in student_prefs:
    #p is a list, containing all of the classes that this student would like to take
#    print(p)
    for c in p:
#        print(c)
        classPopularity[c-1]+=1

  #student conflicts
    for i in range(0,len(p)):
        for j in range (i,len(p)):
            a = p[i]
            b = p[j]
#            print("a: ",a)
#            print("b: ",b)
#            print("class Conflicts: ",classConflicts)
#            print("len: ",len(classConflicts))
            classConflicts[a-1][b-1]+=1
            classConflicts[b-1][a-1]+=1

        #teacher conflicts
        #need to find all of the classes that a given teacher is teaching
#while len(teacher_class)>0:
#    a = teacher_class.pop()
#    b = teacher_class.pop(teacher_class.index(a))
#    print("teacher conflicts with classes a=",a,", b=",b)
#    teacherConflicts[a-1][b-1]+=math.inf
#    teacherConflicts[b-1][a-1]+=math.inf

for n in range(1,teacher_num+1):
    indicies = [i for i, x in enumerate(teacher_class) if x==n]
    print(indicies)
    #note that these lines assume the teacher is only teaching 2 classes
    a=indicies[0]
    b=indicies[1]
    classConflicts[a-1][b-1]=math.inf
    classConflicts[b-1][a-1]=math.inf

print("class conflicts:",classConflicts)
    #any other conflict weighting can be done here

    #now, each pair of classes must be ranked in decreasing order of conflict

