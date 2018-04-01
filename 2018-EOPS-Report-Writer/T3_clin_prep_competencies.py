def create_cp_comp(pd, np, file, program, final_report, csv):
    ## Create df

    df = pd.read_csv(file)

    cp_comp_df = df[['MedKnowledge',
                    'CommSkills',
                    'PatientCare',
                    'Professional',
                    'PractBasedLearn',
                    'SystemPractice', 'ProgramID'
                    ]]
    cp_comp_df = cp_comp_df.loc[cp_comp_df['ProgramID'] == program].drop(['ProgramID'], axis = 1)
    cp_comp_df.rename(columns = {
            'MedKnowledge': 'Medical knowledge',
            'CommSkills': 'Interpersonal & communication skills',
            'PatientCare': 'Patient care',
            'Professional': 'Professionalism',
            'PractBasedLearn': 'Practice-based learning',
            'SystemPractice': 'Systems-based practice'
            }, inplace = True)

    ## Value labels: 1 = Not at all confident, 5 = Very confident

    # Table
    cp_comp = cp_comp_df.agg(["count", "mean", "median"]).transpose().reset_index()

    # Tidy up
    cp_comp.columns = ["Competency", "n", "Mean", "Median"]
    cp_comp["n"] = cp_comp["n"].apply(lambda x: int(x))
    cp_comp["Mean"] = cp_comp["Mean"].apply(lambda x: round(x,2))

    # Title
    title = "Confidence in PA Competencies"
    title_df = pd.DataFrame({'': title.upper()}, index = [0])

    # Write to report
    with open(final_report, 'a', newline = '') as report:
        title_df.to_csv(report, index = False)
    with open(final_report, 'a', newline = '') as report:
        cp_comp.to_csv(report, index = False)