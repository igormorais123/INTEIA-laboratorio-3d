/** Original INTEIA identity. Outlined letters retain exact spelling at every size. */
export const glyphs=[
 ['I','M0 0H16V64H0Z',false],
 ['N','M32 64V0H48L78 41V0H94V64H78L48 23V64Z',false],
 ['T','M110 0H174V14H150V64H134V14H110Z',false],
 ['E','M190 0H243V14H206V25H237V39H206V50H243V64H190Z',false],
 ['I','M263 0H279V64H263Z',true],
 ['A','M288 64L312 0H338L363 64H344L339 50H311L306 64ZM316 36H334L325 14Z',true]
];
export const emblem='M16 8H36L20 84H0ZM39 84L75 8H96L117 84H95L91 66H68L60 84ZM77 47H87L83 27Z';
export function brandSVG({light=false,compact=false}={}){
 const ink=light?'#f0f2f3':'#202930',red='#d92135';
 if(compact)return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="-8 0 136 96"><path fill="${red}" fill-rule="evenodd" d="${emblem}"/></svg>`;
 return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 116" role="img" aria-label="INTEIA — Laboratório 3D"><path fill="${red}" fill-rule="evenodd" d="${emblem}" transform="translate(0 8)"/><path d="M141 19V96" stroke="${ink}" stroke-opacity=".22"/><g transform="translate(183 17) skewX(-12)">${glyphs.map(([letter,d,accent])=>`<path data-letter="${letter}" fill="${accent?red:ink}" fill-rule="evenodd" d="${d}"/>`).join('')}</g><text x="174" y="106" font-family="Arial, sans-serif" font-size="14" font-weight="500" letter-spacing="4.5" fill="${ink}">LABORATÓRIO 3D</text></svg>`;
}
export function drawBrand(ctx,width,height,{light=false}={}){
 ctx.clearRect(0,0,width,height);const scale=Math.min(width/640,height/116);ctx.save();ctx.translate((width-640*scale)/2,(height-116*scale)/2);ctx.scale(scale,scale);
 const ink=light?'#f0f2f3':'#202930',red='#d92135';
 ctx.save();ctx.translate(0,8);ctx.fillStyle=red;ctx.fill(new Path2D(emblem),'evenodd');ctx.restore();
 ctx.strokeStyle=light?'#697078':'#adb1b3';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(141,19);ctx.lineTo(141,96);ctx.stroke();
 ctx.save();ctx.translate(183,17);ctx.transform(1,0,-Math.tan(12*Math.PI/180),1,0,0);for(const [,d,accent] of glyphs){ctx.fillStyle=accent?red:ink;ctx.fill(new Path2D(d),'evenodd');}ctx.restore();
 ctx.fillStyle=ink;ctx.font='500 14px Arial';let x=174;for(const c of 'LABORATÓRIO 3D'){ctx.fillText(c,x,106);x+=ctx.measureText(c).width+4.5;}ctx.restore();
}
