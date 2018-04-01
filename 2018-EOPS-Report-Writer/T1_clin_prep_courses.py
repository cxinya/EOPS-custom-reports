# How well did courses prepare you for clinical rotations?

def create_cp_courses(pd, np, file, program, final_report, csv):

    # Create clin_prep dataframe

    df = pd.read_csv(file)

    cp_courses_df = df[['ProgramID','ClinPrep_Anatomy',
                    'ClinPrep_Biochem',
                    'ClinPrep_Biostat',
                    'ClinPrep_ClinExp',
                    'ClinPrep_ClinMed',
                    'ClinPrep_ClinSkill',
                    'ClinPrep_Ethics',
                    'ClinPrep_Gene',
                    'ClinPrep_EBM',
                    'ClinPrep_Lab',
                    'ClinPrep_Microbio',
                    'ClinPrep_Neuro',
                    'ClinPrep_History',
                    'ClinPrep_Patho',
                    'ClinPrep_Pharm',
                    'ClinPrep_Exam',
                    'ClinPrep_Physio',
                    'ClinPrep_Service']]
    cp_courses_df = cp_courses_df.loc[cp_courses_df['ProgramID'] == program].drop(['ProgramID'], axis = 1)

    # Value labels: 1 = not at all well to 4 = extremely well, 5 = did not take (NA)

    # Remove "Did not take"

    cp_courses_df = cp_courses_df.replace(5, np.NaN)

    # Table

    cp_courses = cp_courses_df.agg(["count", "mean", "median"]).transpose().reset_index()

    # Tidy up

    cp_courses.columns = ["Course", "n", "Mean", "Median"]
    cp_courses["n"] = cp_courses["n"].apply(lambda x: int(x))
    cp_courses["Mean"] = cp_courses["Mean"].apply(lambda x: round(x, 2))
    cp_courses["Course"].replace({'ClinPrep_Anatomy': 'Anatomy',
                                'ClinPrep_Biochem': 'Biochemistry',
                                'ClinPrep_Biostat': 'Biostatistics/Epidemiology',
                                'ClinPrep_ClinExp': 'Clinical experiences during the didactic portion of the curriculum',
                                'ClinPrep_ClinMed': 'Clinical medicine (includes surgery/emergency medicine/peds/ OB/GYN/behavioral health)',
                                'ClinPrep_ClinSkill': 'Clinical/Technical skills',
                                'ClinPrep_Ethics': 'Ethics/Bioethics',
                                'ClinPrep_Gene': 'Genetics',
                                'ClinPrep_EBM': 'Interpretation of literature/Evidence-based medicine/Research',
                                'ClinPrep_Lab': 'Lab interpretation/Diagnosis',
                                'ClinPrep_Microbio': 'Microbiology',
                                'ClinPrep_Neuro': 'Neuroscience',
                                'ClinPrep_History': 'Patient communication skills/History taking',
                                'ClinPrep_Patho': 'Pathology/Pathophysiology',
                                'ClinPrep_Pharm': 'Pharmacology',
                                'ClinPrep_Exam': 'Physical examinations/Patient assessment',
                                'ClinPrep_Physio': 'Physiology',
                                'ClinPrep_Service': 'Service learning'}, inplace = True
                                )

    # Title
    title = "How well did courses prepare you for clinical rotations?"
    title_df = pd.DataFrame({'': title.upper()}, index = [0])

    # Write to report
    with open(final_report, 'a', newline = '') as report:
        title_df.to_csv(report, index = False)
    with open(final_report, 'a', newline = '') as report:
        cp_courses.to_csv(report, index = False)