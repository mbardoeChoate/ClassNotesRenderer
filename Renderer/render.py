import os
from subprocess import call

HOME_DIRECTORY = ".."


class Renderer:
    def __init__(self, home_directory: str = ''):
        self.home_directory = home_directory

    def render(self):
        os.chdir(self.home_directory)
        print(f"Current Top Directory: {os.getcwd()}")
        #######################
        # get list of all folders in this directory
        ######################
        my_directories = [f.path for f in os.scandir(os.getcwd()) if f.is_dir()]
        pdf_directory = []
        for directory in my_directories:
            if 'pdf' in [x.name for x in os.scandir(directory)]:
                pdf_directory.append(directory)

        # print(pdf_directory)
        ####################
        # Go through those directories and find all the .md files and then create the pdf
        ####################
        for directory in pdf_directory:
            print(f"Looking in this directory for md to make into pdfs: \n {directory}")
            os.chdir(directory)
            md_files = [my_file.name for my_file in os.scandir(directory) if my_file.name[-3:] == ".md"]
            print(f"md files found {md_files}")
            ################
            # pandoc those files
            ################
            for file in md_files:
                self.process_file(directory, file)

    def process_file(self, directory: str, filename: str):
        os.chdir(directory)
        file1 = open(filename, "r")
        my_lines = file1.readlines()
        # Strips the newline character
        commands = [line.strip()[10:].strip() for line in my_lines if line.strip()[:10] == "[comment]:"]
        print(f"In the file {filename} we found the commands: {commands}")

        final_call = []
        if 'render' in commands:
            if 'landscape' in commands:
                final_call = ["pandoc", "-s", directory + "/" + filename,
                              '-V', 'geometry:landscape',
                              "-o", directory + "/pdf/" + filename[:-3] + '.pdf']

            else:
                final_call = ["pandoc", "-s", directory + "/" + filename, "-o",
                              directory + "/pdf/" + filename[:-3] + '.pdf']

        if len(final_call) > 0:
            # print (final_call)
            call(final_call)


if __name__ == '__main__':
    r = Renderer(HOME_DIRECTORY)
    r.render()
