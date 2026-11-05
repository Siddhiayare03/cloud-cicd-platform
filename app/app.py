
import os
from flask import Flask, jsonify, render_template_string
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

secret_key = os.environ.get("FLASK_SECRET_KEY")

if not secret_key:
    raise RuntimeError("FLASK_SECRET_KEY is not configured.")

app.config["SECRET_KEY"] = secret_key

csrf = CSRFProtect(app)


DASHBOARD = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CloudFlow | Cloud Operations</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root {
  --bg:#080d19; --panel:#101829; --panel2:#131e32;
  --line:#233149; --text:#edf3ff; --muted:#8291aa;
  --blue:#579bff; --cyan:#40d9e8; --purple:#9c7bff;
  --green:#37d6a0; --orange:#ffbd69;
}
* {box-sizing:border-box}
body {
  margin:0;background:var(--bg);color:var(--text);
  font-family:'DM Sans',sans-serif;
}
body:before {
  content:"";position:fixed;inset:0;pointer-events:none;
  background:radial-gradient(ellipse at 75% 0%,#1b367044,transparent 38%),
  radial-gradient(ellipse at 0% 70%,#35205b22,transparent 35%);
}
.layout {display:flex;min-height:100vh;position:relative}
.sidebar {
  width:245px;position:fixed;inset:0 auto 0 0;
  background:#0b1220;border-right:1px solid var(--line);
  padding:27px 19px;display:flex;flex-direction:column;z-index:5;
}
.brand {display:flex;align-items:center;gap:12px;margin-bottom:48px}
.brand-icon {
  width:39px;height:39px;border-radius:12px;display:grid;place-items:center;
  background:linear-gradient(135deg,#398fff,#8b64f7);
  font-size:21px;box-shadow:0 5px 25px #438cff55;
}
.brand-name {font:700 20px 'Space Grotesk';letter-spacing:-.7px}
.brand-name span {color:var(--blue)}
.nav-label {font-size:10px;color:#64748b;letter-spacing:1.7px;margin:0 0 13px 10px}
.nav {display:flex;flex-direction:column;gap:7px}
.nav a {
  text-decoration:none;color:#91a0b8;padding:12px 13px;border-radius:10px;
  font-size:13px;display:flex;align-items:center;gap:12px;transition:.2s;
}
.nav a:hover,.nav a.active {background:#1b2b46;color:#fff}
.nav a.active {border:1px solid #315487}
.nav-icon {width:20px;text-align:center;font-size:16px}
.sidebar-bottom {margin-top:auto}
.profile {
  border-top:1px solid var(--line);padding-top:20px;
  display:flex;align-items:center;gap:11px
}
.avatar {
  width:36px;height:36px;border-radius:50%;display:grid;place-items:center;
  background:linear-gradient(135deg,#4a91fa,#a477ff);font-weight:700
}
.profile small {display:block;color:var(--muted);font-size:11px;margin-top:3px}
.main {margin-left:245px;width:calc(100% - 245px);padding:30px 38px 50px}
.topbar {display:flex;justify-content:space-between;align-items:center;margin-bottom:34px}
.breadcrumb {font-size:12px;color:var(--muted)}
.breadcrumb span {color:var(--text)}
.top-actions {display:flex;align-items:center;gap:12px}
.status-pill {
  border:1px solid #246d59;background:#12352d;color:var(--green);
  padding:8px 12px;border-radius:30px;font-size:11px;font-weight:600
}
.status-dot {display:inline-block;width:7px;height:7px;background:var(--green);border-radius:50%;margin-right:7px;box-shadow:0 0 10px var(--green)}
.time {font-size:11px;color:var(--muted)}
.hero {
  border:1px solid #29466d;border-radius:19px;padding:32px 35px;
  background:linear-gradient(110deg,#14294a 0%,#17213d 52%,#251c45 100%);
  position:relative;overflow:hidden;margin-bottom:26px;
}
.hero:after {
  content:"";position:absolute;width:310px;height:310px;border-radius:50%;
  right:-70px;top:-150px;border:1px solid #8eb5ff30;
  box-shadow:0 0 0 35px #8eb5ff09,0 0 0 75px #8eb5ff07;
}
.eyebrow {font-size:10px;letter-spacing:2px;color:#91baff;font-weight:700}
h1 {font:700 clamp(27px,4vw,39px) 'Space Grotesk';letter-spacing:-1.5px;margin:13px 0 9px}
.hero p {color:#b3c4df;font-size:13px;max-width:560px;line-height:1.8;margin:0}
.hero-bottom {display:flex;gap:10px;margin-top:23px;flex-wrap:wrap}
.hero-tag {font-size:11px;padding:8px 12px;border-radius:8px;background:#ffffff12;border:1px solid #ffffff18;color:#dce9ff}
.section-head {display:flex;justify-content:space-between;align-items:center;margin:30px 0 15px}
.section-head h2 {font:600 17px 'Space Grotesk';margin:0}
.section-head span {font-size:11px;color:var(--muted)}
.metrics {display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px}
.card {
  background:linear-gradient(145deg,#121e31,#0e1727);
  border:1px solid var(--line);border-radius:14px;padding:19px;
  transition:transform .2s,border-color .2s;
}
.card:hover {transform:translateY(-3px);border-color:#42699b}
.metric-top {display:flex;justify-content:space-between;align-items:center}
.metric-icon {
  width:34px;height:34px;border-radius:10px;display:grid;place-items:center;
  background:#579bff18;color:var(--blue);font-size:16px
}
.metric-label {font-size:11px;color:var(--muted);margin-top:16px}
.metric-value {font:700 27px 'Space Grotesk';margin-top:6px}
.metric-note {font-size:10px;color:var(--muted);margin-top:7px}
.good {color:var(--green)}
.purple {color:var(--purple)}
.orange {color:var(--orange)}
.pipeline {
  display:grid;grid-template-columns:repeat(5,minmax(0,1fr));
  gap:10px;align-items:center;
}
.stage {
  background:#111d30;border:1px solid var(--line);border-radius:13px;
  padding:19px 10px;text-align:center;position:relative;
}
.stage:not(:last-child):after {
  content:"→";position:absolute;right:-13px;top:43%;
  color:#6687b8;font-size:17px;z-index:2
}
.stage-icon {font-size:23px;margin-bottom:10px}
.stage-name {font-size:12px;font-weight:600}
.stage-desc {font-size:10px;color:var(--muted);margin-top:5px}
.stage-state {font-size:9px;color:var(--green);margin-top:12px}
.two-col {display:grid;grid-template-columns:1.15fr .85fr;gap:15px}
.quality-list {display:grid;grid-template-columns:1fr 1fr;gap:12px}
.quality-item {
  background:#0c1626;border:1px solid var(--line);
  border-radius:11px;padding:15px
}
.quality-name {font-size:11px;color:var(--muted)}
.quality-value {font:600 20px 'Space Grotesk';margin-top:8px}
.quality-sub {font-size:10px;color:var(--muted);margin-top:4px}
.coverage-wrap {display:flex;align-items:center;gap:24px;padding:15px 0}
.donut {
  width:112px;height:112px;border-radius:50%;
  background:conic-gradient(var(--blue) 0 90%,#27364c 90% 100%);
  display:grid;place-items:center;flex-shrink:0
}
.donut-inner {
  width:84px;height:84px;border-radius:50%;background:#101a2b;
  display:grid;place-items:center;text-align:center
}
.donut-inner strong {font:700 22px 'Space Grotesk'}
.donut-inner small {font-size:9px;color:var(--muted)}
.legend {font-size:11px;color:var(--muted);line-height:2.2}
.legend b {color:var(--text)}
.legend i {display:inline-block;width:7px;height:7px;border-radius:50%;margin-right:7px}
.activity {display:flex;flex-direction:column;gap:0}
.activity-row {display:flex;gap:13px;padding:13px 0;border-bottom:1px solid #1e2a3e}
.activity-row:last-child {border:0}
.activity-icon {
  width:32px;height:32px;display:grid;place-items:center;border-radius:9px;
  background:#18352e;color:var(--green);flex-shrink:0
}
.activity-title {font-size:12px;font-weight:600}
.activity-desc {font-size:10px;color:var(--muted);margin-top:4px}
.stack {display:flex;flex-wrap:wrap;gap:9px}
.stack span {
  border:1px solid #2b3c55;background:#152238;border-radius:8px;
  padding:9px 12px;font-size:11px;color:#c2d3ec
}
.footer {text-align:center;color:#61728c;font-size:10px;margin-top:35px}
@media(max-width:1050px) {
  .metrics {grid-template-columns:repeat(2,1fr)}
  .two-col {grid-template-columns:1fr}
}
@media(max-width:720px) {
  .sidebar {width:62px;padding:20px 9px}
  .brand {justify-content:center;margin-bottom:35px}
  .brand-name,.nav-label,.nav a span:not(.nav-icon),.profile div:not(.avatar) {display:none}
  .nav a {justify-content:center;padding:13px 5px}
  .profile {justify-content:center}
  .main {margin-left:62px;width:calc(100% - 62px);padding:20px 14px}
  .hero {padding:24px 20px}
  .pipeline {grid-template-columns:1fr;gap:9px}
  .stage:not(:last-child):after {content:"↓";right:50%;top:auto;bottom:-17px}
  .metrics {grid-template-columns:1fr 1fr;gap:9px}
  .card {padding:14px}
  .metric-value {font-size:22px}
  .quality-list {grid-template-columns:1fr 1fr}
  .time {display:none}
}
@media(max-width:390px) {.metrics {grid-template-columns:1fr}}
</style>
</head>
<body>
<div class="layout">
<aside class="sidebar">
  <div class="brand">
    <div class="brand-icon">⌘</div>
    <div class="brand-name">Cloud<span>Flow</span></div>
  </div>
  <div class="nav-label">WORKSPACE</div>
  <nav class="nav">
    <a class="active" href="#overview"><span class="nav-icon">▦</span><span>Overview</span></a>
    <a href="#pipeline"><span class="nav-icon">⑂</span><span>CI/CD Pipeline</span></a>
    <a href="#quality"><span class="nav-icon">◈</span><span>Code Quality</span></a>
    <a href="#activity"><span class="nav-icon">◷</span><span>Activity</span></a>
    <a href="#stack"><span class="nav-icon">▤</span><span>Tech Stack</span></a>
  </nav>
  <div class="sidebar-bottom">
    <div class="profile">
      <div class="avatar">CF</div>
      <div><strong style="font-size:12px">CloudFlow Project</strong><small>Infrastructure workspace</small></div>
    </div>
  </div>
</aside>

<main class="main" id="overview">
  <div class="topbar">
    <div class="breadcrumb">Workspace / <span>Overview</span></div>
    <div class="top-actions">
      <div class="time" id="clock"></div>
      <div class="status-pill"><i class="status-dot"></i>Application healthy</div>
    </div>
  </div>

  <section class="hero">
    <div class="eyebrow">CLOUD OPERATIONS CENTER</div>
    <h1>Build. Deploy. Automate.</h1>
    <p>Your cloud delivery workflow, unified in one place. Build applications, validate code quality, publish container images and deploy to AWS with automated CI/CD.</p>
    <div class="hero-bottom">
      <span class="hero-tag">☁ AWS Infrastructure</span>
      <span class="hero-tag">⚡ Automated Delivery</span>
      <span class="hero-tag">◈ Code Quality</span>
    </div>
  </section>

  <div class="section-head"><h2>Platform overview</h2><span>Project metrics snapshot</span></div>
  <section class="metrics">
    <div class="card">
      <div class="metric-top"><span class="metric-icon">✓</span><span class="good" style="font-size:10px">Passed</span></div>
      <div class="metric-label">Quality Gate</div><div class="metric-value">Passed</div>
      <div class="metric-note">SonarQube Cloud analysis</div>
    </div>
    <div class="card">
      <div class="metric-top"><span class="metric-icon">◉</span><span class="good" style="font-size:10px">Healthy</span></div>
      <div class="metric-label">Test Coverage</div><div class="metric-value">90<span style="font-size:16px">%</span></div>
      <div class="metric-note">SonarQube reported coverage</div>
    </div>
    <div class="card">
      <div class="metric-top"><span class="metric-icon">◇</span><span class="good" style="font-size:10px">Rating A</span></div>
      <div class="metric-label">Reliability</div><div class="metric-value">A</div>
      <div class="metric-note">0 reliability issues reported</div>
    </div>
    <div class="card">
      <div class="metric-top"><span class="metric-icon">⌁</span><span class="good" style="font-size:10px">Clean</span></div>
      <div class="metric-label">Code Duplication</div><div class="metric-value">0.0<span style="font-size:16px">%</span></div>
      <div class="metric-note">No duplicated blocks reported</div>
    </div>
  </section>

  <div class="section-head" id="pipeline"><h2>Delivery pipeline</h2><span>Automated workflow architecture</span></div>
  <section class="pipeline">
    <div class="stage"><div class="stage-icon">⌘</div><div class="stage-name">GitHub</div><div class="stage-desc">Source control</div><div class="stage-state">● Integrated</div></div>
    <div class="stage"><div class="stage-icon">⚙</div><div class="stage-name">Actions</div><div class="stage-desc">Build & test</div><div class="stage-state">● Integrated</div></div>
    <div class="stage"><div class="stage-icon">◫</div><div class="stage-name">Docker</div><div class="stage-desc">Containerize</div><div class="stage-state">● Integrated</div></div>
    <div class="stage"><div class="stage-icon">☁</div><div class="stage-name">Amazon ECR</div><div class="stage-desc">Image registry</div><div class="stage-state">● Integrated</div></div>
    <div class="stage"><div class="stage-icon">▣</div><div class="stage-name">EC2</div><div class="stage-desc">Application host</div><div class="stage-state">● Deployed</div></div>
  </section>

  <div class="section-head" id="quality"><h2>Code quality & security</h2><span>SonarQube Cloud snapshot</span></div>
  <section class="two-col">
    <div class="card">
      <div class="metric-top"><strong style="font:600 14px 'Space Grotesk'">Quality insights</strong><span class="good" style="font-size:10px">Quality Gate passed</span></div>
      <div class="quality-list" style="margin-top:18px">
        <div class="quality-item"><div class="quality-name">Maintainability</div><div class="quality-value good">A</div><div class="quality-sub">Rating</div></div>
        <div class="quality-item"><div class="quality-name">Reliability</div><div class="quality-value good">A</div><div class="quality-sub">0 reported issues</div></div>
        <div class="quality-item"><div class="quality-name">Security</div><div class="quality-value orange">E</div><div class="quality-sub">2 reported issues</div></div>
        <div class="quality-item"><div class="quality-name">Security review</div><div class="quality-value good">A</div><div class="quality-sub">0 hotspots</div></div>
      </div>
    </div>
    <div class="card">
      <div class="metric-top"><strong style="font:600 14px 'Space Grotesk'">Test coverage</strong><span style="font-size:10px;color:var(--muted)">SonarQube</span></div>
      <div class="coverage-wrap">
        <div class="donut"><div class="donut-inner"><div><strong>90%</strong><br><small>Covered</small></div></div></div>
        <div class="legend">
          <div><i style="background:var(--blue)"></i><b>90%</b> Coverage</div>
          <div><i style="background:#27364c"></i><b>10%</b> Uncovered</div>
          <div style="margin-top:8px">Duplication: <b>0.0%</b></div>
        </div>
      </div>
    </div>
  </section>

  <div class="section-head" id="activity"><h2>Infrastructure & activity</h2><span>Configured project components</span></div>
  <section class="two-col">
    <div class="card">
      <div class="metric-top"><strong style="font:600 14px 'Space Grotesk'">Deployment architecture</strong><span class="good" style="font-size:10px">Operational</span></div>
      <div class="activity" style="margin-top:12px">
        <div class="activity-row"><div class="activity-icon">☁</div><div><div class="activity-title">Amazon EC2</div><div class="activity-desc">Hosts the deployed Flask application</div></div></div>
        <div class="activity-row"><div class="activity-icon">▣</div><div><div class="activity-title">Amazon ECR</div><div class="activity-desc">Stores versioned Docker images</div></div></div>
        <div class="activity-row"><div class="activity-icon">⇄</div><div><div class="activity-title">AWS Systems Manager</div><div class="activity-desc">Runs remote deployment commands</div></div></div>
        <div class="activity-row"><div class="activity-icon">♢</div><div><div class="activity-title">GitHub OIDC</div><div class="activity-desc">Federated authentication to AWS</div></div></div>
      </div>
    </div>
    <div class="card" id="stack">
      <div class="metric-top"><strong style="font:600 14px 'Space Grotesk'">Technology stack</strong><span style="font-size:10px;color:var(--muted)">Core tools</span></div>
      <div class="stack" style="margin-top:20px">
        <span>Python</span><span>Flask</span><span>Pytest</span>
        <span>GitHub Actions</span><span>Docker</span><span>Docker Hub</span>
        <span>AWS EC2</span><span>Amazon ECR</span><span>AWS IAM</span>
        <span>AWS SSM</span><span>SonarQube</span><span>Linux</span>
      </div>
      <div style="border-top:1px solid var(--line);margin-top:23px;padding-top:17px">
        <div style="font-size:11px;color:var(--muted)">Application health endpoint</div>
        <div style="font-size:12px;color:var(--cyan);margin-top:8px">/health <span class="good">● Available</span></div>
      </div>
    </div>
  </section>
  <div class="footer">CLOUDFLOW · CLOUD CI/CD PLATFORM · BUILT FOR AUTOMATED DELIVERY</div>
</main>
</div>
<script>
function updateClock() {
  const now = new Date();
  document.getElementById('clock').textContent =
    now.toLocaleString(undefined,{dateStyle:'medium',timeStyle:'short'});
}
updateClock();
setInterval(updateClock,30000);
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(DASHBOARD)

@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "version": "1.0.0"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
