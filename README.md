# Pypers starter

Look at the [Pypers repository](https://github.com/FelixLuciano/pypers) to learn more.


## Setup

Open README.md and run `Create Environment` task button at status bar or run the following command:

```bash
pip install https://github.com/FelixLuciano/pypers/archive/refs/tags/1.0.0.tar.gz
```

### Credentials

Then get Google Cloud credentials. In order to send the pages by Gmail or fetch data from Google Sheets, Google Cloud credentials are required for authentication in this project.

See the [Getting started with authentication](https://cloud.google.com/docs/authentication/getting-started) for Google Cloud API. Then put your key at `[PROJECT]/credentials.json`. and it's ready to use!


## Create a new page

Run `New page` task button at status bar or run the following command:

### On macOS & Linux
```bash
python3 -m pypers create path/to/page
```

### On Windows
```ps
python -m pypers create path\to\page
```
