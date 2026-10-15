# NBA EValuator

A free web tool that checks whether an NBA player points prop is worth betting.

**Live site:** https://jadennguyen-dev.github.io/nba-evaluator/

## What it does

Type a player, the opponent, the points line and the sportsbook odds. The site then:

- **Projects his points for that game**, starting from his recent scoring and adjusting for
  the opponent's defense, home or road, his history against that team, and any key
  teammates or the opponent's best defender being out.
- **Estimates the chance the over or under hits**, based on how much his scoring swings
  from game to game.
- **Compares that chance with the odds** to get the expected value (EV): the average
  profit or loss per $100 bet.
- **Gives a verdict** (Good bet, Marginal or Bad bet) with a plain-English explanation
  of every step, written for people who are new to betting.

It also includes a payout calculator for any American odds, and a player search that
shows season-by-season stats and every game from recent seasons.

## Data

- Player stats and game logs: 2023-24 through 2025-26 regular seasons
  (Basketball-Reference and NBA.com box scores).
- Rosters: 2026-27 rosters from CBS Sports, as of October 14, 2026.
- Team defense ratings: based on 2025-26 games.

## How it works

The whole site is one HTML page that runs in your browser. There is no server, no
login and no data collected. Game logs are stored in `logs/` and loaded only when you
open a player's seasons.

| File | What it is |
|---|---|
| `index.html` | The site |
| `logs/` | Game-by-game logs, split into 12 files |
| `404.html` | Page shown for a broken link |
| `favicon.svg` | Browser tab icon |
| `robots.txt` | Lets search engines list the site |
| `make_deploy.py` | Script used to build this folder from the source version |

## Disclaimer

For entertainment and education only. This is not financial or betting advice, and no
model can guarantee results. You must be of legal betting age where you live.
If gambling stops being fun, call **1-800-GAMBLER**.

## License

The code is under the [MIT License](LICENSE). The NBA statistics come from public
sources and are not covered by it.
