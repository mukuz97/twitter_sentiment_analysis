import sys
import getopt

from TweetDump import Dumper
from Processing import Filter


def main():
    print('Make sure you have created config.ini before proceeding:')
    print('Choose Task:')
    print('1. Dump Tweets')
    print('2. Filter Tweets')
    opt = int(input('Enter response: '))
    if opt == 1:
        Dumper().start_dump()
    elif opt == 2:
        Filter().filter_tweets()


if __name__ == '__main__':
    main()