def create_scp_precept(pd, np, file, program, final_report, csv):
    # Read entire csv
    df = pd.read_csv(file)
    df = df[['Emergency_History',
            'Emergency_Exam',
            'Emergency_Tech',
            'Emergency_Feedback',
            'PrimRural_History',
            'PrimRural_Exam',
            'PrimRural_Tech',
            'PrimRural_Feedback',
            'FamMed_History',
            'FamMed_Exam',
            'FamMed_Tech',
            'FamMed_Feedback',
            'IntMed_History',
            'IntMed_Exam',
            'IntMed_Tech',
            'IntMed_Feedback',
            'Ped_History',
            'Ped_Exam',
            'Ped_Tech',
            'Ped_Feedback',
            'GenSurg_History',
            'GenSurg_Exam',
            'GenSurg_Tech',
            'GenSurg_Feedback',
            'Hospital_History',
            'Hospital_Exam',
            'Hospital_Tech',
            'Hospital_Feedback',
            'Obgyn_History',
            'Obgyn_Exam',
            'Obgyn_Tech',
            'Obgyn_Feedback',
            'Psych_History',
            'Psych_Exam',
            'Psych_Tech',
            'Psych_Feedback', 'ProgramID'
            ]].loc[df['ProgramID'] == program].drop(['ProgramID'], axis = 1)
    var_list = list(enumerate(df.columns.tolist()))

    # Replace 2 with 0

    df = df.replace(2,0)

    # Add table name to csv

    title = "Preceptor experiences"
    title_df = pd.DataFrame({'': title.upper()}, index = [0])

    with open(final_report, 'a', newline = '') as report:
            title_df.to_csv(report, index = False)

    # Rotations and variables

    rotations = ['Emergency medicine',
                'Extended primary care or rural track',
                'Family medicine',
                'General internal medicine',
                'General pediatrics',
                'General surgery',
                'Hospital medicine',
                "Obstetrics/gynecology/women's health",
                'Psychiatry/behavioral medicine']

    i_vars = [list(range(0,4)), list(range(4,8)), list(range(8,12)),
              list(range(12,16)), list(range(16, 20)), list(range(20, 24)),
              list(range(24,28)), list(range(28,32)), list(range(32,36))]

    rotation_vars = list(zip(rotations, i_vars))

    # Create dictionary of dfs for each rotation
    rotation_dfs = {}

    for rotation, i_var in rotation_vars:
        rotation_dfs[rotation] = df.iloc[:,i_var]

    # Create dictionary of completed tables
    rotation_tables = {}

    for rotation in rotations:
        rotation_tables[rotation] = rotation_dfs[rotation].apply(["count", "sum"])
        rotation_tables[rotation].columns = ["   Observed by preceptor taking patient history",
                                            "   Observed by preceptor performing physical exam",
                                            "   Observed by preceptor performing technical procedures",
                                            "   Given mid-point feedback by preceptor"]
        rotation_tables[rotation] = rotation_tables[rotation].transpose()
        rotation_tables[rotation]["% yes"] = round(100 * rotation_tables[rotation]["sum"]/rotation_tables[rotation]["count"], 2)
        rotation_tables[rotation] = rotation_tables[rotation].drop(["sum"], axis = 1).reset_index()
        rotation_tables[rotation].rename(columns = {"index": rotation, "count": "", "% yes": ""}, inplace = True)
        with open(final_report, 'a', newline = '') as report:
            rotation_tables[rotation].to_csv(report, index = False)