import RPi.GPIO as GPIO
import time
import os
import sys
import signal
import subprocess
import threading

# GPIOのピン番号を指定
SWITCH = 18

# GPIOの初期化
GPIO.setmode(GPIO.BCM)
GPIO.setup(SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# プロセスの実行
def execute_process():
    os.system("echo test") # //TODO: 後で決める

# プロセスのKill
def kill_process():
    os.system("pkill -f python3")

# スイッチの状態の確認
def check_switch():
    global flag
    while True:
        if GPIO.input(SWITCH) == 0:
            flag = 0
            return
        time.sleep(0.1)

# メイン関数
def main():
    global flag
    flag = 0
    print("Start")
    while True:
        if flag == 0:
            if GPIO.input(SWITCH) == 0:
                flag = 1
                t1 = threading.Thread(target=check_switch)
                t1.start()
                time.sleep(2)
                if flag == 0:
                    execute_process()
                else:
                    kill_process()
                t1.join()
                flag = 1
        time.sleep(0.1)

# プログラムの終了処理
def signal_handler(signal, frame):
    GPIO.cleanup()
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    main()

