## Need
* pandas 1.0.5
* numpy 1.18.4
* xgboost 1.1.0
* joblib 0.16.0

## 使用方法
test.ipynb 有詳細用法

## 輸入格式
輸入請參考test資料夾內的資料，一切以資料夾內的為基準(學姊給的資料)

### Patient

* ID (str) 如果沒有，請幫忙填入隨意值，且須與record和inpatient相同
* Gender (str)
* Birth (pandas._libs.tslibs.timestamps.Timestamp)

### Record

* PatientID  (str)      
* SeqNo           (int)        目前沒用到，沒有請填空值。
* InDate          (pandas._libs.tslibs.timestamps.Timestamp)
* Area            (str)      
* Type (str)      
* ApplyDot        (int)         
* TotalDot       (int)        
* ICD9CM         (list[int])   

### Inpatient

* PatientID            (str)      
* SeqNo               (int) 目前沒用到，沒有請填空值。
*   HospID               (str)      目前沒用到，沒有請填空值。
*   HospSpecItem         (str)      目前沒用到，沒有請填空值。
*   AcuteBed             (int)        目前沒用到，沒有請填空值。
*   ChronicBed           (int)        目前沒用到，沒有請填空值。
*   TotalBed             (int)        目前沒用到，沒有請填空值。
*   ICD9CM              (list[int])
*   TranTime            (int) 目前沒用到，沒有請填空值。
*   TranCode             (str)       目前沒用到，沒有請填空值。
*  PartDot             (int)        目前沒用到，沒有請填空值。
*  ApplyDot            (int)         目前沒用到，沒有請填空值。
*  DayDot              (float)       目前沒用到，沒有請填空值。
*  TotalDot            (int)        
*  InDate             (pandas._libs.tslibs.timestamps.Timestamp)
*  OutDate            (pandas._libs.tslibs.timestamps.Timestamp)
*  InAge               (int) 目前沒用到，沒有請填空值。
*  Drug               (list[int])
