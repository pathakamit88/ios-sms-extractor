"""
Script to write sms extracted by sms.py script to xml so that it can be read
by SmsBackupRestor app in android.
This way we can sync iOS SMS to Android phone.
"""
import csv
import xml.etree.ElementTree as ET


def main():

  tree = ET.parse('/Users/amitpathak/Dropbox/Apps/SMSBackupRestore/sms.xml')
  root = tree.getroot()
  sms_count = int(root.attrib['count'])

  csv_file = open('/Users/amitpathak/Dropbox/Projects/Scripts/sms.csv')
  reader = csv.reader(csv_file)

  for index, line in enumerate(reader):
    if index == 0:  # 0 is header which is FROM, DATE (in epoch), READABLE_DATE and TEXT
      continue
    date = str(line[1])
    address = line[0]
    body = line[3]
    
    sms_exists = [sms for sms in root if sms.attrib['date'] == date and sms.attrib['address'] == address and sms.attrib['body'] == body]
    if sms_exists:
      continue

    ele = ET.Element('sms', {
        'protocol': '0',
        'date_sent': date,
        'subject': 'null',
        'date': date,
        'service_center': '+919830000187',
        'toa': 'null',
        'locked': '0',
        'status': '-1',
        'readable_date': line[2],
        'read': '1',
        'contact_name': '(Unknown)',
        'sc_toa': 'null',
        'body': body,
        'address': address,
        'type': '1'
    })
    root.append(ele)
    sms_count += 1

  root.attrib['count'] = str(sms_count)
  tree.write('/Users/amitpathak/Dropbox/Apps/SMSBackupRestore/sms.xml')


if __name__ == '__main__':
    main()
