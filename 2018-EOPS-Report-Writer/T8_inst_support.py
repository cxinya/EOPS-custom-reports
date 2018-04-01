def create_supp(pd, np, file, program, final_report, csv):

    df = pd.read_csv(file)

    supp_df = df[['Counseling',
                'Advising',
                'HealthCenter',
                'Computing',
                'Library',
                'ADA','ProgramID']].loc[df['ProgramID'] == program].drop('ProgramID', axis = 1)
    supp_df.rename(columns = {'Counseling': 'Counseling/mental health center',
                            'Advising': 'Faculty advising',
                            'HealthCenter': 'Health center',
                            'Computing': 'Institutional computing (technology)/help desk',
                            'Library': 'Library/learning resource center',
                            'ADA': 'Student success center/ADA office'
                                    }, inplace = True)

    # Value labels:
        # 1-5 = very dissatisfied to very satisfied
        # 6 = school does not offer
        # 7 = offers but never accessed

    #########################
    # Overall n
    #########################
    supp_n = supp_df.count().to_frame().reset_index()
    supp_n.columns = ['Service', 'n']

    #########################
    # Satisfaction
    #########################
    supp_sat = supp_df.replace([6,7], np.nan)
    supp_sat = round(supp_sat.mean(),2).to_frame().reset_index()
    supp_sat.columns = ['Service', "Mean satisfaction"]

    #########################
    # Not offered
    #########################
    supp_offer = supp_df.replace([1,2,3,4,5,7], np.nan)
    supp_offer = supp_offer.count().to_frame().reset_index()
    supp_offer.columns = ['Service', 'Not offered']

    #########################
    # Not used
    #########################
    supp_use = supp_df.replace([1,2,3,4,5,6], np.nan)
    supp_use = supp_use.count().to_frame().reset_index()
    supp_use.columns = ['Service', 'Offered but not used']

    #########################
    # Merge dfs
    #########################

    from functools import reduce
    supp = reduce(lambda left, right: pd.merge(left, right,
                    on = ["Service"], how = "inner"),
                     [supp_n, supp_sat, supp_offer, supp_use])

    #########################
    # Percents
    #########################
    supp['Not offered (%)'] = round(100 * supp['Not offered']/supp['n'],2)
    supp['Offered but not used (%)'] = round(100 * supp['Offered but not used']/supp['n'],2)
    supp = supp.drop(['Not offered', 'Offered but not used'], axis = 1)

    #########################
    # Write to csv
    #########################
    # Title
    title = "Institutional support services"
    title_df = pd.DataFrame({'': title.upper()}, index = [0])

    # Write to report
    with open(final_report, 'a', newline = '') as report:
        title_df.to_csv(report, index = False)
    with open(final_report, 'a', newline = '') as report:
        supp.to_csv(report, index = False)