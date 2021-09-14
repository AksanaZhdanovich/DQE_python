import random
sp = []
for _ in range(100):  #create list of 100 random numbers from 0 to 1000
    sp.append(random.randint(0, 1000)) 
for i in range (0, len(sp)): #sort list from min to max
    min = i
    for j in range( i + 1 , len(sp)):
        if sp[j] < sp[min]:
            min = j
    sp[i] , sp[min] = sp[min], sp[i]
cnt_odd = 0 #count of odd numbers - init
sm_odd = 0 # sum of odd - init
sm_ev = 0 # sum of even - init
for i in sp:  # calculate sum of even, odd numbers and count of odd numbers
    if i % 2 != 0:
        cnt_odd += 1
        sm_odd += i
    else:
        sm_ev += i
av_odd = sm_odd / cnt_odd # calculate average of odd numbers
av_ev = sm_ev / (100 - cnt_odd) # calculate average of even numbers 
print('Average of odd numbers: ', round(av_odd, 2)) #print average of odd numbers
print('Average of even numbers: ', round(av_ev, 2)) #print average of even numbers
