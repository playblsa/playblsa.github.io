import json
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from schedule_data import TOURNAMENT_NAME, TEAM_NAMES, SLOTS, DAY_INFO
from menu_rules_data import (FOOD_TRUCK_VENDOR, FOOD_TRUCK_TAGLINE, FOOD_TRUCK_ITEMS,
                              FOOD_TRUCK_NOTE, DRINKS_SNACKS, RULES_SECTIONS)

def conv(s):
    out = dict(s)
    for k in ('d1','d2'):
        if isinstance(out.get(k), tuple):
            out[k] = list(out[k])
    return out

data = {
    'slots': [conv(s) for s in SLOTS],
    'dayInfo': DAY_INFO,
    'teams': list(TEAM_NAMES.keys()),
    'teamNames': TEAM_NAMES,
    'foodTruck': {
        'vendor': FOOD_TRUCK_VENDOR,
        'tagline': FOOD_TRUCK_TAGLINE,
        'items': FOOD_TRUCK_ITEMS,
        'note': FOOD_TRUCK_NOTE,
    },
    'drinksSnacks': DRINKS_SNACKS,
    'rules': RULES_SECTIONS,
}
DATA_JSON = json.dumps(data)

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>__TOURNAMENT_NAME__ — Live Schedule</title>
<style>
:root{
  --hero:#081849;
  --hero-dark:#050F2E;
  --cream:#ECDFD2;
  --lapis:#213885;
  --plum:#5F3475;
  --accent:#893172;
  --muted:#7A7482;
  --dark-muted:#C7BFC9;
  --line:#CCCACC;
  --ink:#081849;
  --f-display: -apple-system, "Helvetica Neue", Arial, sans-serif;
  --f-body: -apple-system, system-ui, "Segoe UI", Arial, sans-serif;
  --f-mono: ui-monospace, "SF Mono", "Cascadia Code", "Courier New", monospace;
}
*{box-sizing:border-box;}
body{margin:0;background:var(--cream);color:var(--ink);font-family:var(--f-body);}
.app{max-width:900px;margin:0 auto;padding-bottom:48px;}

.topbar{background:linear-gradient(155deg,var(--hero),var(--hero-dark));
  color:var(--cream);padding:22px 20px 18px;position:sticky;top:0;z-index:5;
  box-shadow:0 2px 10px rgba(0,0,0,.15);}
.topbar .eyebrow{color:var(--cream);font-weight:700;font-size:11.5px;letter-spacing:.09em;
  font-family:var(--f-display);}
.topbar h1{margin:2px 0 4px;font-size:26px;letter-spacing:-.01em;font-family:var(--f-display);
  font-weight:800;}

.controls{display:flex;flex-wrap:wrap;gap:10px;align-items:center;padding:14px 20px 0;}
.controls select, .controls .btn{
  font-family:var(--f-body);font-size:14px;padding:9px 12px;border-radius:8px;
  border:1.5px solid var(--line);background:#fff;color:var(--ink);
}
.controls label{font-size:11px;color:var(--muted);font-weight:700;letter-spacing:.05em;
  text-transform:uppercase;display:block;margin-bottom:3px;}
.field{display:flex;flex-direction:column;}
.day-tabs{display:flex;gap:6px;}
.day-tabs button{border:1.5px solid var(--line);background:#fff;color:var(--ink);
  padding:9px 14px;border-radius:8px;font-size:13.5px;font-weight:700;cursor:pointer;
  font-family:var(--f-body);}
.day-tabs button.active{background:var(--hero);color:var(--cream);border-color:var(--hero);}

.legend-row{display:flex;flex-wrap:wrap;gap:14px;align-items:center;padding:12px 20px 0;
  font-size:12px;color:var(--muted);}
.legend-row .chip{display:inline-flex;align-items:center;gap:6px;font-weight:600;}
.diamond-mark{width:10px;height:10px;transform:rotate(45deg);display:inline-block;flex:none;}
.round-badge{width:17px;height:17px;border-radius:50%;display:inline-flex;align-items:center;
  justify-content:center;font-size:10px;font-weight:800;font-family:var(--f-display);flex:none;}

main{padding:14px 20px 0;}

.day-divider{background:var(--hero);color:var(--cream);font-family:var(--f-display);
  font-weight:800;font-size:13px;letter-spacing:.06em;padding:8px 12px;border-radius:6px;
  margin:16px 0 8px;}
.day-divider:first-child{margin-top:0;}

.slot-card{border:1.5px solid var(--line);border-radius:10px;background:#fff;margin-bottom:10px;
  overflow:hidden;}
.slot-time{font-family:var(--f-mono);font-weight:700;color:var(--lapis);font-size:13.5px;
  padding:10px 14px 0;}
.slot-games{display:grid;grid-template-columns:1fr;gap:0;}
@media(min-width:640px){.slot-games.two-col{grid-template-columns:1fr 1fr;}}
.game-half{padding:8px 14px 12px;}
.game-half + .game-half{border-top:1px solid var(--line);}
@media(min-width:640px){
  .slot-games.two-col .game-half + .game-half{border-top:none;border-left:1px solid var(--line);}
}
.diamond-label{display:flex;align-items:center;gap:6px;font-size:10.5px;font-weight:800;
  color:var(--muted);letter-spacing:.05em;margin-bottom:4px;}
.matchup{font-family:var(--f-display);font-weight:800;font-size:18px;}
.matchup.final-matchup .winner{color:var(--lapis);}
.matchup .score-dash{color:var(--muted);font-weight:400;margin:0 3px;}
.final-tag{display:inline-block;background:var(--accent);color:var(--cream);font-family:var(--f-display);
  font-size:9.5px;font-weight:800;letter-spacing:.05em;padding:2px 7px;border-radius:4px;
  margin-left:8px;vertical-align:middle;}
.result-tag{display:inline-block;font-family:var(--f-display);font-size:9.5px;font-weight:800;
  letter-spacing:.05em;padding:2px 7px;border-radius:4px;margin-left:8px;vertical-align:middle;}
.result-tag.win{background:var(--lapis);color:var(--cream);}
.result-tag.loss{background:var(--muted);color:var(--cream);}
.result-tag.tie{background:var(--accent);color:var(--cream);}
.sub{font-size:11.5px;color:var(--muted);margin-top:1px;}
.duty-line{display:flex;align-items:center;gap:7px;font-size:12.5px;margin-top:8px;}
.beer-strip{border-top:1px dashed var(--line);padding:9px 14px;display:flex;align-items:center;
  gap:7px;font-size:12.5px;justify-content:center;background:#F5EFE6;}

.special-row{border-radius:10px;margin-bottom:10px;padding:16px;text-align:center;}
.special-row.muted{background:#E4DACD;color:var(--ink);font-style:italic;}
.special-row.playoff{background:var(--hero);color:var(--cream);}
.special-row.playoff .ptime{font-family:var(--f-mono);color:var(--cream);font-size:13px;text-align:left;}
.special-row.playoff .plabel{font-family:var(--f-display);font-weight:800;font-size:22px;margin:6px 0 4px;}
.special-row.playoff .psub{font-size:11.5px;color:var(--dark-muted);}

.team-entry{border:1.5px solid var(--line);border-radius:10px;background:#fff;margin-bottom:9px;
  padding:10px 14px 12px;}
.team-entry .toprow{display:flex;justify-content:space-between;align-items:baseline;}
.team-entry .time{font-family:var(--f-mono);font-weight:700;color:var(--lapis);font-size:13px;}
.team-entry .dloc{font-size:10px;color:var(--muted);font-weight:800;letter-spacing:.04em;}
.team-entry .body{display:flex;align-items:center;gap:10px;margin-top:6px;}
.team-entry .title{font-family:var(--f-display);font-weight:800;font-size:17px;}
.team-entry .desc{font-size:11.5px;color:var(--muted);margin-top:1px;}

.ref-card{border:1.5px solid var(--line);border-radius:10px;background:#fff;margin-bottom:14px;
  padding:16px 18px;}
.ref-card h2{margin:0 0 2px;font-family:var(--f-display);font-size:17px;color:var(--lapis);}
.ref-card .ref-sub{font-size:12px;color:var(--muted);font-style:italic;margin-bottom:10px;}
.price-row{display:flex;justify-content:space-between;gap:10px;padding:6px 0;
  border-bottom:1px dotted var(--line);font-size:14px;}
.price-row:last-child{border-bottom:none;}
.price-row .pname{color:var(--ink);}
.price-row .pprice{font-weight:700;color:var(--ink);white-space:nowrap;}
.ref-note{font-size:11.5px;color:var(--muted);font-style:italic;margin-top:10px;}
.rules-section h3{font-family:var(--f-display);font-size:14px;color:var(--lapis);
  margin:14px 0 6px;}
.rules-section h3:first-child{margin-top:0;}
.rules-section p{font-size:12.5px;line-height:1.5;color:var(--ink);margin:0 0 8px;}

.hidden{display:none !important;}
</style>
</head>
<body>
<div class="app">
  <div class="topbar">
    <div class="eyebrow">__TOURNAMENT_NAME_UPPER__</div>
    <h1>Live Schedule</h1>
  </div>

  <div class="controls">
    <div class="field">
      <label for="teamSelect">View</label>
      <select id="teamSelect"></select>
    </div>
    <div class="field" id="dayTabsWrap">
      <label>Day</label>
      <div class="day-tabs" id="dayTabs"></div>
    </div>
  </div>

  <div class="legend-row">
    <span class="chip"><span class="diamond-mark" style="background:var(--lapis)"></span>Diamond 1</span>
    <span class="chip"><span class="diamond-mark" style="background:var(--plum)"></span>Diamond 2</span>
    <span class="chip"><span class="round-badge" style="background:var(--lapis);color:var(--cream)">S</span>Scorekeeping (2 players)</span>
    <span class="chip"><span class="round-badge" style="background:var(--accent);color:var(--cream)">B</span>Beer tent (2 players)</span>
  </div>

  <main id="content"></main>
</div>

<script>
const DATA = __DATA_JSON__;
const DAY_ORDER = ["Friday","Saturday","Sunday"];
let teamNames = {};
DATA.teams.forEach(t => teamNames[t] = (DATA.teamNames && DATA.teamNames[t]) || t);
let currentView = "__all__";
let currentDay = "Saturday";

function td(code){ return teamNames[code] || code; }

function poolOf(code){ return code[0]; }

function buildTeamSelect(){
  const sel = document.getElementById("teamSelect");
  sel.innerHTML = "";
  const optAll = document.createElement("option");
  optAll.value = "__all__"; optAll.textContent = "Full master schedule";
  sel.appendChild(optAll);
  const optMenu = document.createElement("option");
  optMenu.value = "__menu__"; optMenu.textContent = "Food Truck & Concession";
  sel.appendChild(optMenu);
  const optRules = document.createElement("option");
  optRules.value = "__rules__"; optRules.textContent = "Tournament Rules";
  sel.appendChild(optRules);
  const poolA = document.createElement("optgroup"); poolA.label = "Pool A";
  const poolB = document.createElement("optgroup"); poolB.label = "Pool B";
  DATA.teams.forEach(t => {
    const o = document.createElement("option");
    o.value = t; o.textContent = td(t) + (td(t)!==t ? "  ("+t+")" : "");
    (poolOf(t)==="A" ? poolA : poolB).appendChild(o);
  });
  sel.appendChild(poolA); sel.appendChild(poolB);
  sel.value = currentView;
}

function buildDayTabs(){
  const wrap = document.getElementById("dayTabs");
  wrap.innerHTML = "";
  DAY_ORDER.forEach(d => {
    const b = document.createElement("button");
    b.textContent = d;
    if(d===currentDay) b.classList.add("active");
    b.onclick = () => { currentDay = d; render(); };
    wrap.appendChild(b);
  });
}

function dutyLine(letter, bg, fg, text){
  return `<div class="duty-line"><span class="round-badge" style="background:${bg};color:${fg}">${letter}</span>${text}</div>`;
}

function matchupHtml(pair, result){
  const t1 = td(pair[0]), t2 = td(pair[1]);
  if(!result){
    return `<div class="matchup">${t1} vs ${t2}</div>`;
  }
  const r1 = result[0], r2 = result[1];
  const w1 = r1 > r2 ? "winner" : "";
  const w2 = r2 > r1 ? "winner" : "";
  return `<div class="matchup final-matchup">
    <span class="${w1}">${t1} ${r1}</span>
    <span class="score-dash">&ndash;</span>
    <span class="${w2}">${r2} ${t2}</span>
    <span class="final-tag">FINAL</span>
  </div>`;
}

function renderMasterDay(day){
  const slots = DATA.slots.filter(s => s.day === day);
  let html = "";
  slots.forEach(s => {
    if(s.kind === "game"){
      const beerHtml = s.beer ? `<div class="beer-strip">${dutyLine("B","var(--accent)","var(--cream)", "Beer tent (2 players): <strong>"+td(s.beer)+"</strong>")}</div>` : "";
      html += `<div class="slot-card">
        <div class="slot-time">${s.start} &ndash; ${s.end}</div>
        <div class="slot-games two-col">
          <div class="game-half">
            <div class="diamond-label"><span class="diamond-mark" style="background:var(--lapis)"></span>DIAMOND 1</div>
            ${matchupHtml(s.d1, s.result1)}
            ${s.score1 ? dutyLine("S","var(--lapis)","var(--cream)","Scorekeeping (2 players): <strong>"+td(s.score1)+"</strong>") : ""}
          </div>
          <div class="game-half">
            <div class="diamond-label"><span class="diamond-mark" style="background:var(--plum)"></span>DIAMOND 2</div>
            ${matchupHtml(s.d2, s.result2)}
            ${s.score2 ? dutyLine("S","var(--lapis)","var(--cream)","Scorekeeping (2 players): <strong>"+td(s.score2)+"</strong>") : ""}
          </div>
        </div>
        ${beerHtml}
      </div>`;
    } else if(s.kind === "playoff"){
      const beerHtml = s.beer ? dutyLine("B","var(--accent)","var(--cream)","Beer tent (2 players): <strong>"+td(s.beer)+"</strong>") : "";
      html += `<div class="special-row playoff">
        <div class="ptime">${s.start} &ndash; ${s.end}</div>
        <div class="plabel">${s.label}</div>
        <div class="psub">Scorekeeping: Tournament Execs</div>
        ${beerHtml ? `<div style="margin-top:8px;display:flex;justify-content:center;">${beerHtml}</div>` : ""}
      </div>`;
    } else {
      const beerHtml = s.beer ? dutyLine("B","var(--accent)","var(--cream)","Beer tent (2 players): <strong>"+td(s.beer)+"</strong>") : "";
      html += `<div class="special-row muted">
        ${s.label}
        ${beerHtml ? `<div style="margin-top:6px;display:flex;justify-content:center;font-style:normal;">${beerHtml}</div>` : ""}
      </div>`;
    }
  });
  return html;
}

function teamGames(code){
  const out = [];
  DATA.slots.forEach(s => {
    if(s.kind === "game" || s.kind === "playoff"){
      if(Array.isArray(s.d1) && s.d1.includes(code)){
        const myIdx = s.d1[0]===code ? 0 : 1;
        out.push({slot:s, role:"play", diamond:"Diamond 1", opponent: s.d1[myIdx===0?1:0], result: s.result1, myIdx});
      }
      if(Array.isArray(s.d2) && s.d2.includes(code)){
        const myIdx = s.d2[0]===code ? 0 : 1;
        out.push({slot:s, role:"play", diamond:"Diamond 2", opponent: s.d2[myIdx===0?1:0], result: s.result2, myIdx});
      }
    }
    if(s.score1 === code){ out.push({slot:s, role:"score", diamond:"Diamond 1"}); }
    if(s.score2 === code){ out.push({slot:s, role:"score", diamond:"Diamond 2"}); }
    if(s.beer === code){ out.push({slot:s, role:"beer", diamond:null}); }
  });
  return out;
}

function resultTag(myRuns, oppRuns){
  const cls = myRuns > oppRuns ? "win" : myRuns < oppRuns ? "loss" : "tie";
  const label = myRuns > oppRuns ? "WIN" : myRuns < oppRuns ? "LOSS" : "TIE";
  return `<span class="result-tag ${cls}">${label}</span>`;
}

function renderTeamView(code){
  const games = teamGames(code);
  let html = `<div style="margin-bottom:10px;">
    <span style="font-family:var(--f-display);font-weight:800;font-size:20px;">${td(code)}</span>
    <span style="font-size:12px;color:var(--muted);"> &middot; Pool ${poolOf(code)} &middot; ${games.filter(g=>g.role==='play').length} pool-play games</span>
  </div>`;
  DAY_ORDER.forEach(day => {
    const dayGames = games.filter(g => g.slot.day === day);
    if(!dayGames.length) return;
    html += `<div class="day-divider">${day}</div>`;
    dayGames.forEach(g => {
      const s = g.slot;
      let dcolor = g.diamond === "Diamond 1" ? "var(--lapis)" : g.diamond === "Diamond 2" ? "var(--plum)" : "var(--accent)";
      let letter = g.role === "play" ? "P" : g.role === "score" ? "S" : "B";
      let fg = "var(--cream)";
      let title, desc;
      if(g.role === "play"){
        if(g.result){
          const myRuns = g.result[g.myIdx], oppRuns = g.result[1-g.myIdx];
          title = `${td(code)} ${myRuns} &ndash; ${oppRuns} ${td(g.opponent)} ${resultTag(myRuns, oppRuns)}`;
          desc = (s.kind === "playoff" ? "Playoff game" : "Pool play game") + " &middot; FINAL";
        } else {
          title = `${td(code)} vs ${td(g.opponent)}`;
          desc = s.kind === "playoff" ? "Playoff game" : "Pool play game";
        }
      } else if(g.role === "score"){
        title = "Scorekeeping duty (2 players)";
        const pair = g.diamond === "Diamond 1" ? s.d1 : s.d2;
        desc = Array.isArray(pair) ? `${g.diamond}: ${td(pair[0])} vs ${td(pair[1])}` : "";
      } else {
        title = "Beer tent duty (2 players)";
        desc = "Send 2 players who aren't playing that slot";
      }
      html += `<div class="team-entry">
        <div class="toprow">
          <span class="time">${s.start} &ndash; ${s.end}</span>
          ${g.diamond ? `<span class="dloc">${g.diamond.toUpperCase()}</span>` : ""}
        </div>
        <div class="body">
          <span class="round-badge" style="background:${dcolor};color:${fg};width:24px;height:24px;font-size:12px;">${letter}</span>
          <div>
            <div class="title">${title}</div>
            <div class="desc">${desc}</div>
          </div>
        </div>
      </div>`;
    });
  });
  return html;
}

function renderMenu(){
  const ft = DATA.foodTruck;
  let html = `<div class="ref-card">
    <h2>Food Truck &mdash; ${ft.vendor}</h2>
    <div class="ref-sub">${ft.tagline}</div>
    ${ft.items.map(([name, price]) => `<div class="price-row"><span class="pname">${name}</span><span class="pprice">${price}</span></div>`).join("")}
    <div class="ref-note">${ft.note}</div>
  </div>`;
  html += `<div class="ref-card">
    <h2>Drinks &amp; Snacks</h2>
    <div class="ref-sub">2026 Price List</div>`;
  DATA.drinksSnacks.forEach(([section, items]) => {
    html += `<h3 style="font-family:var(--f-display);font-size:13px;color:var(--plum);margin:12px 0 4px;">${section}</h3>`;
    html += items.map(([name, price]) => `<div class="price-row"><span class="pname">${name}</span><span class="pprice">${price}</span></div>`).join("");
  });
  html += `</div>`;
  return html;
}

function renderRules(){
  let html = "";
  DATA.rules.forEach(([title, paragraphs]) => {
    html += `<div class="ref-card rules-section"><h3>${title}</h3>`;
    html += paragraphs.map(p => `<p>${p}</p>`).join("");
    html += `</div>`;
  });
  return html;
}

function render(){
  buildDayTabs();
  document.getElementById("dayTabsWrap").style.display = currentView === "__all__" ? "" : "none";
  const content = document.getElementById("content");
  if(currentView === "__all__"){
    content.innerHTML = renderMasterDay(currentDay);
  } else if(currentView === "__menu__"){
    content.innerHTML = renderMenu();
  } else if(currentView === "__rules__"){
    content.innerHTML = renderRules();
  } else {
    content.innerHTML = renderTeamView(currentView);
  }
}

function init(){
  buildTeamSelect();
  render();

  document.getElementById("teamSelect").addEventListener("change", (e) => {
    currentView = e.target.value;
    render();
  });
}
init();
</script>
</body>
</html>
"""

HTML = HTML.replace("__DATA_JSON__", DATA_JSON)
HTML = HTML.replace("__TOURNAMENT_NAME__", TOURNAMENT_NAME)
HTML = HTML.replace("__TOURNAMENT_NAME_UPPER__", TOURNAMENT_NAME.upper())

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html"), "w") as f:
    f.write(HTML)

print("written", len(HTML), "bytes")
