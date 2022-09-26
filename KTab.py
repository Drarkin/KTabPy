TEMPLATE_SVG_RCT=r'<rect x="{p_x}" y="{p_y}" width="{p_w}" height="{p_h}" style="fill:rgba({p_fc});stroke-width:2;stroke:rgba(0,0,0)" />'
TAMPLATE_SVG_LINE=r'  <line x1="{p_x1}" y1="{p_y1}" x2="{p_x2}" y2="{p_y2}" style="stroke:rgba({p_ln});stroke-width:{p_lw}" />'
TEMPLATE_SVG_CRICLE=r' <circle cx="{p_cx}" cy="{p_cy}" r="{p_cr}" style="fill:rgba({p_nf});stroke-width:{p_cw};stroke:rgba({p_cc})" />'
DEFAULT_BASE_COLOR=r'100,200,255'
DEFAULT_MAIN_COLOR=r'100,255,100'
NOTE_COLOR_PALLETE={
    None:{
    'p_nf':'0,0,0',#note fill color
    'p_cc':'0,0,0',# note circle color
    'p_ln':'0,0,0'# note line color
    
    },
    1:{
    'p_nf':'255,255,255',#note fill color
    'p_cc':'0,0,0',# note circle color
    'p_ln':'0,0,0,0'# note line color
    },
    1/8:{
    'p_nf':'100,0,100',#note fill color
    'p_cc':'100,0,100',# note circle color
    'p_ln':'100,0,100'# note line color
    }
#id
   }


class ktab:
    DEFAULT_DIM=50
    note_feet_offset_ratio = .4
    note_line_wid=5
    higlight_note = 3
    type=17
    levels=1 # invaqlid recalc
    dim = 10
    heigth_unit= 8
    background=[]
    offset_x=20+dim
    note_ratio_size = .65
    line_ratio = 1 
    
    def __background_note(obj,cur_lvl, mirror=False):
        offset_extra = 2*(obj.levels-cur_lvl) if mirror else 0
        id = (obj.levels- cur_lvl) * ( 1 if mirror else -1)
        # selects color to use
        if id in list(NOTE_COLOR_PALLETE.keys()):
            fillcolor = DEFAULT_BASE_COLOR
        elif (cur_lvl+1)%obj.higlight_note == 0:
            fillcolor = DEFAULT_MAIN_COLOR
        else:
            fillcolor = DEFAULT_BASE_COLOR
        return {
        'p_x':obj.offset_x + (cur_lvl+offset_extra) * obj.dim,
        'p_y': 0,
        'p_w': obj.dim,
        'p_h': ( cur_lvl / 2 +obj.heigth_unit ) * obj.dim,
        'p_fc':fillcolor,
        'id': id
        }
    
    def calc_note_background(self,cur_lvl):
        self.background.append(ktab.__background_note(self, cur_lvl))
        if cur_lvl == self.levels:
            return 
        self.calc_note_background(cur_lvl+1)
        self.background.append(ktab.__background_note(self, cur_lvl, mirror=True))
        return
    
    def get_line(self, hlvl=0, end=False):
        hlvl = self.heigth_unit if end else hlvl # force end line to be at top
        y= (self.heigth_unit - hlvl -.5 ) * self.dim if not end else self.dim
        return{
        'p_x1':self.offset_x,
        'p_x2':self.offset_x+self.type*self.dim,
        'p_y1':y,
        'p_y2':y,
        'p_ln':r'0,0,0',
        'p_lw':8 * (2 if end else 1) * self.line_ratio
        }
    def rinit(self):
        
        self.offset_x=20+self.dim
        self.background=[]
        self.levels = ( ktab.type -1 ) / 2
        self.calc_note_background(0)
        self.line_ratio= self.dim /self.DEFAULT_DIM
        return
    
    def get_note(self, id, type, time,r=None):
        y_offset = self.heigth_unit-1
        r= r if r else self.note_ratio_size
        radius = self.dim/2 * r
        locus = (y_offset-time)*self.dim+ 0.5*self.dim
        line_width = self.note_line_wid * r
        # By type
        if type in list(NOTE_COLOR_PALLETE.keys()):
            pallete = NOTE_COLOR_PALLETE[type]
        else:
            pallete = NOTE_COLOR_PALLETE[None]
        floor = 2 if type == 1/8 else 1 # diffrent floor for eighth notes
        x1_offset = self.offset_x - (self.note_feet_offset_ratio * floor) *self.dim
        aux =  { 
            #line
            'p_x1':x1_offset,
            'p_x2':self.offset_x+(self.type/2+id)*self.dim,
            'p_y1':locus-radius,
            'p_y2':locus-radius,
            'p_ln':r'0,0,0',
            'p_lw':line_width * self.line_ratio,
            #curcle
            'p_cx':self.offset_x+(self.type/2+id)*self.dim,
            'p_cy':locus,
            'p_cw':line_width * self.line_ratio,
            'p_cr':  radius
        }  
        aux.update(pallete)
        return aux
    
    def __init__(self):
        return

def pnote(id, type, time):
    global CKTAB
    note =  CKTAB.get_note(id, type, time)
    print(TEMPLATE_SVG_CRICLE.format(**note))
    print(TAMPLATE_SVG_LINE.format(**note))

def pline (hvl=0,end=False):
    global CKTAB
    print(TAMPLATE_SVG_LINE.format(**CKTAB.get_line(hvl,end)))
    

def test():
    ktab.dim = 50 # overwrite default
    a = ktab()
    a.rinit()
    global CKTAB
    CKTAB = a
    for note in a.background:
        print(TEMPLATE_SVG_RCT.format(**note))
    
    print(TAMPLATE_SVG_LINE.format(**a.get_line()))
    
    print(TAMPLATE_SVG_LINE.format(**a.get_line(end=True)))
    
    note =  a.get_note(1,1/3,0)
    print(TEMPLATE_SVG_CRICLE.format(**note))
    print(TAMPLATE_SVG_LINE.format(**note))
    pnote(0,.25,0)
    pnote(6,1/8,1)
    pnote(-3,1/4,1)
    pnote(1,1/3,0)
    
    pnote(-8,.25,0)
    pnote(-7,1/8,1)
    pnote(-6,1/4,2)
    pnote(-5,1/3,3)
    pline(4)
    pnote(-4,1/4,4)
    pnote(-3,1,5)
    pnote(-2,1/2,6)
    pnote(-1,1/4,5)


#test()


####################################################################################
## Aux Class to try organize music notes/sheet objects
####################################################################################

############################################
# Music Note ###############################

class MNote:
    def __init__(self,tune,duration):
        if duration not in [1,1/2,1/4,1/8]:
            raise Exception('Given note duration not allowed, review documentation')
        self.tune=tune
        self.type=duration
        self.value = 4* duration
        return
    
    def DEFAULT_DIC():
        # Not tune translations to ktab columns
        return {
            "2''":-8,'2"':-8,
            "7'":-7,
            "5'":-6,
            "3'":-5,
            "1'":-4,
            "6":-3,
            "4":-2,
            "2":-1,
            "1":0,
            "3":1,
            "5":2,
            "7":3,
            "2'":4,
            "4'":5,
            "6'":6,
            "1''":7,'1"':7,
            "3''":8,'3"':8
        }

###############################################
# Sheets # MNotes Composition #################

class Sheet:
    def __init__(self, beats:int=4):
        self.sheet=[[]]
        self.div=[]
        self.iteration = 0
        self.beats = beats
        self.slashes_counter=0
        self.IGNORE_DURATION = 1/8
        self.MEM=0
        return
        
    def _inc_itr(self):
            self.iteration = self.iteration +1
            self.sheet.append([])
        
    def beat(self):
        self.slashes_counter = self.slashes_counter + 1 - self.MEM
        self._inc_itr()
        if self.slashes_counter >= self.beats:
            self.div.append(self.iteration)
            self._inc_itr()
            self.slashes_counter = 0
        #reset mem
        self.MEM = 0
        return True
        
    def add_note(self,note:MNote):
        i = self.iteration
        self.sheet[i].append(note)
        if note.type <= self.IGNORE_DURATION:
            self.MEM = 0.5
        
    def add_note(self,tune,duration:float=1):
        note = MNote(tune,duration)
        i = self.iteration
        self.sheet[i].append(note)
        if note.type <= self.IGNORE_DURATION:
            self.MEM = 0.5

###########################################################################
# Generate Ktab from music sheet #########################################

def Kcomplie(sheet:Sheet):
    global CKTAB
    ktab.dim = 20 # overwrite default
    kt = ktab()
    kt.heigth_unit = len(sheet.sheet) +1
    kt.rinit()
    CKTAB = kt
    translator = MNote.DEFAULT_DIC()
    for note in kt.background:
        print(TEMPLATE_SVG_RCT.format(**note))
    for i in range(len(sheet.sheet)):
        for note in sheet.sheet[i]:
            pnote(translator[note.tune],note.type,i)
    for div in sheet.div:
        pline(div)
    pline(0)
    pline(end=True)
    
###########################################################################
## Example ################################################################
########################################

# lazy calls
s0 = Sheet()
a = s0.add_note
b  = s0.beat
def ab(*args):
    a(*args)
    b()
    
#######################################    
# Summer days # Spirited Away *InProg)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

b()
b()
b()
ab("4",1)

ab("3'",1/4)
ab("3'",1/4)
ab("3'",1/4)
ab("3'",1/4)

ab("2'",1/4)
ab("3'",1/4)
ab("6'",1/4)
a("3'",1/4)
ab("5",1/4)

ab("2'",1/8)
ab("2'",1/4)
b()
b()
ab("1",1)

ab("2'",1/4)
ab("2'",1/4)
ab("2'",1/4)
ab("2'",1/4)


ab("1'",1/4)
ab("2'",1/4)
ab("5'",1/4)
a("7",1/4)
ab("2'",1/4)

ab("1'",1/4)
ab("7",1/4)
ab("1",1/4)
ab("3",1/4)

ab("6",1/8)
ab("7",1/8)
a("3",1/4)
ab("1'",1/4)
ab("1'",1/4)

ab("1'",1/4)
ab("1'",1/4)
ab("1'",1/4)
ab("6",1/8)
ab("7",1/8)

a("3",1/4)
ab("1'",1/4)
ab("1'",1/4)
ab("1'",1/4)
ab("1'",1/4)

ab("1'",1/4)
ab("6",1/8)
ab("7",1/8)
a("3",1/4)
ab("1'",1/4)

ab("1'",1/4)
ab("1'",1/4)
ab("1'",1/4)
ab("1'",1/4)

ab("5'", 1/4)
ab("1'", 1/4)
ab("2'", 1/4)
ab("4", 1)

# Generate SVG Data in STDOUT
Kcomplie(s0)

