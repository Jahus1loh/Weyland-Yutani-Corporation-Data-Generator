import streamlit as st
from processing.dashboard.dashboard import render_dashboard
from processing.data_analysis.analyze_data import analyze_data
from processing.data_analysis.helper_funcs import (
    calculate_daily_total,
    get_mine_data,
)
from processing.generate_data.generate_data import generate_data
from processing.get_generator_data.extract_mines_aspects import (
    extract_mines_aspects,
)
from processing.get_generator_data.get_spreadsheet_data import (
    get_data_from_spreadhseet,
)


@st.cache_data(
    ttl=5,
    show_spinner=False,
)
def get_cached_spreadsheet_data():
    return get_data_from_spreadhseet()


def update_simulation():
    spreadsheet_data = get_cached_spreadsheet_data()
    extracted_data = extract_mines_aspects(spreadsheet_data)

    if extracted_data != st.session_state.get("extracted_data"):
        generated_data = generate_data(extracted_data)
        st.session_state["generated_data"] = generated_data
        st.session_state["analysis_results"] = analyze_data(generated_data)
        st.session_state["extracted_data"] = extracted_data

    return st.session_state["generated_data"]


@st.fragment(run_every=("5s"))
def process():
    try:
        generated_data = update_simulation()
    except Exception as error:
        st.error(f"Could not load spreadsheet data: {error}")
        return
    render_mine_tabs(generated_data)


def render_mine_tabs(generated_data):
    mines = generated_data["mine"].unique().tolist()
    tabs = st.tabs(["All mines"] + mines)
    render_total_tab(tabs[0], generated_data)
    for tab, mine in zip(tabs[1:], mines):
        render_single_mine_tab(tab, generated_data, mine)


def render_total_tab(tab, generated_data):
    with tab:
        daily_total = calculate_daily_total(generated_data)
        render_dashboard(daily_total, "output", "All mines")


def render_single_mine_tab(tab, generated_data, mine):
    with tab:
        mine_data = get_mine_data(generated_data, mine)
        render_dashboard(mine_data, "output", mine)
