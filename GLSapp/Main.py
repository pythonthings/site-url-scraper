"""
Created on 23/01/2015

@author: dave
"""

import csv
import getopt
import os.path
import sys

from GLSapp.ReferenceScraper import ReferenceScraper
from GLSapp.LinkScraper import LinkScraper


# Application handling class
class MainApp:

    def __init__(self):
        self.scraper = None
        self.mode = None

        self.urls = list()

        self.fileUpdated = False

    # Main application entry point
    def main(self):

        # Extract args
        try:
            opts, args = getopt.getopt(
                sys.argv[1:],
                "hf:u:p:l",
                ["help", "file=", "url=", "pattern=", "links"]
            )
        except getopt.GetoptError as err:
            # print help information and exit:
            print(err)  # will print something like "option -a not recognized"
            self.usage()
            sys.exit(2)

        # Process args
        pattern_mode_option = link_mode_option = False
        for o, a in opts:
            if o in ("-h", "--help"):
                self.usage()
                sys.exit()

            if o in ("-p", "--pattern"):
                pattern_mode_option = True
                self.scraper = ReferenceScraper(
                    callback=self.write_csv, pattern=str(a))

            elif o in ("-l", "--links"):
                link_mode_option = True
                self.scraper = LinkScraper(callback=self.write_csv)

            elif o in ("-f", "--file"):
                _urlList = self.read_file(a)
                if len(_urlList) > 0:
                    self.urls += _urlList

            elif o in ("-u", "--url"):
                self.urls.append(a)

        # Checks
        if not pattern_mode_option and not link_mode_option:
            print("Please select either link or pattern mode")
            self.usage()
            sys.exit()

        if pattern_mode_option and link_mode_option:
            print("Cannot run both link and pattern modes")
            self.usage()
            sys.exit()

        # Run
        self.scraper.add_page_list(self.urls)
        self.scraper.run()

    # Display help message
    def usage(self):
        print("Options:")
        print("help: -h, --help")
        print("file: -f, --file")
        print("single url: -u, --url")
        print("search pattern: -p, --pattern")
        print("crawl links: -l, --links")
        pass

    # Read list from CSV file
    def read_file(self, _filename):

        if os.path.isfile(_filename):
            csv_list = []
            with open(_filename, 'r') as f:
                reader = csv.reader(f)
                for line in reader:
                    if "http" in line[0]:
                        csv_list.append(line[0])

            return csv_list

        else:
            print("File: " + _filename + " not found")

        return False

    # Write output into file
    def write_csv(self, _results):
        if not self.fileUpdated:
            self.fileUpdated = True

            fh = open("Results.txt", "w")
            fh.write('\n'.join(sorted(_results)) + '\n')
            fh.close()

            print("Result written!")

# Run application from self
if __name__ == '__main__':
    _app = MainApp()
    _app.main()
