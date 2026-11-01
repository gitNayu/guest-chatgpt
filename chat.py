from playwright.sync_api import sync_playwright
import json
import re

HOME = 'https://chatgpt.com/'


def get_text(data):
    # normal answers are in 'dil', web search answers are in 'references'
    dil = data.get('dil')
    if isinstance(dil, dict) and 'fallbackMarkdown' in dil:
        return dil['fallbackMarkdown']
    for ref in data.get('references') or []:
        model = ref.get('modelDilV2')
        if isinstance(model, dict) and 'fallbackMarkdown' in model:
            return model['fallbackMarkdown']
    return None


def ask(page, text):
    box = page.locator('textarea, [contenteditable="true"]').first
    box.click()
    box.type(text)
    with page.expect_response(lambda r: 'conversation/updates' in r.url) as info:
        page.keyboard.press('Enter')
    raw = info.value.text()
    answer = ''
    for line in raw.split('\n'):
        if 'fallbackMarkdown' not in line:
            continue
        try:
            data = json.loads(line)
        except ValueError:
            continue
        answer = get_text(data) or answer
    return re.sub(r'\\([!-/:-@\[-`{-~])', r'\1', answer)


p = sync_playwright().start()
browser = p.firefox.launch(headless=True)
page = browser.new_context().new_page()
page.goto(HOME)

print('Type new for a new chat, exit to quit.')
while True:
    text = input('You: ').strip()
    if not text:
        continue
    if text == 'exit':
        break
    if text == 'new':
        page.goto(HOME)
        print('New chat started.')
        continue
    print('ChatGPT:', ask(page, text))

browser.close()
p.stop()
