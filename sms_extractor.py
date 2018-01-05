"""
Script to fetch text messages from iOS backup and write those messages in a
csv file.
"""
import os
import time
import sqlite3
import csv
import datetime


HOME_DIR = os.path.expanduser('~')
BACKUPS_DIR = os.path.join(HOME_DIR, 'Library/Application Support/MobileSync/Backup/')
SMS_BACKUP_PATH = '3d/3d0d7e5fb2ce288813306e4d4636395e047a3d28'


def listdir_nohidden(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f


def main():
    backup_folders = list(listdir_nohidden(BACKUPS_DIR))

    if len(backup_folders) > 1:
        print('You have more than one backup file, select appropriate file')
        for index, folder_name in enumerate(backup_folders):
            stat = os.stat(os.path.join(BACKUPS_DIR, folder_name))
            print('%s: Updated - %s, folder name - %s' % (index, time.ctime(stat.st_mtime), folder_name))

        index = int(input('Select folder index: '))
        # index = 0  # Selecting the latest one by default.
        backup_folder = backup_folders[index]
    else:
        backup_folder = backup_folders[0]

    sms_backup_file = os.path.join(BACKUPS_DIR, backup_folder, SMS_BACKUP_PATH)

    conn = sqlite3.connect(sms_backup_file)
    cursor = conn.cursor()

    messages = cursor.execute('Select rowid, text, service, date, date_read, is_sent from message').fetchall()
    message_dict = {}
    for i in messages:
        if i[2] != 'SMS':
            continue
        if i[5] == 1:
            continue
        message_dict[i[0]] = {
            'text': i[1],
            'date': int((datetime.datetime(2001, 1, 1, 0, 0).timestamp() + i[3] + 21000) * 1000)  # Adding IST i.e. 5:30 minutes seconds into it.
        }

    chats = cursor.execute('Select rowid, chat_identifier from chat')
    chat_dict = {}
    for i in chats:
        chat_dict[i[0]] = i[1]

    chat_messages = cursor.execute('Select chat_id, message_id from chat_message_join').fetchall()
    chat_message_dict = {}
    for i in chat_messages:
        chat_message_dict[i[1]] = i[0]

    csv_file = open('/Users/amitpathak/Dropbox/Projects/Scripts/sms.csv', 'w')
    writer = csv.writer(csv_file)
    writer.writerow(['FROM', 'DATE', 'READABLE_DATE', 'TEXT'])
    for messge_id, msg_dict in message_dict.items():
        writer.writerow([
            chat_dict[chat_message_dict[messge_id]].upper(),
            msg_dict['date'],
            datetime.datetime.fromtimestamp(msg_dict['date'] / 1000.0).strftime('%d/%m/%Y %H:%M:%S'),
            msg_dict['text']
        ])
    csv_file.close()


if __name__ == '__main__':
    main()
