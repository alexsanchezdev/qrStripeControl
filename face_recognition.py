import cognitive_face as CF
import pyfirmata
import cv2
from PIL import Image


def main():

    KEY = '7a2565cea8e54a30b345506605f9c4ce'  # Replace with a valid Subscription Key here.
    CF.Key.set(KEY)
    video_capture = cv2.VideoCapture(0)
    DELAY = 3.0
    PORT = '/dev/ttyACM0'
    board = pyfirmata.Arduino(PORT)

    url = 'https://raw.githubusercontent.com/alxsnchez/photo-test/master/test.jpg'
    #person_group = CF.person_group.get('sensei-test')
    #person_group_id = person_group['personGroupId']
    #person = CF.person.create(person_group_id, 'Alex')
    #person_id = person['personId']
    #add_face = CF.person.add_face(url, person_group_id, person_id)
    #train = CF.person_group.train(person_group_id)
    #print person_group
    
    ret, frame = video_capture.read()
    image = cv2.imwrite('image.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80.0])
    
    webcam = 'image.jpg'
    
    webcam_data = CF.face.detect(webcam)
    webcam_ids = []
    
    for image in webcam_data:
        webcam_ids.append(image['faceId'])

    print webcam_ids
    board.digital[13].write(1)
    identify = CF.face.identify(webcam_ids, 'sensei-test', 1, None)
    print len(identify)
    if len(identify) != 0:
        identify_candidate = identify[0]['candidates'][0]
        candidate_id = identify_candidate['personId']
        print candidate_id
    else:
        error()

    verify = CF.face.verify(webcam_data[0]['faceId'], None, 'sensei-test', candidate_id)
    if verify['isIdentical'] == True:
        board.digital[13].write(0)
        board.digital[12].write(1)
        board.pass_time(DELAY)
        board.digital[12].write(0)
    else:
        error()
        

def error():
    board.digital[13].write(0)
    board.digital[11].write(1)
    board.pass_time(DELAY)
    board.digital[11].write(0)
        
if __name__ == "__main__":
    main()
