from pitop import Pitop, Button, LED, UltrasonicSensor, Potentiometer
from time import sleep, monotonic
import random
import pygame

# hardware setup
pitop = Pitop()
screen = pitop.miniscreen

dist_sensor = UltrasonicSensor("D5")
pot = Potentiometer("A0")
btn1 = Button("D4")

led_red = LED("D0")
led_green = LED("D1")
led_yellow = LED("D2")

# audio setup
pygame.mixer.init()

spin_sound = pygame.mixer.Sound("spin.wav")
win_sound = pygame.mixer.Sound("win.wav")
lose_sound = pygame.mixer.Sound("lose.wav")
jackpot_sound = pygame.mixer.Sound("jackpot.wav")

# variables
bal = 10000
bet = 5000

DIST_THRESHOLD = 10
OUT_OF_RANGE_TIMEOUT = 60

SYMBOLS = ["@", "$", "*", "!", "7"]

def rounder(x, base=50):
    return base * round(x / base)

def wait_for_release(button):
    while button.is_pressed:
        sleep(0.01)

# states
IDLE = "IDLE"
WELCOME = "WELCOME"
SHOW_BALANCE = "SHOW_BALANCE"
SET_BET = "SET_BET"
CONFIRM_BET = "CONFIRM_BET"
SPIN = "SPIN"
RESULT = "RESULT"

state = IDLE
out_of_range_start = None

reels = ["?", "?", "?"]
spin_start = None
spin_duration = 2.0
result_hold_time = 3.0
result_start = None
win_amount = 0
result_text = ""

screen.display_text("idle")

# win logic
def evaluate_reels(reels, bet):
    if reels == ["7", "7", "7"]:
        return bet * 10, "jackpot!", "jackpot"

    if reels[0] == reels[1] == reels[2]:
        return bet * 5, "big win!", "win"

    if reels[0] == reels[1] or reels[1] == reels[2]:
        return bet * 2, "small win", "win"

    return 0, "you lose", "lose"

# main loop
    global win_amount, result_text
while not screen.cancel_button.is_pressed:

    dist = dist_sensor.distance
    now = monotonic()

    # out of range timeout
    if dist > DIST_THRESHOLD:
        if out_of_range_start is None:
            out_of_range_start = now
        elif now - out_of_range_start >= OUT_OF_RANGE_TIMEOUT:
            state = IDLE
    else:
        out_of_range_start = None

    if state == IDLE:
        led_green.off()
        led_red.off()
        led_yellow.off()
        screen.display_text("idle")

        if dist <= DIST_THRESHOLD:
            state = WELCOME
            sleep(0.3)

    elif state == WELCOME:
        led_green.on()
        screen.display_text("welcome!\npress button")

        if btn1.is_pressed:
            wait_for_release(btn1)
            state = SHOW_BALANCE

    elif state == SHOW_BALANCE:
        screen.display_text(f"balance:\n${bal}")

        if btn1.is_pressed:
            wait_for_release(btn1)
            state = SET_BET

    elif state == SET_BET:
        pot_val = pot.position if pot.position is not None else 0
        bet = rounder((pot_val * 4.8) + 200)
        if bet > bal:
            bet = bal

        # prevent betting if no money left
        if bal <= 0:
            screen.display_text("no money!\ngame over")
            sleep(2)
            state = IDLE
            bal = 10000  # reset balance
        else:
            screen.display_text(f"set bet:\n${bet}")

            if btn1.is_pressed:
                wait_for_release(btn1)
                state = CONFIRM_BET

    elif state == CONFIRM_BET:
        bal -= bet
        screen.display_text("spinning...")
        spin_start = now
        spin_sound.play()
        state = SPIN

    elif state == SPIN:
        if now - spin_start >= spin_duration:
            reels = [random.choice(SYMBOLS) for _ in range(3)]
            win_amount, result_text, sound_type = evaluate_reels(reels, bet)
            if win_amount > 0:
                bal += win_amount
            spin_sound.stop()
            # play result sound
            if sound_type == "jackpot":
                jackpot_sound.play()
            elif sound_type == "win":
                win_sound.play()
            else:
                lose_sound.play()
            result_start = now
            state = RESULT

    elif state == RESULT:
        # set led based on result
        if win_amount > 0:
            led_green.on()
            led_red.off()
            led_yellow.off()
        else:
            led_green.off()
            led_red.on()
            led_yellow.off()

        screen.display_text(
            f"{reels[0]}  {reels[1]}  {reels[2]}" +
            "\n" +
            f"{result_text}" +
            (f"\n+${win_amount}" if win_amount > 0 else "")
        )
        if now - result_start >= result_hold_time:
            state = WELCOME

    sleep(0.02)
