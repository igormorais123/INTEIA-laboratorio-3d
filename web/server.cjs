const fs = require('node:fs');
const http = require('node:http');
const path = require('node:path');

const root = path.resolve(__dirname);
const port = Number(process.env.PORT || 5186);
const mimeTypes = new Map([
  ['.glb', 'model/gltf-binary'],
  ['.html', 'text/html; charset=utf-8'],
  ['.js', 'text/javascript; charset=utf-8'],
  ['.json', 'application/json; charset=utf-8'],
  ['.png', 'image/png'],
  ['.svg', 'image/svg+xml'],
  ['.webp', 'image/webp'],
]);

function reply(response, status, body = '') {
  response.writeHead(status, {
    'Content-Type': 'text/plain; charset=utf-8',
    'X-Content-Type-Options': 'nosniff',
  });
  response.end(body);
}

const server = http.createServer((request, response) => {
  if (!['GET', 'HEAD'].includes(request.method)) {
    response.setHeader('Allow', 'GET, HEAD');
    reply(response, 405, 'Método não permitido');
    return;
  }

  let pathname;
  try {
    pathname = decodeURIComponent(new URL(request.url, 'http://localhost').pathname);
  } catch {
    reply(response, 400, 'Endereço inválido');
    return;
  }

  const relativePath = pathname === '/' ? 'index.html' : pathname.replace(/^\/+/, '');
  const file = path.resolve(root, relativePath);
  if (file !== root && !file.startsWith(`${root}${path.sep}`)) {
    reply(response, 403, 'Acesso negado');
    return;
  }

  fs.readFile(file, (error, data) => {
    if (error) {
      reply(response, error.code === 'ENOENT' ? 404 : 500, error.code === 'ENOENT' ? 'Não encontrado' : 'Falha ao ler arquivo');
      return;
    }

    response.writeHead(200, {
      'Content-Type': mimeTypes.get(path.extname(file).toLowerCase()) || 'application/octet-stream',
      'X-Content-Type-Options': 'nosniff',
    });
    response.end(request.method === 'HEAD' ? undefined : data);
  });
});

server.on('error', (error) => {
  console.error(`Falha ao iniciar o servidor: ${error.message}`);
  process.exitCode = 1;
});

server.listen(port, '127.0.0.1', () => {
  console.log(`INTEIA: http://127.0.0.1:${port}`);
});
