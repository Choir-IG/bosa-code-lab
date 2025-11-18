import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="BOSA Code Lab", layout="wide")

# ======== 页面标题和说明 ========
st.title("BOSA Code Lab – CSV Quick Explorer")

st.markdown("""
欢迎来到 **BOSA Code Lab** 🧪  

这个小工具目前可以做的事情：

1. 上传一个 `.csv` 文件  
2. 查看前几行数据、列信息  
3. 自动对数值列做描述统计  
4. 画简单的直方图 / 散点图  

后面可以逐步扩展成：EEG 预处理 demo、fMRI RSA demo、BERT–Brain 对齐可视化等不同 Lab。
""")

# ======== 上传区 ========
uploaded_file = st.file_uploader(
    "👉 在这里上传你的 CSV 文件",
    type=["csv"],
    help="文件扩展名必须是 .csv；如果是 Excel，可以先自己在本地另存为 CSV 再上传。"
)

if uploaded_file is not None:
    # 读入 CSV
    try:
        df = pd.read_csv(uploaded_file)
    except UnicodeDecodeError:
        # 尝试另一种编码
        df = pd.read_csv(uploaded_file, encoding="utf-8-sig")
    except Exception as e:
        st.error(f"读取 CSV 出错：{e}")
        st.stop()

    st.success("✅ 文件上传成功！")

    # ======== 基本信息 ========
    st.subheader("1. 基本信息")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("行数 (rows)", df.shape[0])
    with col2:
        st.metric("列数 (columns)", df.shape[1])
    with col3:
        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        st.metric("数值列数量", len(numeric_cols))

    # 显示前几行
    st.markdown("**数据预览（前 5 行）：**")
    st.dataframe(df.head())

    # 显示列信息
    with st.expander("查看所有列名和类型（dtypes）"):
        dtypes_df = pd.DataFrame({
            "column": df.columns,
            "dtype": df.dtypes.astype(str)
        })
        st.dataframe(dtypes_df)

    # ======== 描述统计 ========
    if len(numeric_cols) > 0:
        st.subheader("2. 数值列描述统计")
        st.markdown("对所有数值型列做 `pandas.DataFrame.describe()`：")

        desc = df[numeric_cols].describe().T  # 行=变量
        st.dataframe(desc)

        # ======== 可视化部分 ========
        st.subheader("3. 简单可视化")

        tab1, tab2 = st.tabs(["直方图（Histogram）", "散点图（Scatter Plot）"])

        # --- 直方图 ---
        with tab1:
            col = st.selectbox(
                "选择一个数值列画直方图：",
                numeric_cols,
                index=0
            )
            bins = st.slider("直方图 bins 数量：", min_value=5, max_value=50, value=20)

            fig, ax = plt.subplots()
            ax.hist(df[col].dropna(), bins=bins)
            ax.set_xlabel(col)
            ax.set_ylabel("频数")
            ax.set_title(f"Histogram of {col}")
            st.pyplot(fig)

        # --- 散点图 ---
        with tab2:
            st.markdown("选择两个数值列，画成散点图：")
            x_col = st.selectbox("X 轴变量：", numeric_cols, index=0, key="x_col")
            y_col = st.selectbox("Y 轴变量：", numeric_cols, index=min(1, len(numeric_cols) - 1), key="y_col")

            fig2, ax2 = plt.subplots()
            ax2.scatter(df[x_col], df[y_col], alpha=0.7)
            ax2.set_xlabel(x_col)
            ax2.set_ylabel(y_col)
            ax2.set_title(f"Scatter: {x_col} vs {y_col}")
            st.pyplot(fig2)

    else:
        st.warning("当前数据集中没有检测到数值型列，无法做描述统计和数值可视化。")
else:
    st.info("请先上传一个 CSV 文件开始分析。")
