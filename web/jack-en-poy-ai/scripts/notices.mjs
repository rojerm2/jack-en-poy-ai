import { readdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const directories = readdirSync('node_modules', { withFileTypes: true })
    .filter(entry => entry.isDirectory() && !entry.name.startsWith('.'))
    .flatMap(entry => entry.name.startsWith('@')
        ? readdirSync(join('node_modules', entry.name)).map(name => join('node_modules', entry.name, name))
        : [join('node_modules', entry.name)]);
const notices = ['Third-party license notices', 'These notices come from installed build and runtime dependencies.'];
for (const directory of directories.sort()) {
    for (const entry of readdirSync(directory, { withFileTypes: true })) {
        if (entry.isFile() && /^(license|licence)(\.|$)/i.test(entry.name)) {
            notices.push(`${directory.replace('node_modules/', '')} / ${entry.name}\n${readFileSync(join(directory, entry.name), 'utf8')}`);
        }
    }
}
writeFileSync(join(process.argv[2], 'THIRD_PARTY_NOTICES.txt'), notices.join('\n\n---\n\n') + '\n');
