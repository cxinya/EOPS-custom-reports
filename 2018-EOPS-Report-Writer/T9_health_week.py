def create_health_week(pd, np, file, program, final_report, csv):

    df = pd.read_csv(file)

    health_week_df = df[['Qual_Life',
                        'Emotional',
                        'Mental',
                        'Physical',
                        'Social_Activity',
                        'Spiritual','ProgramID'
                        ]].loc[df['ProgramID'] == program].drop('ProgramID', axis = 1)-1
    health_week_df.rename(columns = {'Qual_Life': 'Overall quality of life',
                                    'Emotional': 'Overall emotional well-being',
                                    'Mental': 'Overall mental well-being',
                                    'Physical': 'Overall physical well-being',
                                    'Social_Activity': 'Level of social activity',
                                    'Spiritual': 'Spiritual well-being'
                                            }, inplace = True)
    # Table

    health_week = health_week_df.agg(["count", "mean", "median"]).transpose().reset_index()

    # Tidy up

    health_week.columns = ["In the past week, rate...", "n", "Mean", "Median"]
    health_week["n"] = health_week["n"].apply(lambda x: int(x))
    health_week["Mean"] = health_week["Mean"].apply(lambda x: round(x, 2))

    #########################
    # Write to csv
    #########################
    # Title
    title = "Health & well-being: In the past week, rate..."
    title_df = pd.DataFrame({'': title.upper()}, index = [0])

    # Write to report
    with open(final_report, 'a', newline = '') as report:
        title_df.to_csv(report, index = False)
    with open(final_report, 'a', newline = '') as report:
        health_week.to_csv(report, index = False)