import cv2

class VideoManager:

    def __init__(self):
        '''Initialize video manager elements'''
        self.capture = None
        self.video_path = None
        self.frame_count = 0
        self.current_frame = 0
        self.fps = 30.0
        self.width = 0
        self.height = 0
        self.duration = 0.0

    def open(self, video_path):
        '''Open video'''
        self.release()
        self.video_path = video_path
        self.capture = cv2.VideoCapture(video_path)

        if not self.capture.isOpened():
            self.capture = None
            return False

        self.frame_count = int(
            self.capture.get(cv2.CAP_PROP_FRAME_COUNT)
        )

        self.fps = self.capture.get(cv2.CAP_PROP_FPS)

        if self.fps <= 0:
            self.fps = 30.0

        self.width = int(
            self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        )

        self.height = int(
            self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        )

        self.duration = (
            self.frame_count / self.fps
        )

        self.current_frame = 0
        return True

    def read(self):
        '''Read frame'''
        if self.capture is None:
            return False, None

        success, frame = self.capture.read()
        if success:
            self.current_frame = int(
                self.capture.get(cv2.CAP_PROP_POS_FRAMES)
            )
        return success, frame

    def seek_frame(self, frame_number):
        '''See to frame'''
        if self.capture is None:
            return False

        frame_number = max(
            0, min(frame_number, self.frame_count - 1)
        )

        self.capture.set(
            cv2.CAP_PROP_POS_FRAMES,
            frame_number
        )

        self.current_frame = frame_number
        success, frame = self.capture.read()
        if success:
            self.current_frame = frame_number + 1

        return success, frame

    def seek_time(self, seconds):
        '''Seek to time'''
        frame_number = int(seconds * self.fps)
        return self.seek_frame(
            frame_number
        )

    def next_frame(self):
        '''Return next frame'''
        return self.seek_frame(
            self.current_frame
        )

    def previous_frame(self):
        '''Return previous frame'''
        return self.seek_frame(
            max(0, self.current_frame - 2)
        )

    def get_current_time(self):
        '''Get current time'''
        if self.fps <= 0:
            return 0.0
        return self.current_frame / self.fps

    def release(self):
        if self.capture is not None:
            self.capture.release()
        self.capture = None