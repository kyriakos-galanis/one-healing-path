import fs from 'node:fs';

process.env.ASTRO_TELEMETRY_DISABLED = '1';

const dirs = [
  'dist/pages/el/therapeftiki-proseggisi',
  'dist/pages/el/item',
  'dist/pages/el/itemlist/category',
  'dist/pages/el/itemlist/tag',
  'dist/pages/el/itemlist/user',
  'dist/pages/el/istologio'
];

for (const d of dirs) {
  try {
    fs.mkdirSync(d, { recursive: true });
  } catch (e) {}
}

import('./node_modules/astro/astro.js');
