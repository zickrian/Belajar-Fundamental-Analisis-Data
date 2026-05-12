from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Olist Sales Dashboard",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded",
)


PRIMARY_COLOR = "#2454A6"
SECONDARY_COLOR = "#0F8B8D"
ALERT_COLOR = "#C8465A"
INK_COLOR = "#172033"
MUTED_COLOR = "#667085"
PANEL_BORDER = "#E3E8EF"
PANEL_BG = "#FFFFFF"
APP_BG = "#F4F7FB"


st.markdown(
    f"""
    <style>
    :root {{
        --app-bg: {APP_BG};
        --panel-bg: {PANEL_BG};
        --panel-border: {PANEL_BORDER};
        --ink: {INK_COLOR};
        --muted: {MUTED_COLOR};
        --primary: {PRIMARY_COLOR};
        --secondary: {SECONDARY_COLOR};
        --alert: {ALERT_COLOR};
    }}

    .stApp {{
        color: var(--ink);
        background: var(--app-bg);
    }}

    [data-testid="stAppViewContainer"] {{
        background:
            linear-gradient(180deg, #EEF4FF 0, #F7FAFC 320px, #F4F7FB 100%);
    }}

    [data-testid="stHeader"] {{
        background: rgba(244, 247, 251, 0.82);
        backdrop-filter: blur(12px);
    }}

    .block-container {{
        max-width: 1320px;
        padding: 1.1rem 2rem 2.4rem;
    }}

    h1, h2, h3, p, label, span, .stMarkdown {{
        color: var(--ink);
    }}

    h1 {{
        font-size: 2.35rem;
        line-height: 1.08;
        margin-bottom: 0.35rem;
    }}

    h2 {{
        font-size: 1.35rem;
        margin-top: 0.8rem;
        margin-bottom: 0.45rem;
    }}

    h3 {{
        font-size: 1.05rem;
        margin-top: 0.55rem;
    }}

    .muted, .muted * {{
        color: var(--muted) !important;
    }}

    .hero {{
        padding: 1.15rem 0 0.65rem;
    }}

    .hero-kicker {{
        width: fit-content;
        padding: 0.28rem 0.62rem;
        border: 1px solid #C9D8F2;
        border-radius: 999px;
        background: rgba(255,255,255,0.72);
        color: #2454A6;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0;
        margin-bottom: 0.7rem;
    }}

    .hero-subtitle {{
        max-width: 860px;
        color: var(--muted);
        font-size: 1.02rem;
        line-height: 1.58;
        margin-bottom: 0.35rem;
    }}

    div[data-testid="stMetric"] {{
        min-height: 118px;
        background: var(--panel-bg);
        border: 1px solid var(--panel-border);
        border-radius: 8px;
        padding: 0.95rem 1rem;
        box-shadow: 0 14px 34px rgba(23, 32, 51, 0.07);
    }}

    div[data-testid="stMetric"] label,
    div[data-testid="stMetric"] [data-testid="stMetricLabel"],
    div[data-testid="stMetric"] [data-testid="stMetricValue"],
    div[data-testid="stMetric"] [data-testid="stMetricDelta"] {{
        color: var(--ink) !important;
    }}

    div[data-testid="stMetric"] [data-testid="stMetricLabel"] {{
        color: var(--muted) !important;
        font-size: 0.86rem;
    }}

    div[data-testid="stMetric"] [data-testid="stMetricValue"] {{
        font-size: 1.62rem;
        letter-spacing: 0;
    }}

    .insight {{
        background: #FFFFFF;
        border: 1px solid var(--panel-border);
        border-radius: 8px;
        padding: 0.95rem 1rem;
        margin: 0.25rem 0 0.9rem;
        box-shadow: 0 8px 22px rgba(23, 32, 51, 0.045);
        color: var(--muted);
        line-height: 1.55;
    }}

    .insight strong {{
        color: var(--ink);
        display: inline-block;
        margin-bottom: 0.18rem;
    }}

    .section-note {{
        color: var(--muted);
        font-size: 0.92rem;
        line-height: 1.55;
        margin-top: -0.2rem;
        margin-bottom: 0.8rem;
    }}

    [data-testid="stSidebar"] {{
        background: #FFFFFF;
        border-right: 1px solid var(--panel-border);
    }}

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] span {{
        color: var(--ink) !important;
    }}

    [data-testid="stSidebar"] .stMarkdown p {{
        color: var(--muted) !important;
        line-height: 1.48;
    }}

    [data-testid="stSidebar"] hr {{
        margin: 1rem 0;
        border-color: var(--panel-border);
    }}

    [data-testid="stSidebar"] [data-testid="stMetric"] {{
        min-height: auto;
        box-shadow: none;
        background: #F8FAFC;
    }}

    div[data-baseweb="select"] > div,
    div[data-baseweb="base-input"] > div,
    div[data-baseweb="input"] > div,
    .stDateInput > div > div,
    .stMultiSelect > div > div,
    .stRadio > div,
    .stSelectbox > div > div {{
        background-color: #FFFFFF !important;
        border-color: #CBD5E1 !important;
        color: var(--ink) !important;
    }}

    div[role="listbox"],
    ul[role="listbox"] {{
        background-color: #FFFFFF !important;
        border: 1px solid #CBD5E1 !important;
    }}

    div[role="option"] {{
        color: var(--ink) !important;
    }}

    div[role="option"]:hover {{
        background-color: #EEF4FF !important;
    }}

    [data-testid="stTabs"] button {{
        color: var(--muted);
        font-weight: 700;
    }}

    [data-testid="stTabs"] button[aria-selected="true"] {{
        color: var(--primary);
    }}

    [data-testid="stDataFrame"],
    [data-testid="stExpander"] details {{
        background: #FFFFFF;
        border: 1px solid var(--panel-border);
        border-radius: 8px;
        overflow: hidden;
    }}

    [data-testid="stAlert"] {{
        border-radius: 8px;
    }}

    @media (max-width: 760px) {{
        .block-container {{
            padding-left: 1rem;
            padding-right: 1rem;
        }}
        h1 {{
            font-size: 1.85rem;
        }}
        div[data-testid="stMetric"] [data-testid="stMetricValue"] {{
            font-size: 1.34rem;
        }}
    }}
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
    if pd.isna(value):
        return "-"
    return f"R${value:,.0f}"


def format_currency_short(value: float) -> str:
    if pd.isna(value):
        return "-"
    if abs(value) >= 1_000_000:
        return f"R${value / 1_000_000:.2f}M"
    if abs(value) >= 1_000:
        return f"R${value / 1_000:.1f}K"
    return f"R${value:,.0f}"


def format_percent(value: float) -> str:
    return f"{value:.1%}" if pd.notna(value) else "-"


def format_number(value: float) -> str:
    return f"{value:,.0f}" if pd.notna(value) else "-"


def render_insight(text: str, color: str | None = None) -> None:
    st.markdown(
        f"""
        <div class="insight">
            {text}
        </div>
        """,
        unsafe_allow_html=True,
    )


def empty_state(message: str) -> None:
    st.info(message)


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
        return pd.DataFrame(
            columns=["order_purchase_month", "order_purchase_date", "orders", "revenue"]
        )

    monthly = (
        df.assign(order_purchase_date=df["order_purchase_timestamp"].dt.to_period("M"))
        .groupby("order_purchase_date", as_index=False)
        .agg(orders=("order_id", "nunique"), revenue=("revenue", "sum"))
        .sort_values("order_purchase_date")
    )
    monthly["order_purchase_month"] = monthly["order_purchase_date"].astype(str)
    monthly["order_purchase_date"] = monthly["order_purchase_date"].dt.to_timestamp()
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
        return pd.DataFrame(
            columns=["customer_state", "total_orders", "late_orders", "late_rate"]
        )

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


def build_payment_mix(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["payment_type_primary", "orders", "share"])

    payment_mix = (
        df.dropna(subset=["payment_type_primary"])
        .groupby("payment_type_primary", as_index=False)
        .agg(orders=("order_id", "nunique"))
        .sort_values("orders", ascending=False)
    )
    total_orders = payment_mix["orders"].sum()
    payment_mix["share"] = payment_mix["orders"] / total_orders if total_orders else 0
    return payment_mix


def build_city_customers(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["customer_city", "customer_state", "customers"])

    return (
        df[["customer_unique_id", "customer_city", "customer_state"]]
        .dropna()
        .drop_duplicates()
        .groupby(["customer_city", "customer_state"], as_index=False)
        .agg(customers=("customer_unique_id", "nunique"))
        .sort_values("customers", ascending=False)
    )


def make_monthly_chart(monthly_trend: pd.DataFrame, metric: str) -> alt.Chart:
    titles = {"orders": "Jumlah pesanan", "revenue": "Revenue"}
    axis = alt.Axis(
        title=titles[metric],
        format="$,.0s" if metric == "revenue" else ",.0f",
    )

    return (
        alt.Chart(monthly_trend)
        .mark_area(
            line={"color": PRIMARY_COLOR if metric == "orders" else SECONDARY_COLOR},
            color=PRIMARY_COLOR if metric == "orders" else SECONDARY_COLOR,
            opacity=0.16,
            interpolate="monotone",
        )
        .encode(
            x=alt.X(
                "order_purchase_date:T",
                title="Bulan pembelian",
                axis=alt.Axis(format="%b %Y", labelAngle=-35),
            ),
            y=alt.Y(f"{metric}:Q", title=titles[metric], axis=axis),
            tooltip=[
                alt.Tooltip("order_purchase_month:N", title="Bulan"),
                alt.Tooltip("orders:Q", title="Pesanan", format=",.0f"),
                alt.Tooltip("revenue:Q", title="Revenue", format="$,.0f"),
            ],
        )
        .properties(height=320)
    )


def make_bar_chart(
    data: pd.DataFrame,
    category_col: str,
    value_col: str,
    title_col: str,
    color: str,
    value_format: str,
    height: int = 360,
) -> alt.Chart:
    return (
        alt.Chart(data)
        .mark_bar(cornerRadiusTopRight=5, cornerRadiusBottomRight=5, color=color)
        .encode(
            x=alt.X(
                f"{value_col}:Q",
                title=None,
                axis=alt.Axis(format=value_format, grid=True),
            ),
            y=alt.Y(
                f"{category_col}:N",
                title=None,
                sort="-x",
                axis=alt.Axis(labelLimit=210),
            ),
            tooltip=[
                alt.Tooltip(f"{title_col}:N", title="Kategori"),
                alt.Tooltip(f"{value_col}:Q", title="Nilai", format=value_format),
            ],
        )
        .properties(height=height)
    )


def main() -> None:
    main_data = load_main_data()
    category_data = load_category_data()

    min_date = main_data["order_purchase_timestamp"].min().date()
    max_date = main_data["order_purchase_timestamp"].max().date()
    state_options = sorted(main_data["customer_state"].dropna().unique().tolist())

    with st.sidebar:
        st.markdown("### Olist Dashboard")
        st.markdown(
            "Gunakan panel ini untuk mempersempit periode dan wilayah pelanggan. "
            "Semua visual di kanan akan mengikuti filter yang aktif."
        )
        st.divider()

        selected_dates = st.date_input(
            "Periode pembelian",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
            help="Tanggal berdasarkan order_purchase_timestamp.",
        )

        if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
            start_date, end_date = selected_dates
        else:
            start_date = end_date = selected_dates

        state_scope = st.radio(
            "Cakupan state",
            options=["Semua state", "Pilih manual"],
            horizontal=True,
        )

        if state_scope == "Semua state":
            selected_states = state_options
            st.caption(f"{len(state_options)} state aktif.")
        else:
            selected_states = st.multiselect(
                "State yang dianalisis",
                options=state_options,
                default=state_options[:8],
                help="Pilih beberapa state untuk membandingkan performa wilayah.",
            )

        st.divider()
        st.markdown("#### Catatan data")
        st.markdown(
            "- Revenue memakai order berstatus delivered.\n"
            "- Late rate dihitung dari selisih estimasi dan tanggal delivery.\n"
            "- Rating memakai rata-rata review per order."
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
    customers_by_city = build_city_customers(filtered_main)
    payment_mix = build_payment_mix(filtered_main)

    total_orders = filtered_main["order_id"].nunique()
    delivered_orders = filtered_delivered["order_id"].nunique()
    total_revenue = filtered_delivered["revenue"].sum()
    late_rate = filtered_delay["is_late"].mean()
    avg_review = filtered_review["review_score_mean"].mean()
    unique_customers = filtered_main["customer_unique_id"].nunique()
    avg_order_value = total_revenue / delivered_orders if delivered_orders else 0

    st.markdown(
        """
        <div class="hero">
            <div class="hero-kicker">Brazilian E-Commerce Public Dataset by Olist</div>
            <h1>Sales, Delivery, and Customer Dashboard</h1>
            <p class="hero-subtitle">
                Dashboard ini menyatukan tren penjualan, kualitas pengiriman, rating pelanggan,
                dan persebaran wilayah agar performa bisnis bisa dibaca dari satu tempat.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    kpi_cols = st.columns(5)
    kpi_cols[0].metric("Total Orders", format_number(total_orders))
    kpi_cols[1].metric("Delivered Revenue", format_currency_short(total_revenue))
    kpi_cols[2].metric("Avg Order Value", format_currency_short(avg_order_value))
    kpi_cols[3].metric("Late Delivery Rate", format_percent(late_rate))
    kpi_cols[4].metric(
        "Average Review", f"{avg_review:.2f} / 5" if pd.notna(avg_review) else "-"
    )

    st.markdown(
        f"""
        <p class="section-note">
            Filter aktif: <strong>{start_date}</strong> sampai <strong>{end_date}</strong>,
            <strong>{len(selected_states)}</strong> state, <strong>{format_number(unique_customers)}</strong>
            pelanggan unik.
        </p>
        """,
        unsafe_allow_html=True,
    )

    overview_tab, sales_tab, delivery_tab, customer_tab, data_tab = st.tabs(
        ["Overview", "Sales", "Delivery", "Customers", "Data"]
    )

    with overview_tab:
        left, right = st.columns([1.35, 1])

        with left:
            st.subheader("Tren pesanan bulanan")
            st.markdown(
                '<p class="section-note">Pergerakan volume order delivered dari bulan ke bulan.</p>',
                unsafe_allow_html=True,
            )
            if monthly_trend.empty:
                empty_state("Belum ada order delivered pada filter saat ini.")
            else:
                st.altair_chart(
                    make_monthly_chart(monthly_trend, "orders").configure_axis(
                        labelColor=MUTED_COLOR,
                        titleColor=MUTED_COLOR,
                        gridColor="#E8EDF4",
                    ),
                    use_container_width=True,
                )

        with right:
            st.subheader("Komposisi pembayaran")
            st.markdown(
                '<p class="section-note">Metode pembayaran paling sering dipakai pelanggan.</p>',
                unsafe_allow_html=True,
            )
            if payment_mix.empty:
                empty_state("Belum ada data pembayaran.")
            else:
                payment_chart = (
                    alt.Chart(payment_mix)
                    .mark_arc(innerRadius=68, outerRadius=118, stroke="#FFFFFF")
                    .encode(
                        theta=alt.Theta("orders:Q"),
                        color=alt.Color(
                            "payment_type_primary:N",
                            title=None,
                            scale=alt.Scale(
                                range=[
                                    PRIMARY_COLOR,
                                    SECONDARY_COLOR,
                                    "#F2A541",
                                    ALERT_COLOR,
                                    "#6C5CE7",
                                ]
                            ),
                        ),
                        tooltip=[
                            alt.Tooltip(
                                "payment_type_primary:N", title="Metode pembayaran"
                            ),
                            alt.Tooltip("orders:Q", title="Pesanan", format=",.0f"),
                            alt.Tooltip("share:Q", title="Share", format=".1%"),
                        ],
                    )
                    .properties(height=320)
                )
                st.altair_chart(payment_chart, use_container_width=True)

        insight_cols = st.columns(3)
        peak_month = (
            monthly_trend.loc[monthly_trend["orders"].idxmax()]
            if not monthly_trend.empty
            else None
        )
        top_category = category_revenue.iloc[0] if not category_revenue.empty else None
        top_state = customers_by_state.iloc[0] if not customers_by_state.empty else None

        with insight_cols[0]:
            render_insight(
                f"<strong>Puncak order:</strong><br>{peak_month['order_purchase_month']} "
                f"dengan {int(peak_month['orders']):,} order."
                if peak_month is not None
                else "<strong>Puncak order:</strong><br>Belum tersedia."
            )
        with insight_cols[1]:
            render_insight(
                f"<strong>Kategori terbesar:</strong><br>{top_category['product_category_name_english']} "
                f"menghasilkan {format_currency_short(top_category['revenue'])}."
                if top_category is not None
                else "<strong>Kategori terbesar:</strong><br>Belum tersedia.",
                SECONDARY_COLOR,
            )
        with insight_cols[2]:
            render_insight(
                f"<strong>Basis pelanggan:</strong><br>{top_state['customer_state']} memimpin "
                f"dengan {int(top_state['customers']):,} pelanggan unik."
                if top_state is not None
                else "<strong>Basis pelanggan:</strong><br>Belum tersedia.",
                "#F2A541",
            )

    with sales_tab:
        st.subheader("Revenue dan kategori produk")
        st.markdown(
            '<p class="section-note">Tab ini menjawab pertanyaan bisnis pertama: tren sales dan kontributor revenue.</p>',
            unsafe_allow_html=True,
        )

        col_a, col_b = st.columns([1.1, 1])
        with col_a:
            if monthly_trend.empty:
                empty_state("Belum ada revenue delivered pada filter saat ini.")
            else:
                st.altair_chart(
                    make_monthly_chart(monthly_trend, "revenue").configure_axis(
                        labelColor=MUTED_COLOR,
                        titleColor=MUTED_COLOR,
                        gridColor="#E8EDF4",
                    ),
                    use_container_width=True,
                )

        with col_b:
            top_categories = category_revenue.head(10)
            if top_categories.empty:
                empty_state("Belum ada data kategori pada filter saat ini.")
            else:
                top_categories = top_categories.assign(
                    category_label=top_categories["product_category_name_english"].str.replace(
                        "_", " ", regex=False
                    )
                )
                st.altair_chart(
                    make_bar_chart(
                        top_categories,
                        "category_label",
                        "revenue",
                        "category_label",
                        PRIMARY_COLOR,
                        "$,.0s",
                    ).configure_axis(
                        labelColor=MUTED_COLOR,
                        titleColor=MUTED_COLOR,
                        gridColor="#E8EDF4",
                    ),
                    use_container_width=True,
                )

        if not category_revenue.empty:
            category_share = category_revenue.iloc[0]["revenue"] / category_revenue[
                "revenue"
            ].sum()
            render_insight(
                f"<strong>Insight sales:</strong> kategori teratas menyumbang "
                f"{format_percent(category_share)} dari revenue item pada filter aktif. "
                "Ini membantu memisahkan kategori utama dari long-tail kategori lain."
            )

    with delivery_tab:
        st.subheader("Keterlambatan pengiriman dan dampaknya ke rating")
        st.markdown(
            '<p class="section-note">Tab ini menjawab wilayah mana yang paling sering terlambat dan bagaimana rating pelanggan berubah.</p>',
            unsafe_allow_html=True,
        )

        col_a, col_b = st.columns([1, 1])
        with col_a:
            top_late_states = late_by_state.head(10)
            if top_late_states.empty:
                empty_state("Data keterlambatan belum cukup untuk dihitung.")
            else:
                st.altair_chart(
                    make_bar_chart(
                        top_late_states,
                        "customer_state",
                        "late_rate",
                        "customer_state",
                        ALERT_COLOR,
                        ".0%",
                    ).encode(
                        tooltip=[
                            alt.Tooltip("customer_state:N", title="State"),
                            alt.Tooltip("late_rate:Q", title="Late rate", format=".1%"),
                            alt.Tooltip(
                                "total_orders:Q", title="Total order", format=",.0f"
                            ),
                            alt.Tooltip(
                                "late_orders:Q", title="Order terlambat", format=",.0f"
                            ),
                        ]
                    ).configure_axis(
                        labelColor=MUTED_COLOR,
                        titleColor=MUTED_COLOR,
                        gridColor="#E8EDF4",
                    ),
                    use_container_width=True,
                )

        with col_b:
            if rating_by_delivery_status.empty:
                empty_state("Belum ada data review untuk filter saat ini.")
            else:
                rating_chart = (
                    alt.Chart(rating_by_delivery_status)
                    .mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5)
                    .encode(
                        x=alt.X("delivery_status:N", title=None, sort=None),
                        y=alt.Y(
                            "avg_review:Q",
                            title="Average review score",
                            scale=alt.Scale(domain=[0, 5]),
                        ),
                        color=alt.Color(
                            "delivery_status:N",
                            title=None,
                            scale=alt.Scale(
                                domain=["Tepat waktu / lebih cepat", "Terlambat"],
                                range=[SECONDARY_COLOR, ALERT_COLOR],
                            ),
                        ),
                        tooltip=[
                            alt.Tooltip("delivery_status:N", title="Status"),
                            alt.Tooltip("avg_review:Q", title="Avg review", format=".2f"),
                            alt.Tooltip(
                                "order_count:Q", title="Jumlah order", format=",.0f"
                            ),
                        ],
                    )
                    .properties(height=360)
                    .configure_axis(
                        labelColor=MUTED_COLOR,
                        titleColor=MUTED_COLOR,
                        gridColor="#E8EDF4",
                    )
                    .configure_view(strokeWidth=0)
                )
                st.altair_chart(rating_chart, use_container_width=True)

        if not late_by_state.empty:
            highest_late_state = late_by_state.iloc[0]
            render_insight(
                f"<strong>Insight delivery:</strong> {highest_late_state['customer_state']} "
                f"memiliki late rate tertinggi sebesar {format_percent(highest_late_state['late_rate'])} "
                f"dari {int(highest_late_state['total_orders']):,} order delivered yang punya data estimasi.",
                ALERT_COLOR,
            )

    with customer_tab:
        st.subheader("Persebaran pelanggan")
        st.markdown(
            '<p class="section-note">Tab ini memperlihatkan state dan kota dengan pelanggan unik terbanyak.</p>',
            unsafe_allow_html=True,
        )

        col_a, col_b = st.columns([1, 1])
        with col_a:
            top_customer_states = customers_by_state.head(10)
            if top_customer_states.empty:
                empty_state("Belum ada data pelanggan pada filter saat ini.")
            else:
                st.altair_chart(
                    make_bar_chart(
                        top_customer_states,
                        "customer_state",
                        "customers",
                        "customer_state",
                        SECONDARY_COLOR,
                        ",.0f",
                    ).configure_axis(
                        labelColor=MUTED_COLOR,
                        titleColor=MUTED_COLOR,
                        gridColor="#E8EDF4",
                    ),
                    use_container_width=True,
                )

        with col_b:
            top_customer_cities = customers_by_city.head(10).assign(
                city_label=lambda df: df["customer_city"].str.title()
                + ", "
                + df["customer_state"]
            )
            if top_customer_cities.empty:
                empty_state("Belum ada data kota pada filter saat ini.")
            else:
                st.altair_chart(
                    make_bar_chart(
                        top_customer_cities,
                        "city_label",
                        "customers",
                        "city_label",
                        PRIMARY_COLOR,
                        ",.0f",
                    ).configure_axis(
                        labelColor=MUTED_COLOR,
                        titleColor=MUTED_COLOR,
                        gridColor="#E8EDF4",
                    ),
                    use_container_width=True,
                )

        if not customers_by_state.empty:
            top_customer_state = customers_by_state.iloc[0]
            render_insight(
                f"<strong>Insight pelanggan:</strong> {top_customer_state['customer_state']} "
                f"adalah state dengan pelanggan unik terbanyak, yaitu "
                f"{int(top_customer_state['customers']):,} pelanggan pada filter aktif.",
                SECONDARY_COLOR,
            )

    with data_tab:
        st.subheader("Tabel ringkasan")
        st.markdown(
            '<p class="section-note">Gunakan tabel ini untuk validasi angka chart atau eksplorasi cepat.</p>',
            unsafe_allow_html=True,
        )

        table_col_1, table_col_2 = st.columns(2)
        with table_col_1:
            st.markdown("#### Monthly trend")
            st.dataframe(
                monthly_trend[["order_purchase_month", "orders", "revenue"]]
                .rename(
                    columns={
                        "order_purchase_month": "Month",
                        "orders": "Orders",
                        "revenue": "Revenue",
                    }
                )
                .style.format({"Orders": "{:,.0f}", "Revenue": "R${:,.0f}"}),
                use_container_width=True,
                height=360,
            )

        with table_col_2:
            st.markdown("#### Late rate by state")
            late_table = late_by_state.head(15).rename(
                columns={
                    "customer_state": "State",
                    "total_orders": "Orders",
                    "late_orders": "Late Orders",
                    "late_rate": "Late Rate",
                }
            )
            st.dataframe(
                late_table.style.format(
                    {
                        "Orders": "{:,.0f}",
                        "Late Orders": "{:,.0f}",
                        "Late Rate": "{:.1%}",
                    }
                ),
                use_container_width=True,
                height=360,
            )


if __name__ == "__main__":
    main()
