# wsbshills
wsbshills is intended to be a fun program to analyze the overall /r/wallstreetbets sentiment on the stonks they shill.

The script writes to a file named `result` a list of ticker symbols sorted by amount of shilling, in the format `(symbol, mentions, positive, negative)`

Note that you should NOT base important trading decisions on the output of this program, and I am not responsible for any losses sustained should you choose to do so. Having said that, I'd love to hear how it goes if you're crazy enough to try it.

Let me know if you have any questions or suggestions!

## Setup/Running
In order to run this script, you will need to get Reddit API credentials [here](https://www.reddit.com/prefs/apps).

Once you have done that, follow these steps:
1. Download/clone this repository.
2. Create a file named `config.ini` in the repo directory, and copy and paste this configuration into it:
```
[wsbshills]
[auth]
username=
password=
clientid=
clientsecret=
```
Fill this config file out with your Reddit username/password, as well as your id/secret from your API credentials (no quotes or anything). **Make CERTAIN that you do not share this file with anyone, or accidentally commit it to version control!**

3. Pip install dependencies: `praw, numpy, configparser`
4. Run `python wsbshills.py`
5. The script will then log in to Reddit with the supplied credentials, browse the top hottest threads on /r/wallstreetbets, and dump the most popular tickers and their calculated sentiment into a file named `result`. This will take a minute or two to complete, depending on how many threads you choose to browse and how many comments there are in the threads.

## Contributing
Contributions are welcome in the form of pull requests, bug reports, and general suggestions. You can either open an issue here or DM me on Reddit.

There are a lot of ways that this script can be improved. Probably most importantly, improvements to the `analyze_comment()` function will lead to more accurate assessments and maximum tendies.

The script currently uses a single CSV file of S&P500 tickers that I found somewhere, as well as a supplementary list of tickers in `ADDL_SYMS.txt`. It would be better to dynamically pull symbols from somewhere, but I haven't found a good free API yet. 

Currently, tickers that are commonly-used words (like A, IT, ARE, SO, ALL, HAS, SEE) should just be ignored, because I haven't figured out a way to definitively tell whether the post is just using the word or shilling the stonk yet.

There are certainly more improvements that could be made, and I plan to continue working on this.


