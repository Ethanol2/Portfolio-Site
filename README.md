# My-Portfolio-Site
**STILL A WORK IN PROGRESS!**

This is a custom markdown to html static site generator that I'm using to build my portfolio website.

It's coded using Python, with the os, re and yaml libraries.

This project extends the project [Static Site Generator](https://github.com/Ethanol2/Static-Site-Generator) created with the boot.dev course.

# Installation and Use
At the moment it's a matter of cloning this project and replacing the content in `content`, `data` and `static` folders with your own. HTML templates are stored in the `templates` folder. Right now you need python3 to run the program from the shell, who's entry point is in main.py.

`python3 main.py "optional path"`

If no path is supplied it will use the directory the shell is running from.

# User Guide

## Header and Footer Content
Currently the header and footer html is entirely generated from yaml files. The ability to use partials is on the list of features I plan on adding. See the yaml guide bellow.

## Body Content
Pages are converted from markdown (see the markdown syntax guide bellow). All markdown content should be in the `content` folder. The folder structure is preserved when parsed and writen to the `docs` folder

### Metadata
Metadata is added with a yaml block at the top of the page

```yaml
title: My Special Page
layout: MySpecialTemplate
```

Currently the only metadata the SSG uses is `title` and `layout`.
If no title is provided, then the SSG will check for the title heading (`# Title Heading`) on the page. If no title heading is found the title will be blank.
If no template is provided then the default will be used.

### Page Example
```markdown
---
title: Hello!
layout: template2
---

# This is my Title Header!
This is page is pretty empty though...
```

## Templates
HTML templates are added into the `templates` folder. If you want to choose your default template, it should be named "default.html". Otherwise the SSG will assign the first template in the folder to be default.

The SSG looks for 5 fields to replace in the html template. Simply ommit a field if you want the template to provide that html explicitly.
```
{{ Title }}
{{ Header }}
{{ Content }}
{{ Footer }}
{{ JavaScript }}
```

## Javascript, CSS, Images, etc Files
All files and folders in the `static` folder are copied to the `docs` folder. Javascript files will be referenced by replacing the `{{ Javascript }}` tag in the html template. 

## Markdown Syntax Guide

This site generator supports (mostly) standard Markdown plus some extras.

---

### Headings

Use `#` at the start of a line (1–6 levels):

```markdown
# Heading 1
## Heading 2
### Heading 3
```

---

### Text Formatting

* **Bold**: `**bold**`
* *Italic*: `_italic_` or `*italic*`
* `Inline code`: `` `code` ``
* > Blockquote: `> quoted text`

---

### Lists

* Unordered list:

  ```markdown
  - Item 1
  - Item 2
  ```
* Ordered list:

  ```markdown
  1. First
  2. Second
  ```

---

### Code Blocks

Use triple backticks:

<pre>
```
# Some python code
def hello():
    return "world"
```
</pre>

---

### Links

Normal markdown for links:

```markdown
[My Github](https://github.com/Ethanol2)
```

```html
<a href="https://github.com/Ethanol2">My GitHub</a>
```


You can also add attributes:

```markdown
[My Github](https://github.com/Ethanol2){target="_blank" class="external"}
```

```html
<a href="https://github.com/Ethanol2" target="_blank" class="external">My GitHub</a>
```

---

### Images

```markdown
![Alt text](https://example.com/image.png)
```

With attributes:

```markdown
![Logo](logo.png){class="logo-img" width="200"}
```

---

### Linked Images

Images can also be links:

```markdown
[![Preview](thumb.png)](https://example.com/page)
```

---

### YouTube Embeds

Embed full or shortened YouTube links:

```markdown
@[youtube](https://www.youtube.com/watch?v=dQw4w9WgXcQ)
```

With attributes (e.g. for styling):

```markdown
@[youtube](https://www.youtube.com/watch?v=dQw4w9WgXcQ){class="video" width="560"}
```

---

### Custom Blocks

This site generator supports a simple syntax for creating custom `<div>` blocks in your Markdown.  
Blocks begin with `:::` followed by a class name, and end with another `:::`.  

Everything inside the block is wrapped in a `<div>` with that class.

#### Basic Usage
```markdown
::: note
This is a highlighted note.
:::
```

---

#### Nested Blocks

Blocks can be nested, which is useful for layouts:

```markdown
::: row
::: column
Left content
:::
::: column
Right content
:::
:::
```
---

#### Wrapping Other Blocks

You can wrap other custom blocks (like CSV tables):

```markdown
::: special-table
::: csv_headers
Name,Score
Alice,10
Bob,8
:::
:::
```

---

#### CSV Tables

Two special block types turn CSV text into tables:

##### Without headers

```markdown
::: csv
a,b,c
1,2,3
:::
```

##### With headers

```markdown
::: csv_headers
Name,Age
Alice,30
Bob,25
:::
```

---

### Tables

I plan on adding support for standard markdown tables... eventually

---

### Horizontal Rules

```markdown
---
```

---

### Passthrough HTML

Wrap text in `{}` to prevent parsing.
The contents are inserted into the final HTML untouched.

```markdown
This is raw {<b>HTML</b>} passthrough.
```

---

### Notes

* Attributes (`{class="..."}` etc.) can be applied to **images, links, and YouTube embeds**.
* Malformed attribute braces (missing `}`) are treated like normal content. This means they could wreck havok on the rest of your content.
* Empty passthrough `{}` produces nothing in the output.

## Yaml Guide for Header and Footer

### 1. Basic Structure

Each HTML element is written as a **YAML key**:

```yaml
header.site-header:
  h1.logo: "My Site"
```

* `header` → the HTML tag
* `.site-header` → the class (optional)
* `"My Site"` → text content inside the element

Produces:

```html
<header class="site-header">
  <h1 class="logo">My Site</h1>
</header>
```

---

### 2. Nesting Elements

Indentation means "this element is inside the one above it":

```yaml
div.wrapper:
  p: "Welcome to my site!"
```

Becomes:

```html
<div class="wrapper">
  <p>Welcome to my site!</p>
</div>
```

---

### 3. Attributes

You can add attributes by writing them under the element:

```yaml
img.logo:
  src: images/logo.png
  alt: My Logo
```

Becomes:

```html
<img class="logo" src="images/logo.png" alt="My Logo" />
```

---

### 4. Multiple Children

If an element has **multiple child elements or text nodes**, use a list (`-`):

```yaml
h1.title:
  - img.icon:
      src: icons/star.svg
      alt: Star
  - " My Site"
```

Becomes:

```html
<h1 class="title">
  <img class="icon" src="icons/star.svg" alt="Star" /> My Site
</h1>
```

---

### 5. Links

Links are simplified: just write the **URL as the key**, and the label as the value.

```yaml
nav.nav-links:
  - "./": Home
  - "about.html": About
  - "contact.html": Contact
```

Becomes:

```html
<nav class="nav-links">
  <a href="./">Home</a>
  <a href="about.html">About</a>
  <a href="contact.html">Contact</a>
</nav>
```

---

### 6. Links with Icons or Extra Settings

If a link has an **icon or attributes**, use a map instead of plain text:

```yaml
nav.contact-links:
  - "https://github.com/me":
      target: _blank
      img:
        src: icons/github.svg
        alt: GitHub
  - "mailto:me@example.com":
      label: "me@example.com"
```

Becomes:

```html
<nav class="contact-links">
  <a href="https://github.com/me" target="_blank">
    <img src="icons/github.svg" alt="GitHub" />
  </a>
  <a href="mailto:me@example.com">me@example.com</a>
</nav>
```

---

### 7. Buttons and Other Elements

Buttons work just like any other element. Children can be elements or spans:

```yaml
button.hamburger:
  aria-label: Toggle menu
  - span
  - span
  - span
```

Becomes:

```html
<button class="hamburger" aria-label="Toggle menu">
  <span></span>
  <span></span>
  <span></span>
</button>
```

---

### 8. Text vs. Elements

* If you write a **string** → it becomes text.
* If you write a **mapping** → it becomes an element.

Example:

```yaml
p:
  - "Hello "
  - strong: "World"
```

Becomes:

```html
<p>Hello <strong>World</strong></p>
```

---

### 9. General Tips

Use indentation carefully (2 spaces per level recommended).
Use quotes around values **only if they contain special characters** (`:`, `@`, `#`, etc.).
Remember: **plain strings = text, mappings = elements**.
Classes are always written as `tag.class`.

