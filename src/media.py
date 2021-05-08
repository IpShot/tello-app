import time, cv2
from threading import Thread

class Media:
    """
    Module for taking photo and recording video
    """
    def __init__(self, drone):
        self.frame_read = drone.get_frame_read()
        self.is_recording = False
        self.recorder = Thread(target=self._record_video)

    def _record_video(self):
        height, width, _ = self.frame_read.frame.shape
        video = cv2.VideoWriter(f'video_{time()}.avi', cv2.VideoWriter_fourcc(*'XVID'), 30, (width, height))

        while self.is_recording:
            video.write(self.frame_read.frame)
            time.sleep(1 / 30)

        video.release()

    def start_video_recording(self):
        self.is_recording = True
        if self.frame_read:
            cv2.imshow('Drone X', self.frame_read.frame)
            self.recorder.start()

        print('Video recording has started')

    def stop_video_recording(self):
        if self.is_recording:
            self.is_recording = False
            if self.frame_read:
                self.recorder.join()
                cv2.destroyAllWindows()

            print('Video recording has stopped')
