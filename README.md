# Python Practice Projects

My solutions to the practice projects from the book ["Automate the Boring Stuff with Python, 2nd Edition"](https://automatetheboringstuff.com/2e/).

My favourite practice projects:
- Chapter 17 – Keeping Time, Scheduling Tasks, and Launching Programs
  - Practice 2. "Scheduled Web Comic Downloader" - scrapes comic websites and downloads new comics once a day.
- Chapter 18 – Sending Email and Text Messages
  - Practice 2. "Umbrella Reminder" - scrapes a weather website, LLM intelligently decides whether there is a chance of rain, the email reminder to grab an umbrella is sent every morning when the rain is expected.
  - Practice 4. "Controlling Your Computer Through Email" - checks emails for instructions, downloads attachments, sends email when the task is done.

Note: the projects were made on Ubuntu OS, with Python 3.10.12.

## What I learned

Some useful notes about what I learned outside of the book while doing the practice projects.

### Chapter 7 – Pattern Matching with Regular Expressions

#### Practice 2. Strong Password Detection

- To use more than one lookahead in regex, we need to put `.*` into the lookahead, e.g.:
  ```python
  password_regex = re.compile(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{8,}$')
  ```
  [combining multiple positive lookaheads - Reddit](https://www.reddit.com/r/regex/comments/1cgvax2/combining_multiple_positive_lookaheads/)

### Chapter 9 – Reading and Writing Files

#### Practice 3. Regex Search

- When we try to find lines in `.txt` files that match a regular expression, we have to use the `re.DOTALL` flag because the lines in `.txt` files end with `\n` - new lines, and without this flag nothing is matching at all due to presence of new lines, e.g.:
  ```python
  user_regex = re.compile(regex_string, re.DOTALL)
  ```

### Chapter 12 – Web Scraping

#### Practice 1. Command Line Emailer

- When I tried to use `pyinputplus.inputPassword()` for accepting the user password, it did not work in PyCharm IDE, I got the following error:
  ```python
  termios.error: (25, 'Inappropriate ioctl for device')
  ```
  Solution: edit configuration options - Modify options - select "Emulate terminal in output console" - run the program.

  (Answer was found [here](https://intellij-support.jetbrains.com/hc/en-us/community/posts/360003383619-Pycharm-2019-termios-error-25-Inappropriate-ioctl-for-device?page=1#community_comment_6589796593042).)

- An issue with Selenium:
  1. I switch to an iframe:
  ```python
  browser.switch_to.frame(sign_in_iframe)
  ```
  2. I input a password and submit a form inside the iframe, and the page reloads, the next page opens
  3. I try to find the next needed element, but the window does not exist anymore. Error:
  ```python
  selenium.common.exceptions.NoSuchWindowException: Message: Browsing context has been discarded
  ```

  The issue happens because there's no that iframe anymore. Solution: switch to default context.
  ```python
  browser.switch_to.default_content()
  ```

#### Practice 2. Image Site Downloader

If you try to scrape a website, and the website is protected against bots by Cloudflare - you will get a 403 Forbidden error, even if you send the 100% exact same HTTP request that is successful in the browser.

Cloudflare can protect a website with the following techniques:
- TLS fingerprinting - to differentiate a real browser from a Python script
	- https://blog.cloudflare.com/ja4-signals/
	- https://developers.cloudflare.com/bots/concepts/ja3-ja4-fingerprint/
- JavaScript challenge - a real browser can run JS and pass the challenge; a simple HTTP client cannot
	- https://developers.cloudflare.com/waf/reference/cloudflare-challenges/

#### Practice 4. Link Verification

Useful resources:
  - URL validation - [5 Best Ways to Check for URLs in a Python String](https://blog.finxter.com/5-best-ways-to-check-for-urls-in-a-python-string/)
  - Convert relative URL to absolute URL - [Python BS4 – How to Scrape Absolute URL Instead of Relative Path](https://blog.finxter.com/scraping-the-absolute-url-of-instead-of-the-relative-path-using-beautifulsoup/)

### Chapter 13 – Working with Excel Spreadsheets

#### Practice Question 14

Q: If you want to retrieve the result of a cell’s formula instead of the cell’s formula itself, what must you do first?

A: Load the workbook with the `data_only=True` parameter.
```python
import openpyxl

# Load the workbook with data_only=True
wb = openpyxl.load_workbook('produceSales.xlsx', data_only=True)
sheet = wb['Sheet']
# Get the calculated value of the formula in cell D2
calculated_value = sheet['D2'].value
print(f'Calculated value of the formula: {calculated_value}')
```
However, `openpyxl` never evaluates formula - it doesn't compute the formula results; it simply reads what's already stored in the file. When you open a workbook with `data_only=True`, `openpyxl` reads the cached results of the formulas from the file. These results are typically calculated by Excel or another spreadsheet application and then saved in the file.

So, `openpyxl` can access and display the formula results only if they have been calculated and saved by the spreadsheet application.

#### Practice 2. Blank Row Inserter

Accessing cells individually in an Excel workbook can be very slow. The sheet methods `iter_rows()` and `iter_cols()` in the `openpyxl` library iterate over rows and columns much faster.

### Chapter 15 – Working with PDF and Word Documents

#### Practice 1. PDF Paranoja (encrypting and decrypting PDFs)

PyPDF2 is deprecated. We should use `pypdf` (it is similar, but also much simpler).
Documentation: https://pypdf.readthedocs.io/en/latest/user/encryption-decryption.html

(https://stackoverflow.com/a/75572419)

#### Practice 3. Brute-Force PDF Password Breaker

By checking `pypdf` source code, I found that `decrypt()` returns one of these 3 values:
```python
class PasswordType(IntEnum):
    NOT_DECRYPTED = 0
    USER_PASSWORD = 1
    OWNER_PASSWORD = 2
```
So we can consider the file decrypted when the result of `pdf_reader.decrypt(password)` is not `0`.

### Chapter 18 – Sending Email and Text Messages

#### Practice 1. Random Chore Assignment Emailer

The fastest technique to clone a list without referencing the original list:
```python
emails_to_choose_from = emails[:]
```

#### Practice 2. Umbrella Reminder

For this practice project, I decided to use a local LLM to intelligently determine the chance of rain based on the weather forecast in text format scraped from a weather website. So I installed a local `ollama` and used a lightweight LLM model `gemma:2b`.

Useful resources:

- [Ollama Tutorial: Running LLMs Locally Made Super Simple](https://www.kdnuggets.com/ollama-tutorial-running-llms-locally-made-super-simple)
- About structured outputs to constrain a model’s output to a specific format defined by a JSON schema: [Structured outputs](https://ollama.com/blog/structured-outputs)

#### Practice 3. Auto Unsubscriber

- [BeautifulSoup – Search by text inside a tag - Geeks For Geeks](https://www.geeksforgeeks.org/beautifulsoup-search-by-text-inside-a-tag/)

#### Practice 4. Controlling Your Computer Through Email

- If I need to send an email which contains Russian letters or other non-ASCII symbols, I need to encode the whole message body:
  ```python
  smtp_obj.sendmail(EMAIL_ADDRESS_FROM, EMAIL_ADDRESS_TO, message.encode('utf-8'))
  ```
  [Encoding issue when sending an email with SMTP - StackOverflow](https://stackoverflow.com/questions/73347774/encoding-issue-when-sending-an-email-with-smtp)
- Learned how to download an email attachment
  (figured it out on my own by inspecting objects in debug mode, there is no useful article about this, this is the only thing I found: https://www.magiksys.net/pyzmail/api/pyzmail.parse.MailPart-class.html)

### Chapter 19 – Manipulating Images

#### Practice 3. Custom Seating Cards

- [Python pillow/PIL doesn't recognize the attribute "textsize" of the object "imagedraw" - StackOverflow](https://stackoverflow.com/questions/77038132/python-pillow-pil-doesnt-recognize-the-attribute-textsize-of-the-object-imag)
	
  `textsize` was deprecated, the correct attribute is `textlength` which gives you the width of the text.
	
  For the height use the fontsize * how many rows of text you wrote.
	Example code:
  ```python
  w = draw.textlength(text, font=font)
  h = fontSize * rows
  ```

### Other things

- How to write docstrings:
```python
def is_strong_password(password):
    """
    Checks if the given password is strong.

    A strong password is defined as one that is at least eight characters long,
    contains both uppercase and lowercase characters, and has at least one digit.

    :param password: The password string to be checked.
    :type password: str
    :return: True if the password is strong, False otherwise.
    :rtype: bool
    """
    return True if password_regex.fullmatch(password) else False
```

- How to configure a logger:
```python
logging.basicConfig(level=logging.DEBUG, filename='filename.log',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
```

## Links
- Repository URL: [https://github.com/albina0104/automate-boring-stuff-python](https://github.com/albina0104/automate-boring-stuff-python)

## Author
- GitHub - [albina0104](https://github.com/albina0104)
