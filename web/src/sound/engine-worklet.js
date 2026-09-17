// AudioWorklet do estúdio de som: casca fina em volta de engine-voice.mjs. Recebe o banco por postMessage
// (buffers transferidos), o perfil e o estado dos controles; devolve a cada ~30 ms o estado do motor
// {rpm, thetaDeg, running, cranking, limiter, load, t, playing, ignition, power, mode}.
// O build empacota este arquivo como IIFE e o site o carrega como Blob (audioWorklet.addModule).
import {createEngineVoice} from './engine-voice.mjs';
import {ENGINE_PROFILES} from './engine-profiles.mjs';

const REPORT_SECONDS = 0.03;

class EngineProcessor extends AudioWorkletProcessor {
  constructor() {
    super();
    this.voice = null; this.pending = {}; this.pendingCurve = null; this.reportT = 0;
    this.port.onmessage = (event) => this.onMessage(event.data);
  }

  onMessage(message) {
    switch (message.type) {
      case 'bank': {
        const profile = ENGINE_PROFILES[message.engine];
        const bank = {
          sampleRate: message.sampleRate,
          loops: message.loops.map((loop) => ({rpm: loop.rpm, load: loop.load, samplesPerCycle: loop.samplesPerCycle, cycles: loop.cycles, data: new Float32Array(loop.data)})),
          starter: message.starter ? {data: new Float32Array(message.starter)} : null,
        };
        try {
          this.voice = createEngineVoice({bank, profile, sampleRate});
          this.voice.setState(this.pending);
          if (this.pendingCurve) this.voice.setCurve(this.pendingCurve);
          this.port.postMessage({type: 'ready', engine: message.engine});
        } catch (error) {
          this.voice = null;
          this.port.postMessage({type: 'error', message: error.message});
        }
        break;
      }
      case 'state': Object.assign(this.pending, message.state); this.voice?.setState(message.state); break;
      case 'curve': this.pendingCurve = message.curve; this.voice?.setCurve(message.curve); break;
      case 'play': this.voice?.play(); break;
      case 'stop': this.voice?.stop(); break;
      default: break;
    }
  }

  process(inputs, outputs) {
    const out = outputs[0][0];
    if (!out) return true;
    if (!this.voice) { out.fill(0); return true; }
    const status = this.voice.render(out);
    this.reportT += out.length / sampleRate;
    if (this.reportT >= REPORT_SECONDS) { this.reportT = 0; this.port.postMessage({type: 'status', ...status}); }
    return true;
  }
}

registerProcessor('inteia-engine', EngineProcessor);
