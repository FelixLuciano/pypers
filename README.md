<h1 align="center">📰 PyNews</h1>
<p align="center">
  Simple python newsletter project
</p>

![Page example](assets/page.webp)

## Install dependencies

```bash
pip install -r requirements.txt
```

## Configuration

`config.json`

```json
{
  "transport": {
    "mail": "mail@example.com",
    "smtp": "smtp.gmail.com"
  },
  "props": {
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
$ python scripts/build.py
> Opening preview...
```


## Send newsletter

```bash
$ python scripts/send.py
> Opening preview...
> Send? (yes/no) yes
> E-mail password:
> Login successfully!
> Sending 1 of 32...
...
> Newsletter launched successfully!
```

## License
This project is [MIT licensed](https://github.com/FelixLuciano/PyNews/blob/main/LICENSE).
