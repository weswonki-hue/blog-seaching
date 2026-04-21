import streamlit as st
from real_estate import get_blog_search_results, process_real_estate_data
from datetime import datetime, timedelta

# 1. 페이지 설정
st.set_page_config(page_title="재개발 실시간 모니터링", layout="wide", page_icon="🔥")

# 2. 제목 및 일주일 날짜 계산
st.title("🔥 재개발·급매 일주일치 통합 대시보드")

# 오늘 기준으로 7일 전 날짜를 YYYYMMDD 형식으로 계산
today = datetime.now()
one_week_ago_date = (today - timedelta(days=7)).strftime('%Y%m%d')

st.write(f"현재 시간: {today.strftime('%Y-%m-%d %H:%M')}")
st.write(f"📅 **{one_week_ago_date[:4]}-{one_week_ago_date[4:6]}-{one_week_ago_date[6:]}** 이후에 올라온 모든 글을 표시합니다.")
st.divider()

# 3. 모니터링 키워드 리스트
target_keywords = [
    "재개발 급매", 
    "재개발 급급매", 
    "재개발 초급매", 
    "재개발 급매물",
    "재개발 급매매"
]

# 4. 메인 대시보드 로직
for kw in target_keywords:
    # 키워드별 섹션 만들기
    st.subheader(f"📍 {kw}")
    
    with st.spinner(f"'{kw}' 최신 소식 수집 중..."):
        # real_estate.py에서 최신순으로 50개를 가져오도록 설정됨
        raw_results = get_blog_search_results(kw, display_count=50)
        
        if raw_results:
            final_data = process_real_estate_data(raw_results)
            
            # 일주일 이내 데이터만 필터링 (postdate가 일주일 전 날짜보다 크거나 같은 것만)
            weekly_data = [p for p in final_data if p['postdate'] >= one_week_ago_date]
            
            if weekly_data:
                st.success(f"최근 일주일 내 등록된 글: {len(weekly_data)}건")
                
                # 리스트 형태로 전체 출력
                for post in weekly_data:
                    # 날짜 가공 (YYYYMMDD -> YYYY-MM-DD)
                    d = post['postdate']
                    fmt_date = f"{d[:4]}-{d[4:6]}-{d[6:]}"
                    
                    # 펼치기(Expander) 메뉴로 구성
                    with st.expander(f"📅 {fmt_date} | {post['title']}"):
                        st.write(f"👤 **블로그:** {post['bloggername']}")
                        st.link_button("상세 매물정보 확인 (네이버 블로그)", post['link'])
            else:
                st.info("최근 7일 이내에 올라온 새로운 포스팅이 없습니다.")
        else:
            st.error("데이터를 가져오는 중 오류가 발생했습니다.")
            
    st.write("") # 섹션 간 여백
    st.divider()

# 5. 사이드바
st.sidebar.header("⚙️ 모니터링 옵션")
if st.sidebar.button("🔄 즉시 새로고침"):
    st.rerun()

st.sidebar.info(f"""
**안내:**
- 네이버 API를 통해 최신순으로 정렬된 데이터를 가져옵니다.
- 7일이 지난 데이터는 자동으로 리스트에서 제외됩니다.
""")