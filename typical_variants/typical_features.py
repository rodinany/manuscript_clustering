import itertools
import os
import pandas as pd
import styleframe as sf


def variants_percentage(clusters, variants_df):
    variants_percents = []
    for index, row in variants_df.iterrows():
        variants_percents.append({x: [] for x in set(row)})
        for cluster in clusters:
            for i in variants_percents[-1]:
                count = list(row[cluster]).count(i)
                variants_percents[-1][i].append(int(count / len(cluster) * 100))

    return variants_percents


def typical_features(variants_percents):
    features = []
    for i in range(len(variants_percents)):
        row = variants_percents[i]
        for value in row:
            if value:
                num_cluster = row[value].index(max(row[value]))
                rest_values = row[value][:num_cluster] + row[value][num_cluster + 1:]
                if max(row[value]) >= 80 and not [x for x in rest_values if x >= 80]:
                    features.append((i, num_cluster))

    features = sorted(features, key=lambda x: x[1])
    clusters_features = {}
    it = itertools.groupby(features, lambda x: x[1])
    for cluster, subiter in it:
        clusters_features[cluster] = [unit[0] for unit in subiter]

    return clusters_features

def colour_features(features, clusters, variants_df):
    variants_sf = sf.StyleFrame(variants_df)
    for i in features:
        variants_sf = variants_sf.apply_style_by_indexes(
            indexes_to_style=features[i],
            cols_to_style=clusters[i],
            styler_obj=sf.Styler(bg_color='92CDDC'))
    return variants_sf


df = pd.read_excel(os.path.join(os.getcwd(), '..', 'matrixes_no_F.п.I.6.xlsx'),
                   sheet_name='full_variants_matrix')
variant_units_df = df.iloc[:, 0]
variants_df = df.iloc[:, 1:-6]

clusters = [[]]
with open(os.path.join(os.getcwd(), '..', 'clusters.txt'), encoding='utf-8') as file:
    for line in file:
        if line != '\n':
            clusters[-1].append(line.split())
        else:
            clusters.append([])

ordered_mss = [ms for main_cluster in clusters for small_cluster in main_cluster for ms in small_cluster]
main_clusters = [[ms for small_cluster in main_cluster for ms in small_cluster] for main_cluster in clusters]
small_clusters = [small_cluster for main_cluster in clusters for small_cluster in main_cluster]



variants_df = variants_df[ordered_mss]
features_indexes = set()

mc_variants_percents = variants_percentage(main_clusters, variants_df)
mc_features = typical_features(mc_variants_percents)
mc_features_indexes = []
for value in mc_features.values():
    mc_features_indexes.extend(value)
features_indexes = features_indexes.union(set(mc_features_indexes))
mc_variants_sf = colour_features(mc_features, main_clusters, variants_df)
print(mc_features)

with sf.StyleFrame.ExcelWriter('all_features.xlsx') as writer:
    mc_variants_sf.to_excel(writer, sheet_name='main_clusters')

for i in mc_features:
    mc_features_df = variants_df[main_clusters[i]].iloc[mc_features[i]]
    mc_features_df = pd.merge(variant_units_df, mc_features_df, left_index=True, right_index=True)
    if i == 0:
        with pd.ExcelWriter('mc_features.xlsx') as writer:
            mc_features_df.to_excel(writer, sheet_name=f'{i+1}_cluster')
    else:
        with pd.ExcelWriter('mc_features.xlsx', mode='a') as writer:
            mc_features_df.to_excel(writer, sheet_name=f'{i+1}_cluster')

sc_variants_percents = variants_percentage(small_clusters, variants_df)
sc_features = typical_features(sc_variants_percents)
mc_features_indexes = []
for value in sc_features.values():
    mc_features_indexes.extend(value)
features_indexes = features_indexes.union(set(mc_features_indexes))
sc_variants_sf = colour_features(sc_features, small_clusters, variants_df)

with sf.StyleFrame.ExcelWriter('all_features.xlsx', mode='a') as writer:
    sc_variants_sf.to_excel(writer, sheet_name='small_clusters')

for i in sc_features:
    sc_features_df = variants_df[small_clusters[i]].iloc[sc_features[i]]
    sc_features_df = pd.merge(variant_units_df, sc_features_df, left_index=True, right_index=True)
    if i == 0:
        with pd.ExcelWriter('sc_features.xlsx') as writer:
            sc_features_df.to_excel(writer, sheet_name=f'{small_clusters[i][0]}_{small_clusters[i][-1]}')
    else:
        with pd.ExcelWriter('sc_features.xlsx', mode='a') as writer:
            sc_features_df.to_excel(writer, sheet_name=f'{small_clusters[i][0]}_{small_clusters[i][-1]}')

features_indexes = list(features_indexes)
features_indexes.sort()
with open('features_indexes.txt', 'w') as file:
    file.write(' '.join(str(index) for index in features_indexes))