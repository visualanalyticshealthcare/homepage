import fs from 'node:fs';
import path from 'node:path';

const distDir = path.join(process.cwd(), 'dist');

function walk(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const fullPath = path.join(dir, entry.name);

    if (!entry.isDirectory()) {
      continue;
    }

    walk(fullPath);

    if (!entry.name.endsWith('.html')) {
      continue;
    }

    const indexPath = path.join(fullPath, 'index.html');
    if (!fs.existsSync(indexPath)) {
      continue;
    }

    const targetPath = path.join(dir, entry.name);
    const html = fs.readFileSync(indexPath);
    fs.rmSync(fullPath, { recursive: true, force: true });
    fs.writeFileSync(targetPath, html);
  }
}

if (fs.existsSync(distDir)) {
  walk(distDir);
}
