import pandas as pd

def remove_solo_message(df):
 
    df_filtered = df[df["parent_id"].str.startswith("t3")]
    ids_to_remove = []
    for idx in df_filtered.index:
        if not idx in df['parent_id']:
            ids_to_remove.append(idx)

    df = df[~df["id"].isin(ids_to_remove)]
    df.to_csv('data/Comments_without_standalone.csv')
    

def get_recursive_replies(df, root, id_col="id", parent_col="parent_id"):
    visited = set()
    result = [root]
    root_id = root['id']
    def recurse(current_id):
        children = df[df[parent_col] == 't1_'+current_id]
        for _, row in children.iterrows():
            row_id = row[id_col]
            if row_id not in visited:
                visited.add(row_id)
                result.append(row)
                recurse(row_id)

    recurse(root_id)
    return pd.DataFrame(result),visited
     

def cli():
    # df = pd.read_csv('data/Comments.csv')
    # remove_solo_message(df)
    df_without_standalone = pd.read_csv('data/Comments_without_standalone.csv')
    print(df_without_standalone)
    visited_ids_list = []
    for idx in df_without_standalone.index:
        row = df_without_standalone.loc[idx]
        id_ = row['id']
        if not id_ in visited_ids_list:
            visited_ids_list.append(id_)
            conv,visited_ids = get_recursive_replies(df_without_standalone,row)
            visited_ids_list+=visited_ids
            print(conv)
            if len(conv)>1:
                conv.to_csv('data/conversations/'+id_+'.csv')


    


