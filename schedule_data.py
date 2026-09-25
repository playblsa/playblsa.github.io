"""
Single source of truth for the 12-team softball tournament schedule.
Update TEAM_NAMES below and re-run the generators to refresh all three
deliverables (master poster, team cards, live HTML page) at once.
"""

"""
Single source of truth for the 12-team softball tournament schedule.
Update TEAM_NAMES below and re-run the generators to refresh all deliverables
(team cards, live HTML page) at once.

Game results: once a game is final, set that slot's result1/result2 to
[runs_for_first_team, runs_for_second_team], matching the team order in
that diamond's d1/d2 tuple. Leave as None until the game is played.
"""

TEAM_NAMES = {
    "A1": "Bat-titudes",
    "A2": "Stealers",
    "A3": "Renegades",
    "A4": "Ice Cold Pitches",
    "A5": "Angels",
    "A6": "Big D's",
    "B1": "Rookies",
    "B2": "Swingers",
    "B3": "Metro Scrappers",
    "B4": "Dynamite Dames",
    "B5": "Basic Pitches",
    "B6": "The Misfits",
}

TOURNAMENT_NAME = "BLSA End of Year Tournament"

# Each "slot" is a dict:
# id: stable short id for referencing this slot when entering results
# day, start, end, kind ("game","lunch","buffer","playoff")
# d1 / d2: (team1, team2) or None
# score1 / score2: scorekeeping team for d1/d2 game, or None / "EXECS"
# result1 / result2: [runs_team1, runs_team2] once final, else None
# beer: team on beer-tent duty this slot, or None
# label: used for lunch/buffer/playoff special rows

SLOTS = [
    # FRIDAY
    dict(id="FRI1", day="Friday", start="6:15 PM", end="8:00 PM", kind="game",
         d1=("A1","A6"), d2=("B1","B6"), score1="B5", score2="A5", beer=None,
         result1=None, result2=None),
    dict(id="FRI2", day="Friday", start="8:00 PM", end="9:45 PM", kind="game",
         d1=("A2","A5"), d2=("B2","B5"), score1="B6", score2="A6", beer=None,
         result1=None, result2=None),
    dict(id="FRI-BUF", day="Friday", start="9:45 PM", end="10:00 PM", kind="buffer",
         label="Unused \u2014 15 min buffer"),

    # SATURDAY
    dict(id="SAT1", day="Saturday", start="8:00 AM", end="9:45 AM", kind="game",
         d1=("A3","A6"), d2=("B3","B6"), score1="B1", score2="A1", beer=None,
         result1=None, result2=None),
    dict(id="SAT2", day="Saturday", start="9:45 AM", end="11:30 AM", kind="game",
         d1=("A2","A4"), d2=("B2","B4"), score1="B3", score2="A3", beer="A3",
         result1=None, result2=None),
    dict(id="SAT-LUNCH", day="Saturday", start="11:30 AM", end="1:00 PM", kind="lunch",
         label="Lunch Break", beer="A5"),
    dict(id="SAT3", day="Saturday", start="1:00 PM", end="2:45 PM", kind="game",
         d1=("A1","A3"), d2=("B1","B3"), score1="B2", score2="A2", beer="B2",
         result1=None, result2=None),
    dict(id="SAT4", day="Saturday", start="2:45 PM", end="4:30 PM", kind="game",
         d1=("A4","A5"), d2=("B4","B5"), score1="B6", score2="A6", beer="A6",
         result1=None, result2=None),
    dict(id="SAT5", day="Saturday", start="4:30 PM", end="6:15 PM", kind="game",
         d1=("A2","A3"), d2=("B2","B3"), score1="B5", score2="A5", beer="B5",
         result1=None, result2=None),
    dict(id="SAT6", day="Saturday", start="6:15 PM", end="8:00 PM", kind="game",
         d1=("A5","A6"), d2=("B5","B6"), score1="B4", score2="A4", beer="A4",
         result1=None, result2=None),
    dict(id="SAT7", day="Saturday", start="8:00 PM", end="9:45 PM", kind="game",
         d1=("A1","A4"), d2=("B1","B4"), score1="B3", score2="A3", beer="B3",
         result1=None, result2=None),
    dict(id="SAT-BUF", day="Saturday", start="9:45 PM", end="10:00 PM", kind="buffer",
         label="Unused \u2014 15 min buffer"),

    # SUNDAY
    dict(id="SUN1", day="Sunday", start="9:30 AM", end="11:15 AM", kind="game",
         d1=("A2","A6"), d2=("B2","B6"), score1="B4", score2="A4", beer="B4",
         result1=None, result2=None),
    dict(id="SUN2", day="Sunday", start="11:15 AM", end="1:00 PM", kind="game",
         d1=("A1","A5"), d2=("B1","B5"), score1="B2", score2="A2", beer="A2",
         result1=None, result2=None),
    dict(id="SUN3", day="Sunday", start="1:00 PM", end="2:45 PM", kind="game",
         d1=("A4","A3"), d2=("B4","B3"), score1="B1", score2="A1", beer="B1",
         result1=None, result2=None),
    dict(id="SUN-BUF", day="Sunday", start="2:45 PM", end="3:15 PM", kind="buffer",
         label="Buffer \u2014 rest before playoffs begin"),
    dict(id="SUN-POOLB", day="Sunday", start="3:15 PM", end="5:15 PM", kind="playoff",
         label="POOL B FINAL", score1="EXECS", score2="EXECS", beer="A1",
         teams=None, result=None),
    dict(id="SUN-POOLA", day="Sunday", start="5:15 PM", end="7:30 PM", kind="playoff",
         label="POOL A FINAL", score1="EXECS", score2="EXECS", beer="B6",
         teams=None, result=None),
]

DAY_INFO = {
    "Friday":   {"hours": "6:00 PM \u2013 10:00 PM"},
    "Saturday": {"hours": "8:00 AM \u2013 10:00 PM  |  Lunch break 11:30 AM\u20131:00 PM"},
    "Sunday":   {"hours": "8:00 AM \u2013 8:00 PM  |  Pool play wraps by 2:45 PM \u2014 playoffs follow"},
}

def team_display(code):
    return TEAM_NAMES.get(code, code)

def team_pool(code):
    return code[0]  # 'A' or 'B'

def team_games(team_code):
    """All (slot, role) entries for this team, in schedule order.
    A team can have more than one entry in the same slot -- e.g. 2 players
    scorekeeping while the rest of the crew is on beer tent duty."""
    out = []
    for s in SLOTS:
        if s["kind"] in ("game", "playoff"):
            for dkey, dname, rkey in (("d1", "Diamond 1", "result1"), ("d2", "Diamond 2", "result2")):
                pair = s.get(dkey)
                if pair and team_code in pair:
                    opponent = pair[0] if pair[1] == team_code else pair[1]
                    result = s.get(rkey)
                    out.append(dict(slot=s, role="play", opponent=opponent, diamond=dname, result=result, pair=pair))
        if s.get("score1") == team_code:
            out.append(dict(slot=s, role="score", opponent=None, diamond="Diamond 1"))
        if s.get("score2") == team_code:
            out.append(dict(slot=s, role="score", opponent=None, diamond="Diamond 2"))
        if s.get("beer") == team_code:
            out.append(dict(slot=s, role="beer", opponent=None, diamond=None))
    return out

if __name__ == "__main__":
    for g in team_games("A1"):
        s = g["slot"]
        print(s["day"], s["start"], "-", s["end"], g["role"], g.get("diamond"), "vs", g.get("opponent"))
