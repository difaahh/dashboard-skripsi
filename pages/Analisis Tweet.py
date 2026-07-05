#BAGIAN 1

# ==========================================================
# IMPORT LIBRARY
# ==========================================================
# Library utama Streamlit
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px # Visualisasi
import pickle # Model
from gensim.corpora import Dictionary
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity# Cosine Similarity

# Preprocessing
from preprocessing import preprocess
from preprop_mber import bersihkan_mbert
from sklearn.preprocessing import normalize

# ==========================================================
# KONFIGURASI HALAMAN
# ==========================================================
st.set_page_config(
    page_title="Analisis Tweet",
    page_icon="🕊️",
    layout="wide"
)

# ==========================================================
# CSS
# ==========================================================
st.markdown("""
    <style>

    section[data-testid="stSidebar"]{
        background:#DED8FF;
    }

    .block-container{
        padding-top:1.5rem;
    }

    .metric-card{
        border-radius:14px;
    }

    .result-card{
        background:#FFFFFF;
        border:1px solid #E5E7EB;
        border-radius:16px;
        padding:18px;
        margin-bottom:18px;
        box-shadow:0 2px 8px rgba(0,0,0,.05);
    }

    .section-title{
        font-size:24px;
        font-weight:700;
        color:#374151;
        margin-bottom:8px;
    }

    </style>
    """, unsafe_allow_html=True)

# ==========================================================
# SIDEBAR
# ==========================================================
with st.sidebar:

    st.markdown(
        "<h2 style='text-align:center;'>DASHBOARD</h2>",
        unsafe_allow_html=True
    )

    st.divider()

    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("Dashboard.py")

    if st.button("💬 LDA", use_container_width=True):
        st.switch_page("pages/LDA.py")

    if st.button("🗃️ mBERT", use_container_width=True):
        st.switch_page("pages/mBERT.py")

    if st.button("🕊️ Analisis", use_container_width=True):
        st.switch_page("pages/Analisis Tweet.py")


# ==========================================================
# CACHE LOADING MODEL
# ==========================================================
# Model hanya dibaca sekali sehingga dashboard lebih cepat.
@st.cache_resource
def load_models():

    # --------------------------
    # LDA
    # --------------------------
    with open("data/OUTPUT_LDA/lda_bow_best.pkl","rb") as f:
        lda_bow=pickle.load(f)

    with open("data/OUTPUT_LDA/lda_tfidf_best.pkl","rb") as f:
        lda_tfidf=pickle.load(f)

    dict_bow=Dictionary.load(
        "data/OUTPUT_LDA/dict_bow.dict"
    )

    dict_tfidf=Dictionary.load(
        "data/OUTPUT_LDA/dict_tfidf.dict"
    )

    # --------------------------
    # mBERT
    # --------------------------
    encoder=SentenceTransformer( "paraphrase-multilingual-mpnet-base-v2")

    with open(
        "data/OUTPUT_MBERT/umap_final.pkl",
        "rb"
    ) as f:
        umap_model=pickle.load(f)

    with open(
        "data/OUTPUT_MBERT/kmeans_final.pkl",
        "rb"
    ) as f:
        kmeans_model=pickle.load(f)

    return (
        lda_bow,
        lda_tfidf,
        dict_bow,
        dict_tfidf,
        encoder,
        umap_model,
        kmeans_model
    )


# ==========================================================
# CACHE DATA
# ==========================================================
# Data pendukung hanya dibaca sekali.
@st.cache_data
def load_data():

    data_bersih=pd.read_excel(
        "data/OUTPUT_LDA/data_bersih.xlsx"
    )

    topword=pd.read_excel(
        "data/OUTPUT_LDA/topword.xlsx"
    )

    cluster=pd.read_excel(
        "data/OUTPUT_MBERT/07_cluster_final.xlsx"
    )

    ctfidf=pd.read_excel(
        "data/OUTPUT_MBERT/09A_ctfidf_semua.xlsx"
    )

    return (
        data_bersih,
        topword,
        cluster,
        ctfidf
    )


# ==========================================================
# MEMANGGIL MODEL DAN DATA
# ==========================================================
(
    lda_bow,
    lda_tfidf,
    dict_bow,
    dict_tfidf,
    encoder,
    umap_model,
    kmeans_model
)=load_models()

(
    data_bersih,
    topword,
    cluster_df,
    ctfidf_df
)=load_data()

col1, col2 = st.columns([0.06, 0.94], vertical_alignment="center")

with col1:
    st.image("assets/tweet.png", width=45)

with col2:
    st.markdown("## Analisis Tweet")

st.caption(
    """
        Masukkan tweet aduan layanan ekspedisi
        untuk dianalisis menggunakan
        LDA maupun mBERT.
        """
        )

st.divider()

#####PART 2a

# ==========================================================
# HELPER
# ==========================================================
# Fungsi untuk menampilkan progress berdasarkan probabilitas.

def show_probability(prob):

    st.progress(float(prob))

    st.caption(
        f"Probabilitas Topik : {prob:.2%}"
    )


# ==========================================================
# HELPER
# ==========================================================
# Mengambil Top Words dari file topword.xlsx

def get_top_words(model_name, topic):

    df = topword[(topword["Model"] == model_name) & (topword["Topik"] == f"Topik {topic}")].copy()
    return df.sort_values("Probabilitas",ascending=False).head(10)

def predict_lda(tweet, representasi):

    # ====================================
    # PREPROCESSING
    # ====================================

    tokens = preprocess(tweet)

    if len(tokens) == 0:
        st.error("Tweet tidak dapat diproses.")

        return

    # ====================================
    # PILIH MODEL
    # ====================================

    if representasi == "BoW":
        dictionary = dict_bow
        lda_model = lda_bow
        nama_model = "LDA-BoW"
        bow = dictionary.doc2bow(tokens)


    else:
        dictionary = dict_tfidf
        lda_model = lda_tfidf
        nama_model = "LDA-TFIDF"
        bow = dictionary.doc2bow(tokens)


    # ====================================
    # cakupan DICTIONARY
    # ====================================

    known_tokens = [

        t for t in tokens if t in dictionary.token2id
    ]

    cakupan = len(
        known_tokens
    ) / len(tokens)

    if cakupan < 0.50:

        st.error(
            """
            Tweet kurang relevan dengan
            layanan ekspedisi.

            Silakan masukkan tweet yang
            berkaitan dengan pengiriman,
            paket, kurir, resi,
            atau kendala ekspedisi.
            """
        )

        st.info(
                        f"""
            **Kata dikenali** {" • ".join(known_tokens)} cakupan Dictionary {cakupan:.0%} """)
        return


    # ====================================
    # INFERENSI LDA
    # ====================================
    hasil = lda_model.get_document_topics( bow, minimum_probability=0)

    topic_id, prob = max( hasil,
        key=lambda x: x[1]
    )

    topic_id += 1

    # ====================================
    # HASIL
    # ====================================
    st.success(f"Hasil Prediksi ({nama_model})" )

    c1, c2 = st.columns(2)
    with c1:
        st.metric( "Topik", topic_id)

    with c2:

        st.metric( "cakupan", f"{cakupan:.0%}")


    show_probability(prob)

    st.info(
                f"""
        **Kata dikenali model**

        {" • ".join(known_tokens)}
        """
            )
    
##########PART 3
    # ====================================
    # TOP WORDS
    # ====================================
    # Menampilkan 5 kata dengan probabilitas
    # tertinggi dari topik hasil prediksi.

    df_top = get_top_words(
        nama_model,
        topic_id
    )

    if len(df_top) > 0:

        st.write("")
        st.subheader("🔑 Top Words")

        fig = px.bar(

            df_top,
            x="Probabilitas",
            y="Kata",
            orientation="h",
            color="Probabilitas",
            color_continuous_scale="Blues",
            text="Probabilitas"

        )

        fig.update_layout(

            template="plotly_white",
            height=380,
            coloraxis_showscale=False,
            margin=dict(
                l=20, r=20, t=20, b=20
            ),

            yaxis=dict(
                categoryorder="total ascending"
            )

        )

        fig.update_traces( texttemplate="%{text:.3f}", textposition="outside")

        st.plotly_chart( fig, use_container_width=True)

    # ====================================
    # DETAIL PREPROCESSING
    # ====================================
    # Menampilkan token hasil preprocessing
    # agar pengguna dapat melihat proses
    # yang dilakukan sebelum inferensi.

    with st.expander(

        "⚙ Detail Preprocessing"
    ):

        st.write(
            "**Token Hasil Preprocessing**"
        )

        st.write(tokens)
        st.write("")
        st.write(
            "**Token Dikenali Model**"
        )

        st.write(known_tokens)
        st.write("")
        st.write(
            f"cakupan Dictionary : **{cakupan:.0%}**"
        )

        st.caption(
            """
            cakupan menunjukkan persentase token
            yang berhasil dikenali oleh dictionary
            LDA.

            Semakin tinggi cakupan maka hasil
            prediksi akan semakin representatif.
            """
        )


        ######PART 4 
# ==========================================================
# HELPER
# ==========================================================
# Mengambil Top Words tiap Cluster
def get_cluster_words(cluster):

    df = ctfidf_df[
        ctfidf_df["Cluster"] == cluster
    ].copy()

    return (
        df
        .sort_values(
            "Score",
            ascending=False
        )
        .head(10)
    )


# ==========================================================
# HELPER
# ==========================================================
# Mengambil contoh tweet tiap Cluster

# def get_cluster_tweets(cluster):
#     contoh = (
#         cluster_df[cluster_df["cluster"] == cluster]["text"].dropna().head(5).tolist()
#     )
#     return contoh


# ==========================================================
# PREDIKSI MBERT
# ==========================================================
    # ============================================
    # PREPROCESSING
    # ============================================
def predict_mbert(tweet):
    teks = bersihkan_mbert(tweet)

    if len(teks) == 0:
        st.error("Tweet tidak dapat diproses.")
        return

# ============================================
# EMBEDDING
# ============================================
    embedding = encoder.encode(
        [teks],
        convert_to_numpy=True
    )

    # Samakan dengan proses training
    embedding = normalize(embedding)

    embedding_umap = umap_model.transform(
        embedding
    )

    # print("Embedding :", embedding.shape)
    # print("UMAP :", embedding_umap.shape)
    # print("KMeans :", kmeans_model.cluster_centers_.shape)
    # print("UMAP components :", umap_model.n_components)
    # st.stop()   # hentikan dulu di sini



    # ============================================
    # PREDIKSI CLUSTER
    # ============================================
    cluster = int(
        kmeans_model.predict(
            embedding_umap
        )[0]

    )

    # ============================================
    # Analisis kata input terhadap Top Words Cluster
    # ============================================

    # Token hasil preprocessing
    tokens = teks.split()

    # Ambil top words cluster yang diprediksi
    cluster_words = ctfidf_df[
        ctfidf_df["Cluster"] == cluster
    ].copy()

    # Dictionary:
    # kata -> score
    word_score = dict(
        zip(
            cluster_words["Kata"],
            cluster_words["Score"]
        )
    )

    hasil_token = []

    for token in tokens:
        if token in word_score:
            hasil_token.append({
                "Kata": token,
                "Status": "✓ Sesuai Cluster",
                "Score": word_score[token]
            })

        else:

            hasil_token.append({
                "Kata": token,
                "Status": "✗ Tidak ditemukan",
                "Score": 0
            })

    df_token = pd.DataFrame(hasil_token)

    # ============================================
    # SIMILARITY
    # ============================================
    # centroid = kmeans_model.cluster_centers_[
    #     cluster
    # ].reshape(1,-1)

    # similarity = cosine_similarity(
    #     embedding_umap,
    #     centroid
    # )[0][0]

    # similarity = max(
    #     similarity,
    #     0
    # )

    # similarity = min(
    #     similarity,
    #     1
    # )

    
    # ============================================
    # HASIL
    # ============================================
    # st.success("Hasil Prediksi mBERT")

    st.markdown("""
        <div class="result-card">

        <h3>📦 Hasil Prediksi mBERT</h3>

        </div>
        """,unsafe_allow_html=True)

    # c1,c2 = st.columns(2)

    # with c1:
    st.metric( "Cluster Terprediksi", cluster)

    # with c2:
        # st.metric( "Kemiripan terhadap Cluster", f"{similarity:.2%}")

    # st.progress(float(similarity))

    # ============================================
    # TOP WORDS
    # ============================================
    df_top = get_cluster_words(
        cluster
    )

    # st.subheader("🔑 Top Words Cluster")

    st.markdown("""
    <div class="section-title">

    🔑 Top Words Cluster

    </div>
    """,unsafe_allow_html=True)

    fig = px.bar(
        df_top,
        x="Score",
        y="Kata",
        orientation="h",
        color="Score",
        color_continuous_scale="Blues",
        text="Score"
    )

    fig.update_layout(
        template="plotly_white",
        height=380,
        coloraxis_showscale=False,
        margin=dict(
            l=20,
            r=20,
            t=20,
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

    st.caption(
    """
    Top words diperoleh menggunakan pembobotan
    c-TF-IDF sehingga merepresentasikan kata
    yang paling dominan pada cluster hasil
    pengelompokan mBERT.
    """
    )

    st.divider()

####
    # st.markdown("## 📝 Interpretasi Cluster")
    st.markdown("""
    <div class="section-title">

    📝 Interpretasi Cluster

    </div>
    """,unsafe_allow_html=True)

    DESKRIPSI_CLUSTER = {

    0: """
    Cluster ini didominasi tweet mengenai proses
    pengiriman paket, kurir, layanan ekspedisi,
    serta aktivitas distribusi barang.
    """,

        1: """
    Cluster ini didominasi tweet mengenai
    kendala pengiriman seperti keterlambatan,
    status paket, dan proses pelacakan.
    """,

        2: """
    Cluster ini berisi tweet mengenai
    kehilangan, kerusakan, ataupun kesalahan
    pengiriman paket.
    """,

        3: """
    Cluster ini berisi interaksi pelanggan
    dengan customer service serta pertanyaan
    mengenai layanan ekspedisi.
    """

    }
    with st.container(border=True):

        st.write(
        DESKRIPSI_CLUSTER.get(
            cluster,
            "-"
        )
    )

    # st.info(
    # DESKRIPSI_CLUSTER.get(
    #     cluster,
    #     "-"
    #     )
    # )

    # st.markdown("## 💬 Contoh Tweet Cluster")

    # contoh = cluster_df[
    #     cluster_df["cluster"]==cluster
    # ].head(5)

#####
    # st.markdown("### 🔍 Analisis Kata c-tfidf")

    # for _, row in df_token.iterrows():
    #     if row["Score"] > 0:
    #         st.success(
    #             f"**{row['Kata']}** "
    #             f"(Score c-TF-IDF : {row['Score']:.3f})"
    #         )

    #     else:
    #         st.error(
    #             f"**{row['Kata']}** "
    #             f"(Tidak termasuk kata representatif cluster)"
    #         )

    # ============================================
    # CONTOH TWEET
    # ============================================
    # contoh = get_cluster_tweets(
    #     cluster
    # )

    # st.subheader(
    #     "📝 Contoh Tweet"
    # )

    # for i,t in enumerate(contoh):

    #     with st.container(
    #         border=True
    #     ):

    #         st.markdown(

    #             f"**Tweet {i+1}**"

    #         )

    #         st.write(t)

    # ============================================
    # DETAIL PREPROCESSING
    # ============================================
    with st.expander(
        "⚙ Detail Preprocessing"
    ):

        # st.write(
        #     "**Hasil Preprocessing**"
        # )
    
        # st.code(teks)

        st.write(teks)
        st.caption(
            """
            Tweet dibersihkan menggunakan
            preprocessing mBERT kemudian
            diubah menjadi embedding menggunakan
            SentenceTransformer
            (paraphrase-multilingual-mpnet-base-v2).

            Embedding direduksi menggunakan
            UMAP kemudian diprediksi
            menggunakan KMeans.
"""
        )


#####part5
# ==========================================================
# INPUT USER
# ==========================================================
model = st.radio(
    "Pilih Model",
    ["LDA", "mBERT"],
    horizontal=True
)

if model == "LDA":
    representasi = st.radio(
        "Representasi",
        ["BoW", "TF-IDF"],
        horizontal=True
    )
else:
    representasi = None

tweet = st.text_area(
    "Masukkan Tweet",
    height=180,
    placeholder="Contoh: Paket saya sudah 4 hari belum datang..."
)

col1, col2 = st.columns(2)

with col1:
    if st.button("Reset"):
        st.rerun()

with col2:
    analisis = st.button(
        "🔍 Analisis",
        type="primary",
        use_container_width=True
    )

# ==========================================================
# MAIN PROGRAM
# ==========================================================
# Menjalankan proses analisis ketika tombol ditekan.

# ==========================================================
# MAIN PROGRAM
# ==========================================================
if analisis:

    try:
        with st.spinner(
            "Sedang menganalisis tweet..."
        ):

            if model == "LDA":
                predict_lda(
                    tweet,
                    representasi
                )

            else:
                predict_mbert(
                    tweet
                )

    except Exception as e:
        st.error(
            "Terjadi kesalahan ketika melakukan analisis."
        )
        st.exception(e)
