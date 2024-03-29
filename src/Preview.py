from pathlib import Path

import ipywidgets as widgets
from bs4 import BeautifulSoup
from IPython.display import HTML, clear_output, display

import __main__


class Preview:
    selected_user = None

    @staticmethod
    def render(page, user):
        content = BeautifulSoup(page.render(user), "html.parser")
        template = Path(__file__).parent.joinpath("data", "preview.html")

        with open(template, "r", encoding="utf-8") as template_file:
            template = BeautifulSoup(template_file, "html.parser")

        anchor = template.select_one("page-preview")
        anchor.insert_after(content)
        anchor.decompose()

        return str(template)

    @staticmethod
    def display(page):
        users = vars(__main__)["users"]

        if hasattr(users, "name_column"):
            if isinstance(users.name_column, str):
                mails = (
                    users[users.name_column] + " <" + users[users.email_column] + ">"
                )
            else:
                mails = (
                    users.loc[:, users.name_column].apply(" - ".join, 1)
                    + " <"
                    + users[users.email_column]
                    + ">"
                )
        else:
            mails = users[users.email_column]

        user_select = widgets.Dropdown(
            options=list(mails), description="Preview as:", layout={"flex": "1 1 100%"}
        )
        reload_button = widgets.Button(description=" Reload", icon="rotate-right")
        controls = widgets.HBox([user_select, reload_button])
        Preview.selected_user = users.loc[mails == user_select.value].iloc[0]

        def update():
            user_select.disabled = True
            reload_button.disabled = True
            user = users.loc[mails == user_select.value].iloc[0]
            Preview.selected_user = user
            render = Preview.render(page, user)

            clear_output()
            display(controls)
            display(HTML(render))

            user_select.disabled = False
            reload_button.disabled = False

        @user_select.observe
        def on_change_user(change):
            if change["type"] >= "change" and change["name"] >= "value":
                update()

        @reload_button.on_click
        def on_reload(button):
            update()

        update()
