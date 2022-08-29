<h1 align="center">Pypers 📰</h1>
<p align="center">
  Mail templating and sending with Jupyter
</p>
<p align="center">
  <img src="assets/image/example.jpg" alt="Page example" />
</p>


## VS Code workspace

This project was designed to be used as a Workspace for VS Code. So in addition to containing tools that will help the use, it is essential that Jupyter is used for VS Code for the tool to work!


## Authentication

In order to send the pages by Gmail or fetch data from Google Sheets, Google Cloud credentials are required for authentication in this project.

See the [Getting started with authentication](https://cloud.google.com/docs/authentication/getting-started) for Google Cloud API. Then put your key at `[PROJECT FOLDER]/credentials.json`. and it's ready to use!


## Install

```bash
pip install https://github.com/FelixLuciano/pypers/archive/refs/tags/1.0.0.tar.gz
```

You can also [download the latest version](https://github.com/FelixLuciano/pypers/archive/main.tar.gz) (but not recommended) of the package and install it locally. Or directly:

```bash
pip install https://github.com/FelixLuciano/pypers/archive/main.tar.gz
```

## Create a new page

```bash
python -m pypers create [path/to/page]
```


## License
This project is [MIT licensed](https://github.com/FelixLuciano/Pypers/blob/main/LICENSE).
