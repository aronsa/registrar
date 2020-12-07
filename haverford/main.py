import math
#two very small classes:

class Room:
    __room_counter = 0
    def __init__(self, name,capacity):
        self.name = name
        self.id = Room.__room_counter
        self.capacity = capacity
        Room.__room_counter +=1
    def getPair(self):
        return (self.id,self.name)
class Course:
    __course_counter = 0
    def __init__(self, course_name):
        #in this case, expect the course name to be a course ID number (unique, nonsequential)
        self.name = course_name
        self.id = Course.__course_counter
        print("name: ",self.name," id: ",self.id)
        Course.__course_counter += 1
        self.popularity = 0
        self.enrollment = 0
        self.scheduled = False
        self.room = None
        self.room_cap = -1
        self.teacher = -1
        self.students = []
        self.time = -1
    def getID(self):
        return self.id
    def getPair(self):
        return(self.id,self.name)
    def __str__(self):
        return str(self.getPair())
    def increment_popularity(self):
        self.popularity +=1
    def getScheduledStatus(self):
        return self.scheduled
    def schedule(self):
        self.scheduled = True
    
    def increment_enrollment(self):
        self.enrollment += 1
    def get_enrollment(self):
        return self.enrollment

capacities = [] # capacities of rooms. e.g: room at index 0 has capacity 84
teacher_class = [] # the class number that each teacher teaches. e.g: teacher at index 0 teaches class no.5
course_dict = {}
text_file = open("demo_constraints.txt", "r")
class_time = int(text_file.readline().split("\t")[1])
for i in range(class_time):
    #this is included because the class times are outputted in the HC case. 
    #Our algorithm currently ignores these lines. Mistake? maybe.
    text_file.readline()
rooms_num = int(text_file.readline().split("\t")[1])
for i in range(rooms_num):
    line = text_file.readline().split("\t")
    capacities.append((Room(line[0],line[1]), int(line[1])))

capacities.sort(key = lambda x: x[1]) # a list of tuples. format: (Room, capacity)

class_num = int(text_file.readline().split("\t")[1]) # total number of classes
teacher_num = int(text_file.readline().split("\t")[1]) # total number of teachers
teacher_class_pairs = []
for i in range(class_num):
    l = text_file.readline().split("\t") 
    if(l[0] != "\n" and l[1] != "\n"):
        classID = int(l[0])
        teacherID = int(l[0])
        if(course_dict.get(classID) ==None):
            course_dict[classID] = Course(classID)
        teacher_class_pairs.append((teacherID,course_dict.get(classID)))

student_prefs = [] # a list of list that contains student preferences

text_file = open("demo_studentprefs.txt", "r")
student_num = int(text_file.readline().split("\t")[1]) # number of students
for i in range(student_num):
    prefs = text_file.readline().split("\t")[1].split(' ')
    fp=[]
    for p in prefs:
        if(p == "\n"):
            break
        fp.append(int(p))
    fp = list(set(fp)) #remove duplicates
    student_prefs.append(fp)

text_file.close()




#main portion of code
#eventually revise these values

#teachersAvailible is removed with a ranking in classConflicts
print("class num: ",class_num)
classPopularity = [0] * class_num
classScheduled = [False] * class_num
classConflicts = [[0]*(class_num+5) for _ in range(class_num+5)]
print(len(course_dict))
#assuming class capacities exist.

for p in student_prefs:
    #p is a list, containing all of the classes that this student would like to take
    for c in p:
    #    classPopularity[c-1]+=1
        course = course_dict.get(c)
        if (course != None): #this will happen for BMC course enrollments
            course.increment_popularity()
  #student conflicts
    for i in range(0,len(p)):
        for j in range (i,len(p)):
            a = p[i]
            b = p[j]
            print("req pair:",a," ",b)
            course_a = course_dict.get(a)
            course_b = course_dict.get(b)
            if(course_a != None and course_b != None):
                ida = course_dict.get(a).getID()
                idb = course_dict.get(b).getID()
                classConflicts[ida][idb]+=1
                classConflicts[idb][ida]+=1
            else:
                print("somthing weird happened here...")
        #teacher conflicts
        #need to find all of the classes that a given teacher is teaching
teacher_class_pairs.sort(key=lambda p:p[0])

for i in range(len(teacher_class_pairs)-1):
    if(teacher_class_pairs[i][1] == teacher_class_pairs[i+1][1]):
        classA =teacher_class_pairs[i][0]
        classB =teacher_class_pairs[i][1]
        a = classA.getID()
        b = classB.getID()
    #note that these lines assume the teacher is only teaching 2 classes
        classConflicts[a][b]=math.inf
        classConflicts[b][a]=math.inf

#now, creating list of tuples that contain (class1,class2,conflictscore)
conflictList = []
for i in range(len(classConflicts)):
    for j in range(0,i):
        c = (i,j, classConflicts[i][j])
        conflictList.append(c)
conflictList.sort(reverse=True, key = lambda t: t[2])

timeslot = [[] for _ in range(class_time)] #this syntax is terrible...
roomSchedules = [[-1]*rooms_num for _ in range(class_time)] #in this case, call roomSchedules[time][roomID-1]
maxRoom = [capacities[-1][1]]*class_time #this will take the largest-capacity room still availible in each timeslot
for conflict in conflictList:
    classes = [conflict[0],conflict[1]]
    for c in classes:
        course_c = course_dict.get(c)
        if(course_c != None and not(course_c.getScheduledStatus())):
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
            course_c.schedule()
            course_c.time = slot_id
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
                course_c.room = best_room
                course_c.room_cap = room_cap

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
class_rooms = []
class_times = []

for i in range(class_num+1):
    for j in range(len(roomSchedules)):
        if i in roomSchedules[j]:
            class_rooms.append(roomSchedules[j].index(i) + 1)
            class_times.append(j+1)

# print(class_rooms)
# print(class_times)

for p in range(len(student_prefs)):
    studentAvailable = [True] * class_time

    for c in student_prefs[p]:
        course = course_dict.get(c)
        if(course != None):
            c = course.getID()
            #print(c)
            #print(class_rooms[c])
            #capacities[class_rooms[c]]
            studentAvailable[course.time]
            if course.enrollment < course.room_cap and studentAvailable[course.time]:
                course.increment_enrollment()
                course.students.append(p+1)
                studentAvailable[course.time] = False

# print(enrollment)
# print(enrollment)
output_file = open("schedule.txt", "w")
output_file.write("Course\tRoom\tTeacher\tTime\tStudents\n")
for c in course_dict:
    c=course_dict[c]
    student_list = ""
    for s in c.students:
        new_student = str(s)+" "
        student_list += new_student
    output_file.write(str(c.getID()) + "\t" + str(c.room) + "\t" + str(c.teacher) + "\t" + str(c.time) + "\t" + student_list + "\n")

output_file.close()
print("complete.")
