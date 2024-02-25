import numpy as np 
import pandas as pd
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import tensorflow as tf
import cv2
import datetime

def model():
    disease={'Fungal infection':0,'Allergy':1,'GERD':2,'Chronic cholestasis':3,'Drug Reaction':4,
    'Peptic ulcer diseae':5,'AIDS':6,'Diabetes ':7,'Gastroenteritis':8,'Bronchial Asthma':9,'Hypertension ':10,
    'Migraine':11,'Cervical spondylosis':12,
    'Paralysis (brain hemorrhage)':13,'Jaundice':14,'Malaria':15,'Chicken pox':16,'Dengue':17,'Typhoid':18,'hepatitis A':19,
    'Hepatitis B':20,'Hepatitis C':21,'Hepatitis D':22,'Hepatitis E':23,'Alcoholic hepatitis':24,'Tuberculosis':25,
    'Common Cold':26,'Pneumonia':27,'Dimorphic hemmorhoids(piles)':28,'Heart attack':29,'Varicose veins':30,'Hypothyroidism':31,
    'Hyperthyroidism':32,'Hypoglycemia':33,'Osteoarthristis':34,'Arthritis':35,
    '(vertigo) Paroymsal  Positional Vertigo':36,'Acne':37,'Urinary tract infection':38,'Psoriasis':39,
    'Impetigo':40}

    main_df=pd.read_csv('D:\Directrix\Training.csv')
    lst1=main_df.columns
    lst1=list(lst1[:-2])

    temp=main_df
    temp.replace({'prognosis':disease},inplace=True)
    y=temp['prognosis']

    X_train=tf.convert_to_tensor(main_df[lst1].values)
    Y_train=tf.convert_to_tensor(y.values)

#       MODEL
    model=tf.keras.models.Sequential([
        tf.keras.layers.Dense(1024,activation='leaky_relu'),
        tf.keras.layers.Dense(512,activation='leaky_relu'),
        tf.keras.layers.Dense(256,activation='leaky_relu'),
        tf.keras.layers.Dense(41,activation='softmax')
    ])

    model.compile(
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        metrics=['accuracy']
    )

    history=model.fit(
        x=X_train,
        y=Y_train,
        epochs=6
    )
    return model

def pred(model,X):
    prediction=model.predict(X)
    disease={'Fungal infection':0,'Allergy':1,'GERD':2,'Chronic cholestasis':3,'Drug Reaction':4,
    'Peptic ulcer diseae':5,'AIDS':6,'Diabetes ':7,'Gastroenteritis':8,'Bronchial Asthma':9,'Hypertension ':10,
    'Migraine':11,'Cervical spondylosis':12,
    'Paralysis (brain hemorrhage)':13,'Jaundice':14,'Malaria':15,'Chicken pox':16,'Dengue':17,'Typhoid':18,'hepatitis A':19,
    'Hepatitis B':20,'Hepatitis C':21,'Hepatitis D':22,'Hepatitis E':23,'Alcoholic hepatitis':24,'Tuberculosis':25,
    'Common Cold':26,'Pneumonia':27,'Dimorphic hemmorhoids(piles)':28,'Heart attack':29,'Varicose veins':30,'Hypothyroidism':31,
    'Hyperthyroidism':32,'Hypoglycemia':33,'Osteoarthristis':34,'Arthritis':35,
    '(vertigo) Paroymsal  Positional Vertigo':36,'Acne':37,'Urinary tract infection':38,'Psoriasis':39,
    'Impetigo':40}
    key_lst=list(disease.keys())
    lst=np.round(prediction).tolist()
    if 1. in lst[0]:
        return (key_lst[lst[0].index(1.)],1)
    else:
        return ('',0)

def precaution(X):
    main_df2=pd.read_csv("D:\Directrix2\symptom_precaution.csv")
    for i in range(len(list(main_df2['Disease']))):
        if main_df2['Disease'][i]==X:
            Y=(main_df2['Precaution_1'][i],main_df2['Precaution_2'][i],main_df2['Precaution_3'][i])
    return Y

def description(X):
    main_df3=pd.read_csv("D:\Directrix2\symptom_Description.csv")
    for i in range(len(list(main_df3['Disease']))):
        if main_df3['Disease'][i]==X:
            Y=main_df3['Description'][i]
    return Y

def medicine(X,lst):
    df=pd.read_csv("D:\Directrix2\Medication.csv")
    df2=pd.read_csv("D:\Directrix2\directrix_symptoms_database_01.csv")
    test=''
    med=''
    dosage=''
    s_med=[]
    s_dosage=[]
    for i in range(len(list(df['Diseases']))):
        if df['Diseases'][i]==X:
            test=df['Test Required'][i]
            med=df['Medicine name'][i]
            dosage=df['Dosage'][i]
    for i in range(len(list(df2['SYMPTOMS']))):
        if df2['SYMPTOMS'][i] in lst:
            s_med.append(df2['MEDICINE_NAMES'][i])
            s_dosage.append(df2['DOSAGE'][i])
    return (test,med,dosage,s_med,s_dosage)

def create_figure(dic,s):
    fig = Figure()
    axis = fig.add_subplot(2,1,1)
    X=[]
    Y1=[]
    Y2=[]
    for i in dic:
        Y1.append(int(dic[i][0]))
        Y2.append(int(dic[i][1]))
        X.append(i)
    if s=='blood_press':
        l1="Systolic"
        l2="Diastolic"
    else:
        l1='After  meal'
        l2='Fasting'
    axis.plot(X,Y1,label=l1)
    axis.plot(X,Y2,label=l2)
    axis.legend()
    axis.set_xticks(X)
    axis.set_xticklabels(X, rotation=60, ha='right')
    return fig

    



    

