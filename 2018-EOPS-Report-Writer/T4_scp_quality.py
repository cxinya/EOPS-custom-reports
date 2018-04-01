def create_scp_qual(pd, np, file, program, final_report, csv):

    # Create df

    df = pd.read_csv(file)

    scp_qual_df = df[['Rotation_Emergency',
                    'Rotation_PrimRural',
                    'Rotation_FamMed',
                    'Rotation_GenIntern',
                    'Rotation_GenPed',
                    'Rotation_GenSurg',
                    'Rotation_Hospital',
                    'Rotation_Obgyn',
                    'Rotation_Psych',
                    'ProgramID']]
    scp_qual_df = scp_qual_df.loc[scp_qual_df['ProgramID'] == program].drop(['ProgramID'], axis = 1)
    scp_qual_df.rename(columns = {
            'Rotation_Emergency': 'Emergency medicine',
            'Rotation_PrimRural': 'Extended primary care or rural track',
            'Rotation_FamMed': 'Family medicine',
            'Rotation_GenIntern': 'General internal medicine',
            'Rotation_GenPed': 'General pediatrics',
            'Rotation_GenSurg': 'General surgery',
            'Rotation_Hospital': 'Hospital medicine',
            'Rotation_Obgyn': "Obstetrics/gynecology/women's health",
            'Rotation_Psych': 'Psychiatry/behavioral medicine',
            }, inplace = True)

    # Value labels: 1 = Poor to 4 = Excellent, 5 = N/A

    # Replace NA
    scp_qual_df = scp_qual_df.replace(5, np.nan)

    # Table
    scp_qual = scp_qual_df.agg(["count", "mean", "median"]).transpose().reset_index()

    # Tidy up
    scp_qual.columns = ["Rotation", "n", "Mean", "Median"]
    scp_qual["n"] = scp_qual["n"].apply(lambda x: int(x))
    scp_qual["Mean"] = scp_qual["Mean"].apply(lambda x: round(x, 2))

    # Title
    title = "Rate quality of education experiences in each rotation"
    title_df = pd.DataFrame({'': title.upper()}, index = [0])

    # Write to report
    with open(final_report, 'a', newline = '') as report:
        title_df.to_csv(report, index = False)
    with open(final_report, 'a', newline = '') as report:
        scp_qual.to_csv(report, index = False)