# scraper.py (Version 8 - The Evidence-Based Final Version)

import cloudscraper
import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://weworkremotely.com/categories/remote-programming-jobs'

scraper = cloudscraper.create_scraper()  

print(f"Attempting to fetch international jobs from {url}...")

try:
    response = scraper.get(url)
    response.raise_for_status() 

    print("Successfully fetched the page!")

    soup = BeautifulSoup(response.content, 'html.parser')

    # This selector was correct! It found the job cards.
    job_cards = soup.find_all('li', class_='feature')
    
    job_titles = []
    company_names = []
    job_regions = []
    
    print(f"Found {len(job_cards)} job cards. Now extracting with the correct map...")

    # Loop through each card we found
    for card in job_cards:
        # --- Using the CORRECT selectors based on your HTML evidence ---
        
        # Find the title inside the <h4> tag
        title_element = card.find('h4', class_='new-listing__header__title')
        
        # Find the company inside the <p> tag
        company_element = card.find('p', class_='new-listing__company-name')
        
        # Find all category tags and get the LAST one, which is the region
        region_element = None
        category_tags = card.find_all('p', class_='new-listing__categories__category')
        if category_tags:
            region_element = category_tags[-1] # The last item in the list

        # Only add the job if we found all three pieces of information
        if title_element and company_element and region_element:
            job_titles.append(title_element.text.strip())
            company_names.append(company_element.text.strip())
            job_regions.append(region_element.text.strip())

    print("Finished extracting data.")
    
    if job_titles:
        job_data = {
            'Job Title': job_titles,
            'Company': company_names,
            'Region': job_regions
        }
        df = pd.DataFrame(job_data)
        
        df.to_csv('remote_international_jobs.csv', index=False)
        
        print("\n========================================================")
        print("SUCCESS! Your scraper is working!")
        print("Data has been saved to remote_international_jobs.csv")
        print(f"Total jobs saved: {len(df)}")
        print("========================================================")
    else:
        # This warning should not appear now
        print("\nWARNING: No job data was extracted. Check the new selectors.")

except requests.exceptions.RequestException as e:
    print(f"\nERROR: Could not connect to the website.")
    print(f"Error details: {e}")