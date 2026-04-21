import os
import sys
import urllib.request
import json
import streamlit as st

def get_blog_search_results(query, display_count=50):
    """
    네이버 블로그 검색 API 호출 (Secrets 보안 적용)
    """
    try:
        client_id = st.secrets["NAVER_CLIENT_ID"]
        client_secret = st.secrets["NAVER_CLIENT_SECRET"]
    except KeyError:
        return []

    encText = urllib.parse.quote(query)
    # sort=date 옵션을 추가하여 API 레벨에서 일차적으로 최신순 요청
    url = f"https://openapi.naver.com/v1/search/blog?query={encText}&display={display_count}&sort=date"
    
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
        return []

def process_real_estate_data(items):
    """
    데이터 정제 및 파이썬 리스트 차원에서의 최신순 재정렬
    """
    processed_list = []
    for item in items:
        title = item['title'].replace('<b>', '').replace('</b>', '')
        processed_list.append({
            'title': title,
            'link': item['link'],
            'bloggername': item['bloggername'],
            'postdate': item.get('postdate', '')
        })
    
    # [핵심] postdate(YYYYMMDD)를 기준으로 내림차순 정렬 (최신이 위로)
    processed_list.sort(key=lambda x: x['postdate'], reverse=True)
    
    return processed_list
