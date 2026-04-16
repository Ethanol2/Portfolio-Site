---
title: Book Organizer | Ethan Colucci
---

# Personal Projects - Book Organizer (Under Development)

![Book Organizer Banner](/images/projects/personal/book-organizer/book-organizer-library.jpg)

#### Tech Stack
- Golang Backend
    - SQLite Database
- Vue.js Frontend

#### Platforms
- Docker

## Overview

This project started as my capstone project and culmination of my Boot.Dev backend developer course. The goal of the project is to help me organize my book downloads on my nas. It's intended to run in Docker, with the backend built in Go and the frontend build using vue.js. It's one of the largest projects I've undertaken on my own, and I'm determined to complete it... even if it does take months..... or years. 

While I'm strictly not using an AI agent to write backend code, I am heavily utilizing Github's Copilot to help me construct the frontend. I made this decision because while I would like to learn node.js and all the frameworks that utilize it, it's not my focus professionally. That said, I'm trying not to be completely reliant; I strive to complete small changes and tweaks on my own, in an effort to gain an understanding of the code and as a safeguard against shortcomings in this approach.

## Features

### New File Scanning

The app periodically scans a configurable downloads folder for new book directories.

- The folder name
- Detected file types (audio files, ebook files, cover art, etc.)

From the UI, are able to view and will be able to manage this pending list.

### Book Library

Books are stored in a `books` table in SQLite. Once a pending download is associated with a book, the app will move its files into the library folder using a fixed structure, for example:

`Author/Series/Book Title/`

Currently the backend can make queries to Google Books and OpenLibrary.

### Frontend and Backend

- **Backend**: Go, exposing a RESTful HTTP API.
- **Frontend**: A Vue single-page application that interacts with the API to:
  - List pending downloads
  - Search and select metadata
  - Create and edit book entries
  - Trigger imports/moves

## Planned Features

### qBittorrent Integration (Nice-to-have)

After the core library flow is working, the app will integrate with qBittorrent to track labeled downloads. For completed torrents with a specific label (e.g. `books`), the app will automatically add them to the pending list. The frontend will also surface whether qBittorrent is reachable.

![Metadata View](/images/projects/personal/book-organizer/book-organizer-metadata.jpg)
![Metadata View](/images/projects/personal/book-organizer/book-organizer-downloads.jpg)

## Links
::: row
[![Github Logo](/icons/github-mark-white.svg) Github](https://github.com/Ethanol2/book-organizer){class=fancy-btn}
:::

---

::: forced-row
::: column style="text-align:center"
[Previous](/projects/no-fuss-tutors/no-fuss-tutors-project.html){class=fancy-btn style="width:75px;flex-direction:column;"}
:::
::: column style="text-align:center"
[Back](/./#Freelance-and-Personal){class=fancy-btn}
:::
::: column style="text-align:center"
[Next](/projects/personal/static-site-generator.html){class=fancy-btn style="width:75px;flex-direction:column;"}
:::
:::