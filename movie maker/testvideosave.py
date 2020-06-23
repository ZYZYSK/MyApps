import numpy as np
import cv2


def main():
    mov = cv2.VideoCapture('eclipse.mp4')
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    out = cv2.VideoWriter('output.avi', fourcc,
                          int(mov.get(5)), (int(mov.get(3)), int(mov.get(4))))
    ans = 0
    while mov.isOpened():
        ans += 1
        ret, frame = mov.read()
        if (ret):
            # frame = cv2.flip(frame, 0)  # 映像を縦方向に反転する
            out.write(frame)
            cv2.imshow('eclipse', frame)
        if cv2.waitKey(1) & 0xff == ord('q') or not ret:
            break
    print(ans)
    mov.release()
    out.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
