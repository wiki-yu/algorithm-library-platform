import cv2
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from collections import deque
from imutils.video import FPS

class Vgg_RollAverage_RealTime(object):

    def __init__(self,size,roll_len):
        self.size = 224
        self.roll_len = 128
    def preprocess_image(self,img, size):
        """
        -TO DO: Normalize and resize the image to feed into the model

        -Inputs/ Arguments:
        img: extracted image from the video with a size of (634 x 640)
        size: same as the size (width, height) as input size of the model

        -Outputs/ Returns:
        img: Normalized data (Z-score) between [0,1]
        """
        img = cv2.resize(img,(self.size,self.size))
        img = img/255
        mean = np.array([0.485, 0.456, 0.406])
        std = np.array([0.229, 0.224, 0.225])
        img = (img - mean) / std
        return img

    def real_time_prediction(self,video_path, weights_filepath, one_frame = False, roll_average = False):
        """
        -TO DO: Make real time prediction on input video

        -Inputs/ Arguments:
        video_path: path to input video
        weights_filepath: path to trained weights
        one_frame: decides if prediction is made based on single frame
        roll_average: decides if prediction is made based on past few (roll_len) frames

        -Outputs/ Returns:
        save_results.csv: results are saved into a csv file into the root directory
        elasped time: time taken to process the video
        Approximate FPS: computed frame per second
        """

        class_names =  ['away', 'clean_tray', 'count_pills', 'drawer', 'scan_papers_computer']
        cap = cv2.VideoCapture(video_path)
        model = load_model(weights_filepath)
        out_df = pd.DataFrame(columns = ['frame_index','pred_cls', 'pred_prob'])
        frame_index = 0
        Q = deque(maxlen=self.roll_len)
        fps = FPS().start()
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            print("frame index: ", frame_index)
            img = self.preprocess_image(frame, self.size)
            pred_probs = model.predict(np.expand_dims(img, axis=0))
            if one_frame:
                pred_prob = max(pred_probs[0])
                index = np.argmax(pred_probs, axis=1)[0]
                pred_cls = class_names[index]
                out_df = out_df.append({'frame_index':frame_index,'pred_cls':pred_cls,'pred_prob':pred_prob},ignore_index=True)
                frame_index+=1
                fps.update()

            if roll_average:
                Q.append(pred_probs)
                rolling_probs = np.array(Q).mean(axis=0)
                rolling_prob = max(rolling_probs[0])
                index = np.argmax(rolling_probs, axis=1)[0]
                pred_cls = class_names[index]
                out_df = out_df.append({'frame_index':frame_index,'pred_cls':pred_cls,'pred_prob':rolling_prob},ignore_index=True)
                frame_index+=1
                fps.update()
        fps.stop()
        print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
        print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

        cap.release()
        cv2.destroyAllWindows()
        out_df.to_csv('save_results.csv')
if __name__=='__main__':
    # Path where the video is saved (modify the video path if requires)
    video_path = 'v-scan_papers_computer-clip2-1.mp4'
    # Path where the model is saved (modify the weights path if requires)
    weights_filepath = './C3D_tf_vgg_test_ines_3.hdf5'

    data_generator_object = Vgg_RollAverage_RealTime(size=224, roll_len=128)
    data_generator_object.real_time_prediction(video_path, weights_filepath, one_frame = False, roll_average = True)
