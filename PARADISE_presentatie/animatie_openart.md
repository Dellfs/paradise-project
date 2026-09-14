# Tekenfilm over PARADISE — prompts voor OpenArt

Een animatiefilmpje van ongeveer 75 seconden, in tekenfilmstijl, met twee
personages en een verhaallijn. Negen scènes van elk 8 seconden.

Het verhaal: **opa Frans** wandelt graag met zijn kleindochter **Lotte**. Frans
heeft diabetes en voelt zijn voeten niet goed meer. Lotte ontdekt waarom dat
gevaarlijk is, en ze gaan samen kijken hoe het gemeten wordt.

Per scène staat er een **beeldprompt** (voor het stilstaande beeld) en een
**bewegingsprompt** (voor image-to-video). De voice-over is Nederlands en staat
eronder; de prompts blijven Engels, omdat de modellen daar beter op reageren.

---

## Stap 1 — Maak eerst je twee personages

Dit is de belangrijkste stap. Zonder vaste personages verandert je opa in elke
scène van gezicht. Maak van elk personage één referentiebeeld, sla het op, en
gebruik het in OpenArt als **Character** (of als reference image) bij élke
scène. Hou daarnaast overal hetzelfde seed aan.

**Opa Frans — characterprompt**

```
Character sheet of a friendly grandfather, around 70 years old, in 2D
hand-drawn cartoon style for a children's animation series. Round kind face,
short grey hair, neat grey moustache, small round glasses, rosy cheeks, warm
smile. Wearing a soft blue cardigan over a white shirt, comfortable dark
trousers and sturdy grey walking shoes. Friendly and a little clumsy.
Full body, neutral standing pose, front view and side view on a plain white
background. Clean thick outlines, flat cel shading, no gradients.
```

**Lotte — characterprompt**

```
Character sheet of a cheerful girl, about 8 years old, in the same 2D
hand-drawn cartoon style for a children's animation series. Brown hair in two
short braids, big curious eyes, freckles, wide grin. Wearing a bright green
hoodie, orange sneakers and blue jeans. Energetic, always a step ahead.
Full body, neutral standing pose, front view and side view on a plain white
background. Clean thick outlines, flat cel shading, no gradients.
```

## Stap 2 — De stijlregel, achter élke scèneprompt

```
Style: 2D hand-drawn cartoon, children's animation series, clean thick
outlines, flat cel shading, expressive faces, simple friendly backgrounds,
warm and cheerful. Colour accents in blue, green and orange. Bright even
lighting, no gradients, no photorealism. 16:9. No text, no letters, no
numbers, no logos.
```

## De negatieve prompt — overal hetzelfde

```
text, letters, words, numbers, watermark, logo, signature, subtitles,
photorealistic, 3D render, anime, horror, scary, gore, blood, wounds, open
sores, ulcers, injury, amputation, hospital gore, sad mood, distorted faces,
extra fingers, extra limbs, deformed hands, creepy smile, dark colours
```

> Die woorden over wonden zijn er niet voor niets. Vraag je een model iets
> rond "diabetic foot", dan maakt het uit zichzelf beelden die je niet aan een
> zaal met kinderen wil tonen.

## Instellingen

| Wat | Waarde |
| --- | --- |
| Beeldverhouding | 16:9 |
| Duur per clip | 8 seconden |
| Seed | kies er één en hou hem vast over alle negen scènes |
| Personages | referentiebeeld uit stap 1 bij elke scène meegeven |
| Beweging | laag tot midden |

---

## Scène 1 — Wandelen in het park

**Beeld**

```
Grandfather Frans and his granddaughter Lotte walking together along a sunny
park path, seen from the side. Lotte skips ahead and looks back laughing,
Frans follows with a warm smile. Green trees, a bench, a few birds, blue sky.
+ stijlregel
```

**Beweging**

```
They walk from left to right along the path. Lotte skips and turns her head
back to Frans. Leaves move gently in the wind. Slow camera pan following them.
```

**Voice-over** — "Dit is opa Frans. En dit is Lotte. Samen wandelen ze elke
zondag — tienduizend stappen, zonder erbij na te denken."

---

## Scène 2 — Het legoblokje

**Beeld**

```
Cosy living room. Lotte stands on one foot holding her other foot, mouth wide
open in a comic yelp, a single bright orange toy brick on the floor beside
her. Next to her, Frans stands calmly on an identical toy brick without
noticing anything, still smiling. Exaggerated cartoon expressions, small
comic motion lines above Lotte.
+ stijlregel
```

**Beweging**

```
Lotte hops on one foot and grabs her toe with a comic bounce. Frans stays
completely still and calm, then looks down puzzled at his own foot. Camera
holds steady, slight zoom in on Frans looking down.
```

**Voice-over** — "Lotte voelt het meteen. Opa Frans voelt niets. Door diabetes
geven de zenuwen in zijn voeten geen seintje meer."

---

## Scène 3 — In de schoen

**Beeld**

```
Cutaway side view of grandfather Frans's shoe while he stands, drawn like a
friendly illustration in a children's book. Inside the shoe, one small area
under the ball of the foot glows warm orange with cartoon heat lines around
it. Frans's face visible above, calm and unaware. Simple pale background.
+ stijlregel
```

**Beweging**

```
The orange area under the ball of the foot pulses slowly twice, with small
cartoon heat lines rising. Frans above keeps smiling, unaware. Slow push-in
on the glowing spot.
```

**Voice-over** — "Maar er is wel iets aan de hand. Op één plekje duwt zijn voet
veel te hard. Als een steentje dat er altijd in zit."

---

## Scène 4 — Naar het ziekenhuis

**Beeld**

```
Bright friendly clinic room with a large window. A smiling clinician in a
light blue uniform holds up a thin flexible insole covered in tiny dots.
Frans sits on a chair with one shoe off, curious. Lotte leans forward wide
eyed, pointing at the insole. Clean simple room, a plant in the corner.
+ stijlregel
```

**Beweging**

```
The clinician turns the insole slowly so it catches the light. Lotte leans in
further and points. Frans nods. Gentle camera push-in on the insole.
```

**Voice-over** — "Dus gaan ze kijken. In het ziekenhuis krijgt opa een
flinterdunne zool met negenennegentig kleine voelertjes, gewoon in zijn eigen
schoen."

---

## Scène 5 — Wandelen met kleuren

**Beeld**

```
Frans walking along a short indoor walkway in the clinic, side view, with a
small device clipped to his belt. Behind each of his steps a colourful cartoon
footprint stays on the floor: blue at the heel, bright orange under the ball
of the foot. Lotte walks alongside, clapping, counting on her fingers. The
clinician watches with a tablet.
+ stijlregel
```

**Beweging**

```
Frans walks steadily from left to right. With every step a coloured footprint
pops onto the floor behind him and stays. Lotte skips beside him clapping.
Tracking shot following the walk.
```

**Voice-over** — "Hij wandelt tien meter. Honderd metingen per seconde, bij elke
stap. Na één minuutje weten ze precies waar het knelt."

---

## Scène 6 — De rode plek op het scherm

**Beeld**

```
Lotte and Frans standing in front of a large friendly screen on a stand. On
the screen a simple cartoon pressure map of a foot sole: mostly cool blue
squares with one bright red-orange area under the ball of the foot. Lotte
points at the red spot with a surprised open mouth, Frans raises his eyebrows.
The clinician stands beside them smiling.
+ stijlregel
```

**Beweging**

```
Lotte raises her arm and points at the red spot on the screen. The red area
pulses gently. Frans leans in. Camera slowly pushes past their shoulders
towards the screen.
```

**Voice-over** — "En daar is het. Rood is waar het duwt. Alles boven
tweehonderd is te veel — en precies daar zou een wonde ontstaan."

---

## Scène 7 — De zool op maat

**Beeld**

```
Warm cosy workshop. A friendly shoemaker in an apron shapes a custom insole at
a wooden workbench, with tools and layers of coloured material around. Frans
and Lotte watch from the other side of the bench, Lotte standing on her toes
to see over it. Wood tones, soft warm light.
+ stijlregel
```

**Beweging**

```
The shoemaker presses and shapes the insole with both hands, then holds it up
proudly. Lotte rises on her toes and her eyes go wide. Slow push-in on the
finished insole.
```

**Voice-over** — "Dan maakt de schoenmaker een zool op maat. Eentje die de druk
weghaalt van net dat plekje dat het niet meer aankan."

---

## Scène 8 — Het rood koelt af

**Beeld**

```
Same screen as before, same framing. The cartoon pressure map of the foot sole
is now evenly cool blue and green across the whole sole, with no red area at
all. Lotte throws both arms in the air cheering, Frans laughs out loud, the
clinician gives a thumbs up. Small cartoon sparkles around the screen.
+ stijlregel
```

**Beweging**

```
The last traces of red fade away and spread into calm blue across the sole.
Lotte throws her arms up and jumps. Frans laughs. Sparkles pop briefly.
Camera holds steady.
```

**Voice-over** — "En kijk. De rode plek is weg. De druk zit niet meer op één
plekje, maar verdeeld over de hele voet."

---

## Scène 9 — Weer samen op pad

**Beeld**

```
The same sunny park path as the opening scene, seen from the side. Frans and
Lotte walking together again, Frans with a confident spring in his step, Lotte
holding his hand and looking up at him. Golden afternoon light, long soft
shadows, birds in the sky. Wide open composition with space on the right.
+ stijlregel
```

**Beweging**

```
They walk from left to right, hand in hand, at an easy pace. The camera slowly
pulls back to a wide shot of the park. Warm light, gentle breeze in the trees.
```

**Voice-over** — "Werkt dat echt? Dat zoeken zes Belgische ziekenhuizen nu
samen uit, ook AZ Groeninge in Kortrijk. Wat we tot nu toe schatten, gaan we
eindelijk meten."

---

## Wat er niet in mag

Twee dingen zijn inhoudelijk belangrijk, en een generator verzint ze anders
zelf:

- **Geen resultaten.** De studie loopt nog niet. Het filmpje mag laten zien
  hoe we meten, niet dat het werkt. Daarom eindigt scène 9 op een vraag.
- **Geen wonden, geen amputaties.** Vandaar de negatieve prompt. Het
  legoblokje in scène 2 legt neuropathie even goed uit, en een kind schrikt er
  niet van.

De getallen in de voice-over kloppen met het protocol: negenennegentig sensoren
per zool, honderd metingen per seconde, tweehonderd kilopascal als grens, zes
centra. Laat ze zo staan.

## Praktisch

- **Muziek**: iets lichts en vrolijks, geen dramatiek. De scène met het
  legoblokje mag een kort komisch accent krijgen.
- **Voice-over**: samen ongeveer 150 woorden, dat is zo'n 70 seconden op een
  rustig tempo. Spreek hem zelf in als je kan — een echte stem werkt beter
  dan een gegenereerde.
- **Montage**: zet de negen clips gewoon achter elkaar, met een korte
  overvloeier. Scène 6 en 8 zijn hetzelfde kader, dus daar werkt een harde
  snit net beter: de zaal ziet het rood verdwijnen.
