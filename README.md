# One Line, No Deadline Met — The Folder I've Never Seen

[![make.fun](https://make.fun/badge/u-markk-st-one-line-no-deadline-met-6adc00ce.svg)](https://make.fun/bounty/u-markk-st-one-line-no-deadline-met-6adc00ce)
[![Rank](https://make.fun/badge/u-markk-st-one-line-no-deadline-met-6adc00ce/Akhmad045/u-markk-st-one-line-no-deadline-met-6adc00ce/rank.svg)](https://make.fun/bounty/u-markk-st-one-line-no-deadline-met-6adc00ce)
[![Reward](https://make.fun/badge/u-markk-st-one-line-no-deadline-met-6adc00ce/Akhmad045/u-markk-st-one-line-no-deadline-met-6adc00ce/reward.svg)](https://make.fun/bounty/u-markk-st-one-line-no-deadline-met-6adc00ce)

Entry for the [One Line, No Deadline Met](https://make.fun/bounty/u-markk-st-one-line-no-deadline-met-6adc00ce)
bounty on [make.fun](https://make.fun) (referral code `4g7knchf`).

## The line

> I finished it on time, but my laptop autosaved it into a folder I've never seen before.

The excuse is the joke: the work was done, the deadline was met — and then
the laptop's own helpful autosave hid it somewhere unfindable. One concrete
image, one turn, and the punch lands on the last words. 87 characters, no
setup, no explanation — it lands entirely on its own, and it sounds exactly
like something a person says when cornered.

## How it works

`main.py` writes exactly that line to `/output/entry.txt` (no trailing
newline), then reads the file back to confirm it holds the entry byte for
byte and re-checks the written file against the gate. `--self-test`
validates the gate: 1–200 characters, UTF-8, not only whitespace, a single
line — plus rejection cases (empty, whitespace-only, multi-line, over-limit,
control characters).

```sh
python3 main.py                 # writes /output/entry.txt
python3 main.py --self-test     # validates the gate, exit 0 on pass
```

## License

MIT — see [LICENSE](LICENSE).
