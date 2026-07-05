import streamlit as st
import pandas as pd
import plotly.express as px

# ======================================================
# KONFIGURASI
# ======================================================

st.set_page_config(
    page_title="Dashboard Pemodelan Topik",
    page_icon="📦",
    layout="wide"
)


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

# ==============================
# HERO SECTION
# ==============================
st.markdown("""
            <style>

            .hero{
                background:#DED8FF;
                padding:15px 35px;
                border-radius:12px;
                text-align:center;
                margin-bottom:25px;
            }

            .hero h1{
                color:#2d3436;
                font-size:46px;
                margin-bottom:25px;
            }

            .hero p{
                width:75%;
                margin:auto;
                font-size:18px;
                line-height:1.5;
                color:#555;
            }

            </style>
            """, unsafe_allow_html=True)


st.markdown("""

            <div class="hero">

            <h1>
            Analisis Pemodelan Topik Layanan Ekspedisi
            </h1>

            <p>

            Lonjakan pertumbuhan logistik telah memicu persaingan yang sangat ketat antar perusahaan ekspedisi untuk memperebutkan kepercayaan pelanggan (Khoirunnazilah et al. 2021), di mana pasar e-commerce faktanya didominasi oleh segelintir perusahaan besar. Penelitian ini akan berfokus pada empat perusahaan yang dianggap sebagai tulang punggung pengiriman barang e-commerce di Indonesia, yaitu J&T Express, JNE, SiCepat, dan Anteraja, yang dipilih berdasarkan dominasi pangsa pasar mereka yang signifikan.
            

            </p>

            </div>

            """, unsafe_allow_html=True)

###SUMMARYCARD

col1, col2, col3, col4 = st.columns(4, gap="medium")

with col1:
        with st.container(border=True):

            st.markdown("""
                <div style="
                height:180px;
                display:flex;
                flex-direction:column;
                justify-content:center;
                align-items:center;
                text-align:center;
                ">

                <div style="font-size:42px;font-weight:700;">2399</div>

                <div style="font-size:18px;margin-top:8px;">
                📄Total Tweet Dianalisis
                </div>

                <div style="
                margin-top:11px;
                background:#FFDAC1;
                color:#002db3;
                padding:6px 16px;
                border-radius:20px;
                font-size:13px;
                font-weight:600;
                ">
                Live Data
                </div>

                </div>
                """, unsafe_allow_html=True)
            
    
with col2:
        with st.container(border=True):

            st.markdown("""
                <div style="
                height:180px;
                display:flex;
                flex-direction:column;
                justify-content:center;
                align-items:center;
                text-align:center;
                ">

                <div style="font-size:42px;font-weight:700;">9</div>

                <div style="font-size:18px;margin-top:8px;">
                🗂️ Topik LDA Teridentifikasi
                </div>

                <div style="
                margin-top:18px;
                background:#F8C8DC;
                color:#002db3;
                padding:6px 16px;
                border-radius:20px;
                font-size:13px;
                font-weight:600;
                ">
                LDA
                </div>

                </div>
                """, unsafe_allow_html=True)
            
    
with col3:
        with st.container(border=True):

            st.markdown("""
                <div style="
                height:180px;
                display:flex;
                flex-direction:column;
                justify-content:center;
                align-items:center;
                text-align:center;
                ">

                <div style="font-size:42px;font-weight:700;">4</div>

                <div style="font-size:18px;margin-top:8px;">
                🗃️​ Cluster mBERT Teridentifikasi
                </div>

                <div style="
                margin-top:18px;
                background:#C1E1C1;
                color:#002db3;
                padding:6px 16px;
                border-radius:20px;
                font-size:13px;
                font-weight:600;
                ">
                mbert
                </div>

                </div>
                """, unsafe_allow_html=True)
            
    
with col4:
        with st.container(border=True):

            st.markdown("""
                <div style="
                height:180px;
                display:flex;
                flex-direction:column;
                justify-content:center;
                align-items:center;
                text-align:center;
                ">

                <div style="font-size:42px;font-weight:700;">4</div>

                <div style="font-size:18px;margin-top:8px;">
                🏢​ Total Ekspedisi
                </div>

                <div style="
                margin-top:18px;
                background:#FFE4B5;
                color:#002db3;
                padding:6px 16px;
                border-radius:20px;
                font-size:13px;
                font-weight:600;
                ">
                JNE, JNT, SiCepat, Anteraja
                </div>

                </div>
                """, unsafe_allow_html=True)
    
st.write("")


###FITURRR
st.markdown("""
<style>

/* ===========================
   FEATURE CARD
=========================== */

div[data-testid="stVerticalBlockBorderWrapper"]{
    border:1.5px solid #D8E3F0 !important;
    border-radius:14px !important;
    padding:18px !important;
    background:white;
    box-shadow:0 2px 8px rgba(0,0,0,.04);
    transition:0.25s;
}

div[data-testid="stVerticalBlockBorderWrapper"]:hover{
    border-color:#8B5CF6 !important;
    box-shadow:0 6px 18px rgba(139,92,246,.18);
}

/* ===========================
   BUTTON
=========================== */

.stButton>button{

    width:100%;

    border-radius:10px;

    height:45px;

    border:1.5px solid #8B5CF6;

    color:#8B5CF6;

    background:white;

    font-weight:600;

    font-size:15px;

}

.stButton>button:hover{

    background:#8B5CF6;

    color:white;

}

/* ===========================
   ICON
=========================== */

.feature-icon{

    font-size:40px;

    margin-bottom:10px;

}

</style>
""", unsafe_allow_html=True)

col1,col2,col3 = st.columns(3, gap="large")
with col1:

    with st.container(border=True):
        st.image("assets/icon_lda.png",width=45)
        st.markdown("### Hasil Topik LDA")
        st.write("""
                Visualisasi distribusi topik hasil pemodelan
                Latent Dirichlet Allocation pada data tweet
                ekspedisi.
                """)

        st.write("")

        if st.button(
            "Lihat Topik →",
            use_container_width=True,
            key="lda"
            ):
            st.switch_page("pages/LDA.py")


with col2:

    with st.container(border=True):

        st.image("assets/icon_mbert.png",width=45)
        st.markdown("### Clustering mBERT")
        st.write("""
                    Analisis clustering menggunakan
                    Multilingual BERT dengan reduksi
                    dimensi UMAP.
                    """)

        st.write("")

        if st.button(
            "Lihat Cluster →",
            use_container_width=True,
            key="mbert"
            ):
            st.switch_page("pages/mBERT.py")

        

with col3:

    with st.container(border=True):

        st.image("assets/tweet.png",width=45)
        st.markdown("### Analisis Tweet")
        st.write("""
                Masukkan tweet baru untuk memperoleh
                hasil analisis topik maupun
                cluster.
                """)

        st.write("")

        if st.button(
            "Coba Sekarang →",
            use_container_width=True,
            key="analisis"
            ):
            st.switch_page("pages/Analisis Tweet.py")


            
#####INFO DATASET
st.write("")
st.write("")

st.subheader("📊 Informasi Dataset")

st.caption("""
Dataset penelitian diperoleh dari hasil scraping media sosial Twitter
yang berisi aduan pelanggan terhadap layanan ekspedisi di Indonesia.
""")

left, right = st.columns([2,3], gap="large")
with left:

    with st.container(border=True, height=430):

        st.markdown("### 📄 Deskripsi Dataset")

        st.write("""
Dashboard ini merupakan visualisasi hasil penelitian skripsi berjudul "Topic Modeling pada Data Twitter (X) Layanan Ekspedisi Menggunakan Latent Dirichlet Allocation (LDA)". Dataset yang digunakan terdiri dari 2.999 tweet aduan pelanggan terhadap empat perusahaan ekspedisi di Indonesia, yaitu JNE, J&T Express, SiCepat, dan AnterAja. Data dikumpulkan melalui proses web scraping menggunakan Apify dengan rentang waktu 2019–2026.

Sebelum dilakukan pemodelan topik, seluruh data telah melalui tahapan preprocessing yang meliputi case folding, cleaning, normalisasi kata, stopword removal, dan tokenisasi. Penelitian ini membandingkan representasi teks Bag-of-Words (BoW) dan TF-IDF pada metode Latent Dirichlet Allocation (LDA), serta clustering Multilingual BERT (mBERT) untuk analisis pengelompokan berbasis representasi semantik
""")
        
with right:

    with st.container(border=True):
        st.markdown("### 📈 Statistik Data Setelah Preprocessing")

        st.image("assets/info_data.png")

#### infoo ekspedisii
st.write("")
st.write("")

st.subheader("🚚 Perusahaan Ekspedisi")

st.caption("""
Empat perusahaan ekspedisi yang menjadi objek penelitian
berdasarkan data layanan ekspedisi pada media sosial Twitter (X).
""")
col1,col2,col3,col4 = st.columns(4,gap="medium")
with col1:

    with st.container(border=True):

        st.image(
            "assets/logo_jne.png",
            width=150
        )

        st.markdown("### JNE")

        st.caption("Jalur Nugraha Ekakurir")

        st.markdown("""
<div style="
text-align:justify;
font-size:15px;
line-height:1.8;
color:#444;
">

<b>JNE Express</b> merupakan perusahaan penyedia jasa pengiriman barang dan
logistik nasional di bawah naungan <b>PT Tiki Jalur Nugraha Ekakurir</b> yang
didirikan pada <b>26 November 1990</b>. Berawal sebagai divisi penanganan
kepabeanan dan pengiriman internasional, JNE berkembang menjadi salah satu
perusahaan ekspedisi terbesar di Indonesia dengan jaringan distribusi yang
menjangkau ribuan titik layanan di seluruh wilayah. Perusahaan ini menyediakan
berbagai layanan pengiriman, mulai dari reguler hingga layanan ekspres, serta
menjadi mitra utama berbagai platform <i>e-commerce</i> dan sektor bisnis.

</div>
""", unsafe_allow_html=True)
        
with col2:

    with st.container(border=True):

        st.image(
            "assets/logo_jnt.png",
            width=150
        )

        st.markdown("### J&T Express")

        st.caption("Express Your Online Business")

        st.markdown("""
<div style="
text-align:justify;
font-size:15px;
line-height:1.8;
color:#444;
">

<b>J&T Express</b> merupakan perusahaan logistik berbasis teknologi di bawah
naungan <b>PT Global Jet Express</b> yang didirikan pada <b>20 Agustus 2015</b>.
Mengusung slogan <b>"Express Your Online Business"</b>, perusahaan ini
mengintegrasikan teknologi digital dalam seluruh proses operasional, mulai dari
pelacakan paket secara <i>real-time</i> hingga pengelolaan jaringan distribusi.
Dengan ekspansi yang pesat di kawasan Asia Tenggara dan dukungan layanan
lintas negara (<i>cross-border logistics</i>), J&T Express menjadi salah satu
penyedia jasa ekspedisi dengan pertumbuhan tercepat di Indonesia.

</div>
""", unsafe_allow_html=True)

with col3:

    with st.container(border=True):

        st.image(
            "assets/logo_sicepat.png",
            width=150
        )

        st.markdown("### SiCepat")

        st.caption("Ketika Semua Jadi Mudah")

        st.markdown("""
<div style="
text-align:justify;
font-size:15px;
line-height:1.8;
color:#444;
">

<b>SiCepat Ekspres</b> merupakan perusahaan logistik nasional di bawah naungan
<b>PT SiCepat Ekspres Indonesia</b> yang didirikan pada <b>2014</b>. Mengusung
slogan <b>"Ketika Semua Jadi Mudah"</b>, perusahaan ini berfokus pada layanan
pengiriman yang cepat dengan dukungan sistem pelacakan paket secara
<i>real-time</i> dan layanan penjemputan paket (<i>pick-up service</i>). SiCepat
berkembang sebagai salah satu mitra strategis berbagai platform
<i>e-commerce</i> di Indonesia dengan menghadirkan layanan logistik yang
efisien, fleksibel, dan terintegrasi secara digital.

</div>
""", unsafe_allow_html=True)

with col4:

    with st.container(border=True):

        st.image(
            "assets/logo_anteraja.png",
            width=150
        )

        st.markdown("### AnterAja")

        st.caption("Pasti Bawa Happy")

        st.markdown("""
<div style="
text-align:justify;
font-size:15px;
line-height:1.8;
color:#444;
">

AnterAja merupakan perusahaan penyedia jasa pengiriman barang (<i>last-mile delivery</i>)
berbasis teknologi di bawah naungan <b>PT Tri Adi Bersama</b>, anak perusahaan
<b>PT Adi Sarana Armada Tbk (ASSA)</b> yang merupakan bagian dari
<b>Triputra Group</b>. Perusahaan ini didirikan pada <b>Maret 2019</b> dengan fokus pada otomatisasi
operasional logistik melalui pemanfaatan <i>Artificial Intelligence (AI)</i> untuk
optimalisasi rute kurir serta integrasi API dengan berbagai platform e-commerce. AnterAja menyediakan tiga layanan utama, yaitu
<b>Regular</b>, <b>Next Day</b>, dan <b>Same Day Service</b>, dengan dukungan kurir
lapangan yang dikenal sebagai <b>Satria</b> untuk proses penjemputan dan
pengantaran paket secara langsung.

</div>
""", unsafe_allow_html=True)
        
st.markdown("""
<style>

.company-card img{

    display:block;

    margin:auto;

}

</style>
""", unsafe_allow_html=True)
        # st.metric("Jumlah Tweet","18.532")

        # st.metric("Periode","2024-2025")

        # st.metric("Bahasa","Indonesia")



###################
# st.subheader("📊 Informasi Dataset")

# st.caption(
#     "Dataset hasil preprocessing yang digunakan pada penelitian."
# )

# df_dataset = pd.read_excel(
#     "data/OUTPUT_MBERT/data_bersih.xlsx"
# )

# st.dataframe(
#     df_dataset,
#     use_container_width=True,
#     hide_index=True
# )