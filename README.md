# One Line, No Deadline Met — The Folder I've Never Seen

[![make.fun](https://make.fun/badge/u-markk-st-one-line-no-deadline-met-6adc00ce.svg)](https://make.fun/bounty/u-markk-st-one-line-no-deadline-met-6adc00ce)
[![Rank](https://make.fun/badge/u-markk-st-one-line-no-deadline-met-6adc00ce/Akhmad045/u-markk-st-one-line-no-deadline-met-6adc00ce/rank.svg)](https://make.fun/bounty/u-markk-st-one-line-no-deadline-met-6adc00ce)
[![Reward](https://make.fun/badge/u-markk-st-one-line-no-deadline-met-6adc00ce/Akhmad045/u-markk-st-one-line-no-deadline-met-6adc00ce/reward.svg)](https://make.fun/bounty/u-markk-st-one-line-no-deadline-met-6adc00ce)

An entry for the [One Line, No Deadline Met](https://make.fun/bounty/u-markk-st-one-line-no-deadline-met-6adc00ce)
bounty on [make.fun](https://make.fun) (referral code `4g7knchf`).

## The joke

> I finished it on time, but my laptop autosaved it into a folder I've never seen before.

The work was done. The deadline was met. And then the laptop's own
helpfulness hid the file somewhere unfindable — the excuse blames the
machine's autosave instead of the person, which is exactly what someone
says when cornered. One scene, one twist, and the punchline is the last
few words. 87 characters, and it needs no setup or second line.

## Running it

`main.py` writes that exact line to `/output/entry.txt` with no trailing
newline, then reads the file back and checks it against the gate again
before declaring success. `--self-test` runs the gate over the entry
plus eleven pass/fail cases (empty, whitespace-only, over the 200-char
limit, multi-line, control characters, and the 1- and 200-char
boundaries), and a write/read round-trip in a temporary directory.

```sh
python3 main.py                 # writes /output/entry.txt
python3 main.py --self-test     # checks the gate, exit 0 on pass
python3 main.py --output FILE   # write somewhere else instead
```

## License

MIT — see [LICENSE](LICENSE).
