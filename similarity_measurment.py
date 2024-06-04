import os
import pandas as pd

var_df = pd.read_excel(os.path.join(os.getcwd(), '.', 'matrixes_no_F.п.I.6.xlsx'),
                       sheet_name='variants_matrix')


# calculating similarity measure for every two pairs of manuscripts
def similarity_measure(df):
    columns = list(df.columns)
    similarity_df = pd.DataFrame()
    for column in columns:
        sim_percents = []
        for i in range(len(columns)):
            if column != columns[i]:
                var_pairs = list(zip(var_df[column], var_df[columns[i]]))
                # the amount of nodes with identical values
                equal_nodes = 0
                # the amount of nodes with values other than zero
                nonzero_nodes = 0
                for i in var_pairs:
                    if i[0] and i[1]:
                        nonzero_nodes += 1
                        if i[0] == i[1]:
                            equal_nodes += 1
                t = (equal_nodes / nonzero_nodes) * 100
                sim_percents.append(round(t))
            else:
                t = 0
                sim_percents.append(t)
        similarity_df[column] = sim_percents
    similarity_df.index = columns
    return similarity_df


similarity_df = similarity_measure(var_df)
print(similarity_df)

# writing down an original unordened similarity matrix
with pd.ExcelWriter('matrixes_no_F.п.I.6.xlsx', mode='a') as writer:
     similarity_df.to_excel(writer, sheet_name='similarity_matrix_unordened')