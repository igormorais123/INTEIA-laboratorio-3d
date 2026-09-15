const fs=require('fs'),esbuild=require('esbuild');
const bundle=esbuild.buildSync({entryPoints:['src/app-v2.js'],bundle:true,minify:true,format:'iife',write:false}).outputFiles[0].text;
const html=fs.readFileSync('src/template-v2.html','utf8').replace('__MODEL__',fs.readFileSync('assets/carro-aula-v2.glb').toString('base64')).replace('__APP__',()=>bundle.replace(/<\/script/gi,'<\\/script'));
fs.writeFileSync('index.html',html);
