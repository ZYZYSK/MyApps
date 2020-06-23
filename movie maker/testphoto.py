import numpy as np
import cv2
from matplotlib import pyplot as plt


def main():
    img = cv2.imread('1.png', 0)
    cv2.imshow('img1', img)
    k = cv2.waitKey(0) & 0xff
    if k != 27:
        cv2.imwrite('3.png', img)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
