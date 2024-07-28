#!/usr/bin/env python3

import datetime
import ipinfo
import subprocess
import threading
import time
import queue

# Color codes
RED = '\033[1;31m'
GREEN = '\033[1;32m'
RESET = '\033[0;0m'

# Replace <TOKEN> with IPinfo.io TOKEN
handler = ipinfo.getHandler('<TOKEN>')
# Replace <INPUT FILE PATH> with actual path
input_file = '<INPUT FILE PATH>'
# Replace <OUTPUT FILE PATH> with actual path; in case the file doesn't exist it will be created
output_file = '<OUTPUT FILE PATH>'


def banner():
    print(f''''{GREEN}
                                          (°͜ʖ°)  (●>●)                  _            
                                        oo_\_/_oo__/____ ___ ______   _(•̪●)__ __  ^◠^ 
                                        |       |       |   |    _ | |       |  | 8  8
                                        |    ___|   _   |   |   | || 8_     _8  |_|  |
                                        |   |___|  |_|  |   |   |_||_  |   | |       |
                                        |    ___|       |   |    __  | |   | |       |
                                        |   |   |   _   |   |   |  | | |   | |   _   |
                                        |___|   |__| |__|___|___|  |_| |___| |__| |__|
    {RESET} {RED}                        
                                                     Author: Abhijeet Kumar
                                                  Github: github.com/wand3rlust
    {RESET}''')


def read_ips(file):
    """
    Reads IP addresses from a file, returning them as a list.
    """
    with open(file, 'r') as file:
        return [line.strip() for line in file.readlines()]


def get_details(ip):
    """
    Fetches detailed information for a given IP address using the ipinfo.io API.
    Removes non-required fields from the details before returning.
    """
    try:
        details = handler.getDetails(ip).all
        remove = ['country_flag_url', 'country_flag', 'country_currency', 'isEU']
        for i in remove:
            details.pop(i, None)
        return details
    except Exception as e:
        print(f'Error getting details for IP {ip}: {e}')
        return None


def worker(ip_queue, result_queue):
    """
    Worker function for threads to process IP addresses from the queue.
    Fetches details for each IP and stores the results in another queue.
    """
    while not ip_queue.empty():
        ip = ip_queue.get()
        try:
            details = get_details(ip)
            #print(details)
            result_queue.put((ip, details))
        except Exception as e:
            result_queue.put((ip, None))
            print(f'Error getting details for IP {ip}: {e}')
        finally:
            ip_queue.task_done()


def generate_heatmap(file):
    """
    Takes the list of IPs and generates a heatmap out of them using the IPinfo.io's summarization tool.
    This is implemented using cURL at the moment so this should work on most *NIX OS as it's available by default.
    For Windows users, cURL has to be installed separately from official website.
    """
    
    # Read IPs from the input file
    with open(file, 'r') as file:
        ip_list = file.read().strip()

    # Prepare the curl command
    curl_command = [
        'curl', '-XPOST', '--data-binary', '@-',
        'https://ipinfo.io/tools/summarize-ips?cli=1'
    ]

    # Execute the curl command with the IP list as input
    process = subprocess.Popen(curl_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output, errors = process.communicate(input=ip_list)

    if process.returncode == 0:
        print('Mapping successful. Output:')
        print(output)
        # Save the heatmap link to a file
        current_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f'heatmap_{current_time}.txt'
        with open(filename, 'w') as heatmap_file:
            heatmap_file.write(output)
    else:
        print(f'Error in mapping IPs: {errors}')


def main():
    banner()
    generate_heatmap(input_file)
    ips = read_ips(input_file)
    thread = int(input('Enter the number of threads to use: '))
    threads = []
    ip_queue = queue.Queue()
    result_queue = queue.Queue()

    # Populate the IP queue
    for ip in ips:
        ip_queue.put(ip)

    # Create and start threads
    for i in range(thread):
        t = threading.Thread(target=worker, args=(ip_queue, result_queue))
        t.start()
        threads.append(t)

    # Wait for all tasks in the queue to be processed
    ip_queue.join()

    # Wait for all threads to complete
    for t in threads:
        t.join()

    # Collect and write to file
    while not result_queue.empty():
        ip, details = result_queue.get()
        if details:
            with open(output_file, 'a') as file:
                file.write(str(details) + '\n')


if __name__ == '__main__':
    startTime = time.perf_counter()
    main()
    endTime = time.perf_counter()
    print(f'It took {endTime - startTime :0.2f} second(s) to complete.')
