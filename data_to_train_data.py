import pandas as pd
import numpy as np
import pickle
from get_data_library import get_data_library as gl

class data_to_train_data:
    def __init__(self):
        pass

    def fit(self, p, r, i):
        r = r[r['Type']!=0]
        get_data_library = gl(p, r, i)
        df = get_data_library.get_confirm_area()
        df = pd.merge(df,get_data_library.get_confirm_month(),on = 'ID')
        df = pd.merge(df,get_data_library.get_confirm_age(),on = 'ID')
        df = pd.merge(df,get_data_library.get_confirm_icd(),on = 'ID')
        df = pd.merge(df,get_data_library.get_confirm_type(),on = 'ID')
        df = pd.merge(df,get_data_library.get_gender(),on = 'ID')
        df = pd.merge(df,get_data_library.get_history_icd(),on = 'ID')
        df = pd.merge(df,get_data_library.get_history_me(),on = 'ID')
        df = pd.merge(df,get_data_library.get_history_total_dot(),on = 'ID')
        df = pd.merge(df,get_data_library.get_history_type_times(),on = 'ID')
        open_file = open('./need_list.pickle', "rb")
        loaded_list = pickle.load(open_file)
        open_file.close()
        train_data = pd.DataFrame(columns = loaded_list)
        train_data.loc[0] = np.nan
        train_data.loc[0].ID = df.loc[0].ID
        train_data.loc[0].confirm_type_0 = df.loc[0].confirm_type_0
        train_data.loc[0].confirm_type_1 = df.loc[0].confirm_type_1
        train_data.loc[0].confirm_type_2 = df.loc[0].confirm_type_2
        train_data.loc[0].confirm_age = df.loc[0].confirm_age
        train_data.loc[0].history_ou_times = df.loc[0].history_ou_times
        train_data.loc[0].history_em_times = df.loc[0].history_em_times
        train_data.loc[0].history_in_times = df.loc[0].history_in_times
        train_data.loc[0].history_dot = df.loc[0].history_dot
        train_data.loc[0]['confirm_month_'+str(df.loc[0].confirm_month)] = 1
        train_data.loc[0]['area_'+str(df.loc[0].area)] = 1
        train_data.loc[0]['gender_'+str(df.loc[0].gender)] = 1
        for icd in df.loc[0].confirm_icd:
            train_data.loc[0]['confirm_icd_'+str(icd)] = 1
        for icd in df.loc[0].history_icd:
            train_data.loc[0]['history_icd_'+str(icd)] = 1
        for icd in df.loc[0].history_me:
            train_data.loc[0]['history_me_'+str(icd)] = 1
        train_data = train_data.fillna(0)
        train_data = train_data.drop('ID',axis = 1)
        return train_data