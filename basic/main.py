import math

capacities = [] # capacities of rooms. e.g: room at index 0 has capacity 84
teacher_class = [] # the class number that each teacher teaches. e.g: teacher at index 0 teaches class no.5

text_file = open("demo_constraints.txt", "r")
class_time = int(text_file.readline().split("\t")[1])
rooms_num = int(text_file.readline().split("\t")[1])
for i in range(rooms_num):
    line = text_file.readline().split("\t")
    capacities.append((int(line[0]), int(line[1])))

capacities.sort(key = lambda x: x[1]) # a list of tuples. format: (room number, capacity)

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

text_file.close()

#main portion of code
#eventually revise these values

#teachersAvailible is removed with a ranking in classConflicts

classPopularity = [0] * class_num
classScheduled = [False] * class_num
classConflicts = [[0]*class_num for _ in range(class_num)]

#assuming class capacities exist.

for p in student_prefs:
    #p is a list, containing all of the classes that this student would like to take
    for c in p:
        classPopularity[c-1]+=1

  #student conflicts
    for i in range(0,len(p)):
        for j in range (i,len(p)):
            a = p[i]
            b = p[j]
            classConflicts[a-1][b-1]+=1
            classConflicts[b-1][a-1]+=1

        #teacher conflicts
        #need to find all of the classes that a given teacher is teaching
for n in range(1,teacher_num+1):
    indicies = [i for i, x in enumerate(teacher_class) if x==n]
    #note that these lines assume the teacher is only teaching 2 classes
    a=indicies[0]
    b=indicies[1]
    classConflicts[a][b]=math.inf
    classConflicts[b][a]=math.inf

#now, creating list of tuples that contain (class1,class2,conflictscore)
conflictList = []
for i in range(len(classConflicts)):
    for j in range(0,i):
        c = (i+1,j+1, classConflicts[i][j])
        conflictList.append(c)
conflictList.sort(reverse=True, key = lambda t: t[2])

timeslot = [[] for _ in range(class_time)] #this syntax is terrible...
roomSchedules = [[-1]*rooms_num for _ in range(class_time)] #in this case, call roomSchedules[time][roomID-1]
maxRoom = [capacities[-1][1]]*class_time #this will take the largest-capacity room still availible in each timeslot
class_rooms = [-1]*class_num
class_times = [-1]*class_num
class_cap = [-1]*class_num

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
            r = 0
            while room_cap < classPopularity[c-1] and r < rooms_num:
                if roomSchedules[slot_id][r] == -1:
                    best_room = r
                    room_cap = capacities[r][1]
                r += 1

            #now the best room has been found
            #schedule room
            if best_room != -1:
                roomSchedules[slot_id][best_room] = c
                class_rooms[c-1] = capacities[best_room][0]
                class_times[c-1] = slot_id
                class_cap[c-1]= capacities[best_room][1]
            if room_cap == maxRoom[slot_id]:
                #there is a smaller maxRoom
                newMaxRoom = -1
                for i in range(len(roomSchedules[slot_id])):
                    if roomSchedules[slot_id][i] == -1 and capacities[i][1] > newMaxRoom:
                        newMaxRoom = capacities[i][1]
                maxRoom[slot_id] = newMaxRoom

# print("roomSchedules: ",roomSchedules)
# print("timeslots: ",timeslot)
#any other conflict weighting can be done here

#now, each pair of classes must be ranked in decreasing order of conflict
#for t in range(len(roomSchedules)):
#    print("======")
#    for i in range(len(roomSchedules[t])):
#            if(roomSchedules[t][i] != -1):
#                course = roomSchedules[t][i]-1
#                class_rooms[course] = i+1 #id+1
#                print("assigned classroom: ",i)
#                class_times[course] = t #I think this should be t+1
           # else:
#                print("room not assigned")
#for i in range(class_num+1):
#    for j in range(len(roomSchedules)):
#        if i in roomSchedules[j]:
#            roomSchedules[j]
#            class_rooms.append(roomSchedules[j].index(i) + 1)
#            class_times.append(j+1)

# print(class_rooms)
# print(class_times)
enrollment = [[] for _ in range (class_num)]
for p in range(len(student_prefs)):
    studentAvailable = [True] * class_time

    for c in student_prefs[p]:
        #print("course: ", c-1, ", capacity: ",capacities[class_rooms[c-1]-1],", enrollment: ",len(enrollment[c-1]))
        #studentAvailable[class_times[c-1]-1]
        #if len(enrollment[c-1]) < capacities[class_rooms[c-1]-1][1] and studentAvailable[class_times[c-1]-1]:
        if len(enrollment[c-1]) < class_cap[c-1] and studentAvailable[class_times[c-1]-1]:
            enrollment[c-1].append(p+1)
            studentAvailable[class_times[c-1]-1] = False
        #elif len(enrollment[c-1]) >= capacities[class_rooms[c-1]-1][1]:
            #print("not enrolled, class ",c," at capacity")
# print(enrollment)
for c in range(class_num):
    print(class_rooms[c])
    print("course: ",c+1, " room: ",class_rooms[c]," cap: ", class_cap[c]," enr: ", len(enrollment[c]))
output_file = open("schedule.txt", "w")
output_file.write("Course\tRoom\tTeacher\tTime\tStudents\n")
for c in range(1,class_num+1):
    student_list = ""
    for s in enrollment[c-1]:
        new_student = str(s)+" "
        student_list += new_student
    output_file.write(str(c) + "\t" + str(class_rooms[c-1]) + "\t" + str(teacher_class[c-1]) + "\t" + str(class_times[c-1]) + "\t" + student_list + "\n")

output_file.close()
print("complete.")
