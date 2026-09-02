# Що завантажувати на хостинг

## Коротко

1. Завантажити **вміст теки `deploy/`** у корінь сайту (`public_html` / `www`).
2. Створити там **`config.php`** з токеном бота — його немає в `deploy/` навмисно.
3. Перевірити `https://automatonpower.com.ua/send-form.php?selftest=1`.

Теку `deploy/` збирає `bash build_deploy.sh` — у ній рівно те, що потрібно сайту,
без вихідних фото й службових скриптів.

---

## 1. Завантажити

Вміст `deploy/` (48 файлів, ~16 МБ) — саме **вміст**, не саму теку:

```
public_html/
├── index.html
├── 21700.html
├── high-density.html
├── ev-packs.html
├── send-form.php          ← приймає заявки
├── config.example.php     ← зразок, не працює сам по собі
├── robots.txt
├── sitemap.xml
├── llms.txt
├── images/                ← 40 файлів
└── datasheets/            ← 3 PDF
```

## 2. Створити на хостингу: `config.php`

**Це єдиний файл, який треба створити руками.** Його немає в git і немає в `deploy/` —
токен бота не можна зберігати в репозиторії.

Поруч із `send-form.php` створити `config.php`:

```php
<?php
return [
    'bot_token' => '1234567890:AAE...',   // від @BotFather
    'chat_id'   => '-1001234567890',      // куди надсилати заявки
    'notify_email' => '',                 // необовʼязково: копія на пошту
    'rate_limit_per_hour' => 5,
];
```

Як отримати токен і `chat_id` — покроково в `TELEGRAM_SETUP.md`.

## 3. Перевірити

Відкрити `https://automatonpower.com.ua/send-form.php?selftest=1` — має віддати JSON:

| Поле | Має бути |
|---|---|
| `config_present` | `true` |
| `token_present` | `true` |
| `chat_id` | ваш ID |
| `can_send` | `true` |
| `php_ok` | `true` |

Потім надіслати тестову заявку через форму на сайті.

---

## Чого на хостингу бути НЕ повинно

Ці файли потрібні тільки для розробки — завантажувати їх не треба:

| | |
|---|---|
| `images automationPower/`, `photos_jpg/` | вихідні фото, ~115 МБ |
| `style.png`, `design.png` | референси дизайну |
| `build_pages.py`, `build_seo.py`, `build_datasheets.mjs` | генератори сторінок |
| `replace_bg.py`, `crop_product.py`, `normalize_icons.mjs`, `gen_images*.sh` | обробка фото |
| `screenshot.mjs`, `serve.mjs`, `audit.mjs`, `checklinks.mjs`, `shot-*.mjs` | локальні перевірки |
| `node_modules`, `.venv-bg/`, `temporary screenshots/` | службове |
| `CLIENT_BRIEF.md`, `README.md`, `DEPLOY.md`, `TELEGRAM_SETUP.md` | документація |

## Вимоги до хостингу

- **PHP 7.4+** — сторінки статичні, але `send-form.php` потребує PHP.
- Вихідні HTTPS-запити з сервера (cURL або `allow_url_fopen`) — це перевіряє `?selftest=1`.
- HTTPS на домені.

Якщо хостинг статичний (GitHub Pages, Netlify без функцій) — форми не працюватимуть,
логіку `send-form.php` треба перенести у serverless-функцію.

## Типи файлів (MIME)

Перевірити, що сервер віддає:

- `sitemap.xml` → `application/xml`
- `robots.txt`, `llms.txt` → `text/plain`
- `.pdf` → `application/pdf`

На Apache це зазвичай уже налаштовано. Якщо `sitemap.xml` відкривається як завантаження —
додати в `.htaccess`:

```apache
AddType application/xml .xml
AddType text/plain .txt
```

## Після оновлення сайту

Сторінки генеруються, тому порядок такий:

```bash
python3 build_pages.py      # 21700 / high-density / ev-packs
python3 build_seo.py        # мета, JSON-LD, robots, sitemap, розміри картинок
bash build_deploy.sh        # збирає deploy/
```

Далі завантажити вміст `deploy/`. `config.php` на сервері не чіпати — він там уже є.
