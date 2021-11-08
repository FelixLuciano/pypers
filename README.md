<h1 align="center">PyNews 📰</h1>
<p align="center">
  Simple newsletter made with python
</p>

![Page example](assets/page.webp)


## Install dependencies

This project has some dependencies (see [`requirements.txt`](requirements.txt)) that are not included in the standard python library, so it is necessary to install them with the following command:

```bash
pip install -r requirements.txt
```


## Configuration

The `config.json` (at project root) file contains essential  definitions be for sending  and some optional properties for templating. Because this file may contain sensitive information it is ignored, so it needs to be created manually at installation.

```json
{
  "sheet": {
    "id": "Google Sheet id",
    "pages": {
      "joins": "Subscribers tab name",
      "leaves": "Unsubscribers tab name"
    },
    "columns": {
      "date": "Date",
      "mail": "Mail",
      "name": "Name"
    }
  },
  "test_user": {
    "Date": "00/00/0000 00:00:00",
    "Mail": "luciano@mail.com",
    "Name": "Luciano"
  },
  "props": {
    "org": "PyNews SA",
    "author": "Luciano Felix",
  }
}

```


## Credentials

TO DO.


## Template properties

Prop can be declared either in `config.json` or in the meta at the top of the file to be used later in writing using the property name in curly braces.

```md
place: my house

# Who made this?
Mabe by {author} at {place}.
```


## Build for preview

Running the python file in `scripts/build.py` runs the process to build your newsletter HTML code. It also opens it in the web browser so you can see the final result that will be sent to the inboxes.

```bash
$ python scripts/build.py
> Opening preview...
```


## Send newsletter

Running the python file in `scripts/send.py` runs the build process in tandem with the newsteller's send process for the inboxes. So, in addition to opening the web browser so you can see the final result, confirm whether you want to send the newsletter and ask for the transport email account access password and then dispatch for the inboxes.

```bash
$ python scripts/send.py
> Opening preview...
> Send? (yes/no) yes
> Sending 1 of 32 to username...
...
> Newsletter launched successfully!
```


## Send newsletter test

TO DO.

```bash
$ python scripts/send.py --test
> Opening preview...
> Send? (yes/no) yes
> Newsletter launched successfully!
```

## VS Code tasks

[Task Explorer](https://marketplace.visualstudio.com/items?itemName=spmeesseman.vscode-taskexplorer)


## License
This project is [MIT licensed](https://github.com/FelixLuciano/PyNews/blob/main/LICENSE).
