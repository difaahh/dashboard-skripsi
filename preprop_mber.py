import re

KAMUS_NORMALISASI={
    "gk":"tidak",
    "ga":"tidak",
    "udh":"sudah",
    "telat":"terlambat",
    "ilang":"hilang",
    "cs":"customer_service",
}

SW_SET={
    "jne","jnt","sicepat","anteraja",
}


# KAMUS_NORMALISASI
# (paste kamus lengkapmu di sini)

# SW_SET
# (hasil bangun_sw_set())

def normalisasi_teks(teks):
    if not isinstance(teks, str):
        return ""

    sorted_kamus = sorted(
        KAMUS_NORMALISASI.items(),
        key=lambda x: -len(x[0])
    )

    for k, v in sorted_kamus:
        teks = re.sub(
            r"\b" + re.escape(k) + r"\b",
            v,
            teks
        )

    return teks


def bersihkan_mbert(teks):

    if not isinstance(teks, str):
        return ""

    teks = teks.lower()

    teks = re.sub(r"http\S+|www\S+", " ", teks)
    teks = re.sub(r"@\w+", " ", teks)
    teks = re.sub(r"#\w+", " ", teks)
    teks = re.sub(r"[^a-zA-Z\s_]", " ", teks)
    teks = re.sub(r"\s+", " ", teks).strip()

    teks = normalisasi_teks(teks)

    token = [
        w
        for w in teks.split()
        if w not in SW_SET and len(w) > 2
    ]

    return " ".join(token)