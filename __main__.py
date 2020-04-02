import sys
import getopt

from TweetDump import Dumper
from Processing import Filter
from CreateCSV import create_csv


def main():
    print('Make sure you have created config.ini before proceeding:')
    print('Choose Task:')
    print('1. Dump Tweets')
    print('2. Filter Tweets')
    print('3. Create all data csv')
    opt = int(input('Enter response: '))
    if opt == 1:
        Dumper().start_dump()
    elif opt == 2:
        Filter().filter_tweets()
    elif opt == 3:
        create_csv()


if __name__ == '__main__':
    main()