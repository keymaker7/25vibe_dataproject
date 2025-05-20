import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="T맵 맛집 지도", layout="wide")
st.title("🍽️ T맵 맛집 지도")
st.write("맛집을 추가/수정/삭제하고, 지도에서 자유롭게 탐색하세요!")

# 1. 초기 세션 상태 만들기
if "restaurants" not in st.session_state:
    st.session_state.restaurants = [
        # 예시 맛집 데이터 (지역, 이름, 위도, 경도)
        {"region": "서울", "name": "을지로 노포곱창", "lat": 37.5667, "lon": 126.9831},
        {"region": "부산", "name": "해운대 암소갈비집", "lat": 35.1631, "lon": 129.1634},
        {"region": "광주", "name": "궁전제과", "lat": 35.1461, "lon": 126.9194}
    ]

# 2. 지역 목록 자동 추출
regions = sorted(list({r["region"] for r in st.session_state.restaurants}))
if "전체" not in regions:
    regions.insert(0, "전체")

st.sidebar.header("맛집 관리")
mode = st.sidebar.radio("모드 선택", ["추가", "수정", "삭제"])
region_input = st.sidebar.text_input("지역", value="서울")
name_input = st.sidebar.text_input("맛집 이름", value="")
lat_input = st.sidebar.number_input("위도", format="%.6f")
lon_input = st.sidebar.number_input("경도", format="%.6f")

# 3. 추가/수정/삭제 버튼 기능
if mode == "추가":
    if st.sidebar.button("맛집 추가하기"):
        if name_input and lat_input and lon_input:
            st.session_state.restaurants.append(
                {"region": region_input, "name": name_input, "lat": lat_input, "lon": lon_input}
            )
            st.success("맛집이 추가되었습니다!")
elif mode == "수정":
    select_name = st.sidebar.selectbox(
        "수정할 맛집 선택",
        [f"{r['region']} - {r['name']}" for r in st.session_state.restaurants]
    )
    idx = [f"{r['region']} - {r['name']}" for r in st.session_state.restaurants].index(select_name)
    if st.sidebar.button("맛집 수정하기"):
        st.session_state.restaurants[idx] = {
            "region": region_input, "name": name_input, "lat": lat_input, "lon": lon_input
        }
        st.success("맛집 정보가 수정되었습니다!")
elif mode == "삭제":
    select_name = st.sidebar.selectbox(
        "삭제할 맛집 선택",
        [f"{r['region']} - {r['name']}" for r in st.session_state.restaurants]
    )
    if st.sidebar.button("맛집 삭제하기"):
        idx = [f"{r['region']} - {r['name']}" for r in st.session_state.restaurants].index(select_name)
        st.session_state.restaurants.pop(idx)
        st.success("맛집이 삭제되었습니다!")

# 4. 지도 표시용 지역 선택
selected_region = st.selectbox("표시할 지역 선택", regions)
if selected_region == "전체":
    show_data = st.session_state.restaurants
else:
    show_data = [r for r in st.session_state.restaurants if r["region"] == selected_region]

# 지도 중심(선택한 지역의 첫 번째 맛집 위치, 없으면 서울 시청)
if show_data:
    center_lat = show_data[0]["lat"]
    center_lon = show_data[0]["lon"]
else:
    center_lat, center_lon = 37.5665, 126.9780

# 5. 지도 생성 및 마커 추가
m = folium.Map(location=[center_lat, center_lon], zoom_start=12)
for r in show_data:
    folium.Marker(
        [r["lat"], r["lon"]],
        tooltip=r["name"],
        popup=f"{r['region']} - {r['name']}"
    ).add_to(m)

st_folium(m, width=900, height=600)

# 6. 현재 표시된 맛집 리스트 출력(선택)
st.markdown("#### 현재 표시 중인 맛집 리스트")
for r in show_data:
    st.write(f"- {r['region']} | {r['name']} ({r['lat']:.5f}, {r['lon']:.5f})")
