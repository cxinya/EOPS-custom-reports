def create_ipe(pd, np, file, program, final_report, csv):

    # Create df

    df = pd.read_csv(file)

    ipe_df = df[['IPE_OtherRoles', 'IPE_Amt', 'ProgramID']].loc[df['ProgramID'] == program].drop('ProgramID', axis = 1)

    ipe_df.columns = ['Agreement', 'Assessment']

    ##########################################
        # The learning experience(s) with students from different health professions helped me gain a better understanding of the roles of other professions in patient care
        # Values: 1 = strongly disagree to 5 = strongly agree
    ##########################################

    ipe_roles = ipe_df['Agreement'].agg(["count", "mean", "median"]).to_frame().transpose().reset_index()
    ipe_roles.rename(columns = {"index": "", "count": "n", "mean": "Mean", "median": "Median"}, inplace = True)
    ipe_roles["n"] = ipe_roles["n"].apply(lambda x: int(x))
    ipe_roles["Mean"] = ipe_roles["Mean"].apply(lambda x: round(x, 2))

    # Title
    title = "The learning experience(s) with students from different health professions helped me gain a better understanding of the roles of other professions in patient care"
    title_df = pd.DataFrame({'': title.upper()}, index = [0])

    # Write to report
    with open(final_report, 'a', newline = '') as report:
        title_df.to_csv(report, index = False)
    with open(final_report, 'a', newline = '') as report:
        ipe_roles.to_csv(report, index = False)

    ##########################################
        # Assessment of amount of IPE experiences
        # Values: 1 = not enough to 3 = too much
    ##########################################

    ipe_amt = ipe_df['Assessment'].agg(["count", "mean", "median"]).to_frame().transpose().reset_index()
    ipe_amt.rename(columns = {"index": "", "count": "n", "mean": "Mean", "median": "Median"}, inplace = True)
    ipe_amt["n"] = ipe_amt["n"].apply(lambda x: int(x))
    ipe_amt["Mean"] = ipe_amt["Mean"].apply(lambda x: round(x, 2))

    # Title
    title = "Assessment of amount of IPE experiences"
    title_df = pd.DataFrame({'': title.upper()}, index = [0])

    # Write to report
    with open(final_report, 'a', newline = '') as report:
        title_df.to_csv(report, index = False)
    with open(final_report, 'a', newline = '') as report:
        ipe_amt.to_csv(report, index = False)










