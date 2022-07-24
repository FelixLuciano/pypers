<h1 align="center">PyNews 📰</h1>
<p align="center">
  Simple newsletter made with python
</p>
<p align="center">
  <img src="public/image/page.jpg" alt="Page example" />
</p>


## VS Code workspace

This project is a workspace for VS Code, and has set of Tasks that are part of the workflow. So when you open the folder you will see recommendations for extensions that should be installed to make the most of what this project has to offer. One of the extensions shows these tasks in an easy-to-access panel.


## Credentials

In order to fetch data from Google Sheets or send the newsletter by Gmail, Google Cloud credentials are required for authentication in this project.

See the [Getting started with authentication](https://cloud.google.com/docs/authentication/getting-started) for Google Cloud API.


## Install dependencies

This project has some dependencies (see [`requirements.txt`](requirements.txt)) that are not included in the standard python library, so it is necessary to install them runnung the following command:

```bash
pip install -r requirements.txt
```


## Create a page

To create a new page in the project, the `create.py` script generates the necessary files in the page's own folder. So create a new page by runnin the Or run the `➕ Create page` task or with the following command:

```bash
$ python src create folder/example
```


## License
This project is [MIT licensed](https://github.com/FelixLuciano/PyNews/blob/main/LICENSE).
