######################################################################
# Location of newly downloaded EOPS dataset from Qualtrics
######################################################################

from datetime import datetime
date = datetime.now()
file = "../Data downloads/" + str(date.strftime("%m.%d.%y")) + " EOPS.csv"

# Import csv
import pandas as pd
try:
    df = pd.read_csv(file, header = 0, skiprows = [1])
except FileNotFoundError:
    print(f"\nERROR: Check that the dataset was downloaded to the correct folder with the correct file name. The correct file path should be:\n  {file}")
    exit()

######################################################################
# Rename Qualtrics variables and program IDs
######################################################################

from rename_qualtrics import rename
rename(file, df, pd)

######################################################################
# Programs to report
######################################################################

print(f"\n---------------------------------------------\n\
EOPS Custom Report Writer - {date.strftime('%m.%d.%y %I.%M%p')}\n\
---------------------------------------------")

from program_info import possible_programs, progname_dict

# Programs that appear in dataset
programs_in_df = sorted(df["ProgramID"].unique())

# Which programs do you need a report for
programs_to_report = [int(x) for x in input("\nProgram IDs, separated by a space: ").split(" ")]

######################################################################
# Create report
######################################################################

import csv
import numpy as np
import os

completed_reports = []
incomplete_reports = []

# Progress log
log = f"../Progress logs/{date.strftime('%m.%d.%y')} log.txt"
log_title = f"---------------------------------------------\n\
EOPS Custom Report Writer - {date.strftime('%m.%d.%y %I.%M %p')}\n\
---------------------------------------------"
# If log file already exists, append, else open and write
if os.path.exists(log) == True:
    logtxt = open(log, "a")
    logtxt.write(f"\n\n{log_title}")
else:
    logtxt = open(log, "w")
    logtxt.write(log_title)

for program in programs_to_report:

    # Error messages
    if program not in possible_programs:
        incomplete_reports.append(program)
        print(f"\nERROR: {program} is not a valid program ID.")
        logtxt.write(f"\nERROR: {program} is not a valid program ID.")
    elif program not in programs_in_df:
        incomplete_reports.append(program)
        print(f"\nERROR: Program {program} ({progname_dict[program]}) is not in this dataset.")
        logtxt.write(f"\nERROR: Program {program} ({progname_dict[program]}) is not in this dataset.")

    #################
    # Valid programs
    #################

    else:

        # File name
        final_report = f"../Unformatted reports/{program} custom EOPS report.csv"

        # Add to completed reports list
        completed_reports.append(program)

        # Write program name
        with open(final_report, 'w', newline='') as report:
            reportwriter = csv.writer(report)
            reportwriter.writerow([progname_dict[program]])

        # 1 - Clin prep: Courses prepped you for clinical rotations
        from T1_clin_prep_courses import create_cp_courses
        create_cp_courses(pd, np, file, program, final_report, csv)

        # 2 - Clin prep: Evaluate instructions
        from T2_clin_prep_instruction import create_cp_instruct
        create_cp_instruct(pd, np, file, program, final_report, csv)

        # 3 - Clin prep: Confidence in competencies
        from T3_clin_prep_competencies import create_cp_comp
        create_cp_comp(pd, np, file, program, final_report, csv)

        # 4 - SCPES: Quality of rotations
        from T4_scp_quality import create_scp_qual
        create_scp_qual(pd, np, file, program, final_report, csv)

        # 5 - SCPES: Preceptor experiences
        from T5_scp_preceptors import create_scp_precept
        create_scp_precept(pd, np, file, program, final_report, csv)

        # 6,7 - IPE: Agreement w statement & assessment of IPE experiences
        from T6_T7_ipe import create_ipe
        create_ipe(pd, np, file, program, final_report, csv)

        # 8 - Institutional support services
        from T8_inst_support import create_supp
        create_supp(pd, np, file, program, final_report, csv)

        # 9 - Health: Feelings in the past week
        from T9_health_week import create_health_week
        create_health_week(pd, np, file, program, final_report, csv)

        # 10 - Health: Feelings in past 30 days
        from T10_health_30 import create_health30
        create_health30(pd, np, file, program, final_report, csv)

        # 11 - Program experiences
        from T11_prog_exp import create_prog_exp
        create_prog_exp(pd, np, file, program, final_report, csv)

        # 12 - Program experiences - satisfaction
        from T12_prog_exp_sat import create_prog_exp_sat
        create_prog_exp_sat(pd, np, file, program, final_report, csv)

        # 13 - Negative Experiences in PA School
        from T13_neg import create_neg
        create_neg(pd, np, file, program, final_report, csv)

        # Print status message
        print(f"\nReport completed: {program} ({progname_dict[program]})")
        logtxt.write(f"\nReport completed: {program} ({progname_dict[program]})")

# Final message
print("\n-------\nSUMMARY\n-------")
if len(completed_reports) > 0:
    print(f'\nReports were generated and saved in the "Unformatted Reports" folder for the following programs:\n  {completed_reports}')
if len(completed_reports) < len(programs_to_report):
    print(f"\nReports for the following programs could not be completed:\n  {incomplete_reports}")

# Final message - print to text file
logtxt.write("\n-------\nSUMMARY\n-------")
if len(completed_reports) > 0:
    logtxt.write(f'\nReports were generated and saved in the "Unformatted Reports" folder for the following programs:\n  {completed_reports}')
if len(completed_reports) < len(programs_to_report):
    logtxt.write(f"\nReports for the following programs could not be completed:\n  {incomplete_reports}")
logtxt.close()
