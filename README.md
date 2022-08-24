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


## Install dependencies

This project has some dependencies (see [`requirements.txt`](requirements.txt)) that are not included in the standard python library, so after cloning this template, it is necessary to install them in an environment running the following command:

```bash
pip install https://github.com/FelixLuciano/pypers/archive/main.tar.gz
```

You can also [download the latest version](https://github.com/FelixLuciano/pypers/archive/main.tar.gz) of the package and install it as a module by following:

```bash
pip install ./path-to/pypers-main.tar.gz
```


## License
This project is [MIT licensed](https://github.com/FelixLuciano/Pypers/blob/main/LICENSE).
