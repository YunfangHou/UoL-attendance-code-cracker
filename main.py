# Coded by Steve on 2022.03.28

import json
import threading
import requests
import re
import time
import traceback


class myThread(threading.Thread):
    def __init__(self, database_address, url, authorization):
        threading.Thread.__init__(self)
        self.database_address = database_address
        self.url = url
        self.authorization = authorization

    def run(self):
        simulate(database_address=self.database_address, url=self.url, authorization=self.authorization)


def simulate(database_address, url, authorization):
    header = {
        'content-type': 'application/json',
        'authorization': authorization,
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36',
    }

    word_length = 0
    with open(database_address) as database:
        word_length = len(database.readline())

    database = open(database_address)
    database_size = sum_count(database_address)

    flag = 0
    counter = 0
    while flag == 0 and counter < database_size:
        try:
            counter += 1
            print(str(counter) + '/' + str(database_size) + ' for ' + database_address)
            access_code = database.readline()
            access_code = access_code.strip('\n')
            print('tested word : ' + access_code)
            payload = {
                "accessCode": access_code,
            }
            session = requests.session()
            r = requests.post(url, data=json.dumps(payload), headers=header)
            # print(r.text)

            match_obj = re.match('(.*)accepted_student_access_code":(.*)(,"attempt")(.*)', r.text)
            print('match result: ' + match_obj.group(2))
            if match_obj.group(2) != 'false':
                time.sleep(1)
            if match_obj.group(2) != 'false':
                flag = 1
                print(
                    '\n***********************\n Access code found! \n Access code might be: ' + access_code + '\n***********************')
                return access_code
        except Exception as e:
            traceback.print_exc()
            break
    return ''


# Multi threads using threading. Fast but multiple result will got and need to be tested one by one
def multi_threads_version(url, authorization):
    three_thread = myThread('three_letter.txt', url, authorization)
    four_thread = myThread('four_letter.txt', url, authorization)
    five_thread = myThread('five_letter.txt', url, authorization)
    wordle_thread = myThread('wordle_database.txt', url, authorization)
    six_thread = myThread('six_letter.txt', url, authorization)

    three_thread.start()
    four_thread.start()
    five_thread.start()
    wordle_thread.start()
    six_thread.start()

    three_thread.join()
    four_thread.join()
    five_thread.join()
    wordle_thread.join()
    six_thread.join()
    print("Exit main thread")


# Single thread version. Slow but precise and brife as only one result will got.
def single_thread_version(url, authorization):
    if simulate('four_letter.txt', url, authorization) == '':
        if simulate('five_letter.txt', url, authorization) == '':
            if simulate('wordle_database.txt', url, authorization) == '':
                if simulate('three_database.txt', url, authorization) == '':
                    simulate('six_database.txt', url, authorization)


def sum_count(file_name):
    return sum(1 for _ in open(file_name))


def main():
    start_time = time.perf_counter()

    url = input('Input the submission URL: ')
    authorization = input('Input the authorization: ')

    print('Use multiple thread or single thread?')
    choice = int(input('Input 1 for multiple thread or 2 for single thread: '))

    if choice == 1:
        multi_threads_version(url, authorization)
    if choice == 2:
        single_thread_version(url, authorization)

    end_time = time.perf_counter()
    duration = end_time - start_time
    print('Finish. Spend ' + str(int(duration)) + ' seconds')


if __name__ == '__main__':
    main()
