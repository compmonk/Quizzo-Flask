from pprint import pprint
import string

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd


def scrape():
    data = []
    urls = [
        "https://amigoz.app/mcq/s/t/basic-general-knowledge-set-1-mcq-questions/5fb90b7bde490d1fde6325f1/?page={}",
        "https://amigoz.app/mcq/s/t/basic-general-knowledge-set-2-mcq-questions/5fb90b7cde490d1fde6325f3/?page={}",
        "https://amigoz.app/mcq/s/t/basic-general-knowledge-set-3-mcq-questions/5fb90b7dde490d1fdb3a3975/?page={}"
    ]
    for url in urls:
        response = requests.get(url.format(1))
        soup = bs(response.text, "html.parser")
        pages = len(soup.find_all("li", class_="page-item"))
        for page_no in range(1, pages):
            response = requests.get(url.format(page_no))
            soup = bs(response.text, "html.parser")
            soup.find_all("li", class_="page-item")
            questions = soup.find_all("div", class_="box-body")
            for question in questions:
                data.append({
                    "question_text": question.find("p").text.strip(),
                    **{"option_{}".format(n): o.find("p").text.strip() for o, n in
                       zip(question.find_all("tr", class_="mcq_option"), string.ascii_uppercase)},
                    "answer": question.find("tr", class_="correct_answer").find("p").text.strip(),
                    "explanation": question.find("div", class_="explanation_wrapper").find_all("p")[1].text.strip()
                })
    pd.DataFrame(data).to_csv("output.csv")
    pprint(len(data))


if __name__ == '__main__':
    scrape()
