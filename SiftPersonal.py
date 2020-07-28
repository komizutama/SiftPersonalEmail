import csv
import yaml

trimmed_list = []
discarded_list = []
jp_list = []

def CorrectEmailHeaders(*email_lists):
    for email_list in email_lists:
        for subscriber in email_list:
            subscriber['Email'] = subscriber.pop('\xef\xbb\xbfEmail')


def OutputLists(**email_lists):
    for csv_name, email_list in email_lists.items():
        with open(csv_name + '.csv', mode='w') as csv_file:
            fieldnames = ['Subscribed', 'Clicked', 'Opened', 'Sent', 'Email']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(email_list)


with open('personal_email_domains.yaml') as f:
    personal_email_domains = yaml.load(f, Loader=yaml.FullLoader)

with open('domains2ignore.yaml') as f:
    unwanted_tlds = yaml.load(f, Loader = yaml.FullLoader)

with open('subscriber_list.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        domain_bits = row['\xef\xbb\xbfEmail'].split('@')[1].lower().split('.')

        if domain_bits[-1] == 'jp':
            jp_list.append(row)
        elif set(domain_bits).intersection(set(personal_email_domains)) or domain_bits[-1] in unwanted_tlds:
            discarded_list.append(row)
        else:
            trimmed_list.append(row)


CorrectEmailHeaders(trimmed_list, discarded_list, jp_list)
OutputLists(sorted_email_addresses = trimmed_list, discarded_email_addresses = discarded_list, Japanese_email_addresses = jp_list)
