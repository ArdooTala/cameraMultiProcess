import threading
import time
import cv2
from CameraCapture import CameraControl


def start_cam():
    rgb_cam = CameraControl(0)
    rgb_cam.roll_camera()

    ir_cam = None
    # ir_cam = CameraControl("http://192.168.0.12:8080/video")
    # ir_cam.roll_camera()

    return rgb_cam, ir_cam


def get_synced_frames(cams):
    responds = []
    print("requesting the cameras".center(100, '='))
    for cam in cams:
        retrieved = threading.Condition()
        responds.append(retrieved)
        print("\tRequesting cam {} - Event > {}".format(cam.cam_id, retrieved))
        cam.req_frame(retrieved)
    print("Waiting for the cameras to respond".center(100, '='))
    for res in responds:
        with res:
            res.wait()
            print("\t> Camera responded: ", res)
    return {cam.cam_id: (cam.ret_result, cam.last_grab, cam.last_frame) for cam in cams}


if __name__ == '__main__':
    rgb, ir = start_cam()
    print("Initialized . . .")
    time.sleep(2)

    while True:
        time.sleep(.05)

        # Returns a dict >> {cam_id: (successful?, Capture_Time, Frame)}
        rslts = get_synced_frames([rgb, ])

        print("results".center(100, '#'))
        for rslt in rslts.items():
            print("\tSuccessful: {}\t\tTimestamp: {}".format(*rslt[1]))
            cv2.imshow(str(rslt[0]), rslt[1][2])
        if cv2.waitKey(1) == ord('q'):
            break

