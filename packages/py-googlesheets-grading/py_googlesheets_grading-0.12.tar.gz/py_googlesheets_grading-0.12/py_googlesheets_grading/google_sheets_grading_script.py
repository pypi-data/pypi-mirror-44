import csv
import os

import pygsheets
from git import Repo
import git

class Grader:
    def csv_converter(input_path, output_path):
        """
        Converts a comma delimited csv file to a tab delimited csv file.
        :param input_path:
        :param output_path:
        """
        print("Converting CSV to tab-delimited file...")
        print('Path: ' + input_path)
        with open(input_path) as inputFile:
            with open(output_path, 'w+', newline='', encoding='utf-16') as outputFile:
                reader = csv.reader(inputFile)
                for row in reader:
                    outputFile.write('\t'.join(row)+'\n')

                #reader = csv.DictReader(inputFile, delimiter=',')
                #writer = csv.DictWriter(outputFile, reader.fieldnames, delimiter='\t',  dialect='excel-tab')
                #writer.writeheader()
                #writer.writerows(reader)

                #csvwriter = csv.writer(reader.fieldnames, dialect='excel-tab')
                #csv_writerows(csvwriter, reader, encoding='utf-16')
        os.remove(input_path)
        print("Conversion complete.")


    def grade_students(spreadsheet_url=None):

        DONT_GRADE = ['ASD009','haa037', 'tny009']
        DO_GRADE = ['ekj008']
        GRADED_STUDENTS_FILE = "GRADED_STUDENTS.txt"
        #SPREADSHEET_URL = spreadsheet_url

        if not spreadsheet_url:
            SPREADSHEET_URL = input("Paste the link to your Google Sheets gradings: ")
        else:
            SPREADSHEET_URL = spreadsheet_url

        return

        # Create graded students file.
        with open(GRADED_STUDENTS_FILE, 'w') as name_file:
            name_file.write("GRADED STUDENTS: \n")
            name_file.close()

        # Authorize pygsheets
        client = pygsheets.authorize()
        print("Authorized!")

        # Get grading sheet
        grading_spreadsheet = client.open_by_url(SPREADSHEET_URL)
        print("Got the spreadsheet!")

        grading_sheets = grading_spreadsheet.worksheets()

        # Go through each individual sheet.
        for sheet in grading_sheets:
            student_id = sheet.get_value('D2')


            # Skip the DONT_GRADE students.
            if student_id not in DO_GRADE:
                continue

            if student_id in DONT_GRADE:
                continue

            print('Student ID: ' + student_id)


            # 1. Clone the student repo.

            curr_repo_path = 'student_repos/'+student_id
            student_repo = Repo.init(curr_repo_path)
            try:
                origin = student_repo.create_remote('origin', 'https://retting.ii.uib.no/' + student_id + '/inf101.v19.sem1')
                #origin = student_repo.create_remote('origin', 'https://retting.ii.uib.no/'+ student_id +'/python-pushing-est') # Testing purposes

            except git.exc.GitCommandError:
                print("You have already cloned this repo in here!")
                origin = student_repo.remote('origin')

            # TESTS AND SHIT
            assert origin.exists()
            assert origin == student_repo.remotes.origin == student_repo.remotes['origin']
            try:
                origin.fetch()
            except git.exc.GitCommandError:
                if student_id:
                    print("Didn't find any student ID.")
                else:
                    print("{} is not a valid student ID.".format(student_id))

                print("Going to next sheet...")
                continue

            student_repo.create_head('master', origin.refs.master)  # create local branch "master" from remote "master"
            student_repo.heads.master.set_tracking_branch(origin.refs.master)  # set local "master" to track remote "master
            student_repo.heads.master.checkout()  # checkout local "master" to working tree

            # lazy renaming
            repo = student_repo

            # 2. MAKE THE GRADING BRANCH
            try:
                repo.git.checkout('grading')
                print("Used previous branch.")

            except git.exc.GitCommandError:
                repo.git.branch('grading')
                repo.git.checkout('grading')
                print("Made new branch.")


            # 3. Save the student's sheet.
            commas_sheet_name = student_id + '_commas'
            finished_sheet_name = student_id
            sheet.export(file_format = pygsheets.ExportType.CSV, filename=commas_sheet_name, path=curr_repo_path+'/')

            # Converts the csv.
            input_path = curr_repo_path+'/' + commas_sheet_name + '.csv'
            output_path = curr_repo_path+'/' + finished_sheet_name +'.csv'
            csv_converter(input_path=input_path, output_path=output_path)



            # 4. COMMIT AND PUSH
            repo.git.add('--all')
            repo.index.commit("FINAL GRADING")
            repo.git.push("origin", "HEAD")
            print("Pushed to repo!")


            # 5. Save the IDs of the student's that have received grading.
            with open(GRADED_STUDENTS_FILE, 'a') as name_file:
                name_file.write(student_id + '\n')
                name_file.close()
