import pandas as pd
import os
from cv2 import cv2
from tensorflow.keras.preprocessing.image import img_to_array
import numpy as np
from joblib import load
from tensorflow.keras.models import load_model
from scipy.stats import mode


class AlcibarAlgorithmPredictor(object):
    """
    The AlcibarAlgorithmPredictor object handles predicting process. This class is
    hard to test unless get broken down to smaller processes.
    TODO: Refactoring output manipulation functions to be less dependent, Rename
    variables to improve code readability.

    """

    def __init__(
        self,
        input_video_path,
        model_path,
    ):
        self.input_video_path = input_video_path
        self.model_path = model_path

    def predict(self):

        # Open video
        vid = cv2.VideoCapture(self.input_video_path)
        if not vid.isOpened():
            raise IOError("Couldn't open webcam or video")

        # Obtain FPS
        video_fps = vid.get(cv2.CAP_PROP_FPS)

        # Ines' model

        # Load Models
        dense_net_model_path = os.path.join(self.model_path, "denseXgB_model_myLayer.h5")
        xgb_model_path = os.path.join(self.model_path, "recognition_xgboost_prev_frames.joblib")
        intermediate_layer_model = load_model(dense_net_model_path)
        xgbmodel = load(xgb_model_path)    

        cnt_list = []
        predResults = []      

        # Initialize variables for the model
        hist_count = 7  # take into account the previous 7 frames
        data_temporal = (
            np.zeros(hist_count * 1024).astype(int).tolist()
        )  # Start the rowlist
        data_temporal = np.array([data_temporal])

        # Start processing the video
        cnt = 0
        while vid.isOpened():
            return_value, frame = vid.read()
            if not return_value:
                break
            image = cv2.resize(frame, (128, 128))
            image = img_to_array(image)
            data = []
            data.append(image)
            data = np.array(data, dtype="float32") / 255.0

            # opencv images are BGR, translate to RGB
            intermediate_test_output = intermediate_layer_model.predict(data)
            data_temporal = data_temporal[0].tolist()
            data_temporal = data_temporal[len(intermediate_test_output[0]) :]
            data_temporal.extend(intermediate_test_output[0])
            data_temporal = np.array([data_temporal])
            ypredNum = xgbmodel.predict(data_temporal)

            cnt_list.extend([cnt])
            predResults.extend([int(ypredNum[0])])

            cnt += 1

        vid.release()

        # Return output
        return video_fps, cnt_list, predResults


def predict(input_video_path, model_path, min_len):

    # Load class names
    classes_id_path = os.path.join(model_path, "classes.txt")
    classfile = open(classes_id_path, "r")
    class_names = [line[:-1] for line in classfile.readlines()]

    model_algorithm = AlcibarAlgorithmPredictor(
        input_video_path = input_video_path,
        model_path = model_path
    )
        
        
    video_fps, cnt_list, predResults = model_algorithm.predict()

    # Clean the output data
    out_df = pd.DataFrame({"frame": cnt_list,"task_label": predResults})
    out_df = process_to_annotation_data(
        out_df, class_names, video_fps, min_len
    )

    # Return output
    return out_df

# Private helper functions

def process_to_annotation_data(df, class_names, video_fps, min_len):
    """
    This function cleans the output data, so that there are
    no jumping frames.
    """
    j = 1  # Helper

    # Minimum qty of frames of the same task in order to
    # consider it a whole task
    min_frames = int(float(min_len) * float(video_fps) * float(0.6))

    # Initialize variables
    df["subgroup"] = (df.iloc[:, -1] != df.iloc[:, -1].shift(1)).cumsum()
    added = (
        df["subgroup"]
        .value_counts()[df["subgroup"].value_counts() < (j + 1)]
        .index.tolist()
    )

    # Modify jumping frames by considering the sourrounding frames
    # check for frames that jump (the total group of those frames are of a max of 7)
    for jj in range(min_frames):

        j = jj + 1

        df["subgroup"] = (df.iloc[:, -2] != df.iloc[:, -2].shift(1)).cumsum()
        added = (
            df["subgroup"]
            .value_counts()[df["subgroup"].value_counts() < (j + 1)]
            .index.tolist()
        )

        cnt = 0
        i_prev = 0
        i_prev_cnt = 0
        while len(added) > 0:
            added.sort()
            i = added[0]

            k = 1  # Helper
            prev = []
            after = []
            prev_yes = 0
            after_yes = 0
            if (i - k) > 0:
                prev = [df[df["subgroup"] == (i - k)].iloc[0, -2]] * len(
                    df[df["subgroup"] == (i - k)]
                )
                prev_yes = 1
            if (i + k) < max(df["subgroup"]) + 1:
                after = [df[df["subgroup"] == (i + k)].iloc[0, -2]] * len(
                    df[df["subgroup"] == (i + k)]
                )
                after_yes = 1
            check_loop = True
            if (prev_yes + after_yes) == 2:
                if mode(prev).mode[0] == mode(after).mode[0]:
                    check_loop = False

            if check_loop:
                k = 1  # Helper
                while len(prev) < j + 2 - i_prev_cnt:
                    k += 1

                    if (i - k) > 0:
                        prev_i = [df[df["subgroup"] == (i - k)].iloc[0, -2]] * len(
                            df[df["subgroup"] == (i - k)]
                        )
                        prev.extend(prev_i)

                    else:
                        break

                k = 1  # Helper
                while len(after) < j + 2 - i_prev_cnt:
                    k += 1
                    if (i + k) < max(df["subgroup"]) + 1:
                        prev_i = [df[df["subgroup"] == (i + k)].iloc[0, -2]] * len(
                            df[df["subgroup"] == (i + k)]
                        )
                        after.extend(prev_i)

                    else:
                        break
                changeTo = prev
                changeTo.extend(after)
                changeTo = mode(changeTo).mode[0]
            else:
                changeTo = mode(prev).mode[0]

            change_idx = df.index[df["subgroup"] == i].tolist()
            df.iloc[change_idx, -2] = changeTo
            df["subgroup"] = (df.iloc[:, -2] != df.iloc[:, -2].shift(1)).cumsum()
            added = (
                df["subgroup"]
                .value_counts()[df["subgroup"].value_counts() < (j + 1)]
                .index.tolist()
            )
            added.sort()
            if i == i_prev:
                i_prev_cnt += 1
            else:
                i_prev_cnt = 0
            i_prev = i
            cnt += 1
            if cnt > max(df["subgroup"]) * (j + 2):
                break

    # Modify the output shape so that for each task we have start frame and end frame
    output_df = pd.DataFrame(columns=["task", "startTime", "endTime"])
    for i in range(max(df["subgroup"])):
        df_i = df[df["subgroup"] == (i + 1)]
        task_str = str(class_names[int(df_i.iloc[0]["task_label"])])
        start_frame = int(min(df_i["frame"]))
        start_frame = frame_to_time(start_frame, video_fps)
        end_frame = int(max(df_i["frame"]))
        end_frame = frame_to_time(end_frame, video_fps)
        output_df = output_df.append(
            pd.DataFrame(
                [[task_str] + [start_frame] + [end_frame]],
                columns=["task", "startTime", "endTime"],
            )
        )

    return output_df

def frame_to_time(frame, video_fps):
    """
    This function converts frame numbers into time strings: '00:00:00.00'
    """
    x = round(frame / video_fps, 2)
    x = pd.to_datetime(x, unit="s").strftime("%H:%M:%S.%f")[:-4]
    return x


if __name__=='__main__':

    input_video_path = 'clean_tray.mp4'
    model_path = './trained_models'
    min_len = 3.05 #lenght in seconds of the smallest blue box (shortest task)

    out_df = predict(input_video_path, model_path, min_len)

    out_df.to_csv("predicted_annotation.csv")


