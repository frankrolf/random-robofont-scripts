## anchorBaby.py

RoboFont script for keeping anchors consistent.

Inspired by an idea from James T. Edmondson, this script will take note of an 
anchor movement in a given glyph, and replicate that movement in all dependent
glyphs.  

For instance, if a font has the glyphs `a` `a.init` and `a.fina`; and all three 
have an anchors named “top”; any dragging of that anchor will be replicated 
in all the dependent glyphs.  
It does not matter which glyph the anchor is dragged in. Anchor names also
do not matter, as long as they are consistent among dependent glyphs.

Ideally, this script is run as a RoboFont startup script.

Writing this was a good trip into the world of observers.
Thanks for the opportunity, James! :-)
