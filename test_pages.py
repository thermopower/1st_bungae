"""
Playwright를 사용한 웹 페이지 테스트
"""
from playwright.sync_api import sync_playwright
import time

def test_all_pages():
    """모든 주요 페이지 테스트"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        base_url = "http://127.0.0.1:5000"

        # 테스트할 페이지 목록
        pages_to_test = [
            "/",
            "/auth/login",
            "/auth/register",
            "/advertiser/register",
            "/influencer/register",
        ]

        results = []

        print("=" * 60)
        print("Testing Flask Application Pages")
        print("=" * 60)

        for path in pages_to_test:
            url = f"{base_url}{path}"
            try:
                print(f"\n[Testing] {url}")
                response = page.goto(url, wait_until="networkidle", timeout=10000)

                status = response.status
                title = page.title()

                if status == 200:
                    print(f"  ✓ Status: {status}")
                    print(f"  ✓ Title: {title}")
                    results.append({
                        'url': url,
                        'status': status,
                        'title': title,
                        'success': True
                    })
                else:
                    print(f"  ✗ Status: {status}")
                    print(f"  ✗ Title: {title}")
                    results.append({
                        'url': url,
                        'status': status,
                        'title': title,
                        'success': False
                    })

            except Exception as e:
                print(f"  ✗ Error: {str(e)[:100]}")
                results.append({
                    'url': url,
                    'error': str(e),
                    'success': False
                })

        browser.close()

        # 최종 결과 요약
        print("\n" + "=" * 60)
        print("Test Results Summary")
        print("=" * 60)

        success_count = sum(1 for r in results if r.get('success', False))
        total_count = len(results)

        for result in results:
            if result.get('success'):
                print(f"✓ {result['url']} - OK ({result.get('status', 'N/A')})")
            else:
                error_msg = result.get('error', f"Status {result.get('status', 'N/A')}")
                print(f"✗ {result['url']} - FAIL ({error_msg[:50]})")

        print(f"\nTotal: {success_count}/{total_count} pages passed")
        print("=" * 60)

if __name__ == '__main__':
    test_all_pages()
