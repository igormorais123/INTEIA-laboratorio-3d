const fs = require('node:fs');
const path = require('node:path');
const esbuild = require('esbuild');

const root = __dirname;
const source = (...parts) => path.join(root, ...parts);

function replaceRequired(template, marker, value) {
  const occurrences = template.split(marker).length - 1;
  if (occurrences !== 1) {
    throw new Error(`Marcador ${marker} esperado uma vez; encontrado ${occurrences}.`);
  }
  // Função de substituição: o código minificado contém padrões como `$&` que o replace por string interpretaria.
  return template.replace(marker, () => value);
}

const bundle = esbuild.buildSync({
  entryPoints: [source('src', 'app-v2.js')],
  bundle: true,
  minify: true,
  format: 'iife',
  write: false,
}).outputFiles[0].text;

const template = fs.readFileSync(source('src', 'template-v2.html'), 'utf8');
const model = fs.readFileSync(source('assets', 'carro-aula-v2.glb')).toString('base64');
const withModel = replaceRequired(template, '__MODEL__', model);
const html = replaceRequired(withModel, '__APP__', bundle.replace(/<\/script/gi, '<\\/script'));

fs.writeFileSync(source('index.html'), html);
