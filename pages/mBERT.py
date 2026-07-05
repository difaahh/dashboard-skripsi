


import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="MBERT",
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

#############

# ======================================================
# HALAMAN MBERT
# ======================================================

st.header("🗃️ Clustering mBERT")


st.caption("""
        Halaman ini menampilkan hasil clustering tweet menggunakan
        Multilingual BERT (mBERT), reduksi dimensi UMAP,
        dan algoritma K-Means.
        """)

st.divider()


col1,col2,col3,col4 = st.columns(4,gap="medium")

with col1:
        with st.container(border=True):
            st.markdown("# **4**")
            st.caption("Jumlah Cluster")
            st.success("KMeans")

with col2:
     with st.container(border=True):
            st.markdown("# **0.9071**")
            st.caption("Silhouette Score")
            st.info("Evaluation")

with col3:
        with st.container(border=True):
            st.markdown("# **2399**")
            st.caption("Jumlah Tweet")
            st.warning("Dataset")

with col4:
        with st.container(border=True):
            st.markdown("# **768**")
            st.caption("Embedding Dimension")
            st.error("mBERT")

############################# CLUSTER UMAP

st.write("")

df_umap = pd.read_excel(
"data/OUTPUT_MBERT/07_cluster_final.xlsx")

fig = px.scatter(
        df_umap,
        x="UMAP_1",
        y="UMAP_2",
        color=df_umap["cluster"].astype(str),
        hover_data={
            "text":True,
            "Kategori":True,
            "cluster":True,
            "UMAP_1":False,
            "UMAP_2":False
        },

        title="Visualisasi Cluster mBERT"

    )
fig.update_layout(

    height=500,

    template="plotly_white",

    title=dict(
        text="Visualisasi Cluster mBERT",
        x=0.5,
        font=dict(
            size=22,
            color="#27283E"   # Ungu tua
        )
    ),

    legend_title="Cluster",

    legend=dict(
        font=dict(
            size=15,
            color="#2F5145"
        ),
        title_font=dict(
            size=16
        )
    ),

    xaxis=dict(
        title="UMAP-1",
        title_font=dict(
            size=18,
            color="#392139"
        ),
        tickfont=dict(
            size=14
        )
    ),

    yaxis=dict(
        title="UMAP-2",
        title_font=dict(
            size=18,
            color="#3B3C27"
        ),
        tickfont=dict(
            size=14
        )
    ),

    margin=dict(
        l=10,
        r=10,
        t=50,
        b=10
    )
)

fig.update_traces(

        marker=dict(
            size=5,
            opacity=0.7
        )

    )

left,right = st.columns([5,1],gap="large")
with left:
     st.subheader("📍 Visualisasi UMAP")
     with st.container(border=True):
          st.plotly_chart(
                fig,
                use_container_width=True,
                config={
                    "scrollZoom": True,
                    "displayModeBar": True}
                    )
with right:

    st.subheader("ℹ️ Informasi Model")
    with st.container(border=True):

        st.metric("Model","mBERT")
        st.metric("Algoritma","KMeans")
        st.metric("Jumlah Cluster","4")
        st.metric("Reduksi","UMAP")

#################################

st.divider()

st.subheader("📊 Evaluasi Model Clustering")

st.caption("""
        Evaluasi dilakukan menggunakan metode Elbow dan Silhouette Score
        untuk menentukan jumlah cluster yang optimal.
        """)

st.write("")


eval_df = pd.DataFrame({

        "K":[2,3,4,5,6,7,8,9,10],
        "Silhouette":[0.8673,0.8932,0.9071,0.4339,0.4346,0.4353,0.4206,0.4435,0.4450],
        "Inertia":[46914.89,16805.22,7353.00,4458.68,3375.45,2540.34,2075.20,1701.71,1456.32]

})


    # col1, col2 = st.columns(2, gap="large")
with st.container(border=True):
    st.markdown("#### 📈 Silhouette Score")

    fig_sil = px.line(
                eval_df,
                x="K",
                y="Silhouette",
                markers=True,
                text="Silhouette",
                title="Silhouette Score"
            )

    fig_sil.update_traces(
        line=dict(color="#061F71", width=4),
        marker=dict(size=10),
        textposition="top center"
            )

    fig_sil.update_layout(
                template="plotly_white",
                height=350,

                xaxis_title="Jumlah Cluster (K)",
                yaxis_title="Silhouette Score",

                title=dict(
                    text="Silhouette Score untuk Berbagai Nilai K",
                    x=0.5,
                    font=dict(size=18)
                ),

                font=dict(size=14),

                hovermode="x unified"
            )

    fig_sil.add_vline(
                x=4,
                line_dash="dash",
                line_color="red"
            )

    fig_sil.add_annotation(
                x=4,
                y=0.45,
                text="Best K = 4",
                showarrow=True,
                arrowhead=2,
                bgcolor="red",
                font=dict(color="white")
            )

    st.plotly_chart(fig_sil, use_container_width=True) 
        # nanti plot elbow
            # st.info("Grafik Elbow akan ditampilkan di sini.")

    
st.write("")

    # with st.container(border=True):

    #     st.markdown("### 📝 Interpretasi Evaluasi")

    #     st.write("""

    #     Interpretasi hasil evaluasi akan ditampilkan di sini.

    #     Contoh:

    #     • Nilai inertia mulai melandai pada K = 8 sehingga dipilih
    #     sebagai kandidat jumlah cluster.

    #     • Nilai Silhouette Score tertinggi diperoleh pada K = 8
    #     sebesar 0,742 yang menunjukkan kualitas clustering
    #     paling baik dibanding jumlah cluster lainnya.

    #     """)



########################### DISTRIBUSI CLUSTER
cluster_count = (
    df_umap["cluster"]
    .value_counts()
    .sort_index()
    .reset_index()
)

cluster_count.columns = [
    "Cluster",
    "Jumlah Tweet"
]

with st.container(border=True):

    fig_cluster = px.bar(

        cluster_count,

        x="Cluster",

        y="Jumlah Tweet",

        text="Jumlah Tweet",

        color="Cluster",                 # Warna tiap cluster berbeda
        color_discrete_sequence=px.colors.qualitative.Pastel
        # Bisa diganti Pastel, Bold, Vivid, dll.
    )

    fig_cluster.update_traces(

        textposition="outside",

        textfont=dict(
            size=15,
            color="black"
        )

    )

    fig_cluster.update_layout(

        height=500,

        template="plotly_white",

        title=dict(
            text="Distribusi Jumlah Tweet pada Setiap Cluster",
            x=0.5,
            font=dict(
                size=22,
                color="#201E20"
            )
        ),

        xaxis=dict(
            title="Cluster",
            title_font=dict(
                size=18,
                color="#0A0125"
            ),
            tickfont=dict(
                size=15
            )
        ),

        yaxis=dict(
            title="Jumlah Tweet",
            title_font=dict(
                size=18,
                color="#241C3C"
            ),
            tickfont=dict(
                size=15
            )
        ),

        font=dict(
            size=14
        ),

        showlegend=False

    )

    st.plotly_chart(
        fig_cluster,
        use_container_width=True
    )

    st.divider()

##### CLUSTER TEKS
st.subheader("📂 Interpretasi Cluster")

st.caption("""
    Pilih salah satu cluster untuk melihat informasi cluster,
    WordCloud, Top Words c-TFIDF, dan contoh tweet.
    """)

df_ctfidf = pd.read_excel(
            "data/OUTPUT_MBERT/09A_ctfidf_semua.xlsx"
        )
tab0, tab1, tab2, tab3 = st.tabs([
    "Cluster 0",
    "Cluster 1",
    "Cluster 2",
    "Cluster 3"
])

with tab0:

    info, wc = st.columns([1,2], gap="large")
    with info:
         with st.container(border=True):

            st.markdown("### 📌 Informasi Cluster")

            st.metric(
                "Jumlah Tweet",
                "1891"
            )

            st.markdown("""
                    **Tema**

                    Layanan Pengiriman & Kinerja Kurir
                    """)
            top5 = (
                df_ctfidf[
                    df_ctfidf["Cluster"]==0
                ]
                .head(5)
            )

            st.write("**Top Words**")
            for kata in top5["Kata"]:

             st.markdown(f"""
                <span style="
                background:#DED8FF;
                padding:6px 20px;
                border-radius:20px;
                margin:4px;
                display:inline-block;
                font-weight:600;
                ">
                🏷️ {kata}
                </span>
                """,
             unsafe_allow_html=True)
    with wc:

        with st.container(border=True, height=800):

            st.markdown("### ☁️ WordCloud")
            st.image(
                "assets/wordcloud_0.png",
                use_container_width=True
            )
            
        with st.container(border=True):

            st.markdown("### 📈 Top Kata c-TFIDF")
            top10 = (
                df_ctfidf[df_ctfidf["Cluster"]==0].head(10)
            )

            fig = px.bar(
                top10,
                x="Score",
                y="Kata",
                orientation="h",
                color="Score",
                color_continuous_scale="purp"

            )

            fig.update_layout(
                template="plotly_white",
                height=450,
                yaxis=dict(
                    categoryorder="total ascending"
                )

            )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

with tab1:

    info, wc = st.columns([1,2], gap="large")
    with info:
         with st.container(border=True):

            st.markdown("### 📌 Informasi Cluster")

            st.metric(
                "Jumlah Tweet",
                "185"
            )

            st.markdown("""
                    **Tema**

                    Pelacakan Resi
                    """)
            top5 = (
                df_ctfidf[
                    df_ctfidf["Cluster"]==1
                ]
                .head(5)
            )

            st.write("**Top Words**")
            for kata in top5["Kata"]:

             st.markdown(f"""
                <span style="
                background:#DED8FF;
                padding:6px 20px;
                border-radius:20px;
                margin:4px;
                display:inline-block;
                font-weight:600;
                ">
                🏷️ {kata}
                </span>
                """,
             unsafe_allow_html=True)
    with wc:

        with st.container(border=True, height=800):

            st.markdown("### ☁️ WordCloud")
            st.image(
                "assets/wordcloud_1.png",
                use_container_width=True
            )
            
        with st.container(border=True):

            st.markdown("### 📈 Top Kata c-TFIDF")
            top10 = (
                df_ctfidf[df_ctfidf["Cluster"]==1].head(10)
            )

            fig = px.bar(
                top10,
                x="Score",
                y="Kata",
                orientation="h",
                color="Score",
                color_continuous_scale="purp"

            )

            fig.update_layout(
                template="plotly_white",
                height=450,
                yaxis=dict(
                    categoryorder="total ascending"
                )

            )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

with tab2:

    info, wc = st.columns([1,2], gap="large")
    with info:
         with st.container(border=True):

            st.markdown("### 📌 Informasi Cluster")

            st.metric(
                "Jumlah Tweet",
                "41"
            )

            st.markdown("""
                    **Tema**

                    Proses Pemesanan COD
                    """)
            top5 = (
                df_ctfidf[
                    df_ctfidf["Cluster"]==2
                ]
                .head(5)
            )

            st.write("**Top Words**")
            for kata in top5["Kata"]:

             st.markdown(f"""
                <span style="
                background:#DED8FF;
                padding:6px 20px;
                border-radius:20px;
                margin:4px;
                display:inline-block;
                font-weight:600;
                ">
                🏷️ {kata}
                </span>
                """,
             unsafe_allow_html=True)
    with wc:

        with st.container(border=True, height=800):

            st.markdown("### ☁️ WordCloud")
            st.image(
                "assets/wordcloud_2.png",
                use_container_width=True
            )
            
        with st.container(border=True):

            st.markdown("### 📈 Top Kata c-TFIDF")
            top10 = (
                df_ctfidf[df_ctfidf["Cluster"]==2].head(10)
            )

            fig = px.bar(
                top10,
                x="Score",
                y="Kata",
                orientation="h",
                color="Score",
                color_continuous_scale="purp"

            )

            fig.update_layout(
                template="plotly_white",
                height=450,
                yaxis=dict(
                    categoryorder="total ascending"
                )

            )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

with tab3:

    info, wc = st.columns([1,2], gap="large")
    with info:
         with st.container(border=True):

            st.markdown("### 📌 Informasi Cluster")

            st.metric(
                "Jumlah Tweet",
                "35"
            )

            st.markdown("""
                    **Tema**

                    Pembayaran COD
                    """)
            top5 = (
                df_ctfidf[
                    df_ctfidf["Cluster"]==3
                ]
                .head(5)
            )

            st.write("**Top Words**")
            for kata in top5["Kata"]:

             st.markdown(f"""
                <span style="
                background:#DED8FF;
                padding:6px 20px;
                border-radius:20px;
                margin:4px;
                display:inline-block;
                font-weight:600;
                ">
                🏷️ {kata}
                </span>
                """,
             unsafe_allow_html=True)
    with wc:

        with st.container(border=True, height=800):

            st.markdown("### ☁️ WordCloud")
            st.image(
                "assets/wordcloud_4.png",
                use_container_width=True
            )
            
        with st.container(border=True):

            st.markdown("### 📈 Top Kata c-TFIDF")
            top10 = (
                df_ctfidf[df_ctfidf["Cluster"]==3].head(10)
            )

            fig = px.bar(
                top10,
                x="Score",
                y="Kata",
                orientation="h",
                color="Score",
                color_continuous_scale="purp"

            )

            fig.update_layout(
                template="plotly_white",
                height=450,
                yaxis=dict(
                    categoryorder="total ascending"
                )

            )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


######################
# st.divider()

# st.subheader("📋 Eksplorasi Tweet per Cluster")

# st.caption("""
# Lihat contoh tweet berdasarkan hasil clustering mBERT.
# """)

# col1, col2 = st.columns(2)

# with col1:
#     pilih_cluster = st.selectbox(
#         "Pilih Cluster",
#         sorted(df_umap["cluster"].unique())
#     )

# with col2:
#     keyword = st.text_input(
#         "Cari Tweet",
#         placeholder="Masukkan kata..."
#     )

# df_show = df_umap[df_umap["cluster"] == pilih_cluster]

# if keyword:
#     df_show = df_show[
#         df_show["teks_mbert"].str.contains(
#             keyword,
#             case=False,
#             na=False
#         )
#     ]

# st.dataframe(
#     df_show[
#         [
#             "teks_mbert",
#             "Kategori",
#             "cluster"
#         ]
#     ],
#     use_container_width=True,
#     hide_index=True
# )