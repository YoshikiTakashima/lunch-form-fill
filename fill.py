import json
import logging
import time

from pdfrw import PdfReader, PdfWriter, PdfDict

ERROR_CODE_MAP = {
    'config.json not found!': 1,
    'config.json missing parameters!': 2,
    'Base PDF did not load': 3,
    'config.json malformatted': 4,
    'PDF cannot be saved': 5
    }
BASE_PDF_PATH = 'ER_Form_for_submission.pdf'

def print_red(text):
    print("\033[31m{}\033[0m".format(text))

def print_green(text):
    print("\033[32m{}\033[0m".format(text))

def fail_critical(MESSAGE):
    logging.critical(MESSAGE)
    exit(ERROR_CODE_MAP[MESSAGE])

def load_config():
    try:
        with open('config.json', 'r') as conf:
            try:
                config = json.loads(conf.read());
                return (
                    config['name'],
                    config['email'],
                    config['phone'],
                    config['address'],
                    config['relation2dept'],
                    config['advisors'],
                ) 
            except KeyError as ke:
                logging.critical('Missing param: ' + str(ke))
                fail_critical('config.json missing parameters!')
            except json.decoder.JSONDecodeError:
                fail_critical('config.json malformatted')
    except FileNotFoundError:
        fail_critical('config.json not found!')

def load_pdf():
    try:
        return PdfReader(BASE_PDF_PATH)
    except:
        fail_critical('Base PDF did not load')

def save_pdf(pdf, date_string):
    re_formatted_time = "{}_{}".format(time.strftime('%m-%d-%Y',
                                                     time.strptime(date_string,'%m/%d/%Y')),
                                       BASE_PDF_PATH)
    try:
        PdfWriter(re_formatted_time,
                  trailer=pdf).write()
    except:
        fail_critical('PDF cannot be saved')
    print("Result written to {}".format(re_formatted_time))
    return

def get_date():
    while True:
        try:
            ret = time.strftime('%m/%d/%Y',
                                time.strptime(input('Which day was it? (MM/DD/YYYY): '),
                                              '%m/%d/%Y'))
            return ret
        except ValueError:
            print_red('Not a valid date!')
            continue
        break

def get_item_name():
    return input('Name of item: ')

def get_price():
    while True:
        try:
            price = float(input('Price of this item: $'))
            return "{:.2f}".format(price)
        except ValueError:
            print_red('Not a valid $ amount!')
            continue

def get_row_info():
    ret = []
    print_green('Finish adding items with Ctrl-C')
    for i in range(1,12):
        try:
            print("Item # {} out of 11 ********************".format(i))
            item = get_item_name()
            price = get_price()
            ret.append((item, price))
            print()
        except KeyboardInterrupt:
            print()
            break;
    print("Ending Item Entry. --------------------")
    return ret
            

def write_to_field(field, value):
    field.update(PdfDict(AP=value, V=value))

def main():
    print_red('Please make sure to update config.json!')

    # load PDF
    pdf = load_pdf()
    fields = dict()
    for field in pdf.Root.AcroForm.Fields:
        fields[field['/T']] = field

    # load config
    (name, email, phone, address, relation_to_dept, advisors) = load_config()
    date = get_date();

    # get items and prices, calculate total
    rows = get_row_info()
    total = float(0)
    for row in rows:
        total += float(row[1])
    total = "{:.2f}".format(float(total))
    print_green("Total is: {}".format(total))

    # fill in data
    write_to_field(fields['(Requestor)'],
                   name)
    write_to_field(fields['(Requestor Date Email Phone Number Mailing Address)'],
                   date)
    write_to_field(fields['(Requestor Date Email Phone Number Mailing Address_2)'],
                   email)
    write_to_field(fields['(Phone Number)'],
                   phone)
    write_to_field(fields['(Requestor Date Email Phone Number Mailing Address_3)'],
                   address)
    write_to_field(fields['(Relationship to Department)'],
                   relation_to_dept)
    write_to_field(fields['(If you are a student who is your faculty advisor)'],
                   advisors)
    write_to_field(fields['(ConferenceMeeting Name)'],
                   'Weekly Meeting')
    write_to_field(fields['(ConferenceMeeting Name Business Justification)'],
                   'Students get takeout if meeting is remote.')
    write_to_field(fields['(Business Travel Begin Date)'],
                   date)
    write_to_field(fields['(Business Travel End Date)'],
                   date)
    for i in range(0,len(rows)):
        write_to_field(fields["(Expense DateRow{})".format(i+1)],
                       date)
        write_to_field(fields["(Expense Description  JustificationRow{})".format(i+1)],
                       rows[i][0])
        write_to_field(fields["(AmountRow{})".format(i+1)],
                       "${}".format(rows[i][1]))
    write_to_field(fields['(Total)'],
                   "${}".format(total))
    
    # Save edited PDF
    save_pdf(pdf, date)
    print_red('Please MANUALLY CHECK before submitting.')

if __name__ == '__main__':
    main()
