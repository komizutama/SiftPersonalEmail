import csv
import yaml

trimmed_list = []
discarded_list = []
jp_list = []



with open('personal_email_domains.yaml') as f:
    personal_email_domains = set(yaml.load(f, Loader=yaml.FullLoader))
    print personal_email_domains

with open('domains2ignore.yaml') as f:
    unwanted_tlds = yaml.load(f, Loader = yaml.FullLoader)
    print unwanted_tlds

with open('subscriber_list.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        domain_name = row['\xef\xbb\xbfEmail'].split('@')[1]
        lower_domain_name = domain_name.lower()
        tld = lower_domain_name.split('.')

        if tld[-1] == 'jp':
            jp_list.append(row)
            print "added to JP"
        elif set(tld).intersection(personal_email_domains) or tld[-1] in unwanted_tlds:
            discarded_list.append(row)
            print "added to discard"
        else:
            trimmed_list.append(row)
            print "added to main"



for subscriber in trimmed_list:
    subscriber['Email'] = subscriber.pop('\xef\xbb\xbfEmail')

for subscriber in discarded_list:
    subscriber['Email'] = subscriber.pop('\xef\xbb\xbfEmail')

for subscriber in jp_list:
    subscriber['Email'] = subscriber.pop('\xef\xbb\xbfEmail')

with open('trimmed_list.csv', mode='w') as csv_file:
    fieldnames = ['Subscribed', 'Clicked', 'Opened', 'Sent', 'Email']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(trimmed_list)

with open('discard_list.csv', mode='w') as csv_file:
    fieldnames = ['Subscribed', 'Clicked', 'Opened', 'Sent', 'Email']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(discarded_list)

with open('jp_list.csv', mode='w') as csv_file:
    fieldnames = ['Subscribed', 'Clicked', 'Opened', 'Sent', 'Email']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(jp_list)
