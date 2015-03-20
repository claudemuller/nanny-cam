#!/usr/bin/env python

# @TODO - default write dir home dir Downloads?
#       - command line arguments
#       - documentation

import numpy as np
import cv2
import time

class NannyCam:
    LOG_TOKEN = '-> '
    INPUT_DEVICE_WIDTH = 3
    INPUT_DEVICE_HEIGHT = 4

    def __init__(self, inputId = 0, codec = 'XVID', fps = 15, showOutput = True, outputDir = '.'):
        self.showOutput = showOutput
        self.inputDevice = cv2.VideoCapture(inputId)
        if self.inputDevice.isOpened():
            self._log('Input device was initialised.')

            try:
                fourcc = cv2.VideoWriter_fourcc(*codec)
            except AttributeError:
                fourcc = cv2.cv.CV_FOURCC(*codec)

            if fourcc:
                self._log('Codec initialised.')

                outputFilename = outputDir + '/vid-' + time.strftime('%d%m%y.%H%M') + '.avi'
                self.outputDevice = cv2.VideoWriter(
                        outputFilename,
                        fourcc,
                        fps,
                        (int(self.inputDevice.get(self.INPUT_DEVICE_WIDTH)), int(self.inputDevice.get(self.INPUT_DEVICE_HEIGHT)))
                )

                if self.outputDevice.isOpened():
                    self._log('Output device was initialised. Writing to ' + outputFilename)

                    self._capture()
                else:
                    self._log('Error initialising output device!')
                    self._cleanUp(1)
            else:
                self._log('Error initialising codec!')
                self._cleanUp(1)
        else:
            self._log('Error initialising input device!')
            self._cleanUp(1)

        self._cleanUp()

    def _capture(self):
        while self.inputDevice.isOpened():
            ret, frame = self.inputDevice.read()

            if ret == True:
                self._log('Frame read...')

                self.outputDevice.write(frame)
                self._log('...and written.')

                if self.showOutput:
                    cv2.imshow('frame', frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break

    def _log(self, message):
        print(self.LOG_TOKEN + message)

    def _cleanUp(self, exitCode = 0):
        self._log('Cleaning up.')

        try:
            self.inputDevice.release()
        except (AttributeError, NameError):
            pass

        try:
            self.outputDevice.release()
        except (AttributeError, NameError):
            pass

        cv2.destroyAllWindows()
        exit(exitCode)

if __name__ == "__main__":
    nc = NannyCam(2)
