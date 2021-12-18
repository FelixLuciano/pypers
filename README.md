<h1 align="center">PyNews 📰</h1>
<p align="center">
  Simple newsletter made with python
</p>
<p align="center">
  <img src="assets/page.webp" alt="Page example" />
</p>


## VS Code workspace

This project is a workspace for VS Code, and has set of Tasks that are part of the workflow. So when you open the folder you will see recommendations for extensions that should be installed to make the most of what this project has to offer. One of the extensions shows these tasks in an easy-to-access panel.

![Tasks](assets/tasks.png)

[See more about Task Explorer](https://marketplace.visualstudio.com/items?itemName=spmeesseman.vscode-taskexplorer).

## Credentials

In order to fetch data from Google Sheets or send the newsletter by Gmail, Google Cloud credentials are required for authentication in this project.

See the [Getting started with authentication](https://cloud.google.com/docs/authentication/getting-started) for Google Cloud API.


## Install dependencies

This project has some dependencies (see [`requirements.txt`](requirements.txt)) that are not included in the standard python library, so it is necessary to install them runnung the `1. 📦 Install dependencies` task or with the following command:

```bash
pip install -r requirements.txt
```


## Create a page

To create a new page in the project, the `create.py` script generates the necessary files in the page's own folder. So create a new page by runnin the Or run the `2. ➕ Create page` task or with the following command:

```bash
$ python scripts/create.py
```


## Template properties

Prop can be declared either in `config.json` or in the meta at the top of the file to be used later in writing using the property name in curly braces.

```md
place: my house

# Who made this?
Mabe by {author} at {place}.
```


## Build for preview

The script `build.py` runs the process to build your newsletter HTML code. It also opens it in the web browser so you can see the final result that will be sent to the inboxes. Build a page preview by runnin the Or run the `3. 📰 Build page` task or with the following command:

```bash
$ python scripts/build.py
> Opening preview...
```


## Watch for canges

O script `watch.py` automatiza processo de construção de página específica, gerando uma nova build sempre que algum arquivo for modificado. Start the watchdog by running the `4. 👁️ Watch` task or with the following command: 

```bash
$ python scripts/watch.py
> Turning on watchdog
> Initial building...
> Building...
> Turning off watchdog
```


## Live preview

With another of the recommended extensions for this project, it is possible to display a live preview integrated with vs code. For this do this run the `5. 📄 Show output` task and then the `6. 🖨️ Live Preview` task.

![Live preview](assets/live_preview.png)


## Send newsletter test

TO DO.

```bash
$ python scripts/send.py --test
> Opening preview...
> Send? (yes/no) yes
> Newsletter launched successfully!
```


## Send newsletter

The script `send.py` runs the build process in tandem with the newsteller's send process for the inboxes. So, in addition to opening the web browser so you can see the final result, confirm whether you want to send the newsletter and ask for the transport email account access password and then dispatch for the inboxes. Send the newsletter by running the `8. 🚀 Send` task or with the following command: 

```bash
$ python scripts/send.py
> Opening preview...
> Send? (yes/no) yes
> Sending 1 of 32 to username...
...
> Newsletter launched successfully!
```


## License
This project is [MIT licensed](https://github.com/FelixLuciano/PyNews/blob/main/LICENSE).
