---
title: "VRV Tutorial | Ethan Colucci"
---

# VR Vision - Tutorial

@[VR Vision Tutorial](https://www.youtube.com/watch?v=WkB_i6dFh8c)

#### Tech Stack
- Unity
- Meta/Oculus VR

## Overview

I refactored the VR Vision tutorial in summer 2024, adding some new elements and removing others. The cannon was my idea, and with some workshopping, I implemented it as a demo for some of the interactions users will face.

### The Canon
The cannon uses a custom bllistics system I created for another internal project. It's frankly overkill for its use here, but it gets the job done. The system can accurately simulate projectiles based on a lookup table of how the given projectile behaves in reality, in combination with the specs of the firearm its being launched from. Unfortunately this is only the second time the system was used, since there aren't really any use cases for it normally.

### Fasteners and Animated Tools
The fastener and tool system on is used in many projects that I participated in. It allows the designer to fully custimize the carateristics of a fastener, by using the real measurements. The tool uses this information to modulate how it animated, whether that's a simple rotation of the mesh or an animation done in Unity's animator. When I left the company it was fully capable with Photon's Fusion multiplayer system.

---

::: forced-row
::: column style="text-align:center"
[Previous](/projects/personal/craft-wars.html){class=fancy-btn style="width:75px;flex-direction:column;"}
:::
::: column style="text-align:center"
[Back](/./#VR-Vision){class=fancy-btn}
:::
::: column style="text-align:center"
[Next](/projects/vr-vision/vr-vision-railcar.html){class=fancy-btn style="width:75px;flex-direction:column;"}
:::
:::