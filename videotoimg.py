import cv2
import os
import videoTester as vt

def done(roll):
    cap=cv2.VideoCapture(0)
    path="/home/siva_ganesh/zips/projects/AttendanceSystem/static/"
    path=path+str(roll)+"/"
    os.mkdir(path)
#    i=0
#    while True:
#        if os.path.exists(path+str(i)):
#            i=i+1
#        else:
#            os.mkdir(path+str(i))
#            print(path+str(i))
#            break

 #   path=path+str(i)+'/'
    count = 0
    while True and count<160:
        ret,test_img=cap.read()
        if not ret :
            continue
       # cv2.imwrite("frame%d.jpg" % count, test_img)     # save frame as JPG file
        imgpath=path+str(count)+'.jpg'
    
        cv2.imwrite(imgpath,test_img)
        count += 1
        resized_img = cv2.resize(test_img, (1000, 700))
        cv2.imshow('face detection Tutorial ',resized_img)
        if cv2.waitKey(30) & 0xFF ==ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    vt.training_student()
    


