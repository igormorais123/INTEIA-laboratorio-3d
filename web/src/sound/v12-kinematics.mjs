// Cinemática biela-manivela do V12: o GLB não traz movimento gravado, os nós são colocados por código a
// partir do ângulo θ do virabrequim que o reprodutor de som informa. Assim a imagem e o áudio andam juntos.
//
// Referencial do GLB (metros): X à direita, Y para cima, Z para a frente. O virabrequim gira em torno de Z,
// passando pela origem. Ângulos em graus são medidos a partir da vertical (+Y) e crescem rumo a +X.
// Um giro de θ do virabrequim corresponde a uma rotação de −θ em torno de Z (regra da mão direita).

const RAD = Math.PI / 180;

/** Ângulo do moente do cilindro, em graus, a partir da vertical. */
export const pinAngleDeg = (cyl, thetaDeg) => thetaDeg + cyl.pinOffsetDeg;

/** Centro do moente do cilindro no referencial do GLB. */
export function pinPosition(engine, cyl, thetaDeg) {
  const psi = pinAngleDeg(cyl, thetaDeg) * RAD;
  return {x: engine.crankRadiusM * Math.sin(psi), y: engine.crankRadiusM * Math.cos(psi), z: cyl.z};
}

/** Distância do centro do virabrequim ao pino do pistão, ao longo do eixo do cilindro. */
export function pistonDistance(engine, cyl, thetaDeg) {
  const gamma = (pinAngleDeg(cyl, thetaDeg) - cyl.axisDeg) * RAD;
  const r = engine.crankRadiusM, l = engine.rodLengthM, s = r * Math.sin(gamma);
  return r * Math.cos(gamma) + Math.sqrt(l * l - s * s);
}

/** Centro do pino do pistão no referencial do GLB. */
export function wristPosition(engine, cyl, thetaDeg) {
  const a = cyl.axisDeg * RAD, d = pistonDistance(engine, cyl, thetaDeg);
  return {x: d * Math.sin(a), y: d * Math.cos(a), z: cyl.z};
}

/** Rotação da biela em torno de Z, em radianos: a malha nasce apontando para +Y a partir do pé grande. */
export function rodRotationZ(engine, cyl, thetaDeg) {
  const pin = pinPosition(engine, cyl, thetaDeg), wrist = wristPosition(engine, cyl, thetaDeg);
  return -Math.atan2(wrist.x - pin.x, wrist.y - pin.y);
}

/** Rotação do virabrequim em torno de Z, em radianos. */
export const crankRotationZ = (thetaDeg) => -thetaDeg * RAD;

/** Curso medido do cilindro (duas vezes o raio do moente); serve de conferência do modelo. */
export const strokeOf = (engine) => 2 * engine.crankRadiusM;

/**
 * Coloca as peças móveis para o ângulo θ.
 * `nodes` resolve um nome do GLB em um objeto com `position.set(x, y, z)` e `rotation.z`.
 * Devolve quantos nós foram movidos, para o chamador saber se o GLB veio completo.
 */
export function poseV12(nodes, manifest, thetaDeg) {
  const engine = manifest.engine;
  let moved = 0;
  const crank = nodes(engine.crankNode);
  if (crank) { crank.rotation.z = crankRotationZ(thetaDeg); moved++; }
  for (const cyl of manifest.cylinders) {
    const piston = nodes(cyl.piston);
    if (piston) {
      const w = wristPosition(engine, cyl, thetaDeg);
      piston.position.set(w.x, w.y, w.z);
      moved++;
    }
    const rod = nodes(cyl.rod);
    if (rod) {
      const p = pinPosition(engine, cyl, thetaDeg);
      rod.position.set(p.x, p.y, p.z);
      rod.rotation.z = rodRotationZ(engine, cyl, thetaDeg);
      moved++;
    }
  }
  for (const name of engine.camNodes) {
    const cam = nodes(name);
    if (cam) { cam.rotation.z = crankRotationZ(thetaDeg * engine.camRatio); moved++; }
  }
  return moved;
}
