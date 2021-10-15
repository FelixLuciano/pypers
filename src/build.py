import os
import json
import webbrowser

import helper


with open("config.json", "r", encoding="utf-8") as config_file:
    config = json.load(config_file)

day, month, year = helper.get_date()
template_data = {
    "day": day,
    "month": month,
    "year": year,
    **config["template"]
}


mail_html = helper.build_mail(config, template_data)
mail_text = helper.extract_text(mail_html)


output_html = "dist/output.html"
output_text = "dist/output.txt"

if not os.path.exists(os.path.dirname(output_html)):
    os.makedirs(os.path.dirname(output_html))

with open(output_html, "w", encoding="utf-8", errors="xmlcharrefreplace") as file:
    file.write(mail_html)

with open(output_text, "w", encoding="utf-8", errors="xmlcharrefreplace") as file:
    file.write(mail_text)

webbrowser.open(os.path.abspath(output_html))

print("Abrindo visualização prévia...")
