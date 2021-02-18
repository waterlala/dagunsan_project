import pandas as pd
import numpy as np


class get_data_library:
    def __init__(self, patient, record, inpatient):
        self.p = patient
        self.r = record
        self.i = inpatient

    def copy_data(self):
        return self.p.copy(), self.r.copy(), self.i.copy()

    def get_confirm_410_date(self):
        patients, records, inpatients = self.copy_data()
        records['is410'] = records['ICD9CM'].apply(lambda x: True
                                                   if 410 in x else False)
        records = records[records['is410']]
        records = records.sort_values('InDate').reset_index(drop=True)
        records = records.drop('is410', axis=1)
        records = records[records['Type'] != 0]
        records = records.drop_duplicates('ID', 'first')
        patients = pd.merge(patients, records[['ID', 'InDate']], on='ID')
        patients = patients.rename(columns={'InDate': '410_date'})
        output = patients[['ID', '410_date']]
        return output

    def get_survival_time(self):
        patients, records, inpatients = self.copy_data()
        patients_410 = self.get_confirm_410_date()
        patients = pd.merge(patients, patients_410, on='ID')
        records.sort_values('InDate', ascending=False)
        records = records.drop_duplicates(subset=['ID'], keep='last')
        records = records.reset_index(drop=True)
        patients = pd.merge(patients, records[['ID', 'InDate']], on='ID')
        patients = patients.rename(columns={'InDate': 'Last_record'})
        patients['Last_record_to_410'] = patients['Last_record'] - patients[
            '410_date']
        patients['Death_to_410'] = patients['Death'] - patients['410_date']
        patients['Last_record_to_410'] = patients['Last_record_to_410'].apply(
            lambda x: x.days)
        patients['Death_to_410'] = patients['Death_to_410'].apply(
            lambda x: x.days)
        output = patients[['ID','Last_record', 'Last_record_to_410', 'Death_to_410']]
        return output

    def get_confirm_area(self):
        patients, records, inpatients = self.copy_data()
        patients_410 = self.get_confirm_410_date()
        patients = pd.merge(patients, patients_410, on='ID')
        df = pd.merge(records, patients[['ID', '410_date']], on='ID')
        df['different'] = df['InDate'] - df['410_date']
        df['different'] = df['different'].apply(lambda x: x.days)
        df = df[(df['different'] >= 0) & (df['different'] <= 7)]

        def get_area(x):
            s_df = df[df['ID'] == x]
            return s_df['Area'].value_counts().sort_values(
                ascending=False).index[0]

        patients['area'] = patients['ID'].apply(get_area)
        output = patients[['ID', 'area']]
        return output

    def get_confirm_month(self):
        patients, records, inpatients = self.copy_data()
        patients_410 = self.get_confirm_410_date()
        patients = pd.merge(patients, patients_410, on='ID')
        patients['confirm_month'] = patients['410_date'].apply(
            lambda x: x.month)
        output = patients[['ID', 'confirm_month']]
        return output

    def get_confirm_age(self):
        patients, records, inpatients = self.copy_data()
        patients_410 = self.get_confirm_410_date()
        patients = pd.merge(patients, patients_410, on='ID')
        patients['confirm_age'] = patients['410_date'] - patients['Birth']
        patients['confirm_age'] = patients['confirm_age'].apply(
            lambda x: x.days / 365)
        output = patients[['ID', 'confirm_age']]
        return output

    def data_is_x_to_confirm_day(self, key0, key1=0):
        patients, records, inpatients = self.copy_data()
        patients_410 = self.get_confirm_410_date()
        records = pd.merge(records, patients_410, on='ID')
        records['different'] = records['410_date'] - records['InDate']
        records['different'] = records['different'].apply(lambda x: x.days)
        inpatients = pd.merge(inpatients, patients_410, on='ID')
        inpatients['different'] = inpatients['410_date'] - records['InDate']
        inpatients['different'] = inpatients['different'].apply(
            lambda x: x.days)

        if key0 == '<':
            records = records[(records['different'] > 0)
                              & (records['different'] < key1)]
            inpatients = inpatients[(inpatients['different'] > 0)
                                    & (inpatients['different'] < key1)]
        elif key0 == '<=':
            records = records[(records['different'] >= 0)
                              & (records['different'] < key1)]
            inpatients = inpatients[(inpatients['different'] >= 0)
                                    & (inpatients['different'] < key1)]
        elif key0 == '>':
            records = records[(records['different'] < 0)]
            inpatients = inpatients[(inpatients['different'] < 0)]
        elif key0 == '>=':
            records = records[(records['different'] <= 0)]
            inpatients = inpatients[(inpatients['different'] <= 0)]
        elif key0 == '==':
            records = records[(records['different'] == 0)]
            inpatients = inpatients[(inpatients['different'] == 0)]

        records = records.drop(['different', '410_date'], axis=1)
        records = records.reset_index(drop=True)
        inpatients = inpatients.drop(['different', '410_date'], axis=1)
        inpatients = inpatients.reset_index(drop=True)
        return patients, records, inpatients

    def get_confirm_icd(self):
        patients, records, inpatients = self.data_is_x_to_confirm_day('==')

        def get_icd(x):
            s_df = records[records['ID'] == x]
            if len(s_df) != 0:
                out = list(s_df['ICD9CM'])
                out = str(out)
                out = out.replace('[', '').replace(']', '')
                out = eval(out)
                if type(out) == int:
                    k = list()
                    k.append(out)
                    out = k
                else:
                    out = list(out)
                out = list(out)
            else:
                return np.nan
            return out

        patients['confirm_icd'] = patients['ID'].apply(get_icd)
        patients = patients[pd.notnull(patients['confirm_icd'])]
        output = patients[['ID', 'confirm_icd']]
        return output

    # 0門診 1住院 2急診
    def get_confirm_type(self):
        patients, records, inpatients = self.copy_data()
        patients_410 = self.get_confirm_410_date()
        patients = pd.merge(patients, patients_410, on='ID')

        df = pd.merge(records, patients[['ID', '410_date']], on='ID')
        df = df[df['InDate'] == df['410_date']]
        df = df[['ID', 'Type']]
        records = df

        for i in range(3):
            m_df = records[records['Type'] == i]
            m_df['Type'] = 1
            a = pd.merge(patients[['ID']], m_df, on='ID',
                         how='left').drop_duplicates()
            a = a[['ID', 'Type']]
            a = a.rename(columns={'Type': 'confirm_type_' + str(i)})
            patients = pd.merge(patients, a, on='ID', how='left')

        patients = patients[[
            'ID', 'confirm_type_0', 'confirm_type_1', 'confirm_type_2'
        ]].fillna(0)
        patients['confirm_type_0'] = patients['confirm_type_0'].astype('int64')
        patients['confirm_type_1'] = patients['confirm_type_1'].astype('int64')
        patients['confirm_type_2'] = patients['confirm_type_2'].astype('int64')
        output = patients
        return output

    def get_gender(self):
        patients, records, inpatients = self.copy_data()
        patients = patients.rename(columns={'Gender': 'gender'})
        output = patients[['ID', 'gender']]
        return output

    def get_history_type_times(self):
        patients, records, inpatients = self.data_is_x_to_confirm_day('<', 3 * 365)
        def get_history_type(row):
            s_df = records[records['ID'] == row['ID']]
            df = s_df['Type'].value_counts()
            save_list = list(df.reset_index()['index'])
            row['history_ou_times'] = 0
            row['history_em_times'] = 0
            row['history_in_times'] = 0
            if 0 in save_list:
                row['history_ou_times'] = df[0]
            if 1 in save_list:
                row['history_in_times'] = df[1]
            if 2 in save_list:
                row['history_em_times'] = df[2]
            return row
        patients = patients.apply(get_history_type,axis = 1)
        output = patients[['ID','history_ou_times','history_em_times','history_in_times']]
        return output
    
    def get_history_icd(self):
        patients, records, inpatients = self.data_is_x_to_confirm_day('<', 3 * 365)
        def get_icd(x):
            s_df = records[records['ID']==x]
            if len(s_df)!= 0:
                out = list(s_df['ICD9CM'])
                out = str(out)
                out = out.replace('[','').replace(']','')
                out = eval(out)
                if type(out) == int:
                    k = list()
                    k.append(out)
                    out = k
                else:
                    out = list(out)
                out = list(set(out))
            else:
                return np.nan
            return out
        patients['history_icd'] = patients['ID'].apply(get_icd)
        output = patients[['ID','history_icd']]
        return output
    
    def get_confirm_icd(self):
        patients, records, inpatients = self.data_is_x_to_confirm_day('==')
        def get_icd(x):
            s_df = records[records['ID']==x]
            if len(s_df)!= 0:
                out = list(s_df['ICD9CM'])
                out = str(out)
                out = out.replace('[','').replace(']','')
                out = eval(out)
                if type(out) == int:
                    k = list()
                    k.append(out)
                    out = k
                else:
                    out = list(out)
                out = list(out)
            else:
                return np.nan
            return out
        patients['confirm_icd'] = patients['ID'].apply(get_icd)
        output = patients[['ID','confirm_icd']]
        return output
    
    def get_after_confirm_icd(self):
        patients, records, inpatients = self.data_is_x_to_confirm_day('>')
        def get_icd(x):
            s_df = records[records['ID']==x]
            if len(s_df)!= 0:
                out = list(s_df['ICD9CM'])
                out = str(out)
                out = out.replace('[','').replace(']','')
                out = eval(out)
                if type(out) == int:
                    k = list()
                    k.append(out)
                    out = k
                else:
                    out = list(out)
                out = list(out)
            else:
                return np.nan
            return out
        patients['after_confirm_icd'] = patients['ID'].apply(get_icd)
        output = patients[['ID','after_confirm_icd']]
        return output
    
    def get_history_me(self):
        patients, records, inpatients = self.data_is_x_to_confirm_day('<', 3 * 365)
        
        
        def get_me(x):
            
            s_df= inpatients[inpatients['ID']==x]
            s_df = s_df[pd.notnull(s_df['Drug'])]
            if len(s_df)!= 0 and str(s_df)!='nan':
                out = list(s_df['Drug'])
                out = str(out)
                out = out.replace('[','').replace(']','')
                out = eval(out)
                if type(out) == int:
                    k = list()
                    k.append(out)
                    out = k
                else:
                    out = list(out)
                out = list(out)
                return out
            else:
                return np.nan
        patients['history_me'] = patients['ID'].apply(get_me)
        output = patients[['ID','history_me']]
        return output
    
    def get_history_total_dot(self):
        patients, records, inpatients = self.data_is_x_to_confirm_day('<', 3 * 365)
        def get_history_dot(x):
            s_df = records[records['ID']==x]
            return s_df['TotalDot'].sum()
        patients['history_dot'] = patients['ID'].apply(get_history_dot)
        output = patients[['ID','history_dot']]
        return output
    
    
    
    
    
    
    
    