# My-Portfolio-Site
**STILL A WORK IN PROGRESS!**

This is a custom markdown to html static site generator to show off my skills and work.

This project extends the project [Static Site Generator](https://github.com/Ethanol2/Static-Site-Generator) created with the boot.dev course.

## What's New
I've extended the original project with these features
- Youtube embeding using custom markdown syntax "@\[My Youtube Video](https://www.youtube.com/watch?v=dQw4w9WgXcQ)"
- CSV interpretation, with the options to include headers or not, and the option to have markdown within cell content. Custom markdown syntax for a basic table:
    ::: csv
    "Cell 1","Cell 2","Cell 3"
    :::

  I plan on having csv file importing eventually.
- Custom tags for images. For example "\!\[This is an image]("img link"){height=300}" will become "\<img src="img link" alt="This is an image" height="300"/>".
