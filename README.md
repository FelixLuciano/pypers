# 📰 PyNews

Simple python newsletter project

## Install dependencies

```bash
pip install -r requirements.txt
```

## Configuration

`config.json`

```json
{
  "email": {
    "address": "mail@example.com",
    "smtp": "smtp.gmail.com"
  },
  "news": {
    "name": "📰 News",
    "subject": "News of the week"
  },
  "template": {
    "author": "John Doe"
  }
}
```

## Subscribers list

`subscribers.txt`

```txt
mail@example.com
othermail@example.com
...
```

## Build for preview

```bash
$ python src/build.py
```


## Send newsletter

```bash
$ python src/send.py
```
