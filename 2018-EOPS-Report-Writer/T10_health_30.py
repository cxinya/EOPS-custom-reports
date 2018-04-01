def create_health30(pd, np, file, program, final_report, csv):

    df = pd.read_csv(file)

    health30_df = df[['Financial_Concerns',
                    'Fatigue',
                    'Social_Support',
                    'ProgramID']].loc[df['ProgramID'] == program].drop('ProgramID', axis = 1) - 1
    health30_df.rename(columns = {'Financial_Concerns': 'Financial concerns',
                            'Fatigue': 'Level of fatigue',
                            'Social_Support': 'Level of satisfaction with social support from friends and family',
                                    }, inplace = True)

    # Table
    health30 = health30_df.agg(["count", "mean", "median"]).transpose().reset_index()

    # Tidy up
    health30.columns = ["In the past 30 days, rate...", "n", "Mean", "Median"]
    health30["n"] = health30["n"].apply(lambda x: int(x))
    health30["Mean"] = health30["Mean"].apply(lambda x: round(x, 2))

    #########################
    # Write to csv
    #########################
    # Title
    title = "Health & well-being: In the 30 days, rate..."
    title_df = pd.DataFrame({'': title.upper()}, index = [0])

    # Write to report
    with open(final_report, 'a', newline = '') as report:
        title_df.to_csv(report, index = False)
    with open(final_report, 'a', newline = '') as report:
        health30.to_csv(report, index = False)