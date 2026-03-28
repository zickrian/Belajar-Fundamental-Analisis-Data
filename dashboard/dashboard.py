from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st
from matplotlib.ticker import FuncFormatter


st.set_page_config(
    page_title="Olist Sales Dashboard",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded",
)

sns.set_theme(
    style="whitegrid",
    rc={
        "figure.facecolor": "#ffffff",
        "axes.facecolor": "#ffffff",
        "axes.edgecolor": "#d5dde5",
        "axes.labelcolor": "#183153",
        "xtick.color": "#355070",
        "ytick.color": "#355070",
        "text.color": "#183153",
        "axes.titlecolor": "#183153",
        "grid.color": "#e7edf3",
    },
)

PRIMARY_COLOR = "#1f4e79"
SECONDARY_COLOR = "#2a9d8f"
ALERT_COLOR = "#d1495b"

currency_formatter = FuncFormatter(lambda x, pos: f"R${x:,.0f}")
percent_formatter = FuncFormatter(lambda x, pos: f"{x:.0%}")


st.markdown(
    """
    <style>
    .stApp {
        color: #183153;
    }
    [data-testid="stAppViewContainer"] {
        background-color: #f6f8fb;
    }
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }
    [data-testid="stHeader"] {
        background: rgba(246, 248, 251, 0.95);
    }
    [data-testid="stSidebar"] {
        background-color: #eaf0f6;
        border-right: 1px solid #d7e0e8;
    }
    [data-testid="stSidebar"] * {
        color: #183153 !important;
    }
    [data-testid="collapsedControl"] {
        display: flex !important;
        color: #183153 !important;
    }
    [data-testid="collapsedControl"] button {
        background-color: #ffffff !important;
        border: 1px solid #d7e0e8 !important;
        border-radius: 999px !important;
        color: #183153 !important;
        box-shadow: 0 4px 12px rgba(24, 49, 83, 0.08);
    }
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #dce4ec;
        border-radius: 14px;
        padding: 0.8rem 1rem;
        box-shadow: 0 4px 14px rgba(24, 49, 83, 0.06);
    }
    div[data-testid="stMetric"] label,
    div[data-testid="stMetric"] [data-testid="stMetricLabel"],
    div[data-testid="stMetric"] [data-testid="stMetricValue"],
    div[data-testid="stMetric"] [data-testid="stMetricDelta"] {
        color: #183153 !important;
    }
    [data-testid="stExpander"] details {
        background-color: #ffffff;
        border: 1px solid #dce4ec;
        border-radius: 12px;
    }
    [data-testid="stExpander"] summary,
    [data-testid="stExpander"] p,
    [data-testid="stExpander"] li {
        color: #183153 !important;
    }
    .stMarkdown,
    .stMarkdown p,
    .stMarkdown li,
    .stCaptionContainer,
    .stText,
    p,
    label {
        color: #2b3e50 !important;
    }
    [data-testid="stDataFrame"] {
        background-color: #ffffff;
        border: 1px solid #dce4ec;
        border-radius: 12px;
    }
    div[data-baseweb="select"] > div,
    div[data-baseweb="base-input"] > div,
    div[data-baseweb="input"] > div,
    .stDateInput > div > div,
    .stMultiSelect > div > div,
    .stSelectbox > div > div,
    .stTextInput > div > div,
    .stNumberInput > div > div {
        background-color: #ffffff !important;
        color: #183153 !important;
        border: 1px solid #c9d5e2 !important;
    }
    div[data-baseweb="select"] input,
    div[data-baseweb="base-input"] input,
    div[data-baseweb="input"] input,
    .stDateInput input,
    .stMultiSelect input,
    .stSelectbox input,
    .stTextInput input,
    .stNumberInput input {
        color: #183153 !important;
        caret-color: #183153 !important;
    }
    div[role="listbox"],
    ul[role="listbox"] {
        background-color: #ffffff !important;
        color: #183153 !important;
        border: 1px solid #c9d5e2 !important;
    }
    div[role="option"] {
        background-color: #ffffff !important;
        color: #183153 !important;
    }
    div[role="option"]:hover {
        background-color: #edf4fb !important;
    }
    .stDateInput button,
    .stMultiSelect button,
    .stSelectbox button {
        color: #183153 !important;
    }
    h1, h2, h3 {
        color: #183153;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_main_data() -> pd.DataFrame:
    data_path = Path(__file__).resolve().parent / "main_data.csv"
    df = pd.read_csv(data_path)
    df["order_purchase_timestamp"] = pd.to_datetime(
        df["order_purchase_timestamp"], errors="coerce"
    )

    for col in ["is_delivered", "is_late"]:
        if df[col].dtype == "object":
            df[col] = df[col].astype(str).str.lower().map(
                {"true": True, "false": False}
            )

    numeric_cols = [
        "items_count",
        "items_price_sum",
        "freight_sum",
        "payment_value_sum",
        "review_score_mean",
        "delivery_delay_days",
        "revenue",
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


@st.cache_data
def load_category_data() -> pd.DataFrame:
    base_dir = Path(__file__).resolve().parent.parent / "data"
    order_items = pd.read_csv(
        base_dir / "olist_order_items_dataset.csv",
        usecols=["order_id", "product_id", "price"],
    )
    products = pd.read_csv(
        base_dir / "olist_products_dataset.csv",
        usecols=["product_id", "product_category_name"],
    )
    translation = pd.read_csv(
        base_dir / "product_category_name_translation.csv",
        usecols=["product_category_name", "product_category_name_english"],
    )

    category_data = (
        order_items.merge(products, on="product_id", how="left")
        .merge(translation, on="product_category_name", how="left")
        .assign(
            product_category_name_english=lambda df: df[
                "product_category_name_english"
            ].fillna("unknown")
        )
    )

    return category_data[["order_id", "product_category_name_english", "price"]]


def format_currency(value: float) -> str:
    return f"R${value:,.0f}"


def format_percent(value: float) -> str:
    return f"{value:.1%}" if pd.notna(value) else "-"


def filter_main_data(
    df: pd.DataFrame,
    start_date,
    end_date,
    selected_states: list[str],
) -> pd.DataFrame:
    filtered = df.copy()
    filtered = filtered.loc[
        filtered["order_purchase_timestamp"].dt.date.between(start_date, end_date)
    ]

    if selected_states:
        filtered = filtered.loc[filtered["customer_state"].isin(selected_states)]

    return filtered


def build_monthly_trend(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["order_purchase_month", "orders", "revenue"])

    monthly = (
        df.assign(
            order_purchase_month=df["order_purchase_timestamp"].dt.to_period("M").astype(
                str
            )
        )
        .groupby("order_purchase_month", as_index=False)
        .agg(orders=("order_id", "nunique"), revenue=("revenue", "sum"))
        .sort_values("order_purchase_month")
    )
    return monthly


def build_category_revenue(
    filtered_delivered: pd.DataFrame, category_data: pd.DataFrame
) -> pd.DataFrame:
    if filtered_delivered.empty:
        return pd.DataFrame(columns=["product_category_name_english", "revenue"])

    selected_orders = filtered_delivered["order_id"].unique()
    category_revenue = (
        category_data.loc[category_data["order_id"].isin(selected_orders)]
        .groupby("product_category_name_english", as_index=False)
        .agg(revenue=("price", "sum"))
        .sort_values("revenue", ascending=False)
    )
    return category_revenue


def build_late_by_state(delay_df: pd.DataFrame) -> pd.DataFrame:
    if delay_df.empty:
        return pd.DataFrame(columns=["customer_state", "total_orders", "late_rate"])

    late_by_state = (
        delay_df.groupby("customer_state", as_index=False)
        .agg(
            total_orders=("order_id", "nunique"),
            late_orders=("is_late", "sum"),
            late_rate=("is_late", "mean"),
        )
        .sort_values(["late_rate", "late_orders"], ascending=[False, False])
    )

    stable_states = late_by_state.loc[late_by_state["total_orders"] >= 20]
    return stable_states if not stable_states.empty else late_by_state


def build_rating_by_delivery_status(review_df: pd.DataFrame) -> pd.DataFrame:
    if review_df.empty:
        return pd.DataFrame(columns=["delivery_status", "avg_review", "order_count"])

    return (
        review_df.assign(
            delivery_status=lambda df: df["is_late"].map(
                {
                    True: "Terlambat",
                    False: "Tepat waktu / lebih cepat",
                }
            )
        )
        .groupby("delivery_status", as_index=False)
        .agg(
            avg_review=("review_score_mean", "mean"),
            order_count=("order_id", "nunique"),
        )
        .sort_values("avg_review", ascending=False)
    )


def build_customers_by_state(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["customer_state", "customers"])

    return (
        df[["customer_unique_id", "customer_state"]]
        .dropna()
        .drop_duplicates()
        .groupby("customer_state", as_index=False)
        .agg(customers=("customer_unique_id", "nunique"))
        .sort_values("customers", ascending=False)
    )


def main() -> None:
    main_data = load_main_data()
    category_data = load_category_data()

    min_date = main_data["order_purchase_timestamp"].min().date()
    max_date = main_data["order_purchase_timestamp"].max().date()
    state_options = sorted(main_data["customer_state"].dropna().unique().tolist())

    st.title("Brazilian E-Commerce Dashboard")
    st.caption(
        "Dashboard ini merangkum tren pesanan, pendapatan, keterlambatan pengiriman, "
        "dan persebaran pelanggan pada dataset Olist."
    )

    with st.expander("Business Questions"):
        st.markdown(
            """
            1. Bagaimana tren jumlah pesanan dan pendapatan dari waktu ke waktu, serta kategori produk apa yang memberikan kontribusi terbesar terhadap pendapatan?
            2. Seberapa sering terjadi keterlambatan pengiriman, wilayah mana yang paling sering mengalami keterlambatan, dan apakah keterlambatan tersebut berpengaruh terhadap penilaian pelanggan?
            3. Wilayah mana yang memiliki jumlah pelanggan terbanyak?
            """
        )

    with st.sidebar:
        st.header("Filter Data")
        selected_dates = st.date_input(
            "Rentang tanggal pembelian",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
        )

        if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
            start_date, end_date = selected_dates
        else:
            start_date = end_date = selected_dates

        selected_states = st.multiselect(
            "Pilih state",
            options=state_options,
            default=state_options,
        )

    if not selected_states:
        st.warning("Pilih minimal satu state agar dashboard dapat menampilkan hasil.")
        st.stop()

    filtered_main = filter_main_data(main_data, start_date, end_date, selected_states)
    filtered_delivered = filtered_main.loc[filtered_main["is_delivered"]].copy()
    filtered_delay = filtered_delivered.dropna(subset=["delivery_delay_days"]).copy()
    filtered_review = filtered_delivered.dropna(
        subset=["delivery_delay_days", "review_score_mean"]
    ).copy()

    if filtered_main.empty:
        st.warning(
            "Tidak ada data pada kombinasi filter saat ini. Coba perluas rentang tanggal atau state."
        )
        st.stop()

    monthly_trend = build_monthly_trend(filtered_delivered)
    category_revenue = build_category_revenue(filtered_delivered, category_data)
    late_by_state = build_late_by_state(filtered_delay)
    rating_by_delivery_status = build_rating_by_delivery_status(filtered_review)
    customers_by_state = build_customers_by_state(filtered_main)

    total_orders = filtered_main["order_id"].nunique()
    total_revenue = filtered_delivered["revenue"].sum()
    late_rate = filtered_delay["is_late"].mean()
    avg_review = filtered_review["review_score_mean"].mean()

    metric_cols = st.columns(4)
    metric_cols[0].metric("Total Orders", f"{total_orders:,}")
    metric_cols[1].metric("Revenue (Proxy)", format_currency(total_revenue))
    metric_cols[2].metric("Late Delivery Rate", format_percent(late_rate))
    metric_cols[3].metric(
        "Average Review",
        f"{avg_review:.2f}" if pd.notna(avg_review) else "-",
    )

    st.markdown(
        f"""
        Filter aktif: **{start_date}** sampai **{end_date}** pada **{len(selected_states)} state**.
        Revenue dihitung dari order delivered agar konsisten dengan analisis di notebook.
        """
    )

    insight_col_1, insight_col_2 = st.columns(2)

    with insight_col_1:
        st.subheader("Pertanyaan 1: Tren dan Kontributor Pendapatan")

        if not monthly_trend.empty:
            peak_month = monthly_trend.loc[monthly_trend["orders"].idxmax()]
            st.write(
                f"Puncak pesanan pada filter saat ini terjadi di **{peak_month['order_purchase_month']}** "
                f"dengan **{int(peak_month['orders']):,} order** dan revenue sekitar "
                f"**{format_currency(peak_month['revenue'])}**."
            )
        else:
            st.write("Belum ada data order delivered pada filter saat ini.")

        fig, ax = plt.subplots(1, 2, figsize=(14, 4.5))

        if not monthly_trend.empty:
            sns.lineplot(
                data=monthly_trend,
                x="order_purchase_month",
                y="orders",
                marker="o",
                color=PRIMARY_COLOR,
                ax=ax[0],
            )
            sns.lineplot(
                data=monthly_trend,
                x="order_purchase_month",
                y="revenue",
                marker="o",
                color=SECONDARY_COLOR,
                ax=ax[1],
            )
            ax[1].yaxis.set_major_formatter(currency_formatter)
        else:
            ax[0].text(0.5, 0.5, "Tidak ada data", ha="center", va="center")
            ax[1].text(0.5, 0.5, "Tidak ada data", ha="center", va="center")

        ax[0].set_title("Tren Jumlah Pesanan per Bulan")
        ax[0].set_xlabel("Bulan")
        ax[0].set_ylabel("Jumlah Pesanan")
        ax[0].tick_params(axis="x", rotation=45)

        ax[1].set_title("Tren Revenue per Bulan")
        ax[1].set_xlabel("Bulan")
        ax[1].set_ylabel("Revenue")
        ax[1].tick_params(axis="x", rotation=45)

        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        st.subheader("Kategori dengan Pendapatan Tertinggi")
        fig, ax = plt.subplots(figsize=(8, 4.8))
        top_categories = category_revenue.head(10)

        if not top_categories.empty:
            sns.barplot(
                data=top_categories,
                y="product_category_name_english",
                x="revenue",
                color=PRIMARY_COLOR,
                ax=ax,
            )
            ax.xaxis.set_major_formatter(currency_formatter)
        else:
            ax.text(0.5, 0.5, "Tidak ada data", ha="center", va="center")

        ax.set_title("Top 10 Kategori Produk berdasarkan Pendapatan")
        ax.set_xlabel("Revenue dari Harga Item")
        ax.set_ylabel("Kategori Produk")
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    with insight_col_2:
        st.subheader("Pertanyaan 2: Keterlambatan dan Rating Pelanggan")

        if not late_by_state.empty:
            highest_late_state = late_by_state.iloc[0]
            st.write(
                f"State dengan late rate tertinggi pada filter saat ini adalah **{highest_late_state['customer_state']}** "
                f"dengan tingkat keterlambatan **{highest_late_state['late_rate']:.1%}**."
            )
        else:
            st.write("Data keterlambatan belum cukup untuk dihitung pada filter saat ini.")

        fig, ax = plt.subplots(figsize=(8, 4.8))
        top_late_states = late_by_state.head(10)

        if not top_late_states.empty:
            sns.barplot(
                data=top_late_states,
                y="customer_state",
                x="late_rate",
                color=ALERT_COLOR,
                ax=ax,
            )
            ax.xaxis.set_major_formatter(percent_formatter)
        else:
            ax.text(0.5, 0.5, "Tidak ada data", ha="center", va="center")

        ax.set_title("Top 10 State dengan Late Rate Tertinggi")
        ax.set_xlabel("Late Rate")
        ax.set_ylabel("State")
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        fig, ax = plt.subplots(figsize=(8, 4.8))
        review_box = filtered_review.assign(
            delivery_status=lambda df: df["is_late"].map(
                {
                    True: "Terlambat",
                    False: "Tepat waktu / lebih cepat",
                }
            )
        )

        if not review_box.empty:
            sns.boxplot(
                data=review_box,
                x="delivery_status",
                y="review_score_mean",
                hue="delivery_status",
                palette={
                    "Tepat waktu / lebih cepat": SECONDARY_COLOR,
                    "Terlambat": ALERT_COLOR,
                },
                dodge=False,
                ax=ax,
            )
            legend = ax.get_legend()
            if legend is not None:
                legend.remove()
        else:
            ax.text(0.5, 0.5, "Tidak ada data", ha="center", va="center")

        ax.set_title("Sebaran Rating berdasarkan Status Pengiriman")
        ax.set_xlabel("Status Pengiriman")
        ax.set_ylabel("Review Score")
        ax.set_ylim(0, 5.2)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    st.subheader("Pertanyaan 3: Wilayah dengan Pelanggan Terbanyak")

    top_customer_states = customers_by_state.head(10)
    if not top_customer_states.empty:
        top_customer_state = top_customer_states.iloc[0]
        st.write(
            f"State dengan pelanggan unik terbanyak pada filter saat ini adalah **{top_customer_state['customer_state']}** "
            f"dengan **{int(top_customer_state['customers']):,} pelanggan**."
        )
    else:
        st.write("Belum ada data pelanggan pada filter saat ini.")

    fig, ax = plt.subplots(figsize=(10, 4.8))
    if not top_customer_states.empty:
        sns.barplot(
            data=top_customer_states,
            x="customer_state",
            y="customers",
            color=PRIMARY_COLOR,
            ax=ax,
        )
    else:
        ax.text(0.5, 0.5, "Tidak ada data", ha="center", va="center")

    ax.set_title("Top 10 State dengan Pelanggan Terbanyak")
    ax.set_xlabel("State")
    ax.set_ylabel("Jumlah Pelanggan Unik")
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.subheader("Tabel Ringkasan")
    table_col_1, table_col_2 = st.columns(2)

    with table_col_1:
        st.dataframe(
            monthly_trend.rename(
                columns={
                    "order_purchase_month": "Month",
                    "orders": "Orders",
                    "revenue": "Revenue",
                }
            ),
            use_container_width=True,
        )

    with table_col_2:
        st.dataframe(
            late_by_state.head(10).rename(
                columns={
                    "customer_state": "State",
                    "total_orders": "Orders",
                    "late_orders": "Late Orders",
                    "late_rate": "Late Rate",
                }
            ),
            use_container_width=True,
        )


if __name__ == "__main__":
    main()
