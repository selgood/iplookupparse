### Weblog Parser by Scott Elgood ###
### 2020-02-16 ###
### Designed for the AWStats output but may work for others ### 
import re
import os
from os import path
import sys
import geoip2.database


def iplookup(foundip):
    if os.path.exists(r".\outputip.txt"):
        print('[-INF-]DIR Exists, remaking...')
        os.remove(r".\outputip.txt")
    else:
        pass

    reader = geoip2.database.Reader(r'C:\Users\%USER%\AppData\Local\Programs\Python\Python37-32\geo.mmdb')
    for eachip in foundip:
        stripip = str(eachip).strip('[]') # Stripping the extra bits off
        stripip2 = str(stripip).strip('\'\'')
        rec = reader.city(stripip2)
        info = (f'[-ALERT-] Collecting Data on {stripip2}. . .')
        state = (f'State/Province: {rec.subdivisions.most_specific.name}') # Returns overall (Fife)
        town = (f'Town: {rec.city.name}') # Returns Close prox (Leven)
        lon = (f'Longitude: {rec.location.longitude}') # Longitutde
        lat = (f'Latitude: {rec.location.latitude}') # Latitude
        post = (f'Postal Code: {rec.postal.code}') # first bit of postcode
        net = (f'Network: {rec.traits.network}') # network traits
        border =('----- ----- ----- -----')
        concat = (f'{info} \n {state} \n {town} \n {lon} \n {lat} \n {post} \n {net} \n {border} \n')
        outfile = open(r'.\outputip.txt', 'a')
        outfile.write(concat)
    outfile.close()


def ipextract(filepath):
    foundip = []
    print(f'[-INF-]Extracting IP from {filepath}')
    with open(filepath, 'r') as stream:
        for line in stream:
            match = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', line) # regex from https://www.oreilly.com/library/view/regular-expressions-cookbook/9780596802837/ch07s16.html
            if match:
                if match not in foundip:
                    foundip.append(match)
                else:
                    pass
    stream.close()
    iplookup(foundip)


def main():
    '''Run Main Script'''
    # --- # Grabbing Args # --- #
    if len(sys.argv) <= 1:
        print('Usage: weblogparse.py FilePath ... ')
        sys.exit(1)
    else:
        for newarg in sys.argv[1:2]:
            filepath = newarg
    pathtest = path.exists(filepath)
    # --- # Checkng to see if filepath exists # --- #
    if pathtest is True:
        print(f'[-INF-] Found {filepath} - parse?')
        userc = input('[-ALERT-]Y/N: \n').lower()
        try:
            if userc =='y':
                print('Parsing...')
                filepath = os.path.abspath(filepath)
                foundips = ipextract(filepath)
            else:
                print('Aborting...')
                exit()
        except FileNotFoundError as err:
            print(f'geo.mmdb not present in Python Directory, please download a database to use! \n[-ALERT-]{err}')
    else:
        print(f'Error! File {filepath} is not a valid filepath or file - did you type it correctly?')



if __name__ == '__main__':
    main()
