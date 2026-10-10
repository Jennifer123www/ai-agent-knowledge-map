import fs from 'node:fs';
import path from 'node:path';

const root = path.resolve('content/wechat/01-foundation-models-and-inference');
const submoduleDirs = fs.readdirSync(path.join(root, 'submodules'))
  .filter((dir) => fs.statSync(path.join(root, 'submodules', dir)).isDirectory())
  .sort();
const files = [
  ['总览主文', 'beginner-main.md'],
  ['总览副文', 'interview-side.md'],
  ...submoduleDirs.flatMap((dir) => [
    [`${dir} 主文`, path.join('submodules', dir, 'beginner-main.md')],
    [`${dir} 副文`, path.join('submodules', dir, 'interview-side.md')],
  ]),
];

function body(file) {
  let text = fs.readFileSync(path.join(root, file), 'utf8');
  text = text.replace(/^---[\s\S]*?---\s*/, '');
  text = text.split('\n## 参考资料')[0];
  text = text.replace(/!\[[^\]]*\]\([^)]*\)/g, '');
  text = text.replace(/\[([^\]]+)\]\([^)]*\)/g, '$1');
  return text.replace(/\s+/g, '');
}

function longestCommonSubstring(a, b) {
  let best = '';
  const row = new Uint32Array(b.length + 1);
  for (let i = 1; i <= a.length; i += 1) {
    for (let j = b.length; j >= 1; j -= 1) {
      if (a[i - 1] === b[j - 1]) {
        row[j] = row[j - 1] + 1;
        if (row[j] > best.length) best = a.slice(i - row[j], i);
      } else row[j] = 0;
    }
  }
  return best;
}

function shingles(text, size = 18) {
  const result = new Set();
  for (let i = 0; i + size <= text.length; i += 1) result.add(text.slice(i, i + size));
  return result;
}

const content = new Map(files.map(([label, file]) => [label, body(file)]));
const groups = [
  ['总览主文', '总览副文'],
  ...submoduleDirs.map((dir) => [`${dir} 主文`, `${dir} 副文`]),
];
let failed = false;
for (const [left, right] of groups) {
  const a = content.get(left);
  const b = content.get(right);
  const common = longestCommonSubstring(a, b);
  const sa = shingles(a);
  const sb = shingles(b);
  let shared = 0;
  for (const item of sa) if (sb.has(item)) shared += 1;
  const ratio = shared / Math.max(1, Math.min(sa.size, sb.size));
  const expectedIntro = left === '总览主文' || left === '01-llm 主文';
  const substantive = common.length >= 30 || ratio > 0.16;
  console.log(`${left} ↔ ${right}: longest=${common.length}, shingle18=${ratio.toFixed(3)}${expectedIntro ? ' (共享案例开场允许)' : ''}`);
  if (substantive) {
    failed = true;
    console.error(`  potential substantive overlap: ${common.slice(0, 80)}`);
  }
}

if (failed) process.exitCode = 1;
