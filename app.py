import streamlit as st
from playwright.sync_api import sync_playwright
from dataclasses import dataclass, asdict, field
import pandas as pd
import os
import time
import asyncio
import sys

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

@dataclass
class Business:
    name: str = None
    address: str = None
    website: str = None
    phone_number: str = None
    reviews_count: int = None
    reviews_average: float = None
    latitude: float = None
    longitude: float = None

@dataclass
class BusinessList:
    business_list: list[Business] = field(default_factory=list)

    def dataframe(self):
        return pd.json_normalize((asdict(b) for b in self.business_list), sep="_")

    def to_csv(self):
        return self.dataframe().to_csv(index=False).encode("utf-8")

    def to_excel(self):
        from io import BytesIO
        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            self.dataframe().to_excel(writer, index=False)
        return output.getvalue()

def extract_coordinates_from_url(url: str) -> tuple[float, float]:
    coordinates = url.split('/@')[-1].split('/')[0]
    lat, lng = coordinates.split(',')[:2]
    return float(lat), float(lng)

def scrape_google_maps(query: str, max_results: int) -> BusinessList:
    business_list = BusinessList()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.google.com/maps", timeout=60000)
        page.locator('//input[@id="searchboxinput"]').fill(query)
        page.keyboard.press("Enter")
        page.hover('//a[contains(@href, "https://www.google.com/maps/place")]')

        prev_count = 0
        for _ in range(30):
            page.mouse.wheel(0, 20000)
            page.wait_for_timeout(5000)
            count = page.locator('//a[contains(@href, "https://www.google.com/maps/place")]').count()
            if count >= max_results or count == prev_count:
                break
            prev_count = count

        listings = page.locator('//a[contains(@href, "https://www.google.com/maps/place")]').all()[:max_results]
        seen = set()
        for listing in listings:
            try:
                listing.click()
                page.wait_for_timeout(4000)

                def text(xpath):
                    return page.locator(xpath).inner_text() if page.locator(xpath).count() else ""

                name = text('//h1[contains(@class, "DUwDvf")]')
                address = text('//button[@data-item-id="address"]//div[contains(@class, "fontBodyMedium")]')
                key = f"{name}_{address}".lower().strip()
                if key in seen:
                    continue
                seen.add(key)

                business = Business(
                    name=name,
                    address=address,
                    website=text('//a[@data-item-id="authority"]//div[contains(@class, "fontBodyMedium")]'),
                    phone_number=text('//button[contains(@data-item-id, "phone")]'),
                    reviews_count=int(text('//button[@jsaction="pane.reviewChart.moreReviews"]//span').replace(',', '') or 0),
                    reviews_average=float(page.locator('//div[@jsaction="pane.reviewChart.moreReviews"]//div[@role="img"]').get_attribute("aria-label").split()[0].replace(',', '.')) if page.locator('//div[@jsaction="pane.reviewChart.moreReviews"]//div[@role="img"]').count() else None,
                    latitude=extract_coordinates_from_url(page.url)[0],
                    longitude=extract_coordinates_from_url(page.url)[1],
                )
                business_list.business_list.append(business)
            except:
                continue
        browser.close()
    return business_list

# ---- Streamlit UI ----

st.title("📍 Google Maps Scraper")
st.markdown("Scrape business listings directly from Google Maps using Playwright.")

query = st.text_input("🔍 Enter your search query:", value="cafes in vellore")
limit = st.slider("📊 Number of listings to scrape:", min_value=5, max_value=100, value=20, step=5)

if st.button("🚀 Start Scraping"):
    with st.spinner("Scraping in progress..."):
        start_time = time.time()
        results = scrape_google_maps(query, limit)
        duration = round(time.time() - start_time, 2)
        st.success(f"✅ Scraped {len(results.business_list)} results in {duration} seconds.")

        st.dataframe(results.dataframe())

        col1, col2 = st.columns(2)
        with col1:
            st.download_button("⬇️ Download CSV", results.to_csv(), file_name="results.csv", mime="text/csv")
        with col2:
            st.download_button("⬇️ Download Excel", results.to_excel(), file_name="results.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")