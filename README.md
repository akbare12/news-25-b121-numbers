# The World in Numbers — Wednesday 25 November 2026

[![make.fun](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/akbare12/news-25-b121-numbers/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/akbare12/news-25-b121-numbers/reward.svg)](https://make.fun/bounty/news-image-20261125)

A one-page newspaper front page for Wednesday 25 November 2026: **50 stories**,
all counted — 3 hero stories, 10 number cards, 37 ALSO lines, a 6-cell number
strip, a 13-pin world map, and a DATE CHECK that leaves out the 24 Nov stories.

## The three heroes

1. **Trump hikes tariffs on 14 trade partners** — China 20%, EU 15%, Vietnam 20%.
2. **Kospi crashes -6.16%** — Samsung -9.9%, SK Hynix -11.1%, circuit breaker,
   foreigners sell KRW 1.95tn.
3. **Shenzhou-24: first foreign astronaut joins Tiangong** — Muhammad Zeeshan Ali
   of Pakistan, 40.

Every number badge on the page is the real number from its own story
(Iowa 9,500 lbs, jobless claims 189K, Bitcoin $58,400). The DATE CHECK band
leaves out the 24 Nov stories on purpose (see the band itself for the list).

## How it is built

- `gen.py` (Pillow, build-time only) renders `entry.png` at 1024x1024.
- `main.py` is **stdlib only** (`os` + `shutil`): it copies `entry.png` into
  `MAKEFUN_OUTPUT_DIR` (default `out/`). It imports no PIL, no numpy.
- Run the build with `python3 gen.py`, then verify with the stdlib-only
  simulation described below.

## Verify (stdlib-only simulation)

```sh
python3 -m venv --without-pip ~/workspace/news-25-b121-sim-venv
cp -r ~/workspace/makefun/news-25-b121-numbers ~/workspace/news-25-b121-sim-repo
chmod -R a-w ~/workspace/news-25-b121-sim-repo
cd ~/workspace && MAKEFUN_OUTPUT_DIR=~/workspace/news-25-b121-sim-out \
  ~/workspace/news-25-b121-sim-venv/bin/python news-25-b121-sim-repo/main.py
sha256sum news-25-b121-sim-out/entry.png makefun/news-25-b121-numbers/entry.png
```

The copy must exit 0 and its sha256 must match `entry.png` in this repo.
