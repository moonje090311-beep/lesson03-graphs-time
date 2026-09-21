import pandas as pd
import plotly.express as px
import streamlit as st

DATA_URL = (
    "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"
)

st.set_page_config(page_title="영화 데이터 그래프 도감 1 - 시간", layout="wide")


# ---------------------------------------------------------------------------
# 데이터 불러오기
# ---------------------------------------------------------------------------
@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_URL)
    # 날짜 열(예: 20240101)을 진짜 날짜(datetime)로 변환
    df["날짜"] = pd.to_datetime(df["날짜"].astype(str), format="%Y%m%d")
    return df.sort_values("날짜").reset_index(drop=True)


def insight(text: str) -> None:
    """그래프 아래에 '이 그래프로 알 수 있는 것' 한 문장을 보여 주는 자리."""
    st.info(f"이 그래프로 알 수 있는 것: {text}")


# ---------------------------------------------------------------------------
# 구역 1: 시간 (날짜에 따른 변화)
# ---------------------------------------------------------------------------
def section_time(df: pd.DataFrame) -> None:
    st.header("구역 1. 시간")

    # --- 그래프 1-1: 영화별 일관객 변화 -------------------------------------
    st.subheader("1-1. 영화별 일관객 변화")

    # 관객이 많았던 영화가 위에 오도록 정렬
    movie_order = (
        df.groupby("영화명")["일관객"].sum().sort_values(ascending=False).index.tolist()
    )
    movie = st.selectbox("영화를 고르세요", movie_order, key="time_movie")

    movie_df = df[df["영화명"] == movie].sort_values("날짜")

    fig = px.line(
        movie_df,
        x="날짜",
        y="일관객",
        markers=True,
        title=f"{movie} - 날짜별 일관객",
    )
    fig.update_traces(
        hovertemplate="날짜: %{x|%Y-%m-%d}<br>일관객: %{y:,}명<extra></extra>"
    )
    fig.update_layout(
        xaxis_title="날짜",
        yaxis_title="일관객(명)",
        hovermode="closest",
    )
    st.plotly_chart(fig, use_container_width=True)

    insight("(여기에 한 문장을 적어 주세요)")


# ---------------------------------------------------------------------------
# 구역 2, 3, ... : 새 그래프는 아래 방식으로 추가하세요
#
#   def section_xxx(df):
#       st.header("구역 2. 제목")
#       st.subheader("2-1. 그래프 제목")
#       ... (그래프 그리기) ...
#       insight("이 그래프로 알 수 있는 것 한 문장")
#
# 그리고 아래 main()에 section_xxx(df) 를 한 줄 추가하면 됩니다.
# ---------------------------------------------------------------------------


def main() -> None:
    st.title("영화 데이터 그래프 도감 1 - 시간")

    df = load_data()
    st.caption(
        f"{df['날짜'].min():%Y-%m-%d} ~ {df['날짜'].max():%Y-%m-%d} "
        f"일별 박스오피스 10위권 기록 ({len(df):,}행)"
    )

    section_time(df)
    st.divider()

    # section_xxx(df)  # 다음 구역은 여기에 추가


if __name__ == "__main__":
    main()
