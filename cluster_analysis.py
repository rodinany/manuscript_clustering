import os
import numpy as np
import pandas as pd

similarity_df = pd.read_excel(os.path.join(os.getcwd(), '.', 'matrixes_no_F.п.I.6.xlsx'),
                              sheet_name='similarity_matrix_unordened', index_col=0)
similarity_df.index = range(0, len(similarity_df))

triangle_values = np.triu(similarity_df, k=1)
triangle_df = pd.DataFrame(data=triangle_values, index=similarity_df.columns, columns=similarity_df.columns)
similarity_percents = list(set(triangle_values[np.triu_indices(len(similarity_df), k = 1)]))
similarity_percents = sorted(similarity_percents, reverse=True)

manuscripts_pairs = []
for percent in similarity_percents:
    manuscripts = list(zip(*np.where(triangle_df.values == percent)))
    manuscripts_pairs.extend(manuscripts)

clusters = []
# в этом множестве содержатся номера всех рукописей, которые уже находятся в каком-либо из кластеров
clustered_ms = set()

for pair in manuscripts_pairs:

  if pair[0] not in clustered_ms and pair[1] not in clustered_ms:
     cluster = [pair[0], pair[1]]
     clusters.append(cluster)
     clustered_ms.update([pair[0], pair[1]])

  elif pair[0] in clustered_ms and pair[1] not in clustered_ms:
     for x in range(len(clusters)):
        if pair[0] in clusters[x]:
           clusters[x].append(pair[1])
           clustered_ms.add(pair[1])

  elif pair[0] not in clustered_ms and pair[1] in clustered_ms:
     for x in range(len(clusters)):
        if pair[1] in clusters[x]:
           clusters[x].append(pair[0])
           clustered_ms.add(pair[0])

clustered_mss = []
for cluster in clusters:
    clustered_mss.append([])
    for ms in cluster:
        clustered_mss[-1].append(similarity_df.columns[ms])
for cluster in clustered_mss:
    print(cluster)

clusters = [ms for cluster in clusters for ms in cluster]
sorted_df = pd.DataFrame(columns=range(0, len(similarity_df)))
for ms in clusters:
    sorted_df.loc[len(sorted_df.index)] = list(similarity_df.iloc[ms])
sorted_df = sorted_df[clusters]

sorted_df.columns = [similarity_df.columns[i] for i in clusters]
sorted_df.index = [similarity_df.columns[i] for i in clusters]

# writing down an ordened and clustered similarity matrix
# with pd.ExcelWriter('matrixes_no_F.п.I.6.xlsx', mode='a') as writer:
#     sorted_df.to_excel(writer, sheet_name='similarity_matrix_ordened')