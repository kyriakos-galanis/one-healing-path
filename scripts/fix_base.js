import fs from 'node:fs';
import path from 'node:path';

// 1. Determine base from astro.config.mjs
const configText = fs.readFileSync('astro.config.mjs', 'utf-8');
const baseMatch = configText.match(/base:\s*['"]([^'"]+)['"]/);
let base = baseMatch ? baseMatch[1].trim() : '';

// Normalize base (e.g. '/one-healing-path')
if (base === '/') {
  base = '';
} else if (base.endsWith('/')) {
  base = base.slice(0, -1);
}

if (!base) {
  console.log('[fix_base] Base is root ("/") - no path rewriting needed.');
  process.exit(0);
}

console.log(`[fix_base] Rewriting asset and page links with base: "${base}"`);

const distDir = path.resolve('dist');

function walk(dir) {
  let results = [];
  const list = fs.readdirSync(dir);
  for (const file of list) {
    const fullPath = path.join(dir, file);
    const stat = fs.statSync(fullPath);
    if (stat && stat.isDirectory()) {
      results = results.concat(walk(fullPath));
    } else if (file.endsWith('.html')) {
      results.push(fullPath);
    }
  }
  return results;
}

const htmlFiles = walk(distDir);
let modifiedCount = 0;

for (const filePath of htmlFiles) {
  let content = fs.readFileSync(filePath, 'utf-8');
  const original = content;

  // Replace href="/el...", src="/images...", action="/el...", etc.
  // Targets: /el, /images, /components, /media, /favicon.ico
  content = content.replace(/(href|src|action)=["']\/(el|images|components|media|favicon\.ico)([^"']*)["']/g, (match, attr, prefix, rest) => {
    return `${attr}="${base}/${prefix}${rest}"`;
  });

  // Replace url=/el/ in meta refresh if present
  content = content.replace(/content=["']0;url=\/el\/?["']/g, `content="0;url=${base}/el/"`);
  content = content.replace(/content=["']2;url=\/el\/?["']/g, `content="0;url=${base}/el/"`);

  // Fix canonical link if missing base
  content = content.replace(/(https:\/\/[^/]+)\/el\//g, (match, domain) => {
    if (domain.includes('github.io')) {
      return `${domain}${base}/el/`;
    }
    return match;
  });

  if (content !== original) {
    fs.writeFileSync(filePath, content, 'utf-8');
    modifiedCount++;
  }
}

console.log(`[fix_base] Processed ${htmlFiles.length} files. Rewrote paths in ${modifiedCount} files.`);
