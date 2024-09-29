import time  # to simulate a real time data, time loop

import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import plotly.express as px  # interactive charts
import streamlit as st  # data web app development
from streamlit_ttyd_custom import terminal

# HTML ELEMENTS
st.set_page_config(
    page_title="CANSAT Dashboard",
    page_icon="",
    layout="wide",
)

# read csv from a github repo
# dataset_url = "https://raw.githubusercontent.com/Lexie88rus/bank-marketing-analysis/master/bank.csv"
dataset_url_1 = "data1.csv"
dataset_url_2 = "data2.csv"
dataset_url_3 = "data3.csv"


# read csv from a URL
# @st.experimental_memo
def get_data(dataset_url) -> pd.DataFrame:
    return pd.read_csv(dataset_url)


def print_debug(i):
    print(f"Called from button {i}")


# dashboard title
st.title("Dashboard - 2024ASI-CANSAT-XXX")
st.divider()

tab1, tab2 = st.tabs(["Statistics", "Terminal"])

# near real-time / live feed simulation
with tab1:
    placeholder_tab1 = st.empty()

with tab2:
    placeholder_tab2 = st.empty()
    # st.text("Terminal showing processes running on your system using the top command")

    # start the ttyd server and display the terminal on streamlit
    ttydprocess, port = terminal(
        ttyd_server_binary="ttyd",
        cmd="bash",
        readonly=False,
        height=500,
        port=6999,
        exit_on_disconnect=False,
    )

    # info on ttyd port
    st.text(f"ttyd server is running on port : {port}")


with placeholder_tab1.container():
    kpi_list_1 = st.columns(5)
    kpi_list_2 = st.columns(5)
    st.divider()
    fig_col = st.columns(3)
    fig_col_names = ["### Altitude", "### Pressure", "### Temperature"]

    placeholder_fig_col = []
    placeholder_kpi_list_1 = []
    placeholder_kpi_list_2 = []

    for c in kpi_list_1:
        placeholder_kpi_list_1.append(c.empty())

    for c in kpi_list_2:
        placeholder_kpi_list_2.append(c.empty())

    for i, c in enumerate(fig_col):
        with c:
            st.markdown(fig_col_names[i])
        placeholder_fig_col.append(c.empty())

with placeholder_tab2.container():
    st.markdown("## CANSAT Status")
    status_columns = st.columns(8)

    st.markdown("## Quick Commands")
    q_comm_columns = st.columns(6)

    st.divider()

    st.markdown("## Terminal")

    placeholder_status_columns = []
    placeholder_q_comm_columns = []
    for c in status_columns:
        placeholder_status_columns.append(c.empty())

    for c in q_comm_columns:
        placeholder_q_comm_columns.append(c.empty())

st.markdown(
    """
    <style>
    .rounded-box-red {
        display: flex;
        justify-content: center;
        align-items: center;
        border: 3px solid #FF0000;
        border-radius: 15px;
        padding: 20px;
        background-color: rgba(255, 0, 0, 0.1);
        margin: 10px;
    }
    </style>

    <style>
    .rounded-box-green {
        display: flex;
        justify-content: center;
        align-items: center;
        border: 3px solid #00FF00;
        border-radius: 15px;
        padding: 20px;
        background-color: rgba(0, 255, 0, 0.1);
        margin: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

for seconds in range(200):
    df1 = get_data(dataset_url_1)
    df2 = get_data(dataset_url_2)
    df3 = get_data(dataset_url_3)

    for p in placeholder_fig_col:
        p.empty()

    for p in placeholder_kpi_list_1:
        p.empty()

    for p in placeholder_kpi_list_2:
        p.empty()

    metrics_1 = [
        ("GNSS Time", "1711949s"),
        ("Current Altitude", f"{df1['altitude'].iloc[-1]} metres"),
        ("Current Pressure", f"{round(df2['pressure'].iloc[-1] * 100, 0)} pascals"),
        ("GNSS Longitude", "24.0467°N"),
        ("GNSS Sats", f"3"),
    ]

    metrics_2 = [
        (
            "Average Speed",
            f"{round(np.polyfit(df1['time'].tail(5).to_numpy(), df1['altitude'].tail(5).to_numpy(), 1)[0], 4)} m/s",
        ),
        ("GNSS Altitude", f"{round(df1['altitude'].iloc[-1], 1)} metres"),
        ("Average Temperature", f"{round(np.mean(df3['temperature']), 1)}°C"),
        ("GNSS Latitude", "18.0435°E"),
        ("Battery Voltage", "12.03 V"),
    ]

    for idx, kpi_block in enumerate(placeholder_kpi_list_1):
        kpi_block.metric(label=metrics_1[idx][0], value=metrics_1[idx][1])

    for idx, kpi_block in enumerate(placeholder_kpi_list_2):
        kpi_block.metric(label=metrics_2[idx][0], value=metrics_2[idx][1])

    with placeholder_fig_col[0]:
        # st.markdown(f"### Altitude")
        fig = px.line(data_frame=df1, x="time", y="altitude")
        st.write(fig)

    with placeholder_fig_col[1]:
        # st.markdown(f"### Pressure")
        fig2 = px.line(data_frame=df2, x="time", y="pressure")
        st.write(fig2)

    with placeholder_fig_col[2]:
        # st.markdown("### Temperature")
        fig3 = px.line(data_frame=df3, x="time", y="temperature")
        st.write(fig3)

    cansat_status = [
        ["0 BOOT", "green"],  # BOOT
        ["1 TEST_MODE", "green"],  # TEST_MODE
        ["2 LAUNCH_PAD", "red"],  # LAUNCH_PAD
        ["3 ASCENT", "red"],  # ASCENT
        ["4 ROCKET_DEPLOY", "red"],  # ROCKET_DEPLOY
        ["5 DESCENT", "green"],  # DESCENT
        ["6 AERBRK_RLS", "red"],  # AEROBREAK_RELEASE
        ["7 IMPACT", "red"],  # IMPACT
    ]

    for idx, box in enumerate(placeholder_status_columns):
        box.empty()
        with box:
            st.markdown(
                f'<div class="rounded-box-{cansat_status[idx][1]}">{cansat_status[idx][0]}</div>',
                unsafe_allow_html=True,
            )

    q_comm = [
        ["STR_T_TLMTRY", "green"],
        ["STP_T_TLMTRY", "red"],
        ["BGN_SMLTN", "green"],
        ["CSTM_SG1", "red"],
        ["CSTM_SG2", "red"],
        ["FRC_DPLY_PRCHT", "red"],
    ]

    for idx, box in enumerate(placeholder_q_comm_columns):
        box.empty()
        with box:
            st.markdown(
                f'<div class="rounded-box-{q_comm[idx][1]}">{q_comm[idx][0]}</div>',
                unsafe_allow_html=True,
            )

    time.sleep(1)