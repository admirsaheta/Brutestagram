# Brutestagram

Brutestagram is a Python script that autom Instagram using a list of username and password combinations. It uses the `httpx` library for making HTTP requests and supports the use of proxies for increased anonymity.

## Installation

1. Clone the repository:

```shell
git clone https://github.com/admirsaheta/brutestagram.git
```

2. Install the required dependencies:

## Usage

1. Create a file called `proxy.txt` and add a list of proxies, one per line.

2. Create a file called `combo.txt` and add a list of username and password combinations, separated by a colon (`:`), one per line.

3. Run the script:

```python
python brutestagram.py
```

4. The script will attempt to log in to Instagram using each combination in `combo.txt` and save the cookies for successful logins to `cookies.txt`.

## Configuration

You can configure the script by modifying the following variables in `brutestagram.py`:

- `proxies_file`: The filename of the file containing the list of proxies.
- `combo_file`: The filename of the file containing the list of username and password combinations.
- `cookies_file`: The filename of the file to save the cookies for successful logins.
- `timeout`: The timeout for HTTP requests in seconds.
- `user_agents`: A list of user agents to use for the requests. A random user agent will be selected for each request.
