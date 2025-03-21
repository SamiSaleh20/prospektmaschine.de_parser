import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

# list vysledkov
vystup = []

#extrakcia  html stranky
url = "https://www.prospektmaschine.de/hypermarkte/"
response = requests.get(url)
html_content = response.content
soup = BeautifulSoup(html_content, "html.parser")

# vyhladanie vsetkych letakov v html
letaky = soup.find_all("div", class_="brochure-thumb")



# spracovanie jednotlivych letakov
for letak in letaky:
    #nazov letaka vzdy ulozeny v strong
    nazov = letak.find("strong").get_text(strip=True)
    #datum vzdy ulozeny v small vklase hedden-sm
    datum = letak.find("small", class_="hidden-sm").get_text(strip=True)
    #ak je -   v datume rozdelime ho na valid from na valid to
    if " - " in datum:
        valid_from, valid_to = datum.split(" - ")
        valid_from = valid_from.replace(".", "-")
        valid_to = valid_to.replace(".", "-")
    # ak je len jeden datum napr s textom mame len valid_from
    else:
        valid_from = datum
        valid_from = valid_from.split(" ")[-1]
        valid_to = None
        valid_from = valid_from.replace(".", "-")


    # url obrazka  v img pri src alebo v specialnej clase img lazyloadBrochure
    obrazok = letak.find("img").get('src')
    if obrazok is None:
        obrazok = letak.find("img", class_="lazyloadBrochure").get('data-src')

    # obchod obrazka vzdy v img clase lazyloadLogo pri alt pricom vymazeme Logo z nazvu
    obchod = letak.find("img", class_="lazyloadLogo").get("alt").replace("Logo ", "")

    # cas parsovanie zoberieme aktualny cas
    parsed_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Pridanie údajov do listu
    vystup.append({
        "title": nazov,
        "thumbnail": obrazok,
        "shop_name": obchod,
        "valid_from": valid_from,
        "valid_to": valid_to,
        "parsed_time": parsed_time

    })

# Uloženie do JSON súboru
with open("vystup.json", "w", encoding="utf-8") as file:
    json.dump(vystup, file, ensure_ascii=False, indent=4)
