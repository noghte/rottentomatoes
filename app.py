from lxml import html
import requests
import time
import csv
import os
import sys

# You can change these values
allow_extract_critics = True
allow_extract_audience = True
page_limit = 52
ctitic_review_prefix = "" #To prevent converting fractions to dates in Excel, you can add a prefix (for example, ctitic_review_prefix = "'")
url_list = ["https://www.rottentomatoes.com/m/star_wars_the_last_jedi/reviews/",
            "https://www.rottentomatoes.com/m/zootopia/reviews/", ]

def main():
    for url in url_list:
        if allow_extract_critics:
            critics_headers = {
                'Host': 'www.rottentomatoes.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:66.0) Gecko/20100101 Firefox/66.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Cache-Control': 'max-age=0',
                'TE': 'Trailers'
            }
            extract_critics(url, critics_headers, page_limit)
        if allow_extract_audience:
            audience_headers = {
                'Host': 'www.rottentomatoes.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:66.0) Gecko/20100101 Firefox/66.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Cache-Control': 'max-age=0'
            }
            extract_audience(url, audience_headers, page_limit)


def extract_critics(url, headers, page_limit):
    page_number = 0
    page = requests.get(url=url)
    timestr = time.strftime("%Y%m%d-%H%M%S")
    movie_name = url.split('/')[4]
    filename = movie_name + '-' + 'critics-' + str(timestr) + '.csv'
    while page.status_code == 200 and page_number < page_limit:
        rows = get_critic_reviews(page)
        page_number += 1
        new_url = url + "?page=" + str(page_number)
        page = requests.get(url=new_url, headers=headers)
        fnames = ['Title', 'Title_link', 'Thumbnail', 'col-sm-13', 'the_review', 'small', 'small1', 'review_date']
        appendtofile(fnames, filename, rows)
        print("page " + str(page_number) + " done")
    print(filename + " created.")


def extract_audience(url, headers, page_limit):
    page_number = 0
    url = url + "?type=user"
    page = requests.get(url=url, headers=headers)
    timestr = time.strftime("%Y%m%d-%H%M%S")
    movie_name = url.split('/')[4]
    filename = movie_name + '-' + 'audience-' + str(timestr) + '.csv'
    while page.status_code == 200 and page_number < page_limit:
        rows = get_audience_reviews(page)
        page_number += 1
        new_url = url + "&page=" + str(page_number)
        page = requests.get(url=new_url, headers=headers)
        fnames = ['Title', 'Title_link', 'user_review', 'review_date', 'rating']
        appendtofile(fnames, filename, rows)
        print("page " + str(page_number) + " done")
    print(filename + " created.")


def appendtofile(fnames, filename, rows):
    file_exists = os.path.isfile(filename)
    f = open(filename, 'a', encoding='utf-8')
    with f:
        writer = csv.DictWriter(f, fieldnames=fnames,lineterminator='\n')
        if not file_exists:
            writer.writeheader()

        for row in rows:
            writer.writerow(row)


def get_critic_reviews(page):
    tree = html.fromstring(page.content.decode("utf-8", "replace"))

    # Titles
    titles = tree.xpath('//a[contains(@class, "unstyled bold articleLink")]/text()')

    # Title_link
    title_links = tree.xpath('//a[contains(@class, "unstyled bold articleLink")]/@href')
    for i, s in enumerate(title_links):
        title_links[i] = "https://www.rottentomatoes.com" + s

    # Thumbnail
    tumbnails = tree.xpath('//img[contains(@class, "critic_thumb fullWidth")]/@src')

    # col-sm-13
    colsm13 = tree.xpath('//em[contains(@class, "subtle")]/text()')

    # the_review
    the_review = tree.xpath('//div[contains(@class, "the_review")]/text()')

    subtle = tree.xpath('//div[@class="small subtle review-link"]')
    small = []
    for s in subtle:
        content_list = s.xpath('.//text()')
        if len(content_list) >= 3 and ':' in content_list[-1]:
            small.append(ctitic_review_prefix + content_list[-1].split(': ')[-1])
        else:
            small.append(None)

    # small1
    small1 = tree.xpath('//a[contains(text(),"Full Review")]')

    # review_date
    review_date = tree.xpath('//div[contains(@class, "review-date subtle small")]/text()')

    # test to see that all the lists have the same number of items
    # for i in (titles,title_links, tumbnails, colsm13,the_review,small,small1,review_date):
    #     print(len(i))

    items = []
    for data in zip(titles, title_links, tumbnails, colsm13, the_review, small, small1, review_date):
        row = {}
        row['Title'] = data[0]
        row['Title_link'] = data[1]
        row['Thumbnail'] = data[2]
        row['col-sm-13'] = data[3]
        row['the_review'] = data[4]
        row['small'] = data[5]
        row['small1'] = data[6]
        row['review_date'] = data[7]
        items.append(row)

    return items


def get_audience_reviews(page):
    tree = html.fromstring(page.content.decode("utf-8", "replace"))

    # Titles
    titles_temp = tree.xpath('//span[@style="word-wrap:break-word"]/text()')
    titles = []
    for t in titles_temp:
        titles.append(t.strip())

    # Title_link
    title_links = tree.xpath('//a[contains(@class, "bold unstyled articleLink")]/@href')
    for i, s in enumerate(title_links):
        title_links[i] = "https://www.rottentomatoes.com" + s

    # user_reviews
    user_reviews_temp = tree.xpath('//div[contains(@class, "user_review")]/node()')
    user_reviews = []
    for s in user_reviews_temp:
        if type(s) is html.HtmlElement and s.tag == 'div':
            user_reviews.append(s.tail.strip())

    # review_dates
    review_dates = tree.xpath('//span[contains(@class, "fr small subtle")]/text()')

    # ratings
    rating_items = tree.xpath('//span[@class="fl"]/node()')
    rate = 0
    ratings = []
    for index, r in enumerate(rating_items):
        if r == ' ':
            if (index > 0):
                ratings.append(rate)
            rate = 0
        elif type(r) is html.HtmlElement:
            rate += 1
        elif r == '½':
            rate += 0.5
    ratings.append(rate)  # last item

    # test to see that all the lists have the same number of items
    # for i in (titles,title_links, tumbnails, colsm13,the_review,small,small1,review_date):
    #     print(len(i))

    items = []
    for data in zip(titles, title_links, user_reviews, review_dates, ratings):
        row = {}
        row['Title'] = data[0]
        row['Title_link'] = data[1]
        row['user_review'] = data[2]
        row['review_date'] = data[3]
        row['rating'] = data[4]
        items.append(row)

    return items


if __name__ == "__main__":
    main()

