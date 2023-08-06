import cv2
import time
import dlib
from imutils import face_utils
from multitask_rag.evaluate import predict_utk as p_utk
from vision_utils.custom_architectures import PretrainedMT
import torch
import torch.nn.functional as F
import os
from torchvision import transforms


detector = dlib.get_frontal_face_detector()
ref = os.path.dirname(os.path.dirname(__file__))
saved_weight = ref + '/multitask_rag/checkpoints/resnet_model_21_val_loss=4.275671.pth'
model = PretrainedMT(model_name='resnet')
model.load_state_dict(torch.load(saved_weight, map_location='cpu'))


def preprocess_utk(image):
    transf = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize((224, 224)),
        transforms.ToTensor()
    ])

    return transf(image).unsqueeze_(0)


def predict_utk(image, model):

    # process image
    image = preprocess_utk(image)

    # prepare model
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.eval()
    model = model.to(device)

    # predict probabilities
    age_pred, gender_pred, race_pred = model(image)
    age_pred = age_pred.detach().to('cpu').numpy()[0][0]
    gender_probs, race_probs = F.softmax(gender_pred, dim=1).detach().to('cpu').numpy()[0],\
                               F.softmax(race_pred, dim=1).detach().to('cpu').numpy()[0]

    # print('------gendr probs', gender_probs)
    # print('------race probs', race_probs)

    # map probabilities to label names
    gender_labs, race_labs = ['Male', 'Female'], ['White', 'Black', 'Asian', 'Indian', 'Other']
    gender = dict([(lab, prob) for lab, prob in zip(gender_labs, gender_probs)])
    race = dict([(lab, prob) for lab, prob in zip(race_labs, race_probs)])

    return age_pred, gender, race


class BaseCamera(object):
    thread = None  # background thread that reads frames from camera
    frame = None  # current frame is stored here by background thread
    last_access = 0  # time of last client access to the camera
    # ...

    @staticmethod
    def frames():
        """Generator that returns frames from the camera."""
        raise RuntimeError('Must be implemented by subclasses.')

    @classmethod
    def _thread(cls):
        """Camera background thread."""
        print('Starting camera thread.')
        frames_iterator = cls.frames()
        for frame in frames_iterator:
            BaseCamera.frame = frame

            # if there hasn't been any clients asking for frames in
            # the last 10 seconds then stop the thread
            if time.time() - BaseCamera.last_access > 10:
                frames_iterator.close()
                print('Stopping camera thread due to inactivity.')
                break
        BaseCamera.thread = None


class CvCamera(BaseCamera):
    @staticmethod
    def frames():
        camera = cv2.VideoCapture(0)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        time.sleep(3)
        while True:
            # read current frame
            _, img = camera.read()

            # img = imutils.resize(img, width=224, height=224)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # detects faces in the grayscale image
            rects = detector(gray, 0)

            # if faces found
            if len(rects) > 0:
                for rect in rects:
                    # get and plot bounding box for each face
                    (bX, bY, bW, bH) = face_utils.rect_to_bb(rect)
                    face = img[bY: bY + bH, bX: bX + bW, :]
                    age, gender, race = predict_utk(face, model)

                    cv2.rectangle(img, (bX, bY), (bX + bW, bY + bH), (0, 0, 255), 1)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(img, str(age),
                                (0, 25), font, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                    cv2.putText(img, str(gender),
                                (0, 50), font, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                    cv2.putText(img, str(race),
                                (0, 75), font, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', img)[1].tobytes()
