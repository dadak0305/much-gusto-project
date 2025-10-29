import streamlit as st
import pandas as pd
import plotly.express as px

# 데이터 로드
df = pd.read_csv("countriesMBTI_16types.csv")

# 🔧 컬럼명 정리 (공백 제거 + 소문자 변환)
df.columns = df.columns.str.strip().str.lower()

# 🔧 첫 번째 컬럼을 'country' 로 강제 설정
df = df.rename(columns={df.columns[0]: "country"})

# 숫자형 변환 + 퍼센트 변환 (소수점 둘째 자리까지)
for col in df.columns[1:]:
    df[col] = pd.to_numeric(df[col], errors='coerce')
    df[col] = (df[col] * 100).round(2)

# 앱 제목 (이모지)
st.header("🧑🏻‍💻서울고 석리송 선생님과 함께하는! 👩🏻‍💻")
st.title("🌍 국가별 MBTI 성향 분석 프로젝트 🔍")

# 데이터 출처
st.markdown(
    "📊 **데이터 출처**: [Kaggle - MBTI Types by Country](https://www.kaggle.com/datasets/yamaerenay/mbtitypes-full/data)"
)

# MBTI 리스트
global_mbti_types = sorted(df.columns[1:])

# 국가 선택
country = st.selectbox("🌏 국가를 선택하세요:", df["country"].unique())

# 선택 국가 데이터 시각화
st.subheader(f"📊 {country}의 MBTI 분포")
selected_data = df[df["country"] == country].iloc[:, 1:].T
selected_data.columns = [country]
selected_data = selected_data.sort_values(by=country, ascending=False)

fig = px.bar(
    selected_data,
    x=selected_data.index,
    y=country,
    text=selected_data[country],
    title=f"{country}의 MBTI 분포",
    labels={country: "비율 (%)"},
    hover_data={country: ':,.2f'},
    color=selected_data.index,
    color_discrete_sequence=px.colors.qualitative.Pastel
)
st.plotly_chart(fig)

# 전체 평균
st.subheader("📊 전체 국가의 MBTI 평균 비율")
mbti_avg = df.iloc[:, 1:].mean().sort_values(ascending=False)
mbti_avg_df = pd.DataFrame({"MBTI": mbti_avg.index, "비율 (%)": mbti_avg.values})

fig_avg = px.bar(
    mbti_avg_df,
    x="MBTI",
    y="비율 (%)",
    text="비율 (%)",
    title="전체 국가별 MBTI 평균",
    labels={"비율 (%)": "평균 비율 (%)"},
    hover_data={"비율 (%)": ':,.2f'},
    color="MBTI",
    color_discrete_sequence=px.colors.qualitative.Pastel
)
st.plotly_chart(fig_avg)

# MBTI 상위 10개국 & 한국
target_mbti = st.selectbox("💡 MBTI 유형을 선택하세요:", global_mbti_types)
st.subheader(f"🏆 {target_mbti} 비율이 높은 국가 TOP 10 & 한국")

try:
    top_10 = df.nlargest(10, target_mbti)[["country", target_mbti]].copy()

    # 한국 추가
    if "south korea" in df["country"].str.lower().values:
        korea_value = df[df["country"].str.lower() == "south korea"][target_mbti].values[0]
        korea_data = pd.DataFrame({"country": ["South Korea"], target_mbti: [korea_value]})
        top_10 = pd.concat([top_10, korea_data])

    top_10 = top_10.sort_values(by=target_mbti, ascending=False)

    fig_top = px.bar(
        top_10,
        x="country",
        y=target_mbti,
        text=target_mbti,
        color="country",
        title=f"{target_mbti} 비율 TOP 10 & 한국",
        labels={target_mbti: "비율 (%)"},
        hover_data={target_mbti: ':,.2f'},
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    st.plotly_chart(fig_top)

except Exception as e:
    st.error(f"데이터 처리 중 오류 발생: {e}")
