## Need
* pandas 1.0.5
* numpy 1.18.4
* xgboost 1.1.0
* joblib 0.16.0

## 使用方法
test.ipynb 有詳細用法

## 輸入格式
輸入請參考test資料夾內的資料，一切以資料夾內的為基準。

### Patient

* ID (str) ID，如果沒有，請幫忙填入隨意值，且須與record和inpatient相同
* Gender (str) 性別，身分證可查。
* Birth (pandas._libs.tslibs.timestamps.Timestamp)  出生日期。

### Record

* PatientID  (str)      ID，如果沒有，請幫忙填入隨意值，且須與patient和inpatient相同
* SeqNo           (int)     不知道，目前沒用到，沒有請填空值。
* InDate          (pandas._libs.tslibs.timestamps.Timestamp) 看診日期
* Area            (str)      看診地區

TaipeiCity        
KaohsiungCity      
TaichungCity       
TaoyuanCity        
TainanCity         
NewTaipeiCity      
ChanghuaCounty     
PingtungCounty     
ChiayiCity         
KeelungCity        
ChiayiCounty       
YilanCounty        
HualienCounty      
YunlinCounty       
HsinchuCity        
MiaoliCounty       
HsinchuCounty       
TaitungCounty       
NantouCounty        
PenghuCounty        
KinmenCounty    


* Type (str)      看診類別  0門診 1住院 2 急診，健保資料只有分門診跟住院，沒差，照填。
* ApplyDot        (int)         申請資療點數，健保資料沒有請填0，或是跟實際醫療點數一樣。
* TotalDot       (int)        實際醫療點數
* ICD9CM         (list[int])   疾病，ICD-9，只有三位數，如410。

### Inpatient

* PatientID            (str)      ID，如果沒有，請幫忙填入隨意值，且須與patient和record相同
* SeqNo               (int) 不知道，目前沒用到，沒有請填空值。
*   HospID               (str)      不知道，目前沒用到，沒有請填空值。
*   HospSpecItem         (str)      不知道，目前沒用到，沒有請填空值。
*   AcuteBed             (int)        不知道，目前沒用到，沒有請填空值。
*   ChronicBed           (int)        不知道，目前沒用到，沒有請填空值。
*   TotalBed             (int)        不知道，目前沒用到，沒有請填空值。
*   ICD9CM              (list[int]) 疾病，ICD-9，只有三位數，如410。
*   TranTime            (int) 不知道，目前沒用到，沒有請填空值。
*   TranCode             (str)       不知道，目前沒用到，沒有請填空值。
*  PartDot             (int)        不知道，目前沒用到，沒有請填空值。
*  ApplyDot            (int)         不知道，目前沒用到，沒有請填空值。
*  DayDot              (float)       不知道，目前沒用到，沒有請填空值。
*  TotalDot            (int)        實際醫療點數
*  InDate             (pandas._libs.tslibs.timestamps.Timestamp)  住(進)院日期
*  OutDate            (pandas._libs.tslibs.timestamps.Timestamp) 出院日期
*  InAge               (int) 不知道，目前沒用到，沒有請填空值。
