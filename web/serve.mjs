/** Serve the static build locally; no application backend or dependencies. */
import http from 'node:http';
import { readFile, stat } from 'node:fs/promises';
import { resolve, extname, sep } from 'node:path';
import { fileURLToPath } from 'node:url';
const root=resolve(fileURLToPath(new URL('./dist/client/',import.meta.url)));
const port=Number(process.env.PORT || 5174);
const mime={'.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.css':'text/css; charset=utf-8','.json':'application/json','.glb':'model/gltf-binary','.png':'image/png','.svg':'image/svg+xml','.ico':'image/x-icon','.txt':'text/plain; charset=utf-8','.woff2':'font/woff2'};
const server=http.createServer(async(req,res)=>{
 try{
  if(req.method!=='GET'&&req.method!=='HEAD'){res.writeHead(405);res.end();return;}
  const url=new URL(req.url,'http://localhost');let path=resolve(root,'.'+decodeURIComponent(url.pathname));
  if(!path.startsWith(root.endsWith(sep)?root:root+sep)&&path!==root){res.writeHead(403);res.end();return;}
  if((await stat(path)).isDirectory()){
   if(!url.pathname.endsWith('/')){res.writeHead(308,{'Location':url.pathname+'/'+url.search});res.end();return;}
   path=resolve(path,'index.html');
  }
  const type=mime[extname(path)]||'application/octet-stream';
  const acceptsGzip=String(req.headers['accept-encoding']||'').split(',').some(part=>{const [encoding,...parameters]=part.trim().split(';');const quality=parameters.find(p=>p.trim().startsWith('q='));return encoding==='gzip'&&(!quality||Number(quality.trim().slice(2))>0);});
  let encoding;
  if(extname(path)==='.glb'&&acceptsGzip){try{await stat(path+'.gz');path+='.gz';encoding='gzip';}catch{/* Plain GLB remains a valid fallback. */}}
  const body=await readFile(path);res.writeHead(200,{'Content-Type':type,'Content-Length':body.length,'Cache-Control':'no-cache','X-Content-Type-Options':'nosniff','Vary':'Accept-Encoding',...(encoding?{'Content-Encoding':encoding}:{})});res.end(req.method==='HEAD'?undefined:body);
 }catch{res.writeHead(404,{'Content-Type':'text/plain'});res.end('Not found');}
});
server.listen(port,'127.0.0.1',()=>console.log(`Entrance hall: http://127.0.0.1:${server.address().port}/`));
server.on('error',error=>{console.error(error.message);process.exitCode=1;});
