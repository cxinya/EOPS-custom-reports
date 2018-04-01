def create_neg(pd, np, file, program, final_report, csv):

    df = pd.read_csv(file)

    neg_df = df[['Self_Embarrassed',
                'Self_Humiliated',
                'Self_Threat',
                'Self_Harm',
                'Self_PerformService',
                'Self_Advances',
                'Self_Favors',
                'Self_DenyOpp_Gender',
                'Self_Offense_Gender',
                'Self_Grades_Gender',
                'Self_DenyOpp_Race',
                'Self_Offense_Race',
                'Self_Grades_Race',
                'Self_DenyOpp_Orient',
                'Self_Offense_Orient',
                'Self_Grades_Orient',
                'Self_DenyOpp_Relig',
                'Self_Offense_Relig',
                'Self_Grades_Relig','ProgramID'
                ]].loc[df['ProgramID'] == program].drop('ProgramID', axis = 1)

    # Values: 1 = never, 2-4 has occurred

    #####################################
    # ns
    #####################################

    # Total responses
    neg_n = neg_df.count().to_frame()

    # Responses by discrimination dimension
    max_n_gender = int(neg_n.loc[['Self_DenyOpp_Gender',
                            'Self_Offense_Gender',
                            'Self_Grades_Gender']].max())
    max_n_race = int(neg_n.loc[['Self_DenyOpp_Race',
                            'Self_Offense_Race',
                            'Self_Grades_Race']].max())
    max_n_orient = int(neg_n.loc[['Self_DenyOpp_Orient',
                            'Self_Offense_Orient',
                            'Self_Grades_Orient']].max())
    max_n_relig = int(neg_n.loc[['Self_DenyOpp_Relig',
                            'Self_Offense_Relig',
                            'Self_Grades_Relig']].max())
    max_ns = pd.DataFrame([['Been discriminated against or harrassed based on my gender',max_n_gender],
                           ['Been discriminated against or harrassed based on my race', max_n_race],
                           ['Been discriminated against or harrassed based on my sexual\n   orientation', max_n_orient],
                           ['Been discriminated against or harrassed based on my religion', max_n_relig]
            ], columns = ["index", 0])
    #
    # Create final ns
    neg_n = neg_n.loc[['Self_Embarrassed',
                'Self_Humiliated',
                'Self_Threat',
                'Self_Harm',
                'Self_PerformService',
                'Self_Advances',
                'Self_Favors']].reset_index()
    neg_n = neg_n.append(max_ns)

    #####################################
    # Counts of yes
    #####################################

    # Reported occured, collapse discrimination categories
    neg_yes = neg_df.replace({1:0, 2:1, 3:1, 4:1})
    neg_yes["Been discriminated against or harrassed based on my gender"] = neg_yes[[
            'Self_DenyOpp_Gender',
            'Self_Offense_Gender',
            'Self_Grades_Gender']].sum(axis = 1)
    neg_yes["Been discriminated against or harrassed based on my race"] = neg_yes[[
            'Self_DenyOpp_Race',
            'Self_Offense_Race',
            'Self_Grades_Race']].sum(axis = 1)
    neg_yes["Been discriminated against or harrassed based on my sexual\n   orientation"] = neg_yes[[
            'Self_DenyOpp_Orient',
            'Self_Offense_Orient',
            'Self_Grades_Orient']].sum(axis = 1)
    neg_yes["Been discriminated against or harrassed based on my religion"] = neg_yes[[
            'Self_DenyOpp_Relig',
            'Self_Offense_Relig',
            'Self_Grades_Relig']].sum(axis = 1)
    neg_yes = neg_yes.replace({0:0, 1:1, 2:1, 3:1})
    neg_yes = neg_yes.drop(['Self_DenyOpp_Gender',
            'Self_Offense_Gender',
            'Self_Grades_Gender',
            'Self_DenyOpp_Race',
            'Self_Offense_Race',
            'Self_Grades_Race',
            'Self_DenyOpp_Orient',
            'Self_Offense_Orient',
            'Self_Grades_Orient',
            'Self_DenyOpp_Relig',
            'Self_Offense_Relig',
            'Self_Grades_Relig'], axis = 1).sum().to_frame().reset_index()
    neg_yes.columns = ["index","yes"]


    #####################################
    # Merge ns and counts of yes
    #####################################

    neg = neg_n.merge(neg_yes, on = "index")
    neg["% yes"] = round(100 * neg["yes"]/neg[0], 2)
    neg = neg.drop("yes", axis = 1)
    neg.columns = ["Did any students in this cohort report…", "n", "% yes"]
    neg = neg.replace({'Self_Embarrassed': 'Been publicly embarrassed',
                    'Self_Humiliated': 'Been publicly humiliated',
                    'Self_Threat': 'Been threatened with physical harm',
                    'Self_Harm': 'Been physically harmed (e.g., hit, slapped, kicked)',
                    'Self_PerformService': 'Been required to perform personal services (e.g., shopping,\n   babysitting)',
                    'Self_Advances': 'Been subjected to unwanted sexual advances',
                    'Self_Favors': 'Been asked to exchange sexual favors for grades or other rewards'})

    #########################
    # Write to csv
    #########################

    # Title
    title = "Negative Experiences in PA School"
    title_df = pd.DataFrame({'': title.upper()}, index = [0])

    # Write to report
    with open(final_report, 'a', newline = '') as report:
        title_df.to_csv(report, index = False)
    with open(final_report, 'a', newline = '') as report:
        neg.to_csv(report, index = False)
