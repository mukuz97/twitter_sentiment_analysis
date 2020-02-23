import sys
import getopt

from TweetDump import Dumper

def main():
    print('Make sure you have created config.ini before proceeding:')
    print('Choose Task:')
    print('1. Dump Tweets')
    print('2. Clean Tweets')
    opt = int(input('Enter response: '))
    if opt == 1:
        Dumper().start_dump()
    elif opt == 2:
        pass

if __name__ == '__main__':
    main()