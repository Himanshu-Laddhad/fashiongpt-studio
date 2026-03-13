"""
Optimized Pinterest Scraper - 10-12 Images Only
Runs Selenium in a thread pool so it doesn't block the async event loop.
"""

import asyncio
import pandas as pd
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time


def _scrape_pinterest_sync(query: str, max_images: int) -> list:
    """
    Synchronous Selenium scrape — called from a thread pool so it never
    blocks the asyncio event loop.
    Returns a list of image-data dicts.
    """
    all_images = []

    opts = Options()
    opts.add_argument("--headless")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--window-size=1920,1080")
    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )

    driver = None
    try:
        driver = webdriver.Chrome(options=opts)

        search_query = query.replace(' ', '+')
        search_url = (
            f"https://www.pinterest.com/search/pins/?q={search_query}"
            f"&rs=typed&term_meta[]={search_query}%7Ctyped"
        )

        print(f"   Accessing Pinterest...")
        driver.get(search_url)
        time.sleep(4)  # initial page load

        seen_urls: set = set()
        scroll_count = 0
        max_scrolls = 6
        previous_count = 0

        while scroll_count < max_scrolls and len(all_images) < max_images * 2:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            for img in driver.find_elements(By.TAG_NAME, "img"):
                try:
                    src = img.get_attribute("src") or ""
                    if (
                        "http" in src
                        and ("pinimg.com" in src or "pinterest.com" in src)
                        and "v1" not in src
                        and "static" not in src
                        and src not in seen_urls
                    ):
                        # Upgrade to highest available Pinterest CDN resolution (736x)
                        src = (
                            src.replace('/236x/', '/736x/')
                               .replace('/474x/', '/736x/')
                               .replace('/564x/', '/736x/')
                               .replace('/200x200_90/', '/736x/')
                               .replace('/75x75_RS/', '/736x/')
                        )
                        seen_urls.add(src)
                        all_images.append({
                            'image_url': src,
                            'description': img.get_attribute("alt") or f"{query} fashion inspiration",
                            'source': 'Pinterest',
                            'pin_id': f'pin_{len(all_images)}',
                            'link': search_url,
                        })

                    if len(all_images) >= max_images * 2:
                        break
                except Exception:
                    continue

            current_count = len(all_images)
            if current_count == previous_count:
                print(f"   Scroll {scroll_count + 1}: No new images, continuing...")
            else:
                print(f"   Scroll {scroll_count + 1}: {current_count} images found")

            previous_count = current_count
            scroll_count += 1

            if len(all_images) >= max_images:
                break

    except Exception as e:
        print(f"   ⚠️ Pinterest Selenium error: {e}")
    finally:
        if driver:
            driver.quit()

    return all_images[:max_images]


async def scrape_pinterest_optimized(
    query: str,
    output_dir: Path,
    max_images: int = 12,
) -> pd.DataFrame:
    """
    Async wrapper: runs the blocking Selenium scraper in a thread pool
    so the asyncio event loop stays free for other tasks.
    """
    print(f"📌 Searching Pinterest for '{query}' (target: {max_images} images)...")

    try:
        loop = asyncio.get_running_loop()
        final_images = await loop.run_in_executor(
            None, _scrape_pinterest_sync, query, max_images
        )
    except Exception as e:
        print(f"   ⚠️ Pinterest scraping error: {e}")
        final_images = []

    if final_images:
        df = pd.DataFrame(final_images)
        output_file = output_dir / "pinterest_images.csv"
        df.to_csv(output_file, index=False, encoding="utf-8-sig")
        print(f"✅ Found {len(df)} Pinterest images")
    else:
        print(f"⚠️ No Pinterest images found for: {query}")
        df = pd.DataFrame()

    return df


# ── quick test ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    async def test():
        output = Path("output/test")
        output.mkdir(parents=True, exist_ok=True)
        result = await scrape_pinterest_optimized("denim jacket", output, max_images=12)
        print(f"\n✅ Test complete: {len(result)} images")
        if not result.empty:
            print(result.head())

    asyncio.run(test())
