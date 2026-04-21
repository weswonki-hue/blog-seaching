import streamlit as st
from real_estate import get_blog_search_results, process_real_estate_data

# 페이지 설정
st.set_page_config(page_title="화8의 부동산 매물 검색기", page_icon="🏠", layout="wide")

st.title("🏠 실시간 부동산 최신글 검색기")
st.markdown("재개발 구역 및 급매 정보를 최신순으로 확인하세요.")

# 사이드바 설정
with st.sidebar:
    st.header("🔍 검색 설정")
    # 기본 검색어를 "구역 급매"로 설정했습니다.
    search_keyword = st.text_input("검색어를 입력하세요", value="구역 급매")
    display_count = st.slider("검색 결과 개수", 10, 100, 50)
    search_button = st.button("검색 시작")

# 메인 로직
if search_button or search_keyword:
    with st.spinner('최신 매물을 불러오는 중...'):
        raw_items = get_blog_search_results(search_keyword, display_count)
        final_data = process_real_estate_data(raw_items)

    if final_data:
        st.success(f"'{search_keyword}'에 대한 최신 포스팅 {len(final_data)}건을 찾았습니다.")
        
        for post in final_data:
            with st.container():
                # 날짜 보기 좋게 변경 (20240421 -> 2024-04-21)
                d = post['postdate']
                fmt_date = f"{d[:4]}-{d[4:6]}-{d[6:]}" if len(d) == 8 else d
                
                col1, col2 = st.columns([4, 1])
                with col1:
                    # 제목 앞에 날짜를 붙여 최신순임을 강조
                    st.markdown(f"**[{fmt_date}]** {post['title']}")
                    st.caption(f"블로그: {post['bloggername']}")
                with col2:
                    st.link_button("링크 열기", post['link'])
                st.divider()
    else:
        st.warning("검색 결과가 없습니다.")
