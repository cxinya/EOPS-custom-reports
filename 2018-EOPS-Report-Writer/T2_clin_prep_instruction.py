def create_cp_instruct(pd, np, file, program, final_report, csv):

    # Create df

    df = pd.read_csv(file)

    cp_instruct_df = df[['ProgramID', 'Instruct_Diverse',
                        'Instruct_Diagnosis',
                        'Instruct_Prevent',
                        'Instruct_Manage',
                        'Instruct_Oral',
                        'Instruct_Palliative',
                        'Instruct_PubHealth',
                        'Instruct_Community',
                        'Instruct_Womens',
                        'Instruct_SocialDet',
                        ]]

    cp_instruct_df = cp_instruct_df.loc[cp_instruct_df['ProgramID'] == program].drop(['ProgramID'], axis = 1)

    cp_instruct_df.rename(columns = {
            'Instruct_Diverse': 'Culturally appropriate care for diverse populations',
            'Instruct_Diagnosis': 'Diagnosis of disease',
            'Instruct_Prevent': 'Disease prevention/health maintenance',
            'Instruct_Manage': 'Management of disease',
            'Instruct_Oral': 'Oral health',
            'Instruct_Palliative': 'Palliative/End of life care',
            'Instruct_PubHealth': 'Public health',
            'Instruct_Community': 'Role of community health and social service agencies',
            'Instruct_Womens': 'Social determinants of health',
            'Instruct_SocialDet': "Women's health"}, inplace = True)

    # Value labels: 1 = no instruction, 2 = insufficient, 3 = appropriate, 4 = excessive
        # Switch so 1 = NA, 2-4 become 1-3

    # Received no instruction

    cp_instruct_none = cp_instruct_df.replace([2,3,4], np.nan)
    cp_instruct_none = cp_instruct_none.sum().to_frame()

    # Received instruction

    cp_instruct_yes = cp_instruct_df.replace([1, 2, 3, 4], [np.nan, 1, 2, 3])
    cp_instruct_yes = cp_instruct_yes.agg(["count", "mean", "median"]).transpose()

    # Complete table

    cp_instruct = cp_instruct_none.merge(cp_instruct_yes, left_index = True, right_index = True)
    cp_instruct = cp_instruct[["count", 0, "mean", "median"]].reset_index()

    # Tidy up

    cp_instruct.columns = ["Topic", "n", "No instruction (n)", "Mean", "Median"]

    cp_instruct["n"] = cp_instruct["n"].apply(lambda x: int(x))
    cp_instruct["No instruction (n)"] = cp_instruct["No instruction (n)"].apply(lambda x: int(x))
    cp_instruct["Mean"] = cp_instruct["Mean"].apply(lambda x: round(x, 2))

    # Title
    title = "Evaluate instruction (both quality and amount) received in the following areas"
    title_df = pd.DataFrame({'': title.upper()}, index = [0])

    # Write to report
    with open(final_report, 'a', newline = '') as report:
        title_df.to_csv(report, index = False)
    with open(final_report, 'a', newline = '') as report:
        cp_instruct.to_csv(report, index = False)