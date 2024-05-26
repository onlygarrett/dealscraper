# DealScraper

Python tool to scrape deals from isthereanydeals.com.
This scripts main purpose is to utilize [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) to scrape deals off of
deal sites and keep a running log.

# Dependencies!

1. Python
2. Poetry
3. VirtualEnv
4. [Chromedriver](https://developer.chrome.com/docs/chromedriver)

# Concept + Future

- Currently pulls from isthereanydeals homepage to log deals.
- The plan is to allow scraping of subsequent pages.
- CLI support and game ignore lists is the next update.

# Setup

1. clone the repo
2. `poetry install`
3. `poetry shell`
4. run with `python dealscraper/__main__.py`
   (**_until I build out the CLI support_**)
5. CSV's will be output nested in the deals directory

# TODO:

- [x] Get Majority of DealsScraper classes built out and running with output
- [x] Get Logging working with active output file
- [ ] Get CLI support working to allow for better UX
- [ ] Get User ignor list and Duplicate list implemented, will probably include a validator
- [ ] Deeper scraping
