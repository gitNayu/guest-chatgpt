# chat.py

A small terminal chat for ChatGPT. No account and no API key. It opens chatgpt.com as a guest in a hidden Firefox and lets you talk to it with `input()` and `print()`.

> This is unofficial. It is not made by OpenAI. The site can change at any time, and then the script can break.

## What it does

- Opens chatgpt.com in a hidden Firefox (Playwright)
- Types your message and presses Enter
- Reads the answer from the server response and prints it
- Keeps the same chat open, so ChatGPT remembers the earlier messages

## Install

```
pip install playwright
playwright install firefox
```

## Run

```
python chat.py
```

## Commands

| Input | What happens |
|-------|--------------|
| any text | sends the message and prints the answer |
| `new` | starts a new chat |
| `exit` | closes the browser and quits |

## Example

```
Type new for a new chat, exit to quit.
You: hello
ChatGPT: Hi! How can I help you today?
You: exit
```

## Problems

- Nothing happens or no answer: change `headless=True` to `headless=False` in `chat.py` and watch what the browser does.
- Empty answer: the site may have changed its response format, so `get_text()` can no longer find the text.
- Guest chats have limits. If the site asks you to log in, the script will not work.

## How it works

The script does not read the page. It waits for the `conversation/updates` response, finds the lines with `fallbackMarkdown` and takes the last one as the answer. Normal answers are stored in `dil`. Web search answers are stored in `references`.

## Files

- `chat.py` - the whole program (about 50 lines)
