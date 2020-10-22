import math
import operator

capacities = {} # capacities of rooms. e.g: room at index 0 has capacity 84
teacher_class = [] # the class number that each teacher teaches. e.g: teacher at index 0 teaches class no.5

text_file = open("demo_constraints.txt", "r")
class_time = int(text_file.readline().split("\t")[1])
rooms_num = int(text_file.readline().split("\t")[1])
for i in range(rooms_num):
    line = text_file.readline().split("\t")
    capacities[int(line[0])] = int(line[1])

capacities = sorted(capacities.items(), key=operator.itemgetter(1)) # a list of tuples. format: (room number, capacity)
#print(capacities)


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
#print("Class Num: ",class_num)
#print("teacher_class: ",teacher_class)

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
    #print(indicies)
    #note that these lines assume the teacher is only teaching 2 classes
    a=indicies[0]
    b=indicies[1]
    classConflicts[a-1][b-1]=math.inf
    classConflicts[b-1][a-1]=math.inf

#now, creating list of tuples that contain (class1,class2,conflictscore)
conflictList = []
for i in range(len(classConflicts)):
    for j in range(0,i):
        c = (i+1,j+1, classConflicts[i][j])
        conflictList.append(c)
#print("unsorted conflict list: ",conflictList)
conflictList.sort(reverse=True, key = lambda t: t[2])
#print("sorted conflict list: ",conflictList)

timeslot = [[] for _ in range(class_time)] #this syntax is terrible...
roomSchedules = [[-1]*rooms_num for _ in range(class_time)] #in this case, call roomSchedules[time][roomID-1]
maxRoom = [capacities[-1][1]]*class_time #this will take the largest-capacity room still availible in each timeslot
for conflict in conflictList:
    classes = [conflict[0],conflict[1]]
    for c in classes:
        if classScheduled[c-1]==False:
            scores = [0]*class_time
            for t in range(class_time):
                for d in timeslot[t]:
                    #it is possible that more students will be able to take the class then can fit in the largest availible room.
                    roomRestriction = classPopularity[c-1] - maxRoom[t]
                    #if the room is smaller than the class, this will be some positive number.
                    scores[t] += max(classConflicts[d][c-1],roomRestriction)
            
            slot_score = min(scores)
            #slot_id is the selected timeslot
            slot_id = scores.index(slot_score)
            timeslot[slot_id].append(c-1)
            classScheduled[c-1]=True
            #need to find classroom
            best_room = -1
            room_cap = -1
            for r in range(rooms_num):
                r=rooms_num - 1 - r
                if(roomSchedules[slot_id][r] == -1 and room_cap < capacities[r][1]): #if room capacity is larger than current room's, and that room is availible
                    best_room = capacities[r][0]
                    room_cap = capacities[r][1]
                    #if room is big enough, stop.
                    if(room_cap >= classPopularity[c-1]):
                        break
                   
            #now the best room has been found
            #schedule room
            if best_room != -1:
                print("timeslot: ",slot_id,"| best room: ",best_room)
                roomSchedules[slot_id][best_room-1] = c

            if room_cap == maxRoom[slot_id]:
                #there is a smaller maxRoom
                newMaxRoom = -1
                for i in range(len(roomSchedules[slot_id])):
                    if roomSchedules[slot_id][i] == -1 and capacities[i][1] > newMaxRoom:
                        newMaxRoom = capacities[i][1]
                maxRoom[slot_id] = newMaxRoom
            print("roomSchedules: ",roomSchedules)

print("timeslots: ",timeslot)
#print("class time: ",class_time)
#print("class conflicts:",classConflicts)
    #any other conflict weighting can be done here

    #now, each pair of classes must be ranked in decreasing order of conflict

