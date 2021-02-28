import cv2
import sys

import boardcv
import vidio
import game_tree as gt

BOARD_SIZE = 19


def main():
    video_source = sys.argv[1]
    video_cap = vidio.get_video_cap(video_source)

    num_frames = 0  # frame counter
    frame_debug = None
    tracker = boardcv.BoardTracker()
    game_tree = gt.GameTree(BOARD_SIZE)

    while True:
        ret, frame = video_cap.read()

        # # TEMP: Draw straight onto the image before giving it to the tracker
        # corners = tracker.get_corner_estimate()
        # cv2.drawContours(frame, [corners], -1, (255,255,255), 2)

        # # Slam a marker at the board corners
        # for corner in corners:
        #     x,y= corner[0]
        #     x= int(x)
        #     y= int(y)
        #     cv2.rectangle(frame, (x-10,y-10),(x+10,y+10),(0,0,255),-1)

        # if num_frames % 10 == 0:  # TODO: Do this per time rather than frames
        # Detect the board
        frame_debug = tracker.update(frame)

        s = tracker.get_board_state_estimate()
        state_changed, game_node = game_tree.update(s)

        if state_changed:
            print(s)
            print(game_node.difference_from_parent())
            print(game_tree.sgf_game.serialise())

        # result = tracker.draw_piece_debug(result)

        cv2.imshow("Program Output", frame_debug)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        num_frames += 1

    # After the loop release the cap object
    video_cap.release()
    # Destroy all the windows
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
