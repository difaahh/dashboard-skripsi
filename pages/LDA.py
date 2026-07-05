import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="LDA",
    page_icon="💬",
    layout="wide"
)


###########################


#################
with st.sidebar:

    # st.image("assets/logo.png", width=90)

    st.markdown(
        "<h2 style='text-align:center;'>DASHBOARD</h2>",
        unsafe_allow_html=True
    )

    # st.caption("Analisis Aduan Ekspedisi")

    st.divider()

    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("Dashboard.py")

    if st.button("💬 LDA", use_container_width=True):
        st.switch_page("pages/LDA.py")

    if st.button("🗃️ mBERT", use_container_width=True):
        st.switch_page("pages/mBERT.py")

    if st.button("🕊️ Analisis", use_container_width=True):
        st.switch_page("pages/Analisis Tweet.py")

st.markdown("""
        <style>

        section[data-testid="stSidebar"]{
            background:#DED8FF !important;
        }

        section[data-testid="stSidebar"] .stButton>button{

            height:52px;
            border-radius:12px;
            border:1px solid #D9E2EC;
            background:white;
            color:#374151;
            font-size:25px;
            font-weight:600;
            text-align:left;
        }

        section[data-testid="stSidebar"] .stButton>button:hover{

            background:#EDE9FE;
            color:#6D28D9;
            border:1px solid #8B5CF6;

        }

        </style>
        """, unsafe_allow_html=True)

#############

col1,col2=st.columns([0.06,0.94],vertical_alignment="center")

with col1:
    st.image("assets/icon_lda.png",width=45)

with col2:
    st.markdown("## Topic Modeling LDA")

st.caption("""
Halaman ini menampilkan hasil pemodelan topik menggunakan
Latent Dirichlet Allocation (LDA) dengan perbandingan
representasi Bag of Words (BoW) dan TF-IDF.
""")

st.divider()
#############################

# ==========================================================
# MEMBUAT DATA TOP WORDS UNTUK DASHBOARD
# ==========================================================

import re
import pandas as pd

# membaca sheet top words yang sudah dibuat


EXCEL_PATH="data/OUTPUT_LDA/LDA_Output_Lengkap.xlsx"
summary=pd.read_excel(EXCEL_PATH,sheet_name="Perbandingan_Model")

st.markdown("""
<style>

/* Hilangkan tulisan "Pilih Representasi" */
div[data-testid="stRadio"] label{
    font-weight:600;
    color:#1E3A8A;
}

/* Background seluruh radio */
div[role="radiogroup"]{
    background:#F8FAFC;
    border:1px solid #DBEAFE;
    border-radius:12px;
    padding:8px;
}

/* Jarak tiap pilihan */
div[role="radiogroup"] > label{
    padding:8px 18px;
    border-radius:10px;
    transition:0.2s;
}

/* Hover */
div[role="radiogroup"] > label:hover{
    background:#DBEAFE;
}

</style>
""", unsafe_allow_html=True)

st.markdown("### 🔎 Representasi Dokumen")

representasi=st.radio("Pilih Representasi",["Semua","BoW","TF-IDF"],horizontal=True)

MODEL_CONFIG={
"LDA-BoW-NoStem":{"dist":"Dist_BoW_NoStem","top":"TopWords_BoW_NoStem","label":"Label_BoW_NoStem","tweet":"Keluhan_BoW_NoStem", "pylda":"assets/pyLDAvis_LDA-BoW-NoStem.html"},
"LDA-BoW-Stem":{"dist":"Dist_BoW_Stem","top":"TopWords_BoW_Stem","label":"Label_BoW_Stem","tweet":"Keluhan_BoW_Stem", "pylda":"assets/pyLDAvis_LDA-BoW-Stem.html"},
"LDA-TFIDF-NoStem":{"dist":"Dist_TFIDF_NoStem","top":"TopWords_TFIDF_NoStem","label":"Label_TFIDF_NoStem","tweet":"Keluhan_TFIDF_NoStem","pylda":"assets/pyLDAvis_LDA-TFIDF-NoStem.html"},
"LDA-TFIDF-Stem":{"dist":"Dist_TFIDF_Stem","top":"TopWords_TFIDF_Stem","label":"Label_TFIDF_Stem","tweet":"Keluhan_TFIDF_Stem","pylda":"assets/pyLDAvis_LDA-TFIDF-Stem.html"},
}
# 
st.divider()
# ==========================================================
# Fungsi untuk menampilkan seluruh hasil satu model LDA
# Contoh pemanggilan:
# show_model("LDA-BoW-Stem")
# ==========================================================

def show_model(name):
    # -----------------------------------------
    # Mengambil konfigurasi sheet sesuai model
    # Misal:
    # LDA-BoW-Stem ->
    # Dist_BoW_Stem
    # TopWords_BoW_Stem
    # Label_BoW_Stem
    # Keluhan_BoW_Stem
    # -----------------------------------------

    cfg = MODEL_CONFIG[name]
    # -----------------------------------------
    # Mengambil ringkasan performa model
    # dari sheet "Perbandingan_Model"
    # -----------------------------------------

    row = summary.loc[summary["Model"] == name].iloc[0]
    # -----------------------------------------
    # Judul Model
    # -----------------------------------------

    st.subheader(name)
    # -----------------------------------------
    # Membuat 4 kolom untuk menampilkan
    # metrik evaluasi model
    # -----------------------------------------

    st.markdown("""
            <style>

            /* Card Metric */
            div[data-testid="stMetric"]{
                background: #EFF6FF;
                border: 1px solid #BFDBFE;
                padding: 15px;
                border-radius: 14px;
                text-align: center;
            }

            /* Judul Metric */
            div[data-testid="stMetric"] label{
                color:#2563EB !important;
                font-weight:600;
                font-size:15px;
            }

            /* Nilai Metric */
            div[data-testid="stMetricValue"]{
                color:#1D4ED8 !important;
                font-size:32px;
                font-weight:bold;
            }

            </style>
            """, unsafe_allow_html=True)
    


    c1, c2, c3, c4 = st.columns(4)
    with c1:
        with st.container():
            c1.metric(
                "Coherence",
                f"{row['Coherence']:.4f}"
            )

    with c2:
        with st.container():
            c2.metric(
                "Log Perplexity",
                f"{row['Log Perplexity']:.4f}"
            )

    with c3:
        with st.container():
            c3.metric(
                "Topic Diversity",
                f"{row['Topic Diversity']:.3f}"
            )

    with c4:
        with st.container():
            c4.metric(
                "Jumlah Topik",
                int(row["Jumlah Topik"])
            )

    # =====================================================
    # DISTRIBUSI TOPIK
    # =====================================================

    # Membaca sheet distribusi sesuai model
    
    dist = pd.read_excel(EXCEL_PATH,sheet_name=cfg["dist"])

    # Membuat grafik batang menggunakan Plotly
    st.subheader("📊 Distribusi Jumlah Tweet per Topik")
    with st.container(border=True):
        fig = px.bar(
            dist,x="Topic", y="Jumlah_Dokumen", color="Jumlah_Dokumen", text="Jumlah_Dokumen",
            hover_data=["Persentase (%)"],
            # nanti kita ganti Blues
            color_continuous_scale="Blues"
        )

        # Mengatur tampilan grafik
        fig.update_layout(
            template="plotly_white",
            height=420,
            title="Distribusi Jumlah Tweet per Topik",
            title_x=0.5
        )

        # Menampilkan grafik
        st.plotly_chart(fig, use_container_width=True)

    # # =====================================================
    # # TOP WORDS
    # # =====================================================
    # # Membaca sheet Top Words
    # try:
    #     df = pd.read_excel(
    #         EXCEL_PATH,
    #         sheet_name=cfg["top"]
    #     )

    #     with st.expander("Top Words"):
    #         st.dataframe(
    #             df,
    #             use_container_width=True
    #         )
    # except:
    #     st.caption(
    #         "Top Words belum tersedia."
    #     )


# =====================================================
# TOP WORDS PER TOPIK
# =====================================================

    try:

        topword = pd.read_excel(
            "data/OUTPUT_LDA/topword.xlsx"
        )

        # filter sesuai model yang sedang dipilih
        top_model = topword[
            topword["Model"] == name
        ]
        # st.subheader("🔑 Top Words per Topik")
        with st.expander("🔑 TOP WORDS PER TOPIK"):
            with st.container (border=True):

                cols = st.columns(2)
                topics = top_model["Topik"].unique()
                for i, topic in enumerate(topics):

                    with cols[i % 2]:

                        df_topic = (
                                    top_model[
                                        top_model["Topik"] == topic
                                    ]
                                    .sort_values(
                                        "Probabilitas",
                                        ascending=False
                                    )
                                    .head(5)
                                )

                        fig = px.bar(
                            df_topic,
                            x="Probabilitas",
                            y="Kata",
                            orientation="h",
                            color="Probabilitas",
                            color_continuous_scale="Blues",
                            text="Probabilitas"

                        )

                        fig.update_layout(

                            title=topic,
                            template="plotly_white",
                            height=350,
                            coloraxis_showscale=False,
                            margin=dict(
                                l=20,
                                r=20,
                                t=40,
                                b=20
                            ),

                            yaxis=dict(
                                categoryorder="total ascending"
                            )

                        )

                        fig.update_traces(
                            texttemplate="%{text:.3f}",
                            textposition="outside"
                        )

                        st.plotly_chart(
                            fig,
                            use_container_width=True
                        )

    except:

        st.warning("Top Words belum tersedia.")
    # =====================================================
    # LABEL TOPIK
    # =====================================================
    try:
        df = pd.read_excel(
            EXCEL_PATH,
            sheet_name=cfg["label"]
        )

        with st.expander("🏷️ LABEL TOPIK"):
            st.dataframe(
                df,
                use_container_width=True
            )
    except:
        st.caption(
            "Label Topik belum tersedia."
        )

    # =====================================================
    # CONTOH TWEET
    # =====================================================

    st.markdown("""
        <style>

        /* Expander */
        details{
            border:1px solid #BFDBFE !important;
            border-radius:12px !important;
            background:#F8FBFF !important;
            margin-bottom:12px;
        }

        /* Header Expander */
        summary{
            background:#DBEAFE !important;
            color:#1E40AF !important;
            font-weight:700;
            padding:12px 16px;
            border-radius:12px;
            font-size:16px;
        }

        /* Saat dibuka */
        details[open] summary{
            border-bottom:1px solid #BFDBFE;
            border-radius:12px 12px 0 0;
        }

        </style>
        """, unsafe_allow_html=True)

    try:
        df = pd.read_excel(
            EXCEL_PATH,
            sheet_name=cfg["tweet"]
        )

        with st.expander("📫 DISTRIBUSI TOPIK SETIAP EKSPEDISI"):
            st.dataframe(
                df,
                use_container_width=True
            )
    except:
        st.caption(
            "Contoh Tweet belum tersedia."
        )
    # =====================================================
    # PYLDAVIS
    # ====================================================
    st.subheader("📊 Grafik PyLDAvis")
    with st.container(border=True):
        

        import streamlit.components.v1 as components
        # Membuka file HTML PyLDAvis
        with open(
            cfg["pylda"],"r", encoding="utf-8"

        ) as f:
            html = f.read()

        # Menampilkan HTML ke Streamlit
        components.html(
            html, height=800, scrolling=True
        )

    st.divider()

if representasi=="Semua":
    st.header("📦 Bag of Words")
    show_model("LDA-BoW-NoStem")
    show_model("LDA-BoW-Stem")
    st.header("📝 TF-IDF")
    show_model("LDA-TFIDF-NoStem")
    show_model("LDA-TFIDF-Stem")
elif representasi=="BoW":
    st.header("📦 Bag of Words")
    show_model("LDA-BoW-NoStem")
    show_model("LDA-BoW-Stem")
else:
    st.header("📝 TF-IDF")
    show_model("LDA-TFIDF-NoStem")
    show_model("LDA-TFIDF-Stem")