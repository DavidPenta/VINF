import re
import csv
from difflib import get_close_matches

def create_dict(): # create dictionary of footballers from wiki
    wiki_players = 'output_wiki.tsv' # output of wiki_crawler.py
    file = open(wiki_players, 'r', encoding='utf-8')
    footballers = {} # dictionary of footballers
    for line in file:
        line = line.strip().split('\t')
        if len(line) > 3 and line[1] is not None and line[1] is not None: # if line is not empty
            name = re.sub(r'\{.*\}', "", line[1]) # remove curly brackets
            name = re.sub(r'<.*>', "", name) # remove < >

            birth_place = re.sub(r'\{.*\}', "", line[2]) # remove curly brackets
            birth_place = re.sub(r'<.*>', "", birth_place)  # remove < >
            birth_place = birth_place.replace('[', '').replace(']', '').replace('"', '') # remove [ ] "
            birth_place = birth_place.split('|')[0].strip() # split by | and take first element
            birth_place = birth_place.split('{')[0].strip() # split by { and take first element

            birth_year = line[3] # take birth year to check if it is the same person if there is not exact match
            birth_year = re.search(r".*\|(\d{4})\|.*", birth_year) # take year from |year| format
            if birth_year is not None:
                birth_year = birth_year.group(1)
            footballers[name] = (birth_place, birth_year)
    return footballers


def merge(footballers):  # merge data from wiki and crawler
    input_file_name = 'output_crawler.tsv' # output of crawler.py
    input_file = open(input_file_name, 'r', encoding='utf-8')
    output_file = open('merged_data.tsv', "w", encoding='utf-8') # output file
    writer = csv.writer(output_file, delimiter='\t', lineterminator='\n')
    for line in input_file: # iterate over lines in crawler output
        line = line.strip().split('\t')
        name = line[1]
        if name in footballers:
            line.append(footballers[name][0]) # add birth place
            line.append(None)
            writer.writerow(line)

        else:
            matches = get_close_matches(name, footballers.keys(), n=1, cutoff=0.7) # find similar names
            if len(matches) > 0: # if there is a match
                birth_year = line[9] # take birth year to check if it is the same person if there is not exact match
                birth_year = re.search(r".*(\d{4})", birth_year) # take year from crawler output
                if birth_year is not None:
                    birth_year = birth_year.group(1)
                    if birth_year == footballers[matches[0]][1]: # if birth year is the same
                        line.append(footballers[matches[0]][0]) # add birth place
                        line.append(matches[0]) # add name
                        writer.writerow(line)
    input_file.close()


if __name__ == '__main__':
    footballers = create_dict()
    merge(footballers)
