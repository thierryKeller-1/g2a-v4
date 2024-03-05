import argparse
import datetime
import subprocess
import platform
import time
import sys
import os
import shlex
import keyboard
from datetime import timedelta
from colorama import just_fix_windows_console, Fore
from toolkits.logger import show_message
from toolkits.constants import CONNEXION_ID


DESCATIVATE_COMMAND = f"sudo nmcli conn down {CONNEXION_ID}"
ACTIVATION_COMMAND = f"sudo nmcli conn up {CONNEXION_ID}"

if platform.system().lower() == 'windows':
    just_fix_windows_console()

class IP_Timer(object):

    def __init__(self, countdown:int=5, time_type:str='min') -> None:
        self.countdown = countdown
        self.time_type = time_type
        self.time_types = ['s', 'm', 'h']
        self.countdown_time = 0

    def params_is_valide(self) -> bool:
        if self.time_type not in self.time_types:
            return False
        if self.countdown < 0:
            return False
        return True
    
    def get_time_type(self) -> str:
        if self.params_is_valide():
            return self.time_type

    def normalize_time(self) -> None:
        if self.params_is_valide():
            match(self.time_type):
                case 's':
                    self.countdown_time = self.countdown
                case 'm':
                    self.countdown_time =  timedelta(minutes=self.countdown).total_seconds()
                case 'h':
                    self.countdown_time = timedelta(hours=self.countdown).total_seconds()
        else:
            show_message('time type error', f"time type should be one of {self.time_types} \n and countdown must be positive integer", 'error')
            time.sleep(2)
            sys.exit()

    def show_time(self, timerest:int) -> None:
        color = Fore.RED if timerest <= 60 else Fore.GREEN
        print(Fore.GREEN + " $ time left before IP will be changed " + color + time.strftime("%H:%M:%S", time.gmtime(timedelta(seconds=timerest).total_seconds())), end='\r')
        self.time_rest -= 1
        time.sleep(1)

    def reset_time(self) -> None:
        self.time_rest = self.countdown_time

    def launch_command(self) -> None:
        global DESCATIVATE_COMMAND
        global ACTIVATION_COMMAND
        if platform.system().lower() == 'windows':
            print("\n\t It's time to change IP, please do It then press enter")
        else:
            print('\n\t desctivation ... ')
            print("\t " + DESCATIVATE_COMMAND)
            try:
                subprocess.run(shlex.split(DESCATIVATE_COMMAND), check=True)
            except supprocess.CalledProcessError as e:
                print(f"\t ===> error {e}")
            print('\t activation ... ')
            print("\t " + ACTIVATION_COMMAND)
            time.sleep(.5)
            try:
                subprocess.run(shlex.split(ACTIVATION_COMMAND), check=True)
            except supprocess.CalledProcessError as e:
                print(f"\t ===> error {e}")

    def run(self) -> None:
        print(" $ starting ... ")
        time.sleep(1)
        self.normalize_time()
        try: 
            while True:
                self.reset_time()
                while self.time_rest >= 0:
                    self.show_time(self.time_rest)
                self.launch_command()
        except KeyboardInterrupt:
            print('\t stopping ...')


def main_arguments() -> object:
    parser = argparse.ArgumentParser(description="IP manager program", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--action', '-a', dest='action', default='',help="")
    parser.add_argument('--duration', '-d', dest='duration', default='5', help="time cycle duration for each new IP")
    parser.add_argument('--unit', '-u', dest='unit', default='s', help="unit of time [s for second m for minute and h for hour]")
    return parser.parse_args()


ARGS_INFO = {
        '-a': {'long': '--action', 'dest': 'action', 'help': "action to be performed"},
        '-d': {'long': '--duration', 'dest': 'duration', "help": "time cycle duration for each IP"},
        '-u': {'long': '--unit', 'dest': 'unit', "help": "time unit [s for second m for minute and h for hour]"},
    }

def check_arguments(args, required):
    miss = []

    for item in required:
        if not getattr(args, ARGS_INFO[item]['dest']):
            miss.append(f'{item} ou {ARGS_INFO[item]["long"]} ({ARGS_INFO[item]["help"]})')

    return miss

if __name__ == '__main__':
    args = main_arguments()

    if args.action and args.action == 'start':
        miss_command = check_arguments(args, ['-a', '-d', '-u'])
        if len(miss_command):
            raise Exception(f"Argument(s) manquant(s): {', '.join(miss_command)}")
        else:
            ip_manager = IP_Timer(
                countdown=int(args.duration),
                time_type=args.unit
            )
            ip_manager.run()
