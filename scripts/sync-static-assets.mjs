import fs from 'node:fs';
import path from 'node:path';

const rootDir = process.cwd();
const pairs = [
  ['content/images', 'public/images'],
  ['content/files', 'public/files'],
  ['content/proceedings', 'public/proceedings']
];

for (const [source, target] of pairs) {
  const sourcePath = path.join(rootDir, source);
  const targetPath = path.join(rootDir, target);

  if (!fs.existsSync(sourcePath)) {
    continue;
  }

  fs.rmSync(targetPath, { recursive: true, force: true });
  fs.mkdirSync(path.dirname(targetPath), { recursive: true });
  fs.cpSync(sourcePath, targetPath, { recursive: true });
}
