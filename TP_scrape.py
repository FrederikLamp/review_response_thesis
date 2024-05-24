#coding=UTF8
"""
Date: February 1st 2024
author: FJL
Trying to web scrape trustpilot reviews
"""

import pandas as pd
import  scrapy
import requests

# Import the CrawlerProcess: for running the spider
from scrapy.crawler import CrawlerProcess

def config(inputmessage):
    #print(inputmessage)
    company_choice = input("Enter 's' for Skorstensgaard or 'a' for Aunsbjerg reviews:\n")
    return company_choice if company_choice == 's' or company_choice == 'a' else config('wrong input!')


skorstensgaard = False
aunsbjerg = False
while skorstensgaard == False and aunsbjerg == False:
    choice = config('Choose your reviews')
    if choice == 's':
        skorstensgaard = True
    elif choice == 'a':
        aunsbjerg = True
    else:
        raise ValueError('something went wrong...')

# ----------------------------------------------------------------------
# Skorstensgaard:
if skorstensgaard:
    url_1star = 'https://dk.trustpilot.com/review/www.skorstensgaard.dk?replies=true&sort=recency&stars=1'
    html_1star = requests.get(url_1star).content

    url_2star = 'https://dk.trustpilot.com/review/www.skorstensgaard.dk?replies=true&sort=recency&stars=2'
    html_2star = requests.get(url_2star).content

    url_3star = 'https://dk.trustpilot.com/review/www.skorstensgaard.dk?replies=true&sort=recency&stars=3'
    html_3star = requests.get(url_3star).content

    url_4star = 'https://dk.trustpilot.com/review/www.skorstensgaard.dk?replies=true&sort=recency&stars=4'
    html_4star = requests.get(url_4star).content

    url_5star = 'https://dk.trustpilot.com/review/www.skorstensgaard.dk?replies=true&sort=recency&stars=5'
    html_5star = requests.get(url_5star).content
# ------------------------------------------------------------------------

if aunsbjerg:
    url_1star = 'https://dk.trustpilot.com/review/www.aunsbjerg.com?replies=true&sort=recency&stars=1'
    html_1star = requests.get(url_1star).content

    url_2star = 'https://dk.trustpilot.com/review/www.aunsbjerg.com?replies=true&sort=recency&stars=2'
    html_2star = requests.get(url_2star).content

    url_3star = 'https://dk.trustpilot.com/review/www.aunsbjerg.com?replies=true&sort=recency&stars=3'
    html_3star = requests.get(url_3star).content

    url_4star = 'https://dk.trustpilot.com/review/www.aunsbjerg.com?replies=true&sort=recency&stars=4'
    html_4star = requests.get(url_4star).content

    url_5star = 'https://dk.trustpilot.com/review/www.aunsbjerg.com?replies=true&sort=recency&stars=5'
    html_5star = requests.get(url_5star).content
# ------------------------------------------------------------------------

# List of URLs to scrape
url_list = [url_1star, url_2star, url_3star, url_4star, url_5star]

# Initialize the dictionary **outside** of the Spider class
df = pd.DataFrame(columns= ['name','rating', 'review', 'reply'])
Trustpilot_data_list = []

chosen_rating = int(input('Enter the star rating of reviews you want to retrieve (1-5):\n'))

# Create the Spider class
class TP_Spider(scrapy.Spider):
    name = "trustpilot_spider"

    def __init__(self, *args, **kwargs):
        super(TP_Spider, self).__init__(*args, **kwargs)
        self.page_count = 0  # Initialize the page count 

    # start_requests method
    def start_requests(self):
        url = url_list[chosen_rating-1] # UPDATE THIS WHEN CHANGING STAR RATING!!
        yield scrapy.Request(url, callback=self.parse_pages)

    # First parsing method
    def parse_pages(self, response):
        #get the blocks containing all review elements
        review_wrappers = response.xpath('//div[contains(@class, "styles_cardWrapper__LcCPA styles_show__HUXRb styles_reviewCard__9HxJJ")]')
        print('Reviews on page: ', len(review_wrappers))
        #iterate through each block and retrieve the review elements

        for wrapper in review_wrappers:
            review_name = wrapper.xpath('.//span[contains(@class, "typography_heading-xxs__QKBS8")][@data-consumer-name-typography="true"]/text()').get()
            review_summary = wrapper.xpath('.//h2[contains(@class, "typography_heading-s__f7029 typography_appearance-default__AAY17")][@data-service-review-title-typography="true"]/text()').get()
            review_text = wrapper.xpath('.//p[@class="typography_body-l__KUYFJ typography_appearance-default__AAY17 typography_color-black__5LYEn"]//text()').getall()
            review_text_total = ' '.join(review_text) if review_text else None
            reply_text = wrapper.xpath('.//p[@class="typography_body-m__xgxZ_ typography_appearance-default__AAY17 styles_message__shHhX"]//text()').getall()
            reply_text = ' '.join(reply_text) if reply_text else None

            # check for review text:
            if review_text_total is not None:

                #retrieve and format the first part of the review to check for similarity with summary:
                formatted_summary = review_summary.strip().lower().rstrip('…')
                start_of_review = review_text_total[:60].strip().lower()

                # if the summary is not unique to the review, only keep review text
                if formatted_summary in start_of_review:
                    full_review = review_text_total

                else:  # if the summary is unique to the review text, concatenate these. 
                    full_review = review_summary + ". " + review_text_total
            # if the review text is None, only keep summary as the review.
            else:
                full_review = review_summary

            Trustpilot_data_list.append([review_name, chosen_rating, full_review, reply_text]) # add data to data frame

        #increment number of pages crawled
        self.page_count += 1

        # Find the next page link/button
        next_page = response.css('a[name="pagination-button-next"]::attr(href)').extract_first()
        if next_page and self.page_count < 40: # only scrape first 40 pages if more than 40 in current category.
            yield response.follow(next_page, self.parse_pages)
        
        # review_names = response.xpath('//span[contains(@class, "typography_heading-xxs__QKBS8")][@data-consumer-name-typography="true"]')
        # review_name_text = [review_names[i].css('::text').extract() for i in range(len(review_names))]
        # print(len(review_name_text))

        # summary_blocks = response.xpath('//h2[contains(@class, "typography_heading-s__f7029 typography_appearance-default__AAY17")][@data-service-review-title-typography="true"]')
        # summary_blocks_text = [summary_blocks[i].css('::text').extract() for i in range(len(summary_blocks))]


        # review_blocks_old = response.xpath('//p[@class="typography_body-l__KUYFJ typography_appearance-default__AAY17 typography_color-black__5LYEn"]')
        # n_reviews_onpage = len(review_blocks_old)
        # print(n_reviews_onpage)
        # review_blocks_text_list = [review_blocks_old[i].css('::text').extract() for i in range(len(review_blocks_old))]
        # # Concatenate the sentences within each inner list
        # concatenated_review_text = [' '.join(line) for line in review_blocks_text_list]

        # reply_blocks = response.xpath('//p[@class="typography_body-m__xgxZ_ typography_appearance-default__AAY17 styles_message__shHhX"]')
        # n_replies_onpage = len(reply_blocks)
        # print(n_replies_onpage)
        # reply_blocks_text_list = [reply_blocks[i].css('::text').extract() for i in range(len(reply_blocks))]
        # concatenated_reply_text = [' '.join(line) for line in reply_blocks_text_list]

        # # UPDATE THIS FOR THE CURRENT STAR RATING SCRAPED:
        # rating_list = [3 for i in range(len(concatenated_review_text))]

        # for i in range(len(summary_blocks_text)):

        #     Trustpilot_data_list.append([str(review_name_text[i][0]), rating_list[i], concatenated_review_text[i], concatenated_reply_text[i]])
        

        #self.page_count += 1

        # Find the next page link/button
        #next_page = response.css('a[name="pagination-button-next"]::attr(href)').extract_first()
        #if next_page and self.page_count < 50:
        #    yield response.follow(next_page, self.parse_pages)


# Run the Spider
process = CrawlerProcess()
process.crawl(TP_Spider)
process.start()



# Convert the list to a DataFrame
new_df = pd.DataFrame(Trustpilot_data_list, columns= df.columns)

# Concatenate existing DataFrame with new data DataFrame
updated_df = pd.concat([df, new_df], axis=0, ignore_index=True)

# Print a preview of the results:
print(updated_df.head())

# Save scraped reviews according to specific trustpilot site:
if aunsbjerg:
    updated_df.to_csv(str(chosen_rating)+'_star_reviews_aunsbjerg.csv', index=True)
if skorstensgaard:
    updated_df.to_csv(str(chosen_rating)+'_star_reviews_skorstensgaard.csv', index=True)

