from pathlib import Path
import subprocess
import sys

HOME_DIRECTORY = ".."


# call(["ls", "-l"]

class Renderer:
    def __init__(self, home_directory: str = ''):
        print("Version 2 Markdown Render")
        self.home_directory = Path(home_directory).resolve()
        self.script_dir = Path(__file__).resolve().parent

    def render(self):
        #os.chdir(self.home_directory)
        #print(f"Current Top Directory: {os.getcwd()}")
        #######################
        # get list of all folders in this directory
        ######################
        my_directories = [d for d in self.home_directory.iterdir() if d.is_dir()]
        pdf_directories = [d for d in my_directories if (d / "pdf").exists()]

        # print(pdf_directory)
        ####################
        # Go through those directories and find all the .md files and then create the pdf
        ####################
        for directory in pdf_directories:
            print(f"Looking in this directory for md to make into pdfs: \n {directory}")
            #os.chdir(directory)
            md_files = [f for f in directory.glob("*.md")]

            print(f"md files found {md_files}")
            ################
            # pandoc those files
            ################
            for file in md_files:
                self.process_file(directory, file)

    def process_file(self, directory: Path, filename: Path):
        #os.chdir(directory)
        lines=[]
        with open(filename, "r") as f:
            lines = f.readlines()

        # Extract [comment]: commands
        commands = []
        for line in lines:
            line = line.strip()
            if line.startswith("<!--") and "command:" in line:
                # Extract the part after 'command:' and before the closing '-->'
                try:
                    content = line.split("command:", 1)[1]
                    command = content.split("-->", 1)[0].strip()
                    commands.append(command)
                except IndexError:
                    print("Index Error")
                    continue  # malformed line, skip it

        print(f"In the file {filename.name} we found the commands: {commands}")

        if 'render' not in commands:
            return

        output_pdf = directory / "pdf" / f"{filename.stem}.pdf"
        pandoc_cmd = [
            "pandoc", "-s", str(filename),
            "--pdf-engine=pdflatex",
            f"--resource-path={directory}"
        ]

        if 'landscape' in commands:
            pandoc_cmd.extend(["-V", "geometry:landscape"])
        else:
            pandoc_cmd.extend(["-V", "geometry:margin=.75in", "-V", "papersize:letter"])

        if 'grid' in commands:
            pandoc_cmd.extend(["-H", str(self.script_dir / "grid-header.tex")])

        pandoc_cmd.extend(["-o", str(output_pdf)])

        print(f"  Running: {' '.join(pandoc_cmd)}")
        subprocess.call(pandoc_cmd)


if __name__ == '__main__':
    # Renderer.render()
    r = Renderer(HOME_DIRECTORY)
    # r.process_file("/Users/mbardoe/Documents/GitHub/CS570-ClassNotes/Homework_Handouts", 'HW_1.md')
    r.render()
