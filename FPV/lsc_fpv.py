import djitellopy as tello
import cv2


def process_tello_video(conn: tello.Tello):
    while True:
        frame = conn.get_frame_read().frame
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
    conn.end()


def main():
    drone = tello.Tello()
    drone.connect()
    drone.streamon()
    process_tello_video(drone)


if __name__ == "__main__":
    main()
