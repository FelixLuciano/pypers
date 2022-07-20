import __main__
import ipywidgets as widgets
from bs4 import BeautifulSoup
from IPython.display import HTML, clear_output, display


class Preview:
    selected_user = None


    @staticmethod
    def render(page, user):
        content = BeautifulSoup(page.render(user), "html.parser")

        with open('public/template/preview.html', 'r', encoding='utf-8') as template_file:
            template = BeautifulSoup(template_file, 'html.parser')

        anchor = template.select_one('page-preview')
        anchor.insert_after(content)
        anchor.decompose()

        return str(template)


    @staticmethod
    def display(page):
        users = vars(__main__)['users']

        if hasattr(users, 'name_column'):
            mails = users[users.name_column] + ' <' + users[users.mail_column] + '>'
        else:
            mails = users[users.mail_column]

        user_select = widgets.Dropdown(
            options=list(mails),
            description='Preview as:',
        )
        reload_button = widgets.Button(
            description=' Reload',
            icon='rotate-right'
        )
        controls = widgets.HBox([user_select, reload_button])

        def update():
            user = users.loc[mails == user_select.value].iloc[0]
            Preview.selected_user = user
            render = Preview.render(page, user)

            clear_output()
            display(controls)
            display(HTML(render))

        def on_change_user(change):
            if change['type'] >= 'change' and change['name'] >= 'value':
                update()

        user_select.observe(on_change_user)

        Preview.selected_user = users.loc[mails == user_select.value].iloc[0]

        def on_reload(button):
            update()

        reload_button.on_click(on_reload)

        update()
