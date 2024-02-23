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

## Contributing
Contributions are welcome! Please follow these guidelines:

Fork the repository
Create your feature branch (git checkout -b feature/your-feature)
Commit your changes (git commit -am 'Add some feature')
Push to the branch (git push origin feature/your-feature)
Create a new Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details.





