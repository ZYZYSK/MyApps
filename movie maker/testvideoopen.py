import numpy as np
import cv2


def main():
    mov = cv2.VideoCapture('eclipse.mp4')
    # for i in range(0, 22):
    #     # print(mov.get(i))
    ans = 0
    while mov.isOpened():
        ans += 1
        ret, frame = mov.read()
        # print(ret)
        # print(frame)
        if(ret):
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imshow('eclipse', gray)
        if cv2.waitKey(1) & 0xff == ord('q') or not ret:
            break
    print(ans)
    mov.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
