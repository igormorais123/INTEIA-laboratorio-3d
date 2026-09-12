export function setupCustomization(materials, studio, renderer, scene) {
  const $ = id => document.getElementById(id);
  const all = materials.materials;
  const groups = {
    body: all.filter(m => m.name.toLowerCase().startsWith('pintura') && !m.name.includes('wing')),
    wings: all.filter(m => m.name.toLowerCase().startsWith('pintura') && m.name.includes('wing')),
    wheels: all.filter(m => m.name.toLowerCase() === 'rodas'),
    carbon: all.filter(m => m.name.toLowerCase().includes('carbon'))
  };
  const originals = new Map(all.map(m => [m, {color:m.color.clone(),roughness:m.roughness,metalness:m.metalness,clearcoat:m.clearcoat,clearcoatRoughness:m.clearcoatRoughness}]));
  const paints = [...groups.body,...groups.wings];
  const finish = {
    gloss: {roughness:.27,metalness:0,clearcoat:1,clearcoatRoughness:.105},
    satin: {roughness:.48,metalness:0,clearcoat:.35,clearcoatRoughness:.3},
    matte: {roughness:.78,metalness:0,clearcoat:0,clearcoatRoughness:.5},
    metallic: {roughness:.3,metalness:.65,clearcoat:1,clearcoatRoughness:.14}
  };
  for (const [group, list] of Object.entries(groups)) {
    $('color-'+group).addEventListener('input', e => {
      list.forEach(m => m.color.set(e.target.value));
      $('value-'+group).textContent=e.target.value.toUpperCase();
    });
  }
  $('paint-finish').onchange=e=>paints.forEach(m=>Object.assign(m,finish[e.target.value]));
  document.querySelectorAll('[data-paint]').forEach(b=>b.onclick=()=>{
    for(const group of ['body','wings']){
      $('color-'+group).value=b.dataset.paint;
      $('color-'+group).dispatchEvent(new Event('input'));
    }
  });
  let exposure=1;
  const applyLight=()=>{
    const dark=document.body.classList.contains('dark');
    renderer.toneMappingExposure=(dark?.92:.88)*exposure;
    $('light-value').textContent=Math.round(exposure*100)+'%';
  };
  $('light-level').oninput=e=>{exposure=Number(e.target.value)/100;applyLight();};
  $('theme').addEventListener('click',()=>{
    applyLight();
    $('floor-color').value='#'+studio.floor.material.color.getHexString();
    $('background-color').value='#'+scene.background.getHexString();
  });
  $('floor-color').oninput=e=>studio.floor.material.color.set(e.target.value);
  $('background-color').oninput=e=>{scene.background.set(e.target.value);scene.fog.color.set(e.target.value);};
  $('reset-style').onclick=()=>{
    originals.forEach((v,m)=>{m.color.copy(v.color);for(const key of ['roughness','metalness','clearcoat','clearcoatRoughness'])m[key]=v[key];});
    for(const group of Object.keys(groups)){
      const color='#'+groups[group][0].color.getHexString();
      $('color-'+group).value=color;$('value-'+group).textContent=color.toUpperCase();
    }
    $('paint-finish').value='gloss';exposure=1;$('light-level').value=100;
    const dark=document.body.classList.contains('dark');studio.setTheme(dark);applyLight();
    $('floor-color').value='#'+studio.floor.material.color.getHexString();
    $('background-color').value='#'+scene.background.getHexString();
  };
}
