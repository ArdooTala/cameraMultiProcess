import datetime
import threading
import cv2


class CameraControl:
    def __init__(self, cam=0):
        self.cam_id = cam

        self.cap = cv2.VideoCapture(cam)
        assert self.cap.isOpened()
        self.roll = False

        self.last_grab = None
        self.ret_result = None
        self.last_frame = None

        self.thread = threading.Thread(target=self.capture)
        self.thread.daemon = True

        self.retrieve_req = False
        self.retrieve_note = None

    def set_props(self):
        pass
        # self.cap.set()

    def roll_camera(self):
        self.roll = True
        self.thread.start()

    def capture(self):
        while self.roll:
            ret = self.cap.grab()
            if ret:
                self.last_grab = datetime.datetime.now()
                print("\t\t\t\tgrab > {1} > {0}".format(self.cam_id, self.last_grab))

            if self.retrieve_req:
                self.retrieve_frame()

    def retrieve_frame(self):
        with self.retrieve_note:
            self.ret_result, self.last_frame = self.cap.retrieve()
            self.retrieve_req = False
            self.retrieve_note.notify()

    def req_frame(self, retrieved):
        self.retrieve_req = True
        self.retrieve_note = retrieved

    def __delete__(self, instance):
        self.roll = False
