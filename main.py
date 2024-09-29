import requests
from bs4 import BeautifulSoup as BS
import fake_useragent
import csv
import logging
from logging import FileHandler, Formatter

'''HTML Coingecko parser on BS4 + Requests'''

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = FileHandler(filename='logs.txt')
handler.setFormatter(Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
logger.addHandler(handler)

logger.info("Starting application.")

msg = ''
exception_msg = ''

def export_csv(file_path, parsed_table):
    result = ''
    try:
        with open(file_path, 'w') as f:
            writer = csv.writer(f)
            for row in parsed_table:
                writer.writerow(row)
        result = "Successfuly export to csv: ./path-to-project/parse.csv."
    except:
        exception_msg = "Error while export to csv: check log details."
        logger.exception(exception_msg)
        raise Exception(exception_msg)
    return result

def show_table(parsed_table):
    try:
        for row in parsed_table:
            print(row)
        result = "Successfuly printed in console."
    except:
        exception_msg = "Error while print to console: check log details."
        logger.exception(exception_msg)
        raise Exception(exception_msg)
    return result

def main():
    logger.debug("Entering to main().")

    print("Starting HTML Coingecko parser.")

    url = 'https://www.coingecko.com/ru'
    user_agent = fake_useragent.UserAgent().random
    headers = {
        'user-agent': user_agent
    }

    msg = f"\nCurrent useragent: {user_agent}."
    print(msg)
    logger.debug(msg)

    # Send GET request.
    request = requests.get(url, headers=headers)
    html = BS(request.content, 'html.parser')
    
    msg = "Send GET request."
    print(msg) 
    logger.debug(msg)

    # Parse table head.
    try:
        coingecko_table = list()
        t_head = html.select('thead th.tw-py-3.tw-px-1.tw-font-semibold.tw-text-xs.tw-text-gray-900.tw-whitespace-nowrap.tw-text-left.tw-bg-white')
        t_head_list = list()
        for row in t_head[2:11]:
            if row.text.strip() == '':
                continue
            else:
                t_head_list.append(row.text.strip())

        coingecko_table.append(t_head_list)
        
        msg = "Parse table head."
        print(msg) 
        logger.debug(msg)
    except:
        exception_msg = "Error while parse table head: check log details."
        logger.exception(exception_msg)
        raise Exception(exception_msg)

    # Parse table rows.
    try:
        t_rows = html.select('tbody tr')
        for row in t_rows:
            t_ds = row.select('.tw-px-1.tw-bg-inherit.tw-text-gray-900')
            t_rows_list = list()
            for td in t_ds[2:11]:
                if td.text.strip() == '' or td.text.strip() == 'Купить':
                    continue
                else:
                    new_text = ''
                    t_text = td.text.strip()
                    for c in range(0, len(t_text)):
                        if t_text[c] == '' or t_text[c] == '\n' or (t_text[c] == ' ' and t_text[c+1] == ' '):
                            continue
                        else:
                            new_text += t_text[c]

                    new_text = new_text.strip()
                    t_rows_list.append(new_text + '\t')

            coingecko_table.append(t_rows_list)

        msg = "Parse table rows."
        print(msg) 
        logger.debug(msg)
    except:
        exception_msg = "Error while parse table rows: check log details."
        logger.exception(exception_msg)
        raise Exception(exception_msg)

    print("\n\nWhere do you want to show parsed table?")
    print("1. Show parsed table in console.")
    print("2. Export parsed table in csv format.")

    choice = input("Enter 1 or 2: ")
    match choice:
        case '1':
            # Show parsing in console.
            msg = "Show parsing in console."
            print(msg) 
            logger.debug(msg)

            print("\n\n")
            msg = show_table(coingecko_table)
            # print(msg)
            logger.info(msg)

        case '2': 
            # Save parsing to .csv.
            msg = "Save parsing to .csv."
            print("\n\n" + msg) 
            logger.debug(msg)

            path = './parse.csv'
            msg = export_csv(path, coingecko_table)
            print(msg)
            logger.info(msg)

        case _:
            msg = "Input choice is not correct!"
            print(msg)
            logger.warning(msg[0:-1] + f" ({choice}).")
    

if __name__ == '__main__':
    main()