
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
<title>CloudFlow | DevOps Dashboard</title>

<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">

<style>
:root {
    --bg: #080d19;
    --panel: #101a2c;
    --panel2: #111f34;
    --border: rgba(148,163,184,.13);
    --muted: #8291a9;
    --text: #edf4ff;
    --blue: #55a6ff;
    --cyan: #39d6e8;
    --purple: #a78bfa;
    --green: #43dda0;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
    background:
      radial-gradient(ellipse at 75% 0%, rgba(45,91,180,.18), transparent 40%),
      radial-gradient(ellipse at 0% 55%, rgba(92,55,160,.12), transparent 35%),
      var(--bg);
    color: var(--text);
    font-family: 'DM Sans', sans-serif;
    min-height: 100vh;
}

button { font: inherit; }

.layout { display: flex; min-height: 100vh; }

.sidebar {
    width: 245px;
    position: fixed;
    inset: 0 auto 0 0;
    background: rgba(9,16,30,.94);
    border-right: 1px solid var(--border);
    padding: 28px 19px;
    display: flex;
    flex-direction: column;
    z-index: 5;
}

.logo {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 48px;
    padding: 0 8px;
}

.logo-icon {
    width: 42px;
    height: 42px;
    border-radius: 13px;
    display: grid;
    place-items: center;
    font-size: 19px;
    color: white;
    background: linear-gradient(135deg,#388cff,#7957ee);
    box-shadow: 0 5px 25px #397aff55;
}

.logo-name {
    font: 700 21px 'Space Grotesk';
    letter-spacing: -.7px;
}

.logo-name span { color: var(--blue); }

.nav-label {
    color: #62728c;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1.8px;
    padding: 0 11px;
    margin-bottom: 13px;
}

.nav-item {
    display: flex;
    align-items: center;
    gap: 13px;
    padding: 12px 13px;
    border-radius: 10px;
    color: #9aa9c0;
    font-size: 13px;
    margin-bottom: 5px;
}

.nav-item.active {
    color: #fff;
    background: linear-gradient(90deg,#2869b833,#7557e522);
    border: 1px solid #568eff35;
}

.nav-item.active i { color: #67adff; }
.nav-item i { width: 17px; text-align: center; }

.sidebar-bottom {
    margin-top: auto;
    background: linear-gradient(135deg,#182b48,#151b35);
    border: 1px solid var(--border);
    padding: 16px;
    border-radius: 13px;
}

.sidebar-bottom small { color: var(--muted); }
.sidebar-bottom strong { display: block; margin: 9px 0 4px; font-size: 13px; }

.main {
    margin-left: 245px;
    width: calc(100% - 245px);
    padding: 30px 42px 40px;
    max-width: 1700px;
}

.topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 39px;
}

.breadcrumb { color: var(--muted); font-size: 12px; }
.breadcrumb strong { color: white; font-weight: 600; }

.top-right { display: flex; align-items: center; gap: 15px; }

.live-pill {
    display: flex;
    align-items: center;
    gap: 9px;
    border: 1px solid var(--border);
    background: #111d30;
    padding: 9px 13px;
    border-radius: 30px;
    font-size: 11px;
    color: #b7c6dc;
}

.dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: var(--green);
    box-shadow: 0 0 12px var(--green);
    animation: pulse 1.8s infinite;
}

@keyframes pulse {
    50% { opacity: .4; box-shadow: 0 0 3px var(--green); }
}

.avatar {
    width: 35px;
    height: 35px;
    display: grid;
    place-items: center;
    border-radius: 11px;
    background: linear-gradient(135deg,#397fe5,#9161eb);
    font-weight: 700;
    font-size: 12px;
}

.hero {
    position: relative;
    overflow: hidden;
    border: 1px solid #548aff35;
    border-radius: 20px;
    padding: 34px 37px;
    background:
      radial-gradient(circle at 85% 45%,#4979e52c,transparent 32%),
      linear-gradient(110deg,#152b4b,#141c36 65%,#211d43);
    margin-bottom: 25px;
}

.hero:after {
    content: '';
    position: absolute;
    width: 250px;
    height: 250px;
    right: 4%;
    top: -130px;
    border: 1px solid #77aaff20;
    border-radius: 50%;
    box-shadow: 0 0 0 30px #77aaff08,0 0 0 60px #77aaff06;
}

.eyebrow {
    color: #76baff;
    font-size: 10px;
    letter-spacing: 2px;
    font-weight: 800;
    margin-bottom: 14px;
}

.hero h1 {
    font: 700 clamp(29px,4vw,43px) 'Space Grotesk';
    letter-spacing: -1.5px;
    margin-bottom: 11px;
}

.hero h1 span {
    background: linear-gradient(90deg,#63b9ff,#ad91ff);
    -webkit-background-clip: text;
    color: transparent;
}

.hero p {
    max-width: 590px;
    color: #a6b7d0;
    font-size: 13px;
    line-height: 1.8;
}

.hero-footer {
    display: flex;
    gap: 10px;
    margin-top: 23px;
    flex-wrap: wrap;
}

.tag {
    font-size: 10px;
    padding: 7px 11px;
    border-radius: 20px;
    color: #c5d8f6;
    background: #ffffff0c;
    border: 1px solid #ffffff16;
}

.section-heading {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 29px 0 15px;
}

.section-heading h2 {
    font: 600 17px 'Space Grotesk';
}

.section-heading span {
    color: var(--muted);
    font-size: 11px;
}

.metrics {
    display: grid;
    grid-template-columns: repeat(4,minmax(0,1fr));
    gap: 14px;
}

.card {
    background: linear-gradient(145deg,#111e32,#101827);
    border: 1px solid var(--border);
    border-radius: 15px;
    padding: 19px;
    transition: .25s ease;
}

.card:hover {
    transform: translateY(-4px);
    border-color: #6a9bff55;
    box-shadow: 0 12px 35px #0004;
}

.metric-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.metric-icon {
    width: 36px;
    height: 36px;
    display: grid;
    place-items: center;
    border-radius: 10px;
    background: #4d8eff19;
    color: #76b7ff;
}

.metric-label { color: var(--muted); font-size: 11px; margin-top: 16px; }
.metric-value { font: 700 25px 'Space Grotesk'; margin-top: 5px; }
.metric-note { color: #72839c; font-size: 10px; margin-top: 7px; }

.good { color: var(--green); }
.blue { color: var(--blue); }

.content-grid {
    display: grid;
    grid-template-columns: 1.45fr 1fr;
    gap: 17px;
    margin-top: 17px;
}

.panel {
    background: linear-gradient(145deg,#111e32,#0e1727);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 22px;
    min-width: 0;
}

.panel-title {
    font: 600 15px 'Space Grotesk';
}

.panel-subtitle {
    color: var(--muted);
    font-size: 10px;
    margin-top: 5px;
}

.pipeline {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 5px;
    margin-top: 35px;
}

.stage {
    min-width: 0;
    text-align: center;
    flex: 1;
}

.stage-icon {
    width: 46px;
    height: 46px;
    border: 1px solid #609cff35;
    background: #347bd21a;
    border-radius: 13px;
    display: grid;
    place-items: center;
    color: #80b9ff;
    font-size: 17px;
    margin: auto;
}

.stage:nth-of-type(3) .stage-icon { color: var(--purple); background: #9671e51b; }
.stage:nth-of-type(5) .stage-icon { color: var(--cyan); background: #39d6e81a; }
.stage:nth-of-type(7) .stage-icon { color: var(--green); background: #43dda01a; }

.stage-name {
    font-size: 10px;
    font-weight: 600;
    margin-top: 11px;
    white-space: nowrap;
}

.stage-caption {
    color: var(--muted);
    font-size: 9px;
    margin-top: 4px;
}

.arrow {
    color: #607b9e;
    font-size: 12px;
    flex-shrink: 0;
    margin-top: -27px;
}

.pipeline-note {
    margin-top: 26px;
    padding: 12px;
    border-radius: 9px;
    background: #1c3150;
    color: #9fb9dc;
    font-size: 10px;
    line-height: 1.7;
}

.quality {
    display: flex;
    align-items: center;
    gap: 22px;
    margin: 27px 0 20px;
}

.ring {
    width: 112px;
    height: 112px;
    flex-shrink: 0;
    border-radius: 50%;
    display: grid;
    place-items: center;
    background: conic-gradient(var(--green) 0% 90%,#293b50 90% 100%);
    position: relative;
}

.ring:before {
    content: '';
    position: absolute;
    inset: 8px;
    background: #101a2c;
    border-radius: 50%;
}

.ring-text { position: relative; text-align: center; }
.ring-text strong { display: block; font: 700 24px 'Space Grotesk'; }
.ring-text span { color: var(--muted); font-size: 9px; }

.quality-copy strong { font-size: 13px; }
.quality-copy p { color: var(--muted); font-size: 10px; line-height: 1.8; margin-top: 8px; }

.stack {
    display: grid;
    grid-template-columns: repeat(3,minmax(0,1fr));
    gap: 12px;
    margin-top: 16px;
}

.tech {
    background: #111d30;
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 17px 14px;
}

.tech i { font-size: 19px; color: #78b6ff; }
.tech strong { display: block; font-size: 12px; margin-top: 12px; }
.tech span { display: block; color: var(--muted); font-size: 10px; margin-top: 5px; }

.footer {
    border-top: 1px solid var(--border);
    margin-top: 34px;
    padding-top: 20px;
    display: flex;
    justify-content: space-between;
    color: #6d7f99;
    font-size: 10px;
    gap: 10px;
}

@media(max-width:1100px) {
    .metrics { grid-template-columns: repeat(2,1fr); }
    .content-grid { grid-template-columns: 1fr; }
}

@media(max-width:700px) {
    .sidebar { display: none; }
    .main { margin-left: 0; width: 100%; padding: 20px 15px; }
    .topbar { margin-bottom: 23px; }
    .hero { padding: 25px 21px; }
    .hero h1 { font-size: 31px; }
    .pipeline { flex-wrap: wrap; row-gap: 25px; }
    .stage { flex: 0 0 27%; }
    .arrow { display: none; }
    .stack { grid-template-columns: repeat(2,1fr); }
    .footer { flex-direction: column; }
}
</style>
</head>

<body>
<div class="layout">

<aside class="sidebar">
    <div class="logo">
        <div class="logo-icon"><i class="fa-solid fa-cloud-bolt"></i></div>
        <div class="logo-name">Cloud<span>Flow</span></div>
    </div>

    <div class="nav-label">WORKSPACE</div>
    <div class="nav-item active"><i class="fa-solid fa-grid-2"></i> Overview</div>
    <div class="nav-item"><i class="fa-solid fa-diagram-project"></i> CI/CD Pipeline</div>
    <div class="nav-item"><i class="fa-brands fa-docker"></i> Containers</div>
    <div class="nav-item"><i class="fa-solid fa-cloud"></i> Infrastructure</div>

    <div class="nav-label" style="margin-top:30px">OBSERVABILITY</div>
    <div class="nav-item"><i class="fa-solid fa-chart-line"></i> Monitoring</div>
    <div class="nav-item"><i class="fa-solid fa-shield-halved"></i> Code Quality</div>
    <div class="nav-item"><i class="fa-solid fa-terminal"></i> Logs</div>

    <div class="sidebar-bottom">
        <small>PROJECT STATUS</small>
        <strong><i class="fa-solid fa-circle-check good"></i> Pipeline configured</strong>
        <small>Automated cloud deployment</small>
    </div>
</aside>

<main class="main">

<header class="topbar">
    <div class="breadcrumb">Workspace &nbsp;/&nbsp; <strong>Overview</strong></div>
    <div class="top-right">
        <div class="live-pill"><span class="dot" id="health-dot"></span><span id="health-label">Checking system...</span></div>
        <div class="avatar">CF</div>
    </div>
</header>

<section class="hero">
    <div class="eyebrow">CLOUD INFRASTRUCTURE PLATFORM</div>
    <h1>Build. Deploy. <span>Automate.</span></h1>
    <p>
        Your cloud delivery command center. Build applications, automate
        deployments, monitor code quality, and deliver software through
        a streamlined CI/CD workflow.
    </p>
    <div class="hero-footer">
        <span class="tag"><i class="fa-brands fa-github"></i> GitHub Actions</span>
        <span class="tag"><i class="fa-brands fa-docker"></i> Docker</span>
        <span class="tag"><i class="fa-brands fa-aws"></i> AWS Cloud</span>
        <span class="tag"><i class="fa-solid fa-shield-halved"></i> Quality Analysis</span>
    </div>
</section>

<div class="section-heading">
    <h2>Platform Overview</h2>
    <span>Project architecture & technology stack</span>
</div>

<section class="metrics">
    <div class="card">
        <div class="metric-top"><div class="metric-icon"><i class="fa-brands fa-github"></i></div><i class="fa-solid fa-arrow-up-right-from-square muted"></i></div>
        <div class="metric-label">CI/CD AUTOMATION</div>
        <div class="metric-value">Enabled</div>
        <div class="metric-note"><span class="good">●</span> GitHub Actions workflow</div>
    </div>

    <div class="card">
        <div class="metric-top"><div class="metric-icon"><i class="fa-brands fa-docker"></i></div></div>
        <div class="metric-label">CONTAINERIZATION</div>
        <div class="metric-value">Docker</div>
        <div class="metric-note">Image build & registry push</div>
    </div>

    <div class="card">
        <div class="metric-top"><div class="metric-icon"><i class="fa-brands fa-aws"></i></div></div>
        <div class="metric-label">CLOUD DEPLOYMENT</div>
        <div class="metric-value">AWS</div>
        <div class="metric-note">Amazon ECR & EC2</div>
    </div>

    <div class="card">
        <div class="metric-top"><div class="metric-icon"><i class="fa-solid fa-chart-pie"></i></div></div>
        <div class="metric-label">TEST COVERAGE</div>
        <div class="metric-value">90%</div>
        <div class="metric-note"><span class="good">●</span> Reported by SonarQube</div>
    </div>
</section>

<section class="content-grid">

    <div class="panel">
        <div class="panel-title">Deployment Workflow</div>
        <div class="panel-subtitle">The automated delivery path configured in this project</div>

        <div class="pipeline">
            <div class="stage">
                <div class="stage-icon"><i class="fa-brands fa-github"></i></div>
                <div class="stage-name">Git Push</div>
                <div class="stage-caption">Source code</div>
            </div>
            <div class="arrow"><i class="fa-solid fa-chevron-right"></i></div>
            <div class="stage">
                <div class="stage-icon"><i class="fa-solid fa-vial"></i></div>
                <div class="stage-name">Pytest</div>
                <div class="stage-caption">Testing</div>
            </div>
            <div class="arrow"><i class="fa-solid fa-chevron-right"></i></div>
            <div class="stage">
                <div class="stage-icon"><i class="fa-solid fa-shield-halved"></i></div>
                <div class="stage-name">SonarQube</div>
                <div class="stage-caption">Quality</div>
            </div>
            <div class="arrow"><i class="fa-solid fa-chevron-right"></i></div>
            <div class="stage">
                <div class="stage-icon"><i class="fa-brands fa-docker"></i></div>
                <div class="stage-name">Docker</div>
                <div class="stage-caption">Build image</div>
            </div>
            <div class="arrow"><i class="fa-solid fa-chevron-right"></i></div>
            <div class="stage">
                <div class="stage-icon"><i class="fa-brands fa-aws"></i></div>
                <div class="stage-name">AWS EC2</div>
                <div class="stage-caption">Deployment</div>
            </div>
        </div>

        <div class="pipeline-note">
            <i class="fa-solid fa-circle-info"></i>
            Workflow overview: GitHub Actions coordinates testing, quality analysis,
            container publishing and AWS deployment.
        </div>
    </div>

    <div class="panel">
        <div class="panel-title">Code Quality</div>
        <div class="panel-subtitle">Latest reported SonarQube coverage</div>

        <div class="quality">
            <div class="ring">
                <div class="ring-text"><strong>90%</strong><span>Coverage</span></div>
            </div>
            <div class="quality-copy">
                <strong>Test coverage report</strong>
                <p>Measured using pytest-cov and imported into SonarQube Cloud.</p>
            </div>
        </div>
        <div class="metric-note"><i class="fa-solid fa-check-circle good"></i> 2 tests passed in the reported run</div>
    </div>
</section>

<div class="section-heading">
    <h2>Technology Stack</h2>
    <span>Tools powering the platform</span>
</div>

<section class="stack">
    <div class="tech"><i class="fa-brands fa-github"></i><strong>GitHub Actions</strong><span>CI/CD automation</span></div>
    <div class="tech"><i class="fa-brands fa-docker"></i><strong>Docker</strong><span>Containerization</span></div>
    <div class="tech"><i class="fa-brands fa-aws"></i><strong>Amazon ECR</strong><span>Image registry</span></div>
    <div class="tech"><i class="fa-solid fa-server"></i><strong>Amazon EC2</strong><span>Application hosting</span></div>
    <div class="tech"><i class="fa-solid fa-chart-line"></i><strong>SonarQube</strong><span>Code quality analysis</span></div>
    <div class="tech"><i class="fa-solid fa-lock"></i><strong>AWS OIDC</strong><span>Secure authentication</span></div>
</section>

<footer class="footer">
    <span>© 2026 CloudFlow · Cloud CI/CD Platform</span>
    <span>Built with Flask · Powered by AWS</span>
</footer>

</main>
</div>

<script>
async function checkHealth() {
    const label = document.getElementById("health-label");
    const dot = document.getElementById("health-dot");

    try {
        const response = await fetch("/health");
        const data = await response.json();

        if (response.ok && data.status === "healthy") {
            label.textContent = "Application Healthy";
            dot.style.background = "#43dda0";
            dot.style.boxShadow = "0 0 12px #43dda0";
        } else {
            throw new Error("Unhealthy");
        }
    } catch (error) {
        label.textContent = "Application Offline";
        dot.style.background = "#ff657a";
        dot.style.boxShadow = "0 0 12px #ff657a";
    }
}

checkHealth();
setInterval(checkHealth, 15000);
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
