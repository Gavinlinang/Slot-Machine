# Slot Machine 
Physical Slot Machine built on Raspberry Pi / Pi-Top

# Features
*Ultrasonic sensor to detect prescense
*Button for user input
*Adjustable bet with potentiometer
*Win Logic: Loss, Small Win (2 matching symbols), Big Win (3 Matching Symvols), Jackpot (Triple 7s)
*Sounds for each result

# State Machine
| State        | Description                                      |
|--------------|--------------------------------------------------|
| `IDLE`       | Waiting for someone to approach                  |
| `WELCOME`    | Player detected                                  |
| `SHOW_BALANCE` | Displays the player’s current balance         |
| `SET_BET`    | Player adjusts bet using potentiometer           |
| `CONFIRM_BET`| Bet is locked in            |
| `SPIN`       | Slot reels spin and sound plays                  |
| `RESULT`     | Shows result and win/loss before resetting to Idle       |

MIT License

Copyright (c) 2026 Jeffrey Huang and Gavin Linang

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
