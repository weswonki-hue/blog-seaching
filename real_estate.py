import os
import sys
import urllib.request
import json
import streamlit as st

def get_blog_search_results(query, display_count=50):
    """
    네이버 블로그 검색 API를 호출하여 결과를 반환합니다.
    Streamlit Secrets를 통해 보안을 강화했습니다.
    """
    # [보안 수정] 직접 적혀있던 API 키를 st.secrets에서 불러오도록 변경했습니다.
    try:
        client_id = st.secrets["NAVER_CLIENT_ID"]
        client_secret = st.secrets["NAVER_CLIENT_SECRET"]
    except KeyError:
        # 로컬 테스트 시 secrets가 설정되지 않았을 경우를 대비한 예외 처리
        print("API 키를 찾을 수 없습니다. Streamlit Secrets 설정을 확인해주세요.")
        return []

    encText = urllib.parse.quote(query)
    url = f"https://openapi.naver.com/v1/search/blog?query={encText}&display={display_count}"
    
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    
    try:
        response = urllib.request.urlopen(request)
        if response.getcode() == 200:
            data = json.loads(response.read().decode('utf-8'))
            return data.get('items', [])
        return []
    except Exception as e:
        print(f"인증 오류 또는 네트워크 에러: {e}")
        return []

def process_real_estate_data(items):
    """
    검색 결과에서 제목, 링크, 블로그명, 그리고 [날짜] 정보를 정제합니다.
    """
    processed_list = []
    for item in items:
        # 제목과 요약에서 보기 싫은 <b> 태그 제거
        title = item['title'].replace('<b>', '').replace('</b>', '')
        
        # postdate 정보를 추가하여 app.py로 전달합니다.
        processed_list.append({
            'title': title,
            'link': item['link'],
            'bloggername': item['bloggername'],
            'postdate': item.get('postdate', '')  # 날짜 정보 추가
        })
    return processed_list

if __name__ == "__main__":
    # 이 부분은 파일을 직접 실행했을 때만 동작합니다.
    search_keyword = "급매"
    print(f"'{search_keyword}' 키워드로 검색을 시작합니다...")
    
    results = get_blog_search_results(search_keyword)
    
    if results:
        final_data = process_real_estate_data(results)
        print(f"\n--- 검색 결과 총 {len(final_data)}건 ---")
        for idx, post in enumerate(final_data, 1):
            print(f"[{idx}] {post['title']}")
            print(f"   날짜: {post['postdate']} | 블로그: {post['bloggername']}")
            print(f"   링크: {post['link']}")
            print("-" * 50)
    else:
        print("API 키 설정이 누락되었거나 오늘 사용량을 초과했을 수 있습니다.")