// Perfis dos motores do estúdio de som. Os valores de inércia são pontos de partida;
// o plano dos bancos calibrados os ajusta e registra no manifesto do banco.
const profile = (data) => Object.freeze({...data, firingOrder: Object.freeze([...data.firingOrder]), layers: Object.freeze([...data.layers])});

export const ENGINE_PROFILES = Object.freeze({
  v12_90s: profile({
    id: 'v12_90s', label: 'V12 anos 90', cylinders: 12, bankAngleDeg: 65,
    firingOrder: [1, 7, 5, 11, 3, 9, 6, 12, 2, 8, 4, 10],
    crankingRpm: 300, idleRpm: 4000, limitRpm: 17000,
    maxRiseRpmPerS: 40000, maxFallRpmPerS: 25000,
    layers: [], bank: './assets/som-v12-v1.json',
  }),
  v6_2026: profile({
    id: 'v6_2026', label: 'V6 2026', cylinders: 6, bankAngleDeg: 90,
    firingOrder: [1, 4, 2, 5, 3, 6],
    crankingRpm: 300, idleRpm: 4000, limitRpm: 15000,
    maxRiseRpmPerS: 30000, maxFallRpmPerS: 20000,
    layers: ['turbo', 'mguk'], bank: './assets/som-v6-v1.json',
  }),
});

export const firingIntervalDeg = (p) => 720 / p.cylinders;

/** Índice da janela de explosão (0..cilindros-1) que contém o ângulo θ do ciclo de 720°. */
export function firingWindowAt(p, thetaDeg) {
  const theta = ((thetaDeg % 720) + 720) % 720;
  return Math.min(p.cylinders - 1, Math.floor(theta / firingIntervalDeg(p)));
}

export const cylinderAt = (p, thetaDeg) => p.firingOrder[firingWindowAt(p, thetaDeg)];
