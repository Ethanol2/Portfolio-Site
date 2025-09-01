---
title: "VRV Megger Testing | Ethan Colucci"
---

# VR Vision - Megger Testing & Generator Fan Motor Replacement VR Training

@[VR Vision Megger Testing & Generator Fan Motor Replacement VR Training](https://www.youtube.com/watch?v=TUBfFgAgtE4)

#### Tech Stack
- Unity
- Meta/Oculus VR
- Photon Pun Multiplayer

## Overview

This training is the first of two modules created mostly by myself as part of a series of five modules for a client. The other module that I focused on was the [Proportional Valve Replacement Training](/projects/vr-vision/vr-vision-prop-valve-replacement.html). This project was created early in my time with the company, and I would take the lead of developing and improving multiple packages used within.

### Electronic Tools
The electronic tools package mainly includes the multimeter, megger and amp clamp simulations seen in this module, and its siblings. It's extensible so that the base class for the tools can be reused for any custom equipment required. It handles interactions with "electronic points" that are quick to setup. Parts can be designated ground, negative, positive, charged and a number of other modifiers. 

### Fasteners and Animated Tools
The fastener and tool system on is used in many projects that I participated in. It allows the designer to fully custimize the carateristics of a fastener, by using the real measurements. The tool uses this information to modulate how it animated, whether that's a simple rotation of the mesh or an animation done in Unity's animator. When I left the company it was fully capable with Photon's Fusion multiplayer system.

---

::: forced-row
::: column style="text-align:center"
[Previous](/projects/vr-vision/vr-vision-railcar.html){class=fancy-btn style="width:75px;flex-direction:column;"}
:::
::: column style="text-align:center"
[Back](/./#VR-Vision){class=fancy-btn}
:::
::: column style="text-align:center"
[Next](/projects/vr-vision/vr-vision-prop-valve-replacement.html){class=fancy-btn style="width:75px;flex-direction:column;"}
:::
:::