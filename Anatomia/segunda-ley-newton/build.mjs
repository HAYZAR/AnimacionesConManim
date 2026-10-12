// Fig. 1 · Segunda ley de Newton: carrito en riel con polea, pesa colgante y cinta de ticks.
// Escala del mundo: 1 unidad = 0,5 cm. x a lo largo del riel, y a lo ancho, z hacia arriba.
// node build.mjs [--light]
import { writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import * as k from "../../.claude/skills/anatomy/kit/iso-kit.mjs";
import * as G from "../../.claude/skills/anatomy/kit/lathe.mjs";
import { kitScript } from "../../.claude/skills/anatomy/scripts/inline-kit.mjs";

const HERE = dirname(fileURLToPath(import.meta.url));
const theme = process.argv.includes("--light") ? "light" : "dark";
const NAME = "segunda-ley-newton";

const WIDTH = 600;
const HEIGHT = 420;

// ── Modelo (verdad) ────────────────────────────────────────────────
const UNITS_PER_M = 200; // 1 unidad = 0,5 cm
const G_ACC = 9.8;
const CART_KG = 0.5; // carrito de dinámica
const BAR_KG = 0.5; // cada barra de acero (8 × 5 × 1,6 cm)
const HANGER_KG = 0.05; // portapesas de 50 g
const DISC_KG = 0.05; // cada pesa ranurada de 50 g
const RUN_M = 0.3; // recorrido hasta que la pesa toca la espuma
const TICK_S = 0.1; // el temporizador marca un punto cada 0,1 s
const MAX_LOAD = 3;
const MAX_DISCS = 3;

// ── Geometría ──────────────────────────────────────────────────────
const PLATE = { x: -30, y: -26, w: 230, d: 62, r: 8 };
const PLATE_H = 10;
const FOOT_H = 5;

const END = 160; // largo del riel: 0,8 m
const TRACK = { x: 0, y: -7, w: END, d: 14, r: 1 };
const TRACK_Z = 124;
const TOP = 132; // cara superior del riel
const POSTS = [30, 130];

const CART_L = 34;
const BODY_Z = 135.8;
const BODY_TOP = 142.8;
const HOOK = [CART_L + 2.6, 0, 141]; // ojal del hilo, relativo al carrito
const BAR_H = 3.2;

const PULLEY = [END + 14, 0, 135];
const GROOVE_R = 6;
const CHEEK_R = 7;

const PAD_FACE = 132.3; // cara del tope de goma
const BUMPER_X = 140;
const START = PAD_FACE - CART_L - RUN_M * UNITS_PER_M; // x trasero del carrito en reposo
const TICK_X = 11; // donde golpea el temporizador

const BOX = { x: END + 10, y: -10, w: 20, d: 20, r: 2 };
const FOAM_TOP = 10; // sobre el piso
const HANGER_LEN = 17.8; // del gancho a la base
const DISC_H = 1.8;
const DISC_R = 3;
const HOOK0 = PULLEY[2] - 20.2; // gancho en reposo, 20 bajo el eje de la polea
const FLOOR = HOOK0 - RUN_M * UNITS_PER_M - HANGER_LEN - FOAM_TOP; // cara superior de la base

const P = k.fitProjection(
  [...k.boxCorners(PLATE, FLOOR - PLATE_H - FOOT_H, FLOOR), [0, 0, BODY_TOP + 3 * BAR_H + 2], [END + 4, 0, PULLEY[2] + CHEEK_R], [-17, 0, 145]],
  WIDTH,
  HEIGHT,
  { pad: 26, azimuth: 57 },
);

const at = (point) => k.iso(point, P);
const S = (paths, style) => k.solidSvg(paths, style);
const L = (d, style) => k.lineSvg(d, style);
const D = (points, style) => k.dotsSvg(points, style);
const byDepth = (points) => [...points].sort((a, b) => k.depthOf([a[0], a[1], 0], P) - k.depthOf([b[0], b[1], 0], P));
const alongY = (x, y, z) => G.frameOf([x, y, z], [0, 1, 0], [1, 0, 0], [0, 0, 1]);
const alongX = (x, y, z) => G.frameAlong([x, y, z], [1, 0, 0]);
const halo = (plan, z, h, blur = 4) => `<path class="iso-halo" d="${k.haloOf(plan, z, h, P)}" style="filter:blur(${blur}px)"/>`;

// ── Base ───────────────────────────────────────────────────────────
function plate() {
  const out = [`<path class="iso-halo" d="${k.haloOf(PLATE, -PLATE_H - FOOT_H, PLATE_H, P)}"/>`];
  for (const [x, y] of byDepth(k.corners(PLATE, 20))) {
    out.push(S(k.cylinder(x, y, 7, -PLATE_H - FOOT_H, 1.6, P, 28), { tone: "lo" }));
    out.push(S(k.cylinder(x, y, 5.4, -PLATE_H - FOOT_H + 1.6, FOOT_H - 1.6, P, 28), { tone: "mid" }));
  }
  out.push(S(k.slabOf(PLATE, -PLATE_H, PLATE_H, P, 8, 1.6), { tone: "mid", inner: L(k.sideSeam(PLATE, -4, P, 8), { tone: "faint" }) }));
  out.push(L(k.planOutline(k.insetPlan(PLATE, 5), 0, P), { tone: "lo" }));
  const screws = k.corners(PLATE, 10);
  out.push(L(screws.map(([x, y]) => k.ring(x, y, 2.2, 0, P, 16)).join(""), { tone: "lo" }));
  out.push(D(screws.map(([x, y]) => at([x, y, 0])), { size: 0.5 }));
  // placa de identificación
  const label = { x: -24, y: 22, w: 30, d: 9, r: 1 };
  out.push(S(k.slabOf(label, 0, 0.8, P, 4), { tone: "lo", crease: "none" }));
  out.push(L(k.planOutline(k.insetPlan(label, 1.4), 0.8, P, 4), { tone: "faint" }));
  out.push(L([[-20, 25.2, 16], [-20, 27.4, 11], [-20, 29.4, 13]].map(([x, y, w]) => k.lineOnTop([x, y], [x + w, y], 0.8, P)).join(""), { tone: "lo", free: true }));
  out.push(D([at([label.x + 27, label.y + 2.5, 0.8]), at([label.x + 27, label.y + 6.5, 0.8])], { size: 0.4 }));
  return out.join("");
}

function post(px) {
  const out = [];
  out.push(S(k.cylinder(px, 0, 7, FLOOR, 3, P, 28, 0.5), { tone: "mid" }));
  out.push(D(k.corners({ x: px - 7, y: -7, w: 14, d: 14, r: 7 }, 2.4).map(([x, y]) => at([x, y, FLOOR + 3])).filter((_, i) => i !== 0), { size: 0.4 }));
  out.push(S(k.cylinder(px, 0, 3, FLOOR + 3, 109 - FLOOR, P, 24), { tone: "mid", crease: "none", inner: L([FLOOR + 30, FLOOR + 60].map((z) => k.sideArc(px, 0, 3, z, P, 16)).join(""), { tone: "faint" }) }));
  const clamp = { x: px - 8, y: -8, w: 16, d: 16, r: 2 };
  out.push(S(k.slabOf(clamp, 112, 10, P, 4, 0.6), { tone: "mid", inner: L(k.sideSeam(clamp, 117, P, 4), { tone: "faint" }) }));
  // tornillo de apriete hacia el frente
  const F = alongY(px, 8, 117);
  out.push(S(G.disc(0, 1.6, 1.3, F, P), { tone: "mid", crease: "none" }));
  out.push(S(G.disc(1.6, 4.6, 2.8, F, P), { tone: "mid" }));
  out.push(k.fadedSvg(G.ribsOf(F, 1.6, 4.6, 2.8, 20, P, { fade: [0.05, 0.4] }), { tone: "lo" }));
  out.push(L(G.circleOf(F, 4.6, 1, P, 16), { tone: "faint" }));
  // silla que recibe el riel
  const saddle = { x: px - 11, y: -8, w: 22, d: 16, r: 1 };
  out.push(S(k.slabOf(saddle, 122, 2, P, 3, 0.4), { tone: "lo" }));
  return out.join("");
}

// ── Riel ───────────────────────────────────────────────────────────
function cap(x) {
  const plan = { x, y: -8, w: 4, d: 16, r: 1 };
  return S(k.slabOf(plan, 122, TOP - 122, P, 3, 0.4), { tone: "mid" }) + D([at([x + 2, -5, TOP]), at([x + 2, 5, TOP])], { size: 0.4 });
}

function track() {
  const out = [cap(-4)];
  out.push(S(k.slabOf(TRACK, TRACK_Z, TOP - TRACK_Z, P, 3, 0.6), { tone: "mid", inner: L(k.sideSeam(TRACK, 127, P, 3), { tone: "faint" }) }));
  out.push(L(k.lineOnTop([0, -4.2], [END, -4.2], TOP, P) + k.lineOnTop([0, 4.2], [END, 4.2], TOP, P), { tone: "faint" }));
  const ticks = k.sideTicks(2, END - 2, 2, 10, 7, TOP, [1.2, 2.6], P);
  out.push(L(ticks.minor, { tone: "lo" }), L(ticks.major, { tone: "mid" }));
  return out.join("");
}

// ── Temporizador de ticks y rollo de cinta ────────────────────────
const ROLL = [-11, -3, 138.6];
function rollBracket() {
  const plan = { x: -17, y: -6, w: 13, d: 2, r: 0.6 };
  return S(k.slabOf(plan, 126, 18, P, 3, 0.3), { tone: "mid" }) + D([at([-6, -5, 144]), at([-15, -5, 144])], { size: 0.4 });
}
function roll() {
  const F = alongY(ROLL[0], ROLL[1], ROLL[2]);
  const out = [];
  out.push(S(G.disc(0, 6, 6.2, F, P), { tone: "hi", crease: "lo" }));
  out.push(L(G.circleOf(F, 6, 4.6, P) + G.circleOf(F, 6, 2.4, P), { tone: "faint" }));
  out.push(S(G.disc(6, 7.2, 1.4, F, P), { tone: "mid" }));
  return out.join("");
}

function ticker() {
  const out = [];
  out.push(S(k.slabOf({ x: 4, y: -7.5, w: 14, d: 3.5, r: 0.6 }, TOP, 2, P, 3), { tone: "lo" }));
  out.push(S(k.slabOf({ x: 4, y: 4, w: 14, d: 3.5, r: 0.6 }, TOP, 2, P, 3), { tone: "lo" }));
  const box = { x: 2, y: -8, w: 18, d: 16, r: 1.6 };
  out.push(S(k.slabOf(box, TOP + 2, 9, P, 5, 0.8), { tone: "mid", inner: L(k.sideSeam(box, TOP + 8, P, 5), { tone: "faint" }) }));
  const lid = TOP + 11;
  out.push(L(k.planOutline(k.insetPlan(box, 2), lid, P, 4), { tone: "faint" }));
  out.push(D(k.corners(box, 1.2).map(([x, y]) => at([x, y, lid])), { size: 0.4 }));
  // disco de carbón y percutor
  out.push(L(k.ring(TICK_X, 0, 4, lid, P, 40), { tone: "lo" }));
  out.push(S(k.cylinder(TICK_X, 0, 2.6, lid, 1.2, P, 28), { tone: "mid" }));
  out.push(S(k.cylinder(TICK_X, 0, 1.2, lid + 1.2, 1.6, P, 20, 0.3), { tone: "hi", crease: "lo" }));
  out.push(k.faceTextSvg(k.topMatrix([5.6, 0], lid, P, "y"), "0,1 s", { size: 2, tone: "lo", anchor: "middle" }));
  out.push(`<g data-part="led">${D([at([17, -5.2, lid])], { size: 0.9, tone: "faint" })}</g>`);
  return out.join("");
}

// ── Carrito (construido con su trasera en x = 0) ───────────────────
function wheel(x, y0) {
  const F = alongY(x, y0, 134.2);
  return S(G.disc(0, 1.8, 2.2, F, P), { tone: "lo" }) + L(G.circleOf(F, 1.8, 0.8, P, 16), { tone: "faint" });
}
function bar(index) {
  const plan = { x: 9, y: -5, w: 16, d: 10, r: 1 };
  const z = BODY_TOP + BAR_H * index;
  return (
    S(k.slabOf(plan, z, BAR_H, P, 3, 0.5), { tone: "hi", crease: "lo" }) +
    L(k.planOutline(k.insetPlan(plan, 1.6), z + BAR_H, P, 3), { tone: "faint" }) +
    D([at([12, 0, z + BAR_H]), at([22, 0, z + BAR_H])], { size: 0.4, tone: "lo" })
  );
}
function cart(load) {
  const body = { x: 0, y: -9, w: CART_L, d: 18, r: 2 };
  const out = [halo(k.insetPlan(body, 3), TOP, 0.1)];
  out.push(wheel(6, -6.6), wheel(28, -6.6));
  out.push(wheel(6, 4.8), wheel(28, 4.8));
  out.push(S(k.slabOf(body, BODY_Z, BODY_TOP - BODY_Z, P, 5, 0.8), { tone: "hi", crease: "lo", inner: L(k.sideSeam(body, 138.4, P, 5), { tone: "faint" }) }));
  out.push(L(k.planOutline(k.insetPlan(body, 2.2), BODY_TOP, P, 4), { tone: "faint" }));
  out.push(D(k.corners(body, 1.1).map(([x, y]) => at([x, y, BODY_TOP])), { size: 0.4, tone: "lo" }));
  // pinza de la cinta, detrás
  out.push(S(k.slabOf({ x: -2.4, y: -3, w: 2.6, d: 6, r: 0.5 }, TOP + 0.3, 5.4, P, 3), { tone: "mid" }));
  out.push(D([at([-1.1, 0, TOP + 5.7])], { size: 0.45 }));
  // ojal del hilo, delante
  out.push(S(k.slabOf({ x: CART_L - 0.2, y: -1.6, w: 2.4, d: 3.2, r: 0.6 }, 139.4, 2.6, P, 3), { tone: "mid" }));
  out.push(L(k.sideRing([HOOK[0], 0, HOOK[2]], 0.7, "y", P, 14), { tone: "mid" }));
  for (let i = 0; i < load; i++) out.push(bar(i));
  return out.join("");
}

// ── Tope con resorte ───────────────────────────────────────────────
const SPRING = [0, 136.4];
function bumperBlock() {
  const plan = { x: BUMPER_X, y: -8, w: 8, d: 16, r: 1 };
  return (
    S(k.slabOf(plan, TOP, 6.5, P, 3, 0.5), { tone: "mid", inner: L(k.sideSeam(plan, TOP + 3, P, 3), { tone: "faint" }) }) +
    D([at([BUMPER_X + 4, -5, TOP + 6.5]), at([BUMPER_X + 4, 5, TOP + 6.5])], { size: 0.45 }) +
    L(k.sideRing([BUMPER_X, 0, SPRING[1]], 1.1, "x", P, 16), { tone: "faint" })
  );
}
function plungerAt(face) {
  const F = alongX(face, 0, SPRING[1]);
  return S(G.disc(1.2, 1.2 + BUMPER_X - face, 0.6, F, P), { tone: "mid", crease: "none" }) + S(G.disc(0, 1.2, 2.2, F, P), { tone: "lo" });
}

// ── Polea ──────────────────────────────────────────────────────────
function pulleyMount() {
  const block = { x: END - 1, y: -5, w: 7, d: 10, r: 1 };
  return (
    cap(END) +
    S(k.slabOf(block, TOP, 5.5, P, 3, 0.5), { tone: "mid" }) +
    D([at([END + 2.5, -2.6, TOP + 5.5]), at([END + 2.5, 2.6, TOP + 5.5])], { size: 0.45 }) +
    S(k.slabOf({ x: END + 5, y: -4, w: 12, d: 1, r: 0.5 }, 133, 4, P, 3), { tone: "mid" }) +
    S(G.disc(-4, -2, 0.7, alongY(PULLEY[0], 0, PULLEY[2]), P), { tone: "lo" })
  );
}
const pulleyF = (y) => alongY(PULLEY[0], y, PULLEY[2]);
function pulleyBack() {
  return S(G.disc(-2, -1, CHEEK_R, pulleyF(0), P), { tone: "mid" }) + S(G.disc(-1, 1, GROOVE_R, pulleyF(0), P), { tone: "lo" });
}
function pulleyFront() {
  const F = pulleyF(0);
  return S(G.disc(1, 2, CHEEK_R, F, P), { tone: "mid" }) + L(G.circleOf(F, 2, CHEEK_R - 0.9, P) + G.circleOf(F, 2, 1.5, P, 16), { tone: "faint" });
}
function pulleyNose() {
  const F = pulleyF(0);
  return (
    S(k.slabOf({ x: END + 5, y: 3, w: 12, d: 1, r: 0.5 }, 133, 4, P, 3), { tone: "mid" }) +
    D([at([END + 7, 4, 137])], { size: 0.4 }) +
    S(G.disc(4, 5.2, 1.6, F, P), { tone: "mid" }) +
    L(G.circleOf(F, 5.2, 0.6, P, 12), { tone: "lo" })
  );
}

// ── Caja de espuma y portapesas ────────────────────────────────────
function catchBox() {
  const foam = k.insetPlan(BOX, 1.6);
  return (
    halo(BOX, 0, 6, 5) +
    S(k.slabOf(BOX, 0, 6, P, 4, 0.6), { tone: "mid", inner: L(k.sideSeam(BOX, 3, P, 4), { tone: "faint" }) }) +
    S(k.slabOf(foam, 6, FOAM_TOP - 6, P, 4), { tone: "lo", crease: "none" }) +
    D(k.dotGrid(foam.x + 2.5, foam.y + 2.5, 6, 6, 2.5, FOAM_TOP, P), { size: 0.35, tone: "faint" })
  );
}

// Portapesas construido con el gancho arriba en z = 0, centrado en x = 220.
const HX = PULLEY[0] + GROOVE_R;
function slotted(z, tone) {
  return S(k.cylinder(HX, 0, DISC_R, z, DISC_H, P, 28, 0.3), { tone, crease: "lo" }) + L(k.lineOnTop([HX, 0.5], [HX, DISC_R], z + DISC_H, P), { tone: "lo" });
}
function hanger(discs) {
  const base = -HANGER_LEN;
  const out = [];
  out.push(S(k.cylinder(HX, 0, DISC_R, base, DISC_H, P, 28, 0.3), { tone: "mid" }));
  for (let i = 0; i < discs; i++) out.push(slotted(base + DISC_H * (i + 1), "hi"));
  const stemFrom = base + DISC_H * (discs + 1);
  out.push(S(k.cylinder(HX, 0, 0.5, stemFrom, -1.6 - stemFrom, P, 12), { tone: "mid", crease: "none" }));
  out.push(L(k.sideRing([HX, 0, -0.8], 0.8, "y", P, 14), { tone: "mid" }));
  return out.join("");
}

// ── Repuestos sobre la base ───────────────────────────────────────
const PEG = [100, 24];
function spareDiscs(count) {
  const out = [S(k.cylinder(PEG[0], PEG[1], 4.4, 0, 1.4, P, 28, 0.4), { tone: "lo" })];
  for (let i = 0; i < count; i++) {
    const z = 1.4 + DISC_H * i;
    out.push(S(k.cylinder(PEG[0], PEG[1], DISC_R, z, DISC_H, P, 28, 0.3), { tone: "hi", crease: "lo" }));
    out.push(L(k.lineOnTop([PEG[0], PEG[1] + 0.5], [PEG[0], PEG[1] + DISC_R], z + DISC_H, P), { tone: "lo" }));
  }
  const top = 1.4 + DISC_H * count;
  out.push(S(k.cylinder(PEG[0], PEG[1], 0.5, top, 14 - top, P, 12), { tone: "mid", crease: "none" }));
  return out.join("");
}
const TRAY = { x: 52, y: 14, w: 22, d: 16, r: 1.2 };
function spareBars(count) {
  const out = [S(k.slabOf(TRAY, 0, 1.4, P, 3, 0.4), { tone: "lo" }), L(k.planOutline(k.insetPlan(TRAY, 1.6), 1.4, P, 3), { tone: "faint" })];
  for (let i = 0; i < count; i++) {
    const plan = { x: TRAY.x + 3, y: TRAY.y + 3, w: 16, d: 10, r: 1 };
    const z = 1.4 + BAR_H * i;
    out.push(S(k.slabOf(plan, z, BAR_H, P, 3, 0.5), { tone: "hi", crease: "lo" }));
    out.push(L(k.planOutline(k.insetPlan(plan, 1.6), z + BAR_H, P, 3), { tone: "faint" }));
  }
  return out.join("");
}

const variants = (name, count, draw, shown) =>
  Array.from({ length: count + 1 }, (_, i) => `<g data-${name}="${i}"${i === shown ? "" : ' style="display:none"'}>${draw(i)}</g>`).join("");

// ── Figura ─────────────────────────────────────────────────────────
const floor = k.translateAlong(P, [0, 0, FLOOR]);
const LOAD0 = 1;
const DISCS0 = 1;
const svg = k.figureSvg({
  width: WIDTH,
  height: HEIGHT,
  label:
    "Un riel de dinámica sobre dos soportes. Un carrito con barras de carga está unido por un hilo que pasa por una polea a una pesa colgante. Al soltarlo, la pesa cae y tira del carrito; un temporizador marca un punto en la cinta cada 0,1 s, y la separación creciente entre puntos muestra la aceleración, igual a F/m.",
  body: [
    `<g transform="${floor}">${plate()}</g>`,
    ...POSTS.map(post),
    `<g transform="${floor}">`,
    `<g data-part="spare-bars">${variants("bars", MAX_LOAD, (i) => spareBars(MAX_LOAD - i), LOAD0)}</g>`,
    `<g data-part="spare-discs">${variants("discs", MAX_DISCS, (i) => spareDiscs(MAX_DISCS - i), DISCS0)}</g>`,
    catchBox(),
    `</g>`,
    track(),
    rollBracket(),
    `<g data-part="tape"></g>`,
    `<g data-part="ink" class="ct-ink"></g>`,
    roll(),
    ticker(),
    `<g data-part="cart" transform="${k.translateAlong(P, [START, 0, 0])}">${variants("load", MAX_LOAD, cart, LOAD0)}</g>`,
    `<path data-part="coil-back" class="iso-line" data-tone="lo" d=""/>`,
    `<g data-part="plunger">${plungerAt(PAD_FACE)}</g>`,
    `<path data-part="coil-front" class="iso-line" data-tone="mid" d=""/>`,
    bumperBlock(),
    pulleyMount(),
    pulleyBack(),
    `<path data-part="string" class="iso-line" data-tone="hi" d="" style="stroke-width:.8"/>`,
    pulleyFront(),
    `<path data-part="spokes" class="iso-line" data-tone="lo" d=""/>`,
    pulleyNose(),
    `<g data-part="hanger" transform="${k.translateAlong(P, [0, 0, HOOK0])}">${variants("hang", MAX_DISCS, hanger, DISCS0)}</g>`,
  ],
});

const controls = `
<div class="ct-panel">
  <div class="ct-row" role="radiogroup" aria-label="Pesa colgante">
    <span class="ct-name">Pesa colgante</span>
    ${Array.from({ length: MAX_DISCS + 1 }, (_, i) => `<button type="button" role="radio" data-set-discs="${i}" aria-checked="${i === DISCS0}">${Math.round((HANGER_KG + DISC_KG * i) * 1000)} g</button>`).join("")}
  </div>
  <div class="ct-row" role="radiogroup" aria-label="Carga sobre el carrito">
    <span class="ct-name">Carga</span>
    ${Array.from({ length: MAX_LOAD + 1 }, (_, i) => `<button type="button" role="radio" data-set-load="${i}" aria-checked="${i === LOAD0}">${(BAR_KG * i).toFixed(1).replace(".", ",")} kg</button>`).join("")}
  </div>
  <div class="ct-row ct-act">
    <button type="button" class="ct-go" data-go>Soltar</button>
  </div>
  <dl class="ct-data">
    <div><dt>F = m<sub>pesa</sub>·g</dt><dd data-out="F">—</dd></div>
    <div><dt>m = carrito + pesa</dt><dd data-out="m">—</dd></div>
    <div><dt>F / m</dt><dd data-out="Fm">—</dd></div>
    <div data-lit><dt>a medida en la cinta</dt><dd data-out="a">—</dd></div>
  </dl>
</div>`;

const CSS = `
.ct-ink .iso-dots[data-tone] circle{fill:var(--anatomy-lit);opacity:1}
.ct-led .iso-dots[data-tone] circle{fill:var(--anatomy-red);opacity:1}
.iso-stage{touch-action:pan-y;cursor:pointer;outline:none}
.iso-stage:focus-visible{outline:1px solid var(--anatomy-muted);outline-offset:6px}
.ct-panel{display:grid;gap:10px;margin-top:22px;font-family:var(--anatomy-mono);font-size:11px;letter-spacing:.03em;color:var(--anatomy-muted)}
.ct-row{display:flex;flex-wrap:wrap;align-items:center;gap:6px}
.ct-name{min-width:112px;text-transform:uppercase;letter-spacing:.1em;font-size:10px}
.ct-panel button{font:inherit;color:var(--anatomy-text);background:transparent;border:0;box-shadow:0 0 0 1px var(--anatomy-faint);padding:5px 9px;cursor:pointer;font-variant-numeric:tabular-nums;transition:box-shadow .2s var(--anatomy-ease),color .2s var(--anatomy-ease)}
.ct-panel button:hover{box-shadow:0 0 0 1px var(--anatomy-mid)}
.ct-panel button[aria-checked="true"]{color:var(--anatomy-strong);box-shadow:0 0 0 1px var(--anatomy-hi)}
.ct-panel button:focus-visible{outline:1px solid var(--anatomy-muted);outline-offset:3px}
.ct-go{min-width:112px;color:var(--anatomy-strong)!important;box-shadow:0 0 0 1px var(--anatomy-hi)!important}
.ct-data{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;margin:4px 0 0;background:var(--anatomy-faint);box-shadow:0 0 0 1px var(--anatomy-faint)}
.ct-data>div{background:var(--anatomy-card);padding:8px 10px}
.ct-data dt{font-size:9.5px;text-transform:uppercase;letter-spacing:.08em}
.ct-data dd{margin:4px 0 0;color:var(--anatomy-strong);font-size:13px;font-variant-numeric:tabular-nums}
.ct-data>div[data-lit] dd{color:var(--anatomy-lit)}
@media (max-width:560px){.ct-data{grid-template-columns:repeat(2,1fr)}.ct-name{min-width:100%}}
`;

const live = `
const P = ${JSON.stringify(P)};
const C = ${JSON.stringify({ UNITS_PER_M, G_ACC, CART_KG, BAR_KG, HANGER_KG, DISC_KG, RUN_M, TICK_S, MAX_LOAD, MAX_DISCS, START, TICK_X, TOP, CART_L, HOOK, PULLEY, GROOVE_R, CHEEK_R, PAD_FACE, BUMPER_X, SPRING, HOOK0, HX, ROLL })};
const stage = document.querySelector(".iso-stage");
const svg = stage.querySelector("svg");
const part = (name) => svg.querySelector('[data-part="' + name + '"]');
const cartEl = part("cart"), hangerEl = part("hanger"), tapeEl = part("tape"), inkEl = part("ink"), plungerEl = part("plunger");
const coilBack = part("coil-back"), coilFront = part("coil-front"), stringEl = part("string"), spokesEl = part("spokes"), ledEl = part("led");
const readout = document.querySelector("[data-readout]");
const out = (name) => document.querySelector('[data-out="' + name + '"]');
const goButton = document.querySelector("[data-go]");
const still = matchMedia("(prefers-reduced-motion: reduce)");
const fmt = (value, digits = 2) => value.toFixed(digits).replace(".", ",");

let load = ${LOAD0}, discs = ${DISCS0};
const hangKg = () => C.HANGER_KG + C.DISC_KG * discs;
const cartKg = () => C.CART_KG + C.BAR_KG * load;
const force = () => hangKg() * C.G_ACC;
const totalKg = () => cartKg() + hangKg();
const accel = () => force() / totalKg();

// estado del movimiento: s en metros recorridos desde el reposo
let phase = "ready", t = 0, s = 0, v = 0, squeeze = 0, squeezeRate = 0, dropped = 0, stamps = [], measured = null, holdUntil = 0, inkAlpha = 1;
let pending = false;
let frame = 0, last = 0, visible = false, touring = !still.matches, tourClock = 0, tourStep = 0, idleTimer = 0;


function draw() {
  const x = C.START + s * C.UNITS_PER_M + squeeze;
  cartEl.setAttribute("transform", translateAlong(P, [x, 0, 0]));
  const fall = Math.min(dropped, C.RUN_M) * C.UNITS_PER_M;
  const hook = C.HOOK0 - fall;
  hangerEl.setAttribute("transform", translateAlong(P, [0, 0, hook]));
  // cinta: del rollo a la pinza trasera del carrito
  const tape = slabOf({ x: C.ROLL[0], y: -2, w: x - 1.2 - C.ROLL[0], d: 4, r: 0.3 }, C.TOP, 0.3, P, 2);
  tapeEl.innerHTML = solidSvg(tape, { tone: "mid", flat: true, crease: "none" });
  // puntos de tinta: cada marca viaja con la cinta
  const dots = stamps.map((xs) => iso([C.TICK_X + (x - xs), 0, C.TOP + 0.3], P)).filter((_, i) => C.TICK_X + (x - stamps[i]) > 20.5);
  inkEl.innerHTML = dots.length ? dotsSvg(dots, { size: 0.75 }) : "";
  inkEl.setAttribute("opacity", inkAlpha.toFixed(3));
  // hilo: ojal → arriba de la polea → por la garganta → al gancho
  const [px, , pz] = C.PULLEY, R = C.GROOVE_R;
  const arc = [];
  for (let i = 0; i <= 8; i++) { const a = Math.PI / 2 - (i / 8) * (Math.PI / 2); arc.push(iso([px + R * Math.cos(a), 0, pz + R * Math.sin(a)], P)); }
  const hookAt = [x + C.HOOK[0] + 0.7, 0, C.HOOK[2]];
  stringEl.setAttribute("d", pathOf([iso(hookAt, P), ...arc, iso([px + R, 0, hook], P)]));
  // radios de la polea: giran con el hilo
  const turn = -(s * C.UNITS_PER_M + squeeze) / R;
  const spokes = [];
  for (let i = 0; i < 5; i++) {
    const a = turn + (i / 5) * Math.PI * 2;
    spokes.push(pathOf([iso([px + 1.5 * Math.cos(a), 2, pz + 1.5 * Math.sin(a)], P), iso([px + (C.CHEEK_R - 0.9) * Math.cos(a), 2, pz + (C.CHEEK_R - 0.9) * Math.sin(a)], P)]));
  }
  spokesEl.setAttribute("d", spokes.join(""));
  // tope: el resorte se comprime cuando el carrito lo empuja
  const face = Math.max(C.PAD_FACE, x + C.CART_L) ;
  plungerEl.setAttribute("transform", translateAlong(P, [face - C.PAD_FACE, 0, 0]));
  const coilSet = coil(face + 1.2, C.BUMPER_X, C.SPRING, 1.7, 5, "x", P);
  coilBack.setAttribute("d", coilSet.back);
  coilFront.setAttribute("d", coilSet.front);
  ledEl.classList.toggle("ct-led", phase === "run" || phase === "brake");
  // lectura
  let text = "listo · pulsa Soltar";
  if (phase === "run") text = "t " + fmt(t) + " s · v " + fmt(v) + " m/s";
  else if (phase === "brake" || phase === "done") text = measured === null ? "fin del recorrido" : "a medida " + fmt(measured) + " m/s²";
  else if (phase === "reset") text = "volviendo al inicio";
  if (readout.textContent !== text) readout.textContent = text;
}

function writeData() {
  out("F").textContent = fmt(force(), 3) + " N";
  out("m").textContent = fmt(totalKg(), 2) + " kg";
  out("Fm").textContent = fmt(accel(), 2) + " m/s²";
  out("a").textContent = measured === null ? "—" : fmt(measured, 2) + " m/s²";
  goButton.textContent = phase === "ready" ? "Soltar" : phase === "reset" ? "Volviendo…" : phase === "run" || phase === "brake" ? "En marcha…" : "Repetir";
  stage.setAttribute("aria-valuetext", "Pesa " + Math.round(hangKg() * 1000) + " g, carga " + fmt(C.BAR_KG * load, 1) + " kg, F/m " + fmt(accel()) + " m/s²" + (measured === null ? "" : ", a medida " + fmt(measured) + " m/s²"));
}

function showVariants() {
  svg.querySelectorAll("[data-load]").forEach((el) => (el.style.display = Number(el.dataset.load) === load ? "" : "none"));
  svg.querySelectorAll("[data-bars]").forEach((el) => (el.style.display = Number(el.dataset.bars) === load ? "" : "none"));
  svg.querySelectorAll("[data-hang]").forEach((el) => (el.style.display = Number(el.dataset.hang) === discs ? "" : "none"));
  svg.querySelectorAll("[data-discs]").forEach((el) => (el.style.display = Number(el.dataset.discs) === discs ? "" : "none"));
  document.querySelectorAll("[data-set-load]").forEach((b) => b.setAttribute("aria-checked", String(Number(b.dataset.setLoad) === load)));
  document.querySelectorAll("[data-set-discs]").forEach((b) => b.setAttribute("aria-checked", String(Number(b.dataset.setDiscs) === discs)));
}

// medida como en el laboratorio: diferencia de dos intervalos sucesivos ÷ T²
function measure() {
  const xs = stamps.filter((_, i) => i * C.TICK_S <= Math.sqrt(2 * C.RUN_M / accel()) + 1e-9);
  if (xs.length < 3) return null;
  const n = xs.length;
  const d1 = (xs[n - 1] - xs[n - 2]) / C.UNITS_PER_M, d0 = (xs[n - 2] - xs[n - 3]) / C.UNITS_PER_M;
  return (d1 - d0) / (C.TICK_S * C.TICK_S);
}

function finishInstantly() {
  const a = accel(), tEnd = Math.sqrt(2 * C.RUN_M / a);
  stamps = [];
  for (let i = 0; i * C.TICK_S <= tEnd + 1e-9; i++) stamps.push(C.START + 0.5 * a * (i * C.TICK_S) ** 2 * C.UNITS_PER_M);
  s = C.RUN_M; dropped = C.RUN_M; t = tEnd; v = 0; squeeze = 0; squeezeRate = 0; inkAlpha = 1;
  measured = measure(); phase = "done";
}

function release() {
  if (phase !== "ready") return;
  if (still.matches) { finishInstantly(); writeData(); draw(); return; }
  phase = "run"; t = 0; s = 0; v = 0; dropped = 0; stamps = [C.START]; measured = null; inkAlpha = 1;
  writeData(); run();
}
function reset() {
  if (phase === "ready") return;
  if (still.matches) { phase = "ready"; s = 0; dropped = 0; squeeze = 0; stamps = []; measured = null; writeData(); draw(); return; }
  phase = "reset"; writeData(); run();
}

function tick(now) {
  const dt = last ? Math.min((now - last) / 1000, 1 / 30) : 1 / 60;
  last = now;
  if (touring) tour(dt);
  const a = accel();
  if (phase === "run") {
    t += dt;
    const tEnd = Math.sqrt(2 * C.RUN_M / a);
    const tt = Math.min(t, tEnd);
    s = 0.5 * a * tt * tt; v = a * tt; dropped = s;
    while ((stamps.length) * C.TICK_S <= tt + 1e-9) stamps.push(C.START + 0.5 * a * (stamps.length * C.TICK_S) ** 2 * C.UNITS_PER_M);
    if (t >= tEnd) { phase = "brake"; squeeze = (t - tEnd) * v * C.UNITS_PER_M; squeezeRate = v * C.UNITS_PER_M; measured = measure(); writeData(); }
  } else if (phase === "brake") {
    // el carrito comprime el resorte del tope (k = 4000 N/m, amortiguado) y se detiene
    const m = cartKg(), kSpring = 4000, damp = 2 * 0.7 * Math.sqrt(kSpring * m);
    for (let i = 0; i < 8; i++) {
      const xm = squeeze / C.UNITS_PER_M, vm = squeezeRate / C.UNITS_PER_M;
      const acc = xm > 0 ? (-kSpring * xm - damp * vm) / m : 0;
      squeezeRate += acc * C.UNITS_PER_M * dt / 8;
      squeeze += squeezeRate * dt / 8;
      if (squeeze < 0) { squeeze = 0; squeezeRate = 0; }
    }
    v = squeezeRate / C.UNITS_PER_M;
    if (Math.abs(squeezeRate) < 0.05 && squeeze < 0.02) { squeeze = 0; squeezeRate = 0; v = 0; phase = "done"; holdUntil = performance.now() + 2600; writeData(); }
  } else if (phase === "reset") {
    const k = 1 - Math.exp(-dt / 0.32);
    s += (0 - s) * k; dropped += (0 - dropped) * k; squeeze = 0; inkAlpha += (0 - inkAlpha) * Math.min(1, k * 2.5);
    if (s < 0.0004 && dropped < 0.0004) { s = 0; dropped = 0; stamps = []; measured = null; inkAlpha = 1; phase = "ready"; writeData(); if (pending) { pending = false; release(); } }
  }
  draw();
  const busy = phase === "run" || phase === "brake" || phase === "reset" || touring;
  frame = visible && busy ? requestAnimationFrame(tick) : 0;
}
const run = () => { if (!frame && visible) { last = 0; frame = requestAnimationFrame(tick); } };

// recorrido automático: duplicar F, luego aumentar m
const TOUR = [[1, 1], [3, 1], [3, 3], [1, 0]];
function tour(dt) {
  tourClock += dt;
  if (phase === "ready" && tourClock > 1.1) { tourClock = 0; release(); }
  else if (phase === "done" && performance.now() > holdUntil) {
    tourStep = (tourStep + 1) % TOUR.length;
    [discs, load] = TOUR[tourStep];
    showVariants(); tourClock = 0; reset();
  } else if (phase !== "ready") tourClock = 0;
}
function interact() {
  touring = false;
  clearTimeout(idleTimer);
  idleTimer = setTimeout(() => { if (!still.matches) { touring = true; tourClock = 0; run(); } }, 9000);
}
function choose(nextDiscs, nextLoad) {
  interact();
  if (nextDiscs === discs && nextLoad === load) return;
  discs = nextDiscs; load = nextLoad;
  showVariants();
  if (phase === "ready") { writeData(); draw(); } else reset();
}
function go() {
  interact();
  if (phase === "ready") release();
  else if (phase === "done") { pending = true; reset(); }
  else if (phase === "reset") pending = true;
}

document.querySelectorAll("[data-set-load]").forEach((b) => b.addEventListener("click", () => choose(discs, Number(b.dataset.setLoad))));
document.querySelectorAll("[data-set-discs]").forEach((b) => b.addEventListener("click", () => choose(Number(b.dataset.setDiscs), load)));
goButton.addEventListener("click", go);
stage.addEventListener("click", go);
stage.addEventListener("keydown", (event) => {
  let handled = true;
  if (event.key === "ArrowRight") choose(Math.min(C.MAX_DISCS, discs + 1), load);
  else if (event.key === "ArrowLeft") choose(Math.max(0, discs - 1), load);
  else if (event.key === "ArrowUp") choose(discs, Math.min(C.MAX_LOAD, load + 1));
  else if (event.key === "ArrowDown") choose(discs, Math.max(0, load - 1));
  else if (event.key === " " || event.key === "Enter") go();
  else handled = false;
  if (handled) event.preventDefault();
});
new IntersectionObserver((entries) => { visible = entries[entries.length - 1].isIntersecting; if (visible) run(); }, { rootMargin: "120px 0px" }).observe(stage);
window.__ct = { release, reset, choose, finishInstantly: () => { finishInstantly(); writeData(); draw(); }, state: () => ({ phase, s, measured, a: accel() }) };
showVariants(); writeData(); draw();
`;

const body = k.plateHtml({
  fig: "Fig 1",
  title: "Segunda ley de Newton",
  hint: "Clic o espacio para soltar",
  readout: "listo · pulsa Soltar",
  keys: [
    { mark: "lit", label: "Puntos de tinta: uno cada 0,1 s. Su separación crece porque el carrito acelera" },
    { mark: "raised", label: "Carrito (0,5 kg), barras de carga (0,5 kg c/u) y pesas ranuradas (50 g c/u)" },
  ],
  caption:
    "La pesa colgante tira del hilo con una fuerza F = m·g y arrastra todo el sistema: el carrito y la propia pesa, de masa total m. Al soltarlo, el temporizador marca la cinta cada 0,1 s. Como el carrito acelera, cada intervalo es más largo que el anterior en a·T², así que la aceleración se mide en la cinta y coincide con F/m. Duplica la pesa y la aceleración casi se duplica; carga el carrito y disminuye. Se desprecian el rozamiento y la masa de la polea y del hilo.",
  body: `<div class="iso-stage" tabindex="0" role="group" aria-label="Carrito en riel: flechas izquierda y derecha cambian la pesa, arriba y abajo cambian la carga, espacio suelta el carrito">${svg}</div>${controls}`,
});

const file = theme === "light" ? `${NAME}-light.html` : `${NAME}.html`;
const html = k
  .pageHtml({ title: "Segunda ley de Newton", theme, body, script: kitScript() + live, width: 720 })
  .replace('<html lang="en">', '<html lang="es">')
  .replace("</style>", `${CSS}</style>`);
writeFileSync(join(HERE, file), html);
console.log("wrote", file);
