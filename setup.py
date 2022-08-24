from setuptools import setup


def parse_requirements(filename):
    lines = (line.strip() for line in open(filename))

    return [line for line in lines if line and not line.startswith("#")]


if __name__ == "__main__":
    setup(
        name="Pypers",
        version="1.0.0",
        description="Mail templating and sending with Jupyter",
        url="https://github.com/FelixLuciano/pypers",
        author="Luciano Felix",
        packages=["pypers"],
        package_dir={"pypers": "src"},
        package_data={"pypers": ["data/*"]},
        license="MIT",
        install_requires=parse_requirements("requirements.txt"),
    )
