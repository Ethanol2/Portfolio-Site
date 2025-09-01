---
title: Static Site Generator | Ethan Colucci
---

# Personal Projects - Static Site Generator

![Static Site Generator](/images/projects/personal/static-site-generator/website-project.jpg)

#### Tech Stack
- Python 3

## Overview

What started as a [guided project I created with the boot.dev course](https://github.com/Ethanol2/Static-Site-Generator) turned into a relatively massive undertaking to transform it into something a lot bigger. I used my version to build this website, and I'm very happy with the results.

::: row
::: column
### Original Features

- **Markdown Parsing**
    - **Block Syntax**
        - Headings  
        - Paragraphs  
        - Unordered & Ordered Lists  
        - Block Quotes  
        - Code Blocks  
    - **Text Formatting Syntax**
        - **Bold**  
        - *Italic*  
        - `Inline code`  
        - [Links](/projects/personal/static-site-generator.html#Overview)  
        - ![Images](/images/projects/personal/static-site-generator/an-image.jpg){style="max-height:20px"}

- **Export to HTML template**
:::
::: column
### Added Features

- **Extended Markdown Parsing**
    - **Tables**
        - Standard Syntax  
        - CSV Syntax (supports full markdown parsing inside cells)  
    - Horizontal Rules  
    - Passthrough Syntax: `{This text will not be parsed}`  
        - Useful for custom HTML inserts and formatting  
    - YouTube Embedding  
        - Converts normal YouTube links into embed code  
    - Custom tags on links, images, and YouTube embeds  
        - Example: `![Alt text](example.com/img.png){class=my-special-css}`  
    - Custom Class Blocks: `::: custom`  
        - Example use: layout formatting (e.g., previous/back/next buttons)  

- **Nested Text Parsing**
  - `**This bold text can also be *italic*.**` → **This bold text can also be *italic*.**

- **YAML Properties in Markdown Pages**
  - Title (falls back to main heading if missing)  
  - HTML Template (falls back to default)  

- **Multiple Template Handling**

- **JavaScript File Handling**
  - Automatically adds JS file references to templates  

- **Header & Footer Generation**
  - Controlled via YAML files
:::
:::

You can see the full markdown syntax guide on the GitHub repo.

## Links
[![Github Logo](/icons/github-mark-white.svg) GitHub](https://github.com/Ethanol2/Portfolio-Site){class=fancy-btn}

---

::: forced-row
::: column style="text-align:center"
[Previous](/projects/no-fuss-tutors/no-fuss-tutors-project.html){class=fancy-btn style="width:75px;flex-direction:column;"}
:::
::: column style="text-align:center"
[Back](/./#Freelance-and-Personal){class=fancy-btn}
:::
::: column style="text-align:center"
[Next](/projects/personal/snake-game.html){class=fancy-btn style="width:75px;flex-direction:column;"}
:::
:::