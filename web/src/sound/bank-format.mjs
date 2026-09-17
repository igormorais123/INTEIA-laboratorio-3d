// Formato do banco de loops do estúdio de som: manifesto JSON + .bin PCM Int16 LE mono 48 kHz.
// parseBank converte para o formato consumido por prepareBank/createPhasePlayer (phase-player.mjs).
export const BANK_VERSION = 1;
export const BANK_SAMPLE_RATE = 48000;
export const BANK_FORMAT = 'pcm_s16le';

export function validateManifest(manifest) {
  if (!manifest || manifest.version !== BANK_VERSION) throw new Error('Manifesto do banco: versão desconhecida');
  if (manifest.sampleRate !== BANK_SAMPLE_RATE) throw new Error(`Manifesto do banco: taxa ${manifest.sampleRate} Hz (esperado ${BANK_SAMPLE_RATE})`);
  if (manifest.format !== BANK_FORMAT) throw new Error(`Manifesto do banco: formato ${manifest.format}`);
  if (!Number.isInteger(manifest.bytes) || manifest.bytes <= 0) throw new Error('Manifesto do banco: bytes inválido');
  if (!Array.isArray(manifest.loops) || manifest.loops.length < 2) throw new Error('Manifesto do banco: menos de dois loops');
  const segments = manifest.loops.map((loop, i) => {
    if (!Number.isFinite(loop.rpm) || loop.rpm <= 0) throw new Error(`Loop ${i}: rpm inválido`);
    if (loop.load !== 'on' && loop.load !== 'off') throw new Error(`Loop ${i}: carga ${loop.load}`);
    if (!Number.isInteger(loop.samplesPerCycle) || !Number.isInteger(loop.cycles) || loop.cycles < 1) throw new Error(`Loop ${i}: ciclos inválidos`);
    if (loop.frames !== loop.samplesPerCycle * loop.cycles) throw new Error(`Loop ${i}: frames ≠ amostras por ciclo × ciclos`);
    if (Math.abs(loop.rpm - (120 * BANK_SAMPLE_RATE) / loop.samplesPerCycle) > 1e-6) throw new Error(`Loop ${i}: rpm não corresponde a amostras por ciclo`);
    return {offset: loop.offset, end: loop.offset + loop.frames * 2, name: `loop ${i}`};
  });
  if (manifest.starter && manifest.starter.frames > 0) segments.push({offset: manifest.starter.offset, end: manifest.starter.offset + manifest.starter.frames * 2, name: 'starter'});
  segments.sort((a, b) => a.offset - b.offset);
  let cursor = 0;
  for (const segment of segments) {
    if (!Number.isInteger(segment.offset) || segment.offset % 2 !== 0) throw new Error(`${segment.name}: deslocamento ímpar`);
    if (segment.offset < cursor) throw new Error(`${segment.name}: sobrepõe o trecho anterior`);
    if (segment.end > manifest.bytes) throw new Error(`${segment.name}: passa do fim do arquivo`);
    cursor = segment.end;
  }
  return true;
}

function toFloat32(buffer, offset, frames) {
  const view = new Int16Array(buffer, offset, frames);
  const out = new Float32Array(frames);
  for (let i = 0; i < frames; i++) out[i] = view[i] / 32768;
  return out;
}

/** Converte manifesto + ArrayBuffer no banco em memória usado pelo reprodutor. */
export function parseBank(manifest, arrayBuffer) {
  validateManifest(manifest);
  if (arrayBuffer.byteLength !== manifest.bytes) throw new Error(`Banco: ${arrayBuffer.byteLength} bytes, manifesto diz ${manifest.bytes}`);
  const loops = manifest.loops.map((loop) => ({
    rpm: loop.rpm, load: loop.load, samplesPerCycle: loop.samplesPerCycle, cycles: loop.cycles,
    data: toFloat32(arrayBuffer, loop.offset, loop.frames),
  }));
  const starter = manifest.starter && manifest.starter.frames > 0 ? {data: toFloat32(arrayBuffer, manifest.starter.offset, manifest.starter.frames)} : null;
  return {sampleRate: manifest.sampleRate, loops, starter};
}

/** Confere o SHA-256 do .bin quando crypto.subtle existir; devolve null quando não for possível conferir. */
export async function verifyBankHash(manifest, arrayBuffer) {
  const subtle = globalThis.crypto?.subtle;
  if (!subtle || !manifest.sha256) return null;
  const digest = await subtle.digest('SHA-256', arrayBuffer);
  const hex = [...new Uint8Array(digest)].map((b) => b.toString(16).padStart(2, '0')).join('');
  return hex === manifest.sha256;
}

/** Baixa manifesto e .bin (mesma pasta), valida e devolve {bank, manifest}. */
export async function loadBank(manifestUrl, {fetchImpl = globalThis.fetch, signal} = {}) {
  const manifestResponse = await fetchImpl(manifestUrl, {signal});
  if (!manifestResponse.ok) throw new Error(`Manifesto do banco: HTTP ${manifestResponse.status}`);
  const manifest = await manifestResponse.json();
  validateManifest(manifest);
  const binUrl = new URL(manifest.bin, new URL(manifestUrl, globalThis.location?.href ?? 'http://localhost/')).href;
  const binResponse = await fetchImpl(binUrl, {signal});
  if (!binResponse.ok) throw new Error(`Banco: HTTP ${binResponse.status}`);
  const buffer = await binResponse.arrayBuffer();
  const verified = await verifyBankHash(manifest, buffer);
  if (verified === false) throw new Error('Banco: SHA-256 não confere');
  return {bank: parseBank(manifest, buffer), manifest, verified};
}
