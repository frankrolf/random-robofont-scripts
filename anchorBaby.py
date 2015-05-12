'''
anchorBaby.py
-------------

Inspired by an idea from James T. Edmondson, this script will take note of an 
anchor movement in a given glyph, and replicate that movement in all dependent
glyphs.
For instance, if a font has the glyphs /a, /a.init and /a.fina; and all three 
have an anchors named "top"; any dragging of this anchor will be replicated 
in all the other glyphs. This way, anchor positions stay consistent.

It does not matter which glyph the anchor is dragged in. Anchor names also
do not matter, as long as they are consistent among dependent glyphs.

This was a good trip into the world of observers.
Thanks for the opportunity, James! :)
'''

from mojo.events import addObserver, removeObserver


class AnchorWatcher(object):

    def __init__(self, anchor):
        self.anchor = anchor
        self.glyph = self.anchor.getParent()
        self.font = self.glyph.getParent()
        self.friends = self.findFriends(self.glyph.name)
        self.anchor.addObserver(self, "anchorChangedCallback", "Anchor.Changed")
        # print 'added observer for anchor', '"%s"' % self.anchor.name, 'in', self.glyph.name


    def unsubscribe(self):
        self.anchor.removeObserver(self, "Anchor.Changed")
        # print 'removed observer for anchor', '"%s"' % self.anchor.name, 'in', self.anchor.getParent().name


    def findFriends(self, glyphName):
        '''
        Find all glyphs that share the same name before the dot,
        except the main glyph.
        e.g. ['a', 'a.alt', 'a.norm', 'a.fina', 'a.whatever'].
        '''
        baseGlyphName = glyphName.split('.')[0]
        return [g.name for g in self.font if g.name.split('.')[0] == baseGlyphName and not g.name == glyphName]


    def anchorChangedCallback(self, sender):
        for glyphName in self.friends:
            for anchor in self.font[glyphName].anchors:
                if anchor.name == self.anchor.name:
                    anchor.position = self.anchor.position



class GlyphWatcher(object):
    def __init__(self):
        self.observedGlyphs = {}
        addObserver(self, "glyphObserver", "currentGlyphChanged")


    def glyphObserver(self, info):
        activeGlyph = info['glyph']
        if activeGlyph:
            self.observedGlyphs.setdefault(activeGlyph.name, [])
        
        for gName in self.observedGlyphs.keys():
            if gName == activeGlyph.name:
                'Collect Anchor observer objects for the active glyph.'
                for anchor in activeGlyph.anchors:
                    aw = AnchorWatcher(anchor)
                    self.observedGlyphs[gName].append(aw)
            else:
                'Unsubscribe from Anchor observer objects in inactive glyphs.'
                for observer in self.observedGlyphs[gName]:
                    observer.unsubscribe()
                del self.observedGlyphs[gName]
                

GlyphWatcher()
