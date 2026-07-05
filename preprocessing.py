
import re
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

stemmer=StemmerFactory().create_stemmer()

KAMUS_NORMALISASI={
    "gk":"tidak",
    "ga":"tidak",
    "udh":"sudah",
    "telat":"terlambat",
    "ilang":"hilang",
    "cs":"customer_service",
}

STOPWORDS_CUSTOM={
    "jne","jnt","sicepat","anteraja",
}

def cleansing(text):
    text=str(text).lower()
    text=re.sub(r"(https?://\S+|www\.\S+)"," ",text)
    text=re.sub(r"[@#]\w+"," ",text)
    text=re.sub(r"[^\w\s]"," ",text)
    text=re.sub(r"\d+"," ",text)
    text=re.sub(r"\s+"," ",text).strip()
    return text

def normalisasi(text):
    for k,v in sorted(KAMUS_NORMALISASI.items(), key=lambda x:-len(x[0])):
        text=re.sub(r"\b"+re.escape(k)+r"\b",v,text)
    return text

def preprocess(text):
    text=cleansing(text)
    text=normalisasi(text)
    tokens=text.split()
    tokens=[t for t in tokens if t not in STOPWORDS_CUSTOM and len(t)>2]
    tokens=[stemmer.stem(t) for t in tokens]
    return tokens
