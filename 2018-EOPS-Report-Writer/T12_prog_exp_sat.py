def create_prog_exp_sat(pd, np, file, program, final_report, csv):

    df = pd.read_csv(file)

    prog_exp_sat_df = df[['ProgSat_Affil',
                        'ProgSat_SFR',
                        'ProgSat_Loc',
                        'ProgSat_FacDiv',
                        'ProgSat_StudDiv',
                        'ProgSat_Dual',
                        'ProgSat_FacRep',
                        'ProgSat_Admit',
                        'ProgSat_ClinExp',
                        'ProgSat_PANCE',
                        'ProgSat_Mission',
                        'ProgSat_ProgRep',
                        'ProgSat_Facil',
                        'ProgSat_ClinCurric',
                        'ProgSat_FinAid',
                        'ProgSat_Tuition', 'ProgramID'
                        ]].loc[df['ProgramID'] == program].drop('ProgramID', axis = 1)
    prog_exp_sat_df.rename(columns = {'ProgSat_Affil': 'Affiliation with a hospital or clinic system',
                        'ProgSat_SFR': 'Class size/student-faculty ratio',
                        'ProgSat_Loc': 'Desirability of program location',
                        'ProgSat_FacDiv': 'Diversity of faculty',
                        'ProgSat_StudDiv': 'Diversity of student body',
                        'ProgSat_Dual': 'Dual degree offered (PA plus MPH)',
                        'ProgSat_FacRep': 'Faculty reputation',
                        'ProgSat_Admit': 'Likelihood of admission',
                        'ProgSat_ClinExp': 'Opportunities to gain clinical experience (e.g., rotations)',
                        'ProgSat_PANCE': 'PANCE pass rates',
                        'ProgSat_Mission': 'Program mission consistent with personal values',
                        'ProgSat_ProgRep': 'Program reputation',
                        'ProgSat_Facil': 'Quality of program facilities (e.g., labs and equipment)',
                        'ProgSat_ClinCurric': 'Rigor of clinical curriculum',
                        'ProgSat_FinAid': 'Scholarships and financial aid',
                        'ProgSat_Tuition': 'Tuition'
                        }, inplace = True)

    # Values: 1-5 satisfaction, 6 = NA

    # Replace NA
    prog_exp_sat_df = prog_exp_sat_df.replace(6, np.nan)

    # Table
    prog_exp_sat = prog_exp_sat_df.agg(["count", "mean", "median"]).transpose().reset_index()

    # Tidy up
    prog_exp_sat.columns = ["Satisfaction with...", "n", "Mean", "Median"]
    prog_exp_sat['n'] = prog_exp_sat['n'].apply(lambda x: int(x))
    prog_exp_sat['Mean'] = prog_exp_sat['Mean'].apply(lambda x: round(x,2))

    #########################
    # Write to csv
    #########################
    # Title
    title = "PA Program Experiences: Satisfaction with..."
    title_df = pd.DataFrame({'': title.upper()}, index = [0])

    # Write to report
    with open(final_report, 'a', newline = '') as report:
        title_df.to_csv(report, index = False)
    with open(final_report, 'a', newline = '') as report:
        prog_exp_sat.to_csv(report, index = False)