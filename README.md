# DoctorHelper

> **Research project only.** It has not reached the stage of clinical use. Do not use it to make medical decisions.

A small web demo that reads photos of a Chinese medical record, translates the text into English and summarizes it.

I built it in September–October 2023.

**[See it work](https://oak-wjr.github.io/DoctorHelper/)** on a made-up medical record: the two images, the text PaddleOCR read, Chrome's translation and t5-small's summary from one run ([video](https://oak-wjr.github.io/DoctorHelper/demo.mp4)).

## How it works

1. **OCR**: PaddleOCR reads the Chinese text on one or more photos, on your own computer.
2. **Translate**: Chrome's built-in [Translator API](https://developer.chrome.com/docs/ai/translator-api) translates the text into English line by line, in the browser on your own computer.
3. **Summary**: the general-purpose t5-small model shortens the English text on your own computer. The text is cut into whole sentences and grouped into pieces of about 480 characters; t5-small rewrites each piece shorter, and the pieces are joined again. This repeats until the text is about a third of its original length, for at most five rounds, and stops early when a round makes the text no shorter. Finally, sentences made of the same words are dropped.

Each step's result is copied into the next step, where it can be corrected before going on.

`ocr-table.py` and `ocr-table2.py` are two experiments with lab reports that are printed as tables.

## Running it

You need Python 3.10 and Google Chrome 138 or later on a desktop computer.

```sh
pip install -r requirements.txt
python web.py
```

Then open http://127.0.0.1:8000 in Chrome. The first start downloads the PaddleOCR and t5-small models and NLTK's sentence data. The first translation makes Chrome download its Chinese–English translation pack, about 80 MB (October 2026); the page shows the progress, and Chrome often needs one more click of Translate after that download.

## Limits

- Use made-up records only.
- t5-small is a small general-purpose model, not one made for medical text, so a summary can leave out or change important facts. Machine translations can be wrong too.
- The Translate step needs desktop Chrome 138 or later; in other browsers, such as Safari, Firefox and Edge, type the English text into Step 3 instead.
- Each time the page opens, it loads Bootstrap and jQuery from public CDNs; photos and text are never sent to them.
- The summary runs on your computer's processor, so a long record can take about a minute.
- Uploaded photos are only kept in a temporary file while they are read.

## History

I started on 30 August 2023 with a script that read one image with PaddleOCR. The three-step page was first committed on 12 September 2023, and the same day I made the summary run in rounds until the text was a third of its length. The first commit (September 2023) is the original work, with its original date (see the [commit history](https://github.com/OAK-WJR/DoctorHelper/commits/main)), and the next commit holds the September–October 2023 changes that were never committed at the time. In this public copy, private details and some code are left out, and Chinese text has been translated into English; commit dates and author names are unchanged. In October 2026 I cleaned the project up for publication: the page now only opens on your own computer and the debugger is off; uploaded photos are no longer saved; the summary can no longer loop forever; the Translate step is back on the page; and I added this README and the license. The free translation service the 2023 version used no longer works reliably: in a test on 8 October 2026 it sometimes returned the text untranslated, without an error. Translation now uses Chrome's built-in Translator API, on your own computer. Later I plan to add another translation method.

## License

[PolyForm Noncommercial 1.0.0](LICENSE). Third-party material is listed in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) and keeps its own terms.
