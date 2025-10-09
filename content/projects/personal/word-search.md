---
title: Word Search | Ethan Colucci
---

# Freelance - Word Search

@[Word Search Video](https://www.youtube.com/embed/YrIWI2LO68M?)

#### Tech Stack
- Unity C#

#### Platforms
- Android

## Overview

A project I was hired to do when I did freelance on Fiver. It's a word search game that allows users to add their own list of words. Each puzzle is generated randomly for a unique experience each time.

The client wanted the ability for users to import their own words into the game, plus various ways to increase the difficulty. The game supports toggling diagonal words, backwards words and even rotated letters, if you're feeling especially mean.

This project is 4 years old, and really shows its age with regards to my skill level at the time. I'm planning a redevelopment of this project, both for a contrasting look at my new and old approaches, but also for my own enjoyment and maybe even an app store release.

## Under the Hood

### Scene Layout

I'm not a fan of how past me setup this project. In the 4 years since I completed this job I've learned a ton about Unity and how to work with its systems. The architecture of this project sidesteps challenges that working with Unity UI and input, but in turn introduces some limitations.

The app generates a grid of letters in word space. Each letter contains a canvas, which houses a Text Mesh Pro text object and the letter's decoration. In this case a white circle.

To select letters the user drags their finger accross their phone screen (or if on a PC, drag the mouse). The `Player Word Finder` component tracks the selected letters by using `RaycastAll` from the initial point of contact to the current point. This is the reason I opted to use word space objects instead of screen space. When the user lifts their finger the script checks the letters hit by the raycast and matches it with the word list.

![Raycast Demo](/images/projects/personal/word-search/word-search-batman.png)

One consequence of this is that it makes it challenging to accomodate different screen sizes. It also makes the creation of the game GUI to be less intuitive, since you need to design around an element that isn't a part of the canvas. Finally the whole solution isn't even that good. Or, to be more cheritable, it needs some more work to bring it to a point that current me would release it to a client or player.

Right now the raycast start exactly where the user puts their finger down, to exactly where they drag their finger to. It means that letters that can't be a part of the same word can be highlighted in a single selection.

![Raycast Failure](/images/projects/personal/word-search/word-search-bad-line.png)

If I do get around to redoing this project, and opt for the same selection method, I would do a few things simple differently (aside from handling the letter grid in a single canvas); First the raycast start and end points would snap to their nearest letters. This fixes the case where a user barely misses their intended start point. Second I would snap the raycast angle to the nearest 45 degrees, to prevent the illegal selections.

Beyond the core logic, I would also change the structure of the entire `Player Word Finder` script. Most of the logic is handled in the update callback, something I generally avoid these days. Today I would utilize a `RectTransform` and the `IPointerDown` and `IPointerUp` interfaces. The pointer down callback would trigger a coroutine that would handle the raycasting logic. The pointer up callback would flag the coroutine to finish and do the word processing logic.

### Grid Fill

Filling the letter grid is handled by the `Grid Generate` script. While there are certainly efficiency and logic improvements that could be added, the logic in this component is generally fine.

The GenerateGrid method creates a word search puzzle grid in Unity. It sorts the provided words by length, then attempts to place each word in the grid in a random direction (vertical, horizontal, or diagonal), allowing for backwards placement if enabled. If a word can't fit, it's skipped. After placing all possible words, the method fills remaining empty grid spaces with random letters and instantiates letter GameObjects for display. It also tracks which words were successfully placed and updates the relevant data structures. It checks for and handles cases like word overlap and grid boundaries.

In a rewrite I would look into ways I could improve the consistency of filling with the most words, or including an adjustable parameter that changes the word density.

## Links

::: row
[![Github Logo](/icons/github-mark-white.svg) GitHub](https://github.com/Ethanol2/WordSearch){class=fancy-btn}
:::

---

::: forced-row
::: column style="text-align:center"
[Previous](/projects/personal/road-to-olympus.html){class=fancy-btn style="width:75px;flex-direction:column;"}
:::
::: column style="text-align:center"
[Back](/./#Freelance-and-Personal){class=fancy-btn}
:::
::: column style="text-align:center"
[Next](/projects/personal/craft-wars.html){class=fancy-btn style="width:75px;flex-direction:column;"}
:::
:::