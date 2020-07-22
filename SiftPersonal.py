import csv
import yaml

trimmed_list = []

with open('personal_email_domains.yaml') as f:
    personal_email_domains = yaml.load(f, Loader=yaml.FullLoader)

with open('subscriber_list.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        if row['\xef\xbb\xbfEmail'].split('@')[1] not in personal_email_domains:
            trimmed_list.append(row)

for subscriber in trimmed_list:
    print subscriber
    subscriber['Email'] = subscriber.pop('\xef\xbb\xbfEmail')
    print subscriber

with open('trimmed_list.csv', mode='w') as csv_file:
    fieldnames = ['Subscribed', 'Clicked', 'Opened', 'Sent', 'Email']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(trimmed_list)
