import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const expectedPages = [
  'site/index.html',
  'site/learn/index.html',
  'site/learn/concepts.html',
  'site/interview/index.html',
  'site/interview/questions.html'
];
const sharedScript = 'site/assets/js/site-search.js';
const failures = [];

const requireFile = file => {
  if (!fs.existsSync(path.join(root, file))) failures.push(`Missing required file: ${file}`);
};

expectedPages.forEach(requireFile);
requireFile(sharedScript);

const isExternal = href => /^(?:[a-z][a-z0-9+.-]*:|\/\/)/i.test(href);
for (const page of expectedPages) {
  const sourcePath = path.join(root, page);
  if (!fs.existsSync(sourcePath)) continue;
  const source = fs.readFileSync(sourcePath, 'utf8');
  const hrefPattern = /\bhref\s*=\s*(["'])(.*?)\1/gms;
  for (const match of source.matchAll(hrefPattern)) {
    const href = match[2].trim();
    const localPath = href.split(/[?#]/, 1)[0];
    if (!localPath || isExternal(localPath) || !localPath.endsWith('.html')) continue;
    const target = path.resolve(path.dirname(sourcePath), localPath);
    if (!fs.existsSync(target)) failures.push(`${page} links to missing file: ${href}`);
  }

  const scriptPattern = /<script\b([^>]*)>([\s\S]*?)<\/script>/gi;
  for (const match of source.matchAll(scriptPattern)) {
    if (/\bsrc\s*=/i.test(match[1]) || !match[2].trim()) continue;
    try {
      new Function(match[2]);
    } catch (error) {
      failures.push(`${page} has invalid inline JavaScript: ${error.message}`);
    }
  }
}

if (fs.existsSync(path.join(root, sharedScript))) {
  try {
    new Function(fs.readFileSync(path.join(root, sharedScript), 'utf8'));
  } catch (error) {
    failures.push(`${sharedScript} has invalid JavaScript: ${error.message}`);
  }
}

if (failures.length) {
  console.error('Site check failed:');
  failures.forEach(failure => console.error(`- ${failure}`));
  process.exit(1);
}

console.log(`Site check passed: ${expectedPages.length} HTML pages, local links, and scripts are valid.`);
