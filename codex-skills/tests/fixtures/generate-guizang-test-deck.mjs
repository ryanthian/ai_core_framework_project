#!/usr/bin/env node
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const workspace = resolve(here, '../../..');
const skillRoot = resolve(workspace, 'codex-skills/third-party/guizang-ppt-skill');
const outputDir = resolve(workspace, 'codex-skills/tests/fixtures/guizang-ppt');
const outputFile = resolve(outputDir, 'index.html');

const template = readFileSync(resolve(skillRoot, 'assets/template-swiss.html'), 'utf8');

const slides = `
<section class="slide accent" data-layout="SWISS-COVER-ASCII" data-animate="hero" data-slide-id="title">
  <div class="canvas-card">
    <canvas class="ascii-bg" aria-hidden="true"></canvas>
    <div class="chrome-min"><div class="l">AI WORKFLOW</div><div class="r">TEST · 01 / 05</div></div>
    <div style="flex:1;padding:0;display:grid;grid-template-rows:auto 1fr auto;gap:2.6vh">
      <div data-anim="kicker" class="t-meta" style="color:rgba(255,255,255,.78);letter-spacing:.22em">PHASE 1 SKILL TEST</div>
      <h1 data-anim="title" style="align-self:center;font-family:var(--sans),var(--sans-zh);font-weight:200;font-size:min(9.6vw,16vh);line-height:.94;letter-spacing:-.025em;color:#fff">AI-Assisted<br/>Software Development</h1>
      <div data-anim="bottom" style="border-top:1px solid rgba(255,255,255,.22);padding-top:2vh">
        <div class="lead" style="max-width:56ch;color:rgba(255,255,255,.86)">A small deck proving the Guizang skill can generate and validate a reusable HTML presentation.</div>
      </div>
    </div>
  </div>
</section>

<section class="slide" data-layout="S03" data-animate="statement" data-slide-id="problem">
  <div class="canvas-card">
    <div class="chrome-min"><div class="l">PROBLEM</div><div class="r">02 / 05</div></div>
    <div style="margin:auto 0;display:grid;gap:3vh;max-width:76ch">
      <div class="t-meta" style="letter-spacing:.22em;color:var(--accent)">WHERE AGENTS DRIFT</div>
      <h2 class="h-statement">Work gets risky when output looks finished before evidence exists.</h2>
      <p class="lead">The failure mode is not lack of effort. It is skipping the proof step.</p>
    </div>
  </div>
</section>

<section class="slide" data-layout="S03" data-animate="statement" data-slide-id="workflow">
  <div class="canvas-card">
    <div class="chrome-min"><div class="l">WORKFLOW</div><div class="r">03 / 05</div></div>
    <div style="margin:auto 0;display:grid;gap:3vh;max-width:80ch">
      <div class="t-meta" style="letter-spacing:.22em;color:var(--accent)">OPERATING LOOP</div>
      <h2 class="h-statement">Understand → inspect → select skills → plan → implement.</h2>
      <p class="lead">The loop is intentionally simple so it survives across projects.</p>
    </div>
  </div>
</section>

<section class="slide" data-layout="S03" data-animate="statement" data-slide-id="verification">
  <div class="canvas-card">
    <div class="chrome-min"><div class="l">VERIFICATION</div><div class="r">04 / 05</div></div>
    <div style="margin:auto 0;display:grid;gap:3vh;max-width:80ch">
      <div class="t-meta" style="letter-spacing:.22em;color:var(--accent)">EVIDENCE GATE</div>
      <h2 class="h-statement">A claim is only accepted after the command, artifact, or readback proves it.</h2>
      <p class="lead">This is the boundary between a nice-looking report and an auditable system.</p>
    </div>
  </div>
</section>

<section class="slide split" data-layout="SWISS-CLOSING-ASCII" data-animate="split-statement" data-slide-id="conclusion">
  <div class="canvas-card">
    <div class="split-half">
      <div class="half b-accent" style="padding:5.6vh 3.6vw 4.4vh;justify-content:space-between;position:relative;overflow:hidden">
        <canvas class="ascii-bg" aria-hidden="true"></canvas>
        <div class="chrome-min" style="position:relative;z-index:1"><div class="l">05 / 05</div><div class="r">CONCLUSION</div></div>
        <div style="position:relative;z-index:1;display:grid;gap:2vh">
          <div class="t-meta" style="color:rgba(255,255,255,.78);letter-spacing:.22em">TAKEAWAY</div>
          <h2 style="font-family:var(--sans),var(--sans-zh);font-size:min(6.6vw,12vh);line-height:.94;font-weight:200;color:#fff">Reusable skills need reusable proof.</h2>
        </div>
      </div>
      <div class="half" style="padding:5.6vh 3.6vw 4.4vh;justify-content:center">
        <div style="display:grid;gap:2.2vh">
          <p class="lead">Pin the source.</p>
          <p class="lead">Run the validator.</p>
          <p class="lead">Keep rollback close.</p>
        </div>
      </div>
    </div>
  </div>
</section>`;

const notes = `const SPEAKER_NOTES = [
  { id: 'title', title: 'AI-Assisted Software Development', section: 'Opening', minutes: 0.5, purpose: 'Introduce the workflow test deck.', talk: ['State that this is a contained verification deck.', 'Name the objective: reusable proof.', 'Set expectation that the deck validates tooling, not content strategy.'], transition: 'Move from the test title into the problem.' },
  { id: 'problem', title: 'Problem', section: 'Context', minutes: 0.7, purpose: 'Explain why verification matters.', talk: ['Describe the gap between output and evidence.', 'Make clear that polished docs are not enough.', 'Frame verification as an engineering boundary.'], transition: 'Move from risk to the workflow that reduces it.' },
  { id: 'workflow', title: 'Workflow', section: 'Method', minutes: 0.8, purpose: 'Show the operating loop.', talk: ['Read the workflow as a sequence.', 'Emphasize skill selection as a decision, not a ritual.', 'Connect planning to smaller implementation surfaces.'], transition: 'Move from workflow to proof.' },
  { id: 'verification', title: 'Verification', section: 'Method', minutes: 0.8, purpose: 'Define the evidence gate.', talk: ['Name the proof artifact before claiming success.', 'Run the command or inspect the output.', 'Report failures plainly.'], transition: 'Move from verification to the closing rule.' },
  { id: 'conclusion', title: 'Conclusion', section: 'Close', minutes: 0.5, purpose: 'Leave one memorable operating rule.', talk: ['Repeat that skills need proof.', 'Point to source lock, validator, and rollback.', 'Close without implying AI-Core is next.'], transition: 'End of test deck.' }
];`;

const slideStart = template.indexOf('<!-- ============================================================\n     SLIDES 插入区');
const slideEnd = template.indexOf('\n</div>\n\n<div id="nav"></div>', slideStart);
if (slideStart < 0 || slideEnd < 0) throw new Error('Cannot locate slide insertion region.');

let html = `${template.slice(0, slideStart)}${slides}${template.slice(slideEnd)}`;
html = html.replace(/const SPEAKER_NOTES = \[[\s\S]*?\];/, notes);
html = html.replace('[必填] 替换为 PPT 标题 · Deck Title', 'AI-Assisted Software Development Workflow');

mkdirSync(outputDir, { recursive: true });
writeFileSync(outputFile, html, 'utf8');
console.log(`Generated ${outputFile}`);
