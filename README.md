# Abstract Retriever

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/yourusername/abstract-retriever/blob/main/LICENSE)

Short description of your project.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/abstract-retriever.git
```

1. Navigate to the project directory:

```bash
cd abstract-retriever
```

2.Create and activate a virtual environment:

```bash
python -m venv env
source env/bin/activate  # On macOS/Linux
.\env\Scripts\activate   # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

For parsing some abstracts, you need to use chromedriver.
if you want to us that install chromedriver and pass along its path as an environmental variable when you start the app.

#### Using Chromedriver om a Mac

```
brew install chromedriver
```

find the path to chromedriver
```
which chromedriver
```

Have an environmental variable for chrome driver path, or when you launch the app or service etc.
```
CHROMEDRIVER_PATH='/path/to/chromedriver' python example.py
```

example, using the ptw that is mentioned later
```
CHROME_DRIVER_PATH=/opt/homebrew/bin/chromedriver ptw tests/abstract_parsers/test_journals_physiology_parser.py abstract_retriever/ -nv
```

copy .env file and add your apy keys to it
```bash
cp .env.example .env
```

## Usage

```python
get_abstract("https://www.sciencedirect.com/science/article/abs/pii/S1005030224000446")
```

```python
get_abstract("https://doi.org/10.1016/j.jmst.2023.12.007")
```

```python
get_abstract_from_doi("10.1016/j.jmst.2023.12.007")
```
## A simple Search UI
If you want to see it in action, you can start the gradio app.

You will need gradio
```bash
pip install gradio
```

You can check serch syntax [here](https://schema.elsevier.com/dtds/document/bkapi/search/SCOPUSSearchTips.htm)
```bash
python example.py
```

or if you want to develop the example and reload the app when you change the code, you can start it with:
```bash
gradio example.py
```

## Testing

### Using ptw for Automated Testing

ptw (pytest-watch) is a tool that automatically runs your tests whenever your code changes. This is useful for maintaining a fast development workflow and ensuring that your tests are always up-to-date.

### Installation
You can install ptw using pip:

```bash
pip install pytest-watch
```

### Usage
Usage
Once installed, you can use ptw from the command line to watch your project directory for changes and automatically run your tests:

```bash
ptw
```

If you for instance wish to just watch one test file while you are working on the parsers code you could do this, so as not having to run all tests when working on one particular parser.
```bash
ptw tests/abstract_parsers/test_science_direct_parser.py abstract_retriever/abstract_parsers -nv
```

## Contributing
Contributions are welcome! Please follow these guidelines:

Fork the repository
Create your feature branch (git checkout -b feature/your-feature)
Commit your changes (git commit -am 'Add some feature')
Push to the branch (git push origin feature/your-feature)
Create a new Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details.





