# Freesia
> Freesia is a simple way to create Graphical user interfaces in Qt

 - Qt can be annoying and unfriendly to new programmers Freesia aims to combat that by using syntax similar to tkinter while providing the power of Qt.
 - It provides a neat way of binding events and styling widgets
 

### Examples
##### Example 1
```
from freesia import *
root = Window()
mainloop()
```
##### Example 2
```
from freesia import *
random_theme = get_theme()
root = Window(title="Example", bg=randon_theme[0])
label = Label(root, text="Hello World!")
label.place(0.5, 0.5, anchor="CENTER")
mainloop()
```

### Documentation
https://lukegw.com/freesia/docs

### Installation
As of version 3.3.0, you can simply install freesia by using `pip`:
```
pip install freesia
```

### Updating
As of version 3.3.0, updating freesia is as easy as:
```
pip install freesia -U
```

### Changelog
The changelog can be viewed in `CHANGELOG.md`

### License
This project is under the `GNU LGPL v2` license
Please see `LICENSE` file for more details