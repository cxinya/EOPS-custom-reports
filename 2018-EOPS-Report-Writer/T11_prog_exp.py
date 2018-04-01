def create_prog_exp(pd, np, file, program, final_report, csv):

    df = pd.read_csv(file)

    prog_exp_df = df[['ProgramQuality',
                    'AgainPA',
                    'AttendAgain',
                    'RecommendPACareer', 'ProgramID'
                    ]].loc[df['ProgramID'] == program].drop('ProgramID', axis = 1)
    prog_exp_df.rename(columns = {'ProgramQuality': 'Overall, I am satisfied with the quality of my PA education.',
                    'AgainPA': 'If I could revisit my career choice again, I would attend school to\n  become a PA.',
                    'AttendAgain': 'If I could revisit my program choice again, I would attend the same\n  program.',
                    'RecommendPACareer': 'I would recommend the PA career to others',
                    }, inplace = True)

    # Values: 1 = strongly disagree, 5 = strongly agree

    # Table
    prog_exp = prog_exp_df.agg(["count", "mean", "median"]).transpose().reset_index()

    # Tidy up
    prog_exp.columns = ["", "n", "Mean", "Median"]
    prog_exp["n"] = prog_exp["n"].apply(lambda x: int(x))
    prog_exp["Mean"] = prog_exp["Mean"].apply(lambda x: round(x,2))

    #########################
    # Write to csv
    #########################
    # Title
    title = "PA Program Experiences"
    title_df = pd.DataFrame({'': title.upper()}, index = [0])

    # Write to report
    with open(final_report, 'a', newline = '') as report:
        title_df.to_csv(report, index = False)
    with open(final_report, 'a', newline = '') as report:
        prog_exp.to_csv(report, index = False)