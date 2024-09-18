import curses
import pygame
import sys
from time import sleep


def main(stdscr, audio_file):
    # Initialize pygame mixer
    pygame.mixer.init()
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()

    # Setup curses
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)

    # Get audio length
    sound = pygame.mixer.Sound(audio_file)
    total_length = sound.get_length()

    paused = False

    while True:
        # Clear screen
        stdscr.clear()

        # Handle key presses
        key = stdscr.getch()
        if key == ord(" "):  # Spacebar
            if paused:
                pygame.mixer.music.unpause()
                paused = False
            else:
                pygame.mixer.music.pause()
                paused = True
        elif key == curses.KEY_LEFT:
            pygame.mixer.music.set_pos(max(0, pygame.mixer.music.get_pos() / 1000 - 5))
        elif key == curses.KEY_RIGHT:
            pygame.mixer.music.set_pos(
                min(total_length, pygame.mixer.music.get_pos() / 1000 + 5)
            )
        elif key == curses.KEY_UP:
            pygame.mixer.music.set_pos(max(0, pygame.mixer.music.get_pos() / 1000 - 30))
        elif key == curses.KEY_DOWN:
            pygame.mixer.music.set_pos(
                min(total_length, pygame.mixer.music.get_pos() / 1000 + 30)
            )
        elif key == ord("q"):
            break

        # Update status bar
        current_time = pygame.mixer.music.get_pos() / 1000
        status = f"Time: {current_time:.2f} / {total_length:.2f} seconds"
        stdscr.addstr(curses.LINES - 1, 0, status)

        stdscr.refresh()
        sleep(0.1)

    # Cleanup
    pygame.mixer.quit()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <audio_file>")
        sys.exit(1)

    audio_file = sys.argv[1]
    curses.wrapper(lambda stdscr: main(stdscr, audio_file))
