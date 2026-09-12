// Steady, incompressible coefficient model. Coefficients are inputs, never inferred from the mesh.
export function aerodynamicTest({speedKmh=0,headwindKmh=0,crosswindKmh=0,temperatureC=15,pressureKPa=101.325,area=null,cd=null,clDown=null,length=5.5}) {
  const values=[speedKmh,headwindKmh,crosswindKmh,temperatureC,pressureKPa,length];
  if(!values.every(Number.isFinite)||temperatureC<=-273.15||pressureKPa<=0||length<=0)throw new RangeError('Condições inválidas');
  const t=temperatureC+273.15,rho=pressureKPa*1000/(287.05*t);
  const axial=(speedKmh+headwindKmh)/3.6,lateral=crosswindKmh/3.6;
  const speed=Math.hypot(axial,lateral),q=.5*rho*speed**2;
  const viscosity=1.716e-5*(t/273.15)**1.5*(273.15+110.4)/(t+110.4);
  const mach=speed/Math.sqrt(1.4*287.05*t),reynolds=rho*speed*length/viscosity;
  const hasCoefficients=[area,cd,clDown].every(v=>typeof v==='number'&&Number.isFinite(v))&&area>0&&cd>=0&&clDown>=0;
  const drag=hasCoefficients?q*cd*area:null,downforce=hasCoefficients?q*clDown*area:null;
  return {rho,speed,axial,lateral,q,mach,reynolds,yawDeg:speed?Math.atan2(lateral,axial)*180/Math.PI:0,
    drag,downforce,airPower:drag===null?null:drag*speed,
    axialDrag:drag===null?null:drag*(speed?axial/speed:0),
    lateralDrag:drag===null?null:drag*(speed?lateral/speed:0),
    validCoefficients:hasCoefficients,withinIncompressibleRange:mach<.3};
}
