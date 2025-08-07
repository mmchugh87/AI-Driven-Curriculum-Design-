#!/usr/bin/env python3
"""
Indeed Job Scraper - Advanced Web Scraper with Cloudflare Bypass
A comprehensive web scraper for Indeed.com using Camoufox browser automation
to handle Cloudflare challenges and extract job data.
"""

import os
import time
import random
import asyncio
import logging
import pandas as pd
from datetime import datetime
from camoufox import AsyncCamoufox
from bs4 import BeautifulSoup
import re
import csv
from urllib.parse import urljoin, quote_plus

# Import the captcha solving library
from camoufox_captcha import solve_captcha

# Set up logging
logging.basicConfig(
    level='INFO',
    format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

# Configuration
DEFAULT_POSITION = "python analyst"
DEFAULT_LOCATION = "remote"
DEFAULT_MAX_JOBS = 800
DEFAULT_DELAY_MIN = 3
DEFAULT_DELAY_MAX = 8

def print_indeed_splash():
    """Print Indeed scraper splash screen"""
    print("=" * 80)
    print("=" * 80)
    print("||" + " " * 76 + "||")
    print("||" + " " * 26 + "INDEED JOB SCRAPER" + " " * 30 + "||")
    print("||" + " " * 76 + "||")
    print("||" + " " * 18 + "Advanced Cloudflare Bypass System" + " " * 25 + "||")
    print("||" + " " * 76 + "||")
    print("||" + " " * 15 + "Powered by Camoufox Browser Automation" + " " * 23 + "||")
    print("||" + " " * 76 + "||")
    print("=" * 80)
    print("=" * 80)
    print("")
    print("Initializing Indeed scraping system...")
    print("Loading Cloudflare bypass modules...")
    print("Preparing data collection...")
    print("")


def get_today_datetime():
    """Get today's date and time in YYYY-MM-DD_HH-MM format"""
    return datetime.now().strftime("%Y-%m-%d_%H-%M")


def get_indeed_url(position, location):
    """Generate Indeed search URL"""
    base_url = "https://www.indeed.com/jobs"
    position_encoded = quote_plus(position)
    location_encoded = quote_plus(location)
    url = f"{base_url}?q={position_encoded}&l={location_encoded}"
    return url


async def handle_cookie_consent(page):
    """Check for and handle cookie consent dialogs on Indeed"""
    try:
        page_content = await page.content()
        
        # Look for cookie consent indicators
        cookie_indicators = [
            'accept all', 'accept cookies', 'cookie consent', 'cookies policy',
            'we use cookies', 'cookie notice', 'privacy notice', 'accept all cookies',
            'onetrust', 'cookie banner', 'cookie preferences'
        ]
        
        if any(indicator in page_content.lower() for indicator in cookie_indicators):
            print("🍪 Cookie consent dialog detected!")
            
            # Try different selectors for "Accept All" buttons
            accept_selectors = [
                'button#onetrust-accept-btn-handler',
                '#onetrust-accept-btn-handler',
                'button:has-text("Accept All")',
                'button:has-text("Accept all")',
                'button:has-text("ACCEPT ALL")',
                'a:has-text("Accept All")',
                '[id*="accept"]:has-text("Accept All")',
                '[class*="accept"]:has-text("Accept All")',
                'button[id*="accept-all"]',
                'button[class*="accept-all"]',
                '[role="button"]:has-text("Accept All")'
            ]
            
            for i, selector in enumerate(accept_selectors):
                try:
                    print(f"  Trying cookie selector {i+1}/{len(accept_selectors)}: {selector}")
                    accept_button = await page.query_selector(selector)
                    if accept_button:
                        print(f"  Found Accept All button with selector: {selector}")
                        await accept_button.click()
                        print("✓ Cookie consent accepted!")
                        await asyncio.sleep(3)
                        return True
                except Exception as e:
                    continue
            
            print("⚠️  Could not automatically accept cookies")
        
        return False
        
    except Exception as e:
        print(f"Error during cookie consent check: {e}")
        return False


async def check_and_handle_cloudflare(page):
    """Check for and handle Cloudflare challenges on Indeed"""
    try:
        page_content = await page.content()
        
        # Look for Cloudflare indicators
        cloudflare_indicators = [
            'cloudflare', 'checking your browser', 'just a moment', 'please wait',
            'verify you are human', 'challenge', 'security check'
        ]
        
        if any(indicator in page_content.lower() for indicator in cloudflare_indicators):
            print("🔒 Cloudflare challenge detected!")
            print("=" * 60)
            print("CLOUDFLARE VERIFICATION REQUIRED")
            print("=" * 60)
            print("Attempting automatic captcha solving...")
            
            try:
                # Use camoufox-captcha to solve the Cloudflare challenge
                await solve_captcha(page, captcha_type='cloudflare', challenge_type='interstitial')
                print("✓ Cloudflare challenge solved automatically!")
                
                # Wait for page to stabilize
                await asyncio.sleep(5)
                
                # Check for cookie consent after captcha resolution
                await handle_cookie_consent(page)
                
                # Verify the challenge was solved
                current_content = await page.content()
                success_indicators = ['job', 'vacancy', 'position', 'indeed.com']
                
                if any(indicator in current_content.lower() for indicator in success_indicators):
                    print("✓ Verification successful - Indeed page loaded")
                    return True
                    
            except Exception as captcha_e:
                print(f"❌ Automatic captcha solving failed: {captcha_e}")
                print("Attempting fallback resolution...")
            
            # Fallback: wait for automatic resolution
            print("Waiting for Cloudflare to resolve automatically...")
            max_wait = 30
            check_interval = 2
            
            for attempt in range(0, max_wait, check_interval):
                print(f"  Waiting... ({attempt}/{max_wait}s)")
                await asyncio.sleep(check_interval)
                
                try:
                    current_content = await page.content()
                    success_indicators = ['job', 'vacancy', 'position', 'indeed.com']
                    cf_indicators = ['cloudflare', 'checking your browser', 'just a moment']
                    
                    cf_gone = not any(cf in current_content.lower() for cf in cf_indicators)
                    job_content = any(success in current_content.lower() for success in success_indicators)
                    
                    if cf_gone and job_content:
                        print("✓ Cloudflare resolved automatically!")
                        await asyncio.sleep(3)
                        return True
                        
                except Exception:
                    continue
            
            # Manual intervention required
            print("⚠️  Manual intervention required")
            print("Please complete the Cloudflare challenge manually")
            print("Once the Indeed job search page loads, press ENTER to continue...")
            input("Press ENTER after completing Cloudflare challenge: ")
            print("Continuing with scraping...")
            return True
        
        return False
        
    except Exception as e:
        print(f"Error during Cloudflare check: {e}")
        return False


async def random_delay(min_seconds=DEFAULT_DELAY_MIN, max_seconds=DEFAULT_DELAY_MAX):
    """Add random delay to mimic human behavior"""
    delay = random.uniform(min_seconds, max_seconds)
    await asyncio.sleep(delay)


async def extract_job_data(page, job_element):
    """Extract job data from a job element on the search results page"""
    try:
        # Get the job element's HTML
        job_html = await job_element.inner_html()
        soup = BeautifulSoup(job_html, 'html.parser')
        
        # Extract job link first (following notebook pattern)
        try:
            link_elem = await job_element.query_selector('a')
            if link_elem:
                href = await link_elem.get_attribute('href')
                if href:
                    if href.startswith('/'):
                        links = f"https://www.indeed.com{href}"
                    else:
                        links = href
                else:
                    links = 'NaN'
            else:
                links = 'NaN'
        except:
            links = 'NaN'
        
        # Extract job title (following notebook pattern)
        try:
            title = soup.select('.jobTitle')[0].get_text().strip()
        except:
            title = 'NaN'
        
        # Extract company name (following notebook pattern)
        try:
            company = soup.find_all(attrs={'data-testid': 'company-name'})[0].get_text().strip()
        except:
            company = 'NaN'
        
        # Extract location (following notebook pattern)
        try:
            location = soup.find_all(attrs={'data-testid': 'text-location'})[0].get_text().strip()
        except:
            location = 'NaN'
        
        # Extract salary (following notebook pattern)
        try:
            salary = soup.select('.salary-snippet-container')[0].get_text().strip()
        except:
            salary = 'NaN'
        
        # Extract company rating (following notebook pattern)
        try:
            rating = soup.find("div",{"class":"companyInfo"}).find("span",{"class":"ratingsDisplay"}).text
        except:
            rating = 'NaN'
        
        # Extract job date (following notebook pattern exactly)
        try:
            date = soup.find_all('span',attrs={'data-testid': 'myJobsStateDate'})[0].get_text().strip()
            words_posted_today = ["Today" , "Just", "ongoing"]
            if "ago" in date:
                date_temp = date.split()
                date_temp = date_temp[-3:]
                date = (date_temp[0] + ' ' + date_temp[1] + ' ' + date_temp[2])
            elif any(x in date for x in words_posted_today):
                date = "0 days ago"
            else:
                date = 'NaN'
        except:
            date = 'NaN'
        
        # Extract job snippet description (following notebook pattern)
        try:
            description = soup.select('.job-snippet')[0].get_text().strip()
        except:
            description = ''
        
        # Return data in notebook format
        job_data = {
            'Title': title,
            'Company': company,
            'Location': location,
            'Rating': rating,
            'Date': date,
            'Salary': salary,
            'Description': description,
            'Links': links
        }
        
        return job_data
        
    except Exception as e:
        print(f"Error extracting job data: {e}")
        return None


async def scrape_full_job_description(page, job_url):
    """Scrape the full job description from the job detail page"""
    try:
        print(f"  Scraping full description from: {job_url}")
        await page.goto(job_url, wait_until='networkidle')
        await random_delay(2, 4)
        
        # Handle potential Cloudflare on job detail page
        await check_and_handle_cloudflare(page)
        
        # Extract full job description (following notebook pattern)
        try:
            jd = await page.query_selector('#jobDescriptionText')
            if jd:
                full_description = await jd.inner_text()
                return full_description.strip()
            else:
                print("    No job description found. Skipping...")
                return ""
        except Exception as e:
            print(f"    Error extracting description: {e}")
            return ""
            
    except Exception as e:
        print(f"  Error loading job page {job_url}: {e}")
        return ""


async def get_next_page_url(page, current_start):
    """Get the URL for the next page of results"""
    try:
        # Indeed uses &start= parameter for pagination
        next_start = current_start + 10
        
        # Check if next page exists by looking for pagination elements
        next_links = await page.query_selector_all('a[data-testid="pagination-page-next"]')
        if next_links:
            next_url = await next_links[0].get_attribute('href')
            if next_url:
                if next_url.startswith('/'):
                    return f"https://www.indeed.com{next_url}"
                else:
                    return next_url
        
        # Fallback: construct URL manually
        current_url = page.url
        if '&start=' in current_url:
            base_url = current_url.split('&start=')[0]
        else:
            base_url = current_url
        
        return f"{base_url}&start={next_start}"
        
    except Exception as e:
        print(f"Error getting next page URL: {e}")
        return None


async def scrape_indeed_jobs(position=DEFAULT_POSITION, location=DEFAULT_LOCATION, max_jobs=DEFAULT_MAX_JOBS, scrape_full_descriptions=True):
    """Main function to scrape Indeed jobs"""
    print_indeed_splash()
    
    # Initialize data storage following notebook pattern
    dataframe = pd.DataFrame(columns=["Title", "Company", "Location", "Rating", "Date", "Salary", "Description", "Links"])
    jn = 0
    start_time = datetime.now()
    
    print(f"Starting Indeed scrape for: '{position}' in '{location}'")
    print(f"Target: {max_jobs} jobs")
    print("=" * 60)
    
    # Initialize Camoufox browser
    browser_options = {
        'headless': False,  # Set to True for headless mode
        'humanize': True,
        'geoip': True,
        'i_know_what_im_doing': True,
        'config': {'forceScopeAccess': True},
        'disable_coop': True
    }
    
    async with AsyncCamoufox(**browser_options) as browser:
        page = await browser.new_page()
        print("Browser initialized with Camoufox + Captcha Solver")
        
        # Get the Indeed search URL
        search_url = get_indeed_url(position, location)
        print(f"Starting URL: {search_url}")
        
        # Main scraping loop following notebook pattern
        for i in range(0, max_jobs, 10):
            try:
                # Navigate to current page (following notebook URL pattern)
                current_url = search_url + "&start=" + str(i)
                
                print(f"\nPage {(i//10)+1} - Loading: {current_url}")
                await page.goto(current_url, wait_until='networkidle')
                await random_delay(3, 5)
                
                # Handle Cloudflare if present
                await check_and_handle_cloudflare(page)
                
                # Handle cookie consent
                await handle_cookie_consent(page)
                
                # Find job elements (following notebook pattern)
                job_elements = await page.query_selector_all('.job_seen_beacon')
                
                if not job_elements:
                    print("No job elements found on this page")
                    # Try alternative selectors
                    job_elements = await page.query_selector_all('[data-testid="job-card"]')
                    if not job_elements:
                        job_elements = await page.query_selector_all('.slider_container .slider_item')
                
                if not job_elements:
                    print("No jobs found on this page - ending scrape")
                    break
                
                print(f"Found {len(job_elements)} job elements")
                
                # Extract job data from each element (following notebook pattern)
                for job_element in job_elements:
                    if jn >= max_jobs:
                        break
                    
                    try:
                        job_data = await extract_job_data(page, job_element)
                        if job_data:
                            jn += 1
                            
                            # Add to dataframe following notebook pattern
                            dataframe = pd.concat([dataframe, pd.DataFrame([job_data])], ignore_index=True)
                            
                            # Print following notebook pattern
                            print("Job number {0:4d} added - {1:s}".format(jn, job_data['Title']))
                            
                            # Add delay between job extractions
                            await random_delay(1, 2)
                    
                    except Exception as e:
                        print(f"Error processing job: {e}")
                        continue
                
                # Check if we have enough jobs
                if jn >= max_jobs:
                    print(f"Reached target of {max_jobs} jobs")
                    break
                
                # Add delay between pages
                await random_delay(5, 8)
                
            except Exception as e:
                print(f"Error on page: {e}")
                break
        
        # Scrape full descriptions if requested (following notebook pattern)
        if scrape_full_descriptions and len(dataframe) > 0:
            print(f"\nScraping full job descriptions for {len(dataframe)} jobs...")
            
            links_list = dataframe['Links'].tolist()
            descriptions = []
            indices_to_remove = []
            
            for index, link in enumerate(links_list):
                if link != 'NaN' and link != '':
                    try:
                        print(f"Description {index+1}/{len(links_list)}: {dataframe.iloc[index]['Title']}")
                        full_desc = await scrape_full_job_description(page, link)
                        descriptions.append(full_desc)
                        
                        # Add delay between description scrapes
                        await random_delay(3, 6)
                        
                    except Exception as e:
                        print(f"Error scraping description for job {index+1}: {e}")
                        indices_to_remove.append(index)
                        continue
                else:
                    print(f"No job description found for link at index {index}. Skipping...")
                    indices_to_remove.append(index)
                    continue
            
            # Filter out rows with indices to remove (following notebook pattern)
            mask = ~dataframe.index.isin(indices_to_remove)
            dataframe = dataframe[mask].copy()
            
            # Ensure the lengths of descriptions match the length of the dataframe
            if len(descriptions) != len(dataframe):
                if len(descriptions) < len(dataframe):
                    # Pad descriptions with empty strings
                    descriptions += [''] * (len(dataframe) - len(descriptions))
                else:
                    # Truncate descriptions
                    descriptions = descriptions[:len(dataframe)]
            
            # Assign descriptions to dataframe
            dataframe['Description'] = descriptions
    
    # Save results following notebook pattern
    if len(dataframe) > 0:
        # Convert the dataframe to a csv file (following notebook pattern exactly)
        date = datetime.today().strftime('%Y-%m-%d_%H-%M')
        csv_filename = date + "_" + position + "_" + location + ".csv"
        dataframe.to_csv(csv_filename, index=False)
        
        # Print summary
        end_time = datetime.now()
        duration = end_time - start_time
        
        print("\n" + "=" * 60)
        print("SCRAPING COMPLETED!")
        print("=" * 60)
        print(f"Total jobs scraped: {len(dataframe)}")
        print(f"Time taken: {duration}")
        print(f"Results saved to: {csv_filename}")
        print("=" * 60)
        
        # Display the dataframe (following notebook pattern)
        print("\nDataframe preview:")
        print(dataframe.head())
    
    else:
        print("No jobs were scraped.")
    
    return dataframe


async def main():
    """Main entry point with configuration"""
    
    # Configuration - modify these values as needed (following notebook pattern)
    position = DEFAULT_POSITION
    locations = DEFAULT_LOCATION  # Note: using 'locations' to match notebook variable name
    postings = DEFAULT_MAX_JOBS   # Note: using 'postings' to match notebook variable name
    
    # You can also accept command line arguments here if needed
    import sys
    if len(sys.argv) > 1:
        position = sys.argv[1]
    if len(sys.argv) > 2:
        locations = sys.argv[2]
    if len(sys.argv) > 3:
        postings = int(sys.argv[3])
    
    # Call the scraping function
    dataframe = await scrape_indeed_jobs(
        position=position,
        location=locations,
        max_jobs=postings,
        scrape_full_descriptions=True
    )
    
    return dataframe


if __name__ == "__main__":
    asyncio.run(main())
