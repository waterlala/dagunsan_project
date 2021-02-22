import pandas as pd
import numpy as np

class simple_train_data:
    def __init__(self):
        pass

    def fit(self, input_patients, input_records, input_inpatients):
        p = input_patients
        r = input_records.drop(['SeqNo','ApplyDot'],axis = 1)
        r = r.rename(columns = {'PatientID':'ID'})
        r['Type'] = r['Type'].astype('int64')
        i = input_inpatients.rename(columns = {'PatientID':'ID'})
        i = i[['ID','ICD9CM','InDate','OutDate']]
        return p, r, i