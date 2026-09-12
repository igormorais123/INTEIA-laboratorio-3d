import * as THREE from 'three';
import {aerodynamicTest} from './aero-physics.mjs';
export function createWindTunnel({scene,model,mechanics,reduced}) {
  const $=id=>document.getElementById(id);
  const root=new THREE.Group();root.name='INTEIA Wind Tunnel - illustrative tracers';scene.add(root);root.visible=false;
  const bounds=new THREE.Box3().setFromObject(model),size=bounds.getSize(new THREE.Vector3()),center=bounds.getCenter(new THREE.Vector3());
  const count=1700,points=new Float32Array(count*6),geometry=new THREE.BufferGeometry();
  geometry.setAttribute('position',new THREE.BufferAttribute(points,3).setUsage(THREE.DynamicDrawUsage));
  const streaks=new THREE.LineSegments(geometry,new THREE.LineBasicMaterial({color:0x299ba6,transparent:true,opacity:.52,depthWrite:false}));streaks.frustumCulled=false;root.add(streaks);
  const wire=new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.BoxGeometry(size.x+3,size.y+2,size.z+5)),new THREE.LineBasicMaterial({color:0x748a91,transparent:true,opacity:.18}));wire.position.copy(center);wire.position.y=(size.y+2)/2;root.add(wire);
  const dragArrow=new THREE.ArrowHelper(new THREE.Vector3(0,0,-1),new THREE.Vector3(0,size.y+1,0),1,0xe69b27,.22,.12);
  const downArrow=new THREE.ArrowHelper(new THREE.Vector3(0,-1,0),new THREE.Vector3(0,size.y+1,0),1,0x975de2,.22,.12);root.add(dragArrow,downArrow);
  let enabled=false,phase=0,result=null,example=false,lastInvalid=null;
  const ids=['air-speed','air-headwind','air-crosswind','air-temp','air-pressure','air-area','air-cd','air-cl'];
  const number=id=>$(id).value.trim()===''?null:Number($(id).value);
  const params=()=>({speedKmh:number('air-speed'),headwindKmh:number('air-headwind'),crosswindKmh:number('air-crosswind'),temperatureC:number('air-temp'),pressureKPa:number('air-pressure'),area:number('air-area'),cd:number('air-cd'),clDown:number('air-cl'),length:size.z});
  const fmt=(v,d=0)=>v===null?'—':v.toLocaleString('pt-BR',{maximumFractionDigits:d,minimumFractionDigits:d});
  function calculate(){
    const p=params();
    try{result=aerodynamicTest(p);}catch{result=null;}
    $('air-speed-value').textContent=p.speedKmh+' km/h';$('air-cross-value').textContent=p.crosswindKmh+' km/h';$('air-head-value').textContent=p.headwindKmh+' km/h';
    const r=result,invalid=mechanics.amount>.001||mechanics.target>.001||!mechanics.motionAvailable||mechanics.isolated;
    $('air-q').textContent=r?fmt(r.q)+' Pa':'—';$('air-rho').textContent=r?fmt(r.rho,3)+' kg/m³':'—';
    $('air-relative').textContent=r?fmt(r.speed*3.6,1)+' km/h':'—';$('air-yaw').textContent=r?fmt(r.yawDeg,1)+'°':'—';
    $('air-re').textContent=r?fmt(r.reynolds/1e6,2)+' milhões':'—';$('air-mach').textContent=r?fmt(r.mach,3):'—';
    const allowed=r?.validCoefficients&&!invalid&&r.withinIncompressibleRange;
    $('air-drag').textContent=allowed?fmt(r.drag)+' N':'—';$('air-down').textContent=allowed?fmt(r.downforce)+' N':'—';
    $('air-power').textContent=allowed?fmt(r.airPower/1000,1)+' kW':'—';
    $('air-export').disabled=!allowed;
    $('air-warning').textContent=!r?'Preencha temperatura e pressão válidas.':invalid?'Monte todas as peças e saia do isolamento para calcular forças.':!r.withinIncompressibleRange?'Mach ≥ 0,3: fora da faixa deste modelo incompressível.':!r.validCoefficients?'Informe área, Cd e C↓ medidos, ou carregue o exemplo didático.':example?'EXEMPLO DIDÁTICO: área e coeficientes hipotéticos, não medidos neste carro.':'Coeficientes informados pelo usuário; precisão depende da origem e da condição de ensaio.';
    $('air-hud-values').textContent=enabled?(allowed?`${fmt(r.speed*3.6)} km/h · Arrasto ${fmt(r.drag)} N · Carga ${fmt(r.downforce)} N`:`${r?fmt(r.speed*3.6):'—'} km/h · forças indisponíveis`):'';
    dragArrow.visible=downArrow.visible=!!allowed&&r.speed>0;
    if(allowed&&r.speed>0){dragArrow.setDirection(new THREE.Vector3(r.lateral,0,-r.axial).normalize());dragArrow.setLength(Math.max(.1,Math.min(2.4,r.drag/3000)),.18,.09);downArrow.setLength(Math.max(.1,Math.min(2.4,r.downforce/5000)),.18,.09);}
    drawChart(p,allowed);lastInvalid=invalid;
  }
  function drawChart(p,allowed){
    const canvas=$('air-chart'),ctx=canvas.getContext('2d'),w=canvas.width,h=canvas.height;ctx.clearRect(0,0,w,h);
    ctx.strokeStyle='#92999b';ctx.beginPath();ctx.moveTo(34,12);ctx.lineTo(34,h-26);ctx.lineTo(w-12,h-26);ctx.stroke();
    ctx.fillStyle='#85898b';ctx.font='11px sans-serif';ctx.fillText('0',18,h-10);ctx.fillText('300 km/h',w-65,h-10);
    if(!allowed){ctx.fillText('Forneça coeficientes para gerar a curva',42,60);return;}
    const data=Array.from({length:61},(_,i)=>aerodynamicTest({...p,speedKmh:i*5}));
    const max=Math.max(1,...data.filter(r=>r.withinIncompressibleRange).map(r=>Math.max(r.drag,r.downforce)));
    ctx.fillText(fmt(max/1000,1)+' kN',38,12);
    for(const [field,color] of [['drag','#c58212'],['downforce','#985ed3']]){ctx.strokeStyle=color;ctx.lineWidth=2;ctx.beginPath();let started=false;data.forEach((r,i)=>{if(!r.withinIncompressibleRange){started=false;return;}const x=34+i/60*(w-48),y=h-26-r[field]/max*(h-48);started?ctx.lineTo(x,y):ctx.moveTo(x,y);started=true;});ctx.stroke();}
  }
  ids.forEach(id=>$(id).addEventListener('input',()=>{if(['air-area','air-cd','air-cl'].includes(id))example=false;calculate();}));
  $('air-example').onclick=()=>{example=true;$('air-area').value=1.5;$('air-cd').value=.9;$('air-cl').value=3;calculate();};
  $('air-reset').onclick=()=>{example=false;for(const id of ['air-area','air-cd','air-cl'])$(id).value='';$('air-speed').value=150;$('air-headwind').value=0;$('air-crosswind').value=0;$('air-temp').value=15;$('air-pressure').value=101.325;calculate();};
  $('wind-toggle').onclick=()=>{enabled=!enabled;root.visible=enabled;$('air-panel').hidden=!enabled;$('air-hud').hidden=!enabled;$('wind-toggle').setAttribute('aria-pressed',String(enabled));calculate();};
  $('air-export').onclick=()=>{
    if($('air-export').disabled)return;
    const p=params();const rows=['# INTEIA: modelo por coeficientes; nao e CFD','# origem_coeficientes='+ (example?'exemplo_hipotetico':'usuario_nao_validado'),`# area_m2=${p.area};Cd=${p.cd};Cdown=${p.clDown};temperature_C=${p.temperatureC};pressure_kPa=${p.pressureKPa};headwind_kmh=${p.headwindKmh};crosswind_kmh=${p.crosswindKmh}`,'speed_car_kmh,relative_kmh,yaw_deg,rho_kg_m3,q_Pa,drag_N,downforce_N,air_power_W,mach,within_model'];
    for(let v=0;v<=300;v+=10){const r=aerodynamicTest({...p,speedKmh:v}),valid=r.withinIncompressibleRange;rows.push([v,r.speed*3.6,r.yawDeg,r.rho,r.q,valid?r.drag:'',valid?r.downforce:'',valid?r.airPower:'',r.mach,valid].join(','));}
    const url=URL.createObjectURL(new Blob([rows.join('\n')],{type:'text/csv;charset=utf-8'})),a=document.createElement('a');a.href=url;a.download='INTEIA-ensaio-aerodinamico.csv';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
  };
  calculate();
  return {update(dt){
    if(!enabled)return;
    const invalid=mechanics.amount>.001||mechanics.target>.001||!mechanics.motionAvailable||mechanics.isolated;
    if(invalid!==lastInvalid)calculate();
    const r=result;if(!r)return;
    streaks.visible=!invalid&&r.speed>0;
    if(invalid)return;
    // Analytic illustrative paths around an envelope, not a solved velocity/pressure field.
    if(!reduced.matches)phase+=dt*r.speed*.018;
    const yaw=r.yawDeg*Math.PI/180,cz=Math.cos(yaw),sx=Math.sin(yaw),len=size.z+5;
    for(let i=0;i<count;i++){
      const lane=i%85,seed=Math.floor(i/85),baseX=((lane%17)/16-.5)*(size.x+2.4),baseY=.12+Math.floor(lane/17)/4*(size.y+1.5);
      for(let end=0;end<2;end++){
        const z=len/2-(((seed/20+phase+end*.009)%1+1)%1)*len;
        const near=Math.exp(-(((z-center.z)/(size.z*.43))**4)),low=Math.exp(-baseY/(size.y*.8));
        const x=baseX+Math.sign(baseX||.01)*near*low*.48;
        const y=baseY+near*Math.exp(-((baseX/(size.x*.6))**2))*.55;
        const at=i*6+end*3;points[at]=x*cz-z*sx;points[at+1]=y;points[at+2]=z*cz+x*sx;
      }
    }
    geometry.attributes.position.needsUpdate=true;
  }};
}
