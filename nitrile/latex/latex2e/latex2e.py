from package_defs import *

from ..parsers import *



#latex command documentation
#http://www.ntg.nl/doc/biemesderfer/ltxcrib.pdf

class latex2e:

    #these chars are verboten by the parser and won't work even in verbatim mode

    verb_codes = {
        #the control codes chars (0-32 and 127) are all invalid in latex
        #with the exception of 9 (tab), 10 (LF), and 13 (CF)
        '\x00':InvalidChar,'\x01':InvalidChar,'\x02':InvalidChar,'\x03':InvalidChar,
        '\x04':InvalidChar,'\x05':InvalidChar,'\x06':InvalidChar,'\x07':InvalidChar,
        '\x08':InvalidChar,                                      '\x0b':InvalidChar,
        '\x0c':InvalidChar,                   '\x0e':InvalidChar,'\x0f':InvalidChar,
        '\x10':InvalidChar,'\x11':InvalidChar,'\x12':InvalidChar,'\x13':InvalidChar,
        '\x14':InvalidChar,'\x15':InvalidChar,'\x16':InvalidChar,'\x17':InvalidChar,
        '\x18':InvalidChar,'\x19':InvalidChar,'\x1a':InvalidChar,'\x1b':InvalidChar,
        '\x1c':InvalidChar,'\x1d':InvalidChar,'\x1e':InvalidChar,'\x1f':InvalidChar,
        '\x7f':InvalidChar, 
        #latex just seems to ignore chars128-255, replicating that behavior
        '\x80':'','\x81':'','\x82':'','\x83':'','\x84':'','\x85':'','\x86':'','\x87':'',
        '\x88':'','\x89':'','\x8a':'','\x8b':'','\x8c':'','\x8d':'','\x8e':'','\x8f':'',
        '\x90':'','\x91':'','\x92':'','\x93':'','\x94':'','\x95':'','\x96':'','\x97':'',
        '\x98':'','\x99':'','\x9a':'','\x9b':'','\x9c':'','\x9d':'','\x9e':'','\x9f':'',
        '\xa0':'','\xa1':'','\xa2':'','\xa3':'','\xa4':'','\xa5':'','\xa6':'','\xa7':'',
        '\xa8':'','\xa9':'','\xaa':'','\xab':'','\xac':'','\xad':'','\xae':'','\xaf':'',
        '\xb0':'','\xb1':'','\xb2':'','\xb3':'','\xb4':'','\xb5':'','\xb6':'','\xb7':'',
        '\xb8':'','\xb9':'','\xba':'','\xbb':'','\xbc':'','\xbd':'','\xbe':'','\xbf':'',
        '\xc0':'','\xc1':'','\xc2':'','\xc3':'','\xc4':'','\xc5':'','\xc6':'','\xc7':'',
        '\xc8':'','\xc9':'','\xca':'','\xcb':'','\xcc':'','\xcd':'','\xce':'','\xcf':'',
        '\xd0':'','\xd1':'','\xd2':'','\xd3':'','\xd4':'','\xd5':'','\xd6':'','\xd7':'',
        '\xd8':'','\xd9':'','\xda':'','\xdb':'','\xdc':'','\xdd':'','\xde':'','\xdf':'',
        '\xe0':'','\xe1':'','\xe2':'','\xe3':'','\xe4':'','\xe5':'','\xe6':'','\xe7':'',
        '\xe8':'','\xe9':'','\xea':'','\xeb':'','\xec':'','\xed':'','\xee':'','\xef':'',
        '\xf0':'','\xf1':'','\xf2':'','\xf3':'','\xf4':'','\xf5':'','\xf6':'','\xf7':'',
        '\xf8':'','\xf9':'','\xfa':'','\xfb':'','\xfc':'','\xfd':'','\xfe':'','\xff':'',
        }
    
    text_codes = {

        # {}%\# are defined at the begining of the document everything else is defined at begin{document}

        
        "{"  : GroupParser,
        #"}"
        "%"  : CommentParser,
        " "  : WhitespaceParser,
        "\t" : WhitespaceParser,
        "\n" : WhitespaceParser,                             
        "$"  : InlineMathParser,
        "\\" : CommandParser,
        "~"  : u"\N{NO-BREAK SPACE}",
        "|"  : u"\N{em dash}", 
        "<"  : u"\N{INVERTED EXCLAMATION MARK}",
        ">"  : u"\N{INVERTED QUESTION MARK}",
        "'"  : MultiParser([u"\N{RIGHT SINGLE QUOTATION MARK}",
                            u"\N{RIGHT DOUBLE QUOTATION MARK}",]),
        "`"  : MultiParser([u"\N{LEFT SINGLE QUOTATION MARK}",
                            u"\N{LEFT SINGLE QUOTATION MARK}",]),
        '"'  : u"\N{RIGHT DOUBLE QUOTATION MARK}",
        '-'  : MultiParser(["-",u"\N{en dash}", u"\N{em dash}", ]),
        "}"  :Exception (),
        "#"  : Exception("Parser encountered a '#' character, which are not allowed. "
                         "if you need a literal hash mark try escaping it with '\#'"),
        "&"  : Exception("Parser encountered a '&' character, "
                         "which are not allowed outside of tabular environments. "
                         "If you need a literal ampersand try escaping it with '\&'"),
        "_"  : Exception("Parser encountered an '_'. "
                         "The underscore can only be used in math mode. "
                         "If you need a literal underscore try excaping it with '\_'. "
                         "I would like to use subscripts in text mode too, "
                         "but that is not how latex works :-("),
        "^"  : Exception("Parser encountered an '^'. "
                         "The carrot can only be used in math mode. "
                         "If you need a literal carrot try excaping it with '\^{}'. "
                         "I would like to use subscripts in text mode too, "
                         "but that is not how latex works :-("),
    }

    math_codes = {

        "^" :superscript,
        "_" :subscript,
        "'" : u"\N{PRIME}",
        "|"  : None,
        "<"  : None,
        ">"  : None,
        "-"  : u"\N{MINUS SIGN}",
        "#"  : Exception("Parser encountered a '#' character, which are not allowed. "
                         "if you need a literal hash mark try escaping it with '\#'"),
        "&"  : Exception("Parser encountered a '&' character, "
                         "which are not allowed outside of tabular environments. "
                         "If you need a literal ampersand try escaping it with '\&'"),
                         }
    
    all_cmds = {

        "begin" : BeginEnvironment,
        "end" : null(args=1),
        "verb" :VerbParser,
        "-"  : u"\N{soft hyphen}",
        
        #Table 1: LATEX 2e Escapable "Special" Characters
        "$" : symbol(u"$"),
        "%" : symbol(u"%"),
        "_" : symbol(u"_"),
        "}" : symbol(u"}"),
        "&" : symbol(u"&"),
        "#" : symbol(u"#"),
        "{" : symbol(u"{"),

        #Table 3: LATEX 2e Commands Defined to Work in Both Math and Text Mode
        "P"         : symbol(u"\N{PILCROW SIGN}"),
        "S"         : symbol(u"\N{SECTION SIGN}"),
        "copyright" : symbol(u"\N{COPYRIGHT SIGN}"),
        "dag"       : symbol(u"\N{DAGGER}"),
        "ddag"      : symbol(u"\N{DOUBLE DAGGER}"),
        "dots"      : symbol(u"\N{HORIZONTAL ELLIPSIS}"),
        "pounds"    : symbol(u"\N{POUND SIGN}"),

        #Table 5: Non-ASCII Letters (Excluding Accented Letters)
        #\aa isn't here because it dosn't actually work in mathmode
        "AA" : symbol(u"\N{LATIN CAPITAL LETTER A WITH RING ABOVE}"),
        "AE" : symbol(u"\N{LATIN CAPITAL LETTER AE}"),
        "ae" : symbol(u"\N{LATIN SMALL LETTER AE}"),
        "L"  : symbol(u"\N{LATIN CAPITAL LETTER L WITH STROKE}"),
        "o"  : symbol(u"\N{LATIN SMALL LETTER O WITH STROKE}"),
        "O"  : symbol(u"\N{LATIN CAPITAL LETTER O WITH STROKE}"),
        "OE" : symbol(u"\N{LATIN CAPITAL LIGATURE OE}"),
        "oe" : symbol(u"\N{LATIN SMALL LIGATURE OE}"),
        "ss" : symbol(u"\N{LATIN SMALL LETTER SHARP S}"),
        "SS" : symbol(u"SS"), #is this supposed to be a german sharp s?
        "l"  : symbol(u"\N{LATIN SMALL LETTER L WITH STROKE}"),


        #symbols which work in math mode but are classified at math or text
        " "              : symbol(u" "),
        ","              : symbol(u"\N{THIN SPACE}"), #thin space 1/6 quad
        "angle"          : symbol(u"\N{ANGLE}"), #not math mode only
        "ldots"          : symbol(u"\N{HORIZONTAL ELLIPSIS}"),
        "lbrack"         : symbol("["),
        "mathunderscore" : symbol(u"_"),
        "quad"           : symbol(' '),
        "rbrack"         : symbol(u"]"),
        "vdots"          : symbol(u"\N{Vertical Ellipsis}"),

        
        "ldots"     : symbol(u"\N{HORIZONTAL ELLIPSIS}"),
        "i"         : symbol(u"\N{LATIN SMALL LETTER DOTLESS I}"),
        "j"         : symbol(u"\N{LATIN SMALL LETTER DOTLESS J}"),
        "lq"        : symbol(u"\N{LEFT SINGLE QUOTATION MARK}"),
        "rq"        : symbol(u"\N{RIGHT SINGLE QUOTATION MARK}"), #
        "thinspace" : symbol(u"\N{THIN SPACE}"),#the proper space between single and double quotes (dont know if this is correct 1/6 em)

        "label"           : null(1),
        #"rb" :null(),
        #"lb" :null(),
        #"rv"     : null(),
        "\\" : null(), #terminates a line
        "hfill"           : tolken(),
        "nonumber"        : null(),

        
        
        #Table 2: Predefined LATEX 2e Text-mode Commands
        #symbol table claims that these are textmode only but all
        #but textasciicircum, textasciitilde,textdollar
        "textasteriskcentered": symbol(u"*"),
        "textbackslash"       : symbol(u"\\"),
        "textbar"             : symbol(u"|"),
        "textbraceleft"       : symbol(u"{"),
        "textbraceright"      : symbol(u"}"),
        "textbullet"          : symbol(u"\N{BULLET}"),
        "textcopyright"       : symbol(u"\N{COPYRIGHT SIGN}"),
        "textdagger"          : symbol(u"\N{DAGGER}"),
        "textdaggerdbl"       : symbol(u"\N{DOUBLE DAGGER}"),
        "textellipsis"        : symbol(u"\N{HORIZONTAL ELLIPSIS}"),
        "textemdash"          : symbol(u"\N{EM DASH}"),
        "textendash"          : symbol(u"\N{EN DASH}"),
        "textexclamdown"      : symbol(u"\N{INVERTED EXCLAMATION MARK}"),
        "textgreater"         : symbol(u">"),
        "textless"            : symbol(u"<"),
        "textordfeminine"     : symbol(u"\N{FEMININE ORDINAL INDICATOR}"),
        "textordmasculine"    : symbol(u"\N{MASCULINE ORDINAL INDICATOR}"),
        "textparagraph"       : symbol(u"\N{PILCROW SIGN}"),
        "textperiodcentered"  : symbol(u"\N{MIDDLE DOT}"),
        "textquestiondown"    : symbol(u"\N{INVERTED QUESTION MARK}"),
        "textquotedblleft"    : symbol(u"\N{LEFT DOUBLE QUOTATION MARK}"),
        "textquotedblright"   : symbol(u"\N{RIGHT DOUBLE QUOTATION MARK}"),
        "textquoteleft"       : symbol(u"\N{LEFT SINGLE QUOTATION MARK}"),
        "textquoteright"      : symbol(u"\N{RIGHT SINGLE QUOTATION MARK}"),
        "textregistered"      : symbol(u"\N{REGISTERED SIGN}"),
        "textsection"         : symbol(u"\N{SECTION SIGN}"),
        "textsterling"        : symbol(u"\N{POUND SIGN}"),
        "texttrademark"       : symbol(u"\N{TRADE MARK SIGN}"),
        "textunderscore"      : symbol(u"_"),
        "textvisiblespace"    : symbol(u"\N{OPEN BOX}"),


        "textbf"        : null(1),
        "textit"        : null(1),
        "textsl"        : null(1),
        "texttqt"       : null(1),
        "texttt"        : null(1),

        }

    text_cmds = {
        #letters from table 5 which don't actually work in both math and text mode
        #\aa causes and error and \l creates a script l like \ell
        "aa" : symbol(u"\N{LATIN SMALL LETTER A WITH RING ABOVE}"),

        # #Table 2: Predefined LATEX 2e Text-mode Commands
        "textasciicircum"     : symbol(u"^"),
        "textasciitilde"      : symbol(u"~"),
        "textdollar"          : symbol(u"$"),

        #Table 17: Text-mode Accents
        '"' : combining("\N{COMBINING DIAERESIS}"),
        "'" : combining("\N{COMBINING ACUTE ACCENT}"),
        "." : combining("\N{COMBINING DOT ABOVE}"),
        "=" : combining("\N{COMBINING MACRON}"),
        "^" : combining("\N{COMBINING CIRCUMFLEX ACCENT}"),
        "`" : combining("\N{COMBINING GRAVE ACCENT}"),
        "~" : combining("\N{COMBINING TILDE}"),
        "b" : combining("\N{COMBINING MACRON BELOW}"),
        "c" : combining("\N{COMBINING CEDILLA}"),
        "d" : combining("\N{COMBINING DOT BELOW}"),
        "H" : combining("\N{COMBINING DOUBLE ACUTE ACCENT}"),        
        "r" : combining("\N{COMBINING RING ABOVE}"),
        "t" : combining("\N{COMBINING DOUBLE INVERTED BREVE}"),
        "u" : combining("\N{COMBINING BREVE}"),
        "v" : combining("\N{COMBINING CARON}"),
        "textcircled" : combining("\N{COMBINING ENCLOSING CIRCLE}"),

        #not documented 
        "k" : combining("\N{COMBINING OGONEK}"),
        
        #undocumented 
        "documentclass" : Meta(2,arg_parsers={0:OptionalArgumentParser()}),
        "usepackage"    : UsePackage,
        "eqref"         : null(1),
        "marginparpush" : null(),
        #"scalebox"      : null(2,{}),


        "LaTeX"     : symbol(u"LaTeX"),
        "TeX"       : symbol(u"TeX"),


        
        #formatting
        #")" : (0,{}), #start Math mode
        #"(" : (0,{}), #end Math mode
        #"*"  : (0,{}), #multiplication signs where page break is allowd
        #"+"  : (0,{}), #moves left margin to the right by one tab stop. Begin tabbed line
        #"-"  : (0,{}), #optional hyphan
        #"/"  : (0,{}), #inserts italics adjustment space
        #"@"  : (1,{}), # declares the period that follows is to be asentence-ending period
        #"["  : (0,{}), #same as \begin{displaymath} or $$

        #"\\*": (0,{}), #terminates a line but disallows a pabge break
        #"]"  : (0,{}), #same as \end{displaymath} or $$

        "addcontentsline" : {'args':1,'element': "set-meta"}, #add to toc
        "address"         : declaration, #return address in letter
        "addtocontents"   : {'args':2,'element': 'set-meta'}, #add to toc
        "addtocounter"    : {'args':2,'element': 'set-meta'}, #adds amount to counte
        #"alpha"           : (1,{}), #prints counter as lowercase letter
        #"Alpha"           : (1,{}), #prints counter as uppercase letter
        "and"             : declaration, # seperates authors for \maketitle
        
        "appendix"        : declaration, #starts appendix
        "arabic"          : {'args':1, 'element': "get-meta"}, #prints counter as arabic numeral
        "author"          : {'args':1, 'element': "set-meta"}, #declares authors for \maketitle
        #"begin" handled by parser directly
        "bf"              : declaration, #switch to boldface
        "bibitem"         : null(1),
        "bibliography"    : (1,{}),
        "bibliographystyle": (1,{}),
        
        "boldmath"        : declaration,#changes math italics and math symbols to boldface. Should be used outside of math mode.
        "caption"         : null(2,{0:""}),
        "cc"              : {'args':1,'element':'set-meta'}, #carbon copy for letter
        "centering"       : declaration, #everything after will be centered
        "chapter"         : {'args':2,'defaults':{0:""},'element':'start-section'},
        "chapter*"        : {'args':1,'element':'start-section'},
        "cite"            : null(2,{0:""}),
        "closing"         : {'args':1,'action':'set-info'}, #closing text in letter
        
        "date"            : {'args':1,'action':'set-info'},
        "day"             : {'args':1,'action':'get-ifno'},#current day of the month
        
        "documentstyle"   : {'args':2,'defaults':{0:""},'action':'set-info'},
        "dotfill"         : declaration,
        "em"              : declaration,
        "encl"            : declaration, #declares a list of enclusers for letter document style
        #end handled by parser
        "fbox"            : {'args':1,'action':'format'}, #framed box around text
        "fnsymbol"        : {'args':1,'action':'get-meta'},
        "footnote"        : null(1),
        "footnotemark"    : {'args':1,'action':'get-meta'}, #puts a footnote number into the text
        "footnotetext"    : {'args':1,'action':'set-info'}, #specifies the text for a footnote which was indicated by a \footnotemark
        "frame"           : {'args':1,'action':'format'}, #makes a framed (outlined) box around text, with no margin between the text and the frame.
        "framebox"        : {'args':3,'defaults':{0:"",1:""},'action':'format'},
        "glossary"        : {'args':1,'action':'set-info'},
        "glossaryentry"   : (1,{}),

        "hline"           : null(),
        "hrulefill"       : (0,{},None),
        "hspace"          : (1,{},None),
        "hspace*"         : (1,{},None),
        "huge"            : declaration,
        "hyphenation"     : (1,{},None),
        "include"         : (1,{},None),
        "includeonly"     : (1,{},None),
        "index"           : (1,{},None),
        "indexenrty"      : (2,{},None),
        "input"           : (1,{},None),
        "it"              : declaration,
        "item"            : null(1,{0:""}),

        "large"           : declaration,
        "Large"           : declaration,
        "LARGE"           : declaration,
        
        "linebreak"       : declaration,
        "marginpar"       : {'args': 1},
        "markboth"        : {'args': 2},
        "markright"       : {'args': 1},
        "mbox"            : {'args': 1},
        "month"           : {'args': 0},
        "newcommand"      : NewCommand,
        "newenvironment"  : {'args': 2, 'defaults': {1:"0"}},
        "newline"         : {'args': 0},
        "newpage"         : {'args': 0},
        "newtheorem"      : {'args': 4, "defaults": {1:"",3:""}},
        "noindent"        : null,
        "nolinebreak"     : {'args': 1, "defaults": {0:"0"}},

        "nopagebreak"     : {'args': 1, "defaults": {0:"0"}},
        "normalsize"      : declaration,
        "obeycr"          : {'args':0}, #makes embedded carriage returns act like line terminators
        "opening"         : {'args':1}, #declares an opening for letter document style  
        "pagebreak"       : tolken(1,{0:"0"},level = 10),
        "pageref"         : {'args':1},
        "paragraph"       : {'args':2,'defaults':{0:""}},
        "paragraph*"      : {'args':1},
        "parbox"          : {'args':3,'defaults':{0:""}},
        "part"            : {'args':2,'defaults':{0:""}},
        "part*"           : {'args':1},
        "ps"              : {'args':1},
        "raggedbottom"    : declaration,
        "raggedleft"      : declaration,
        "raggedright"     : declaration,
        "raisebox"        : {'args':4, 'defaults': {1:0,2:0}},
        "ref"             : null(1),
        "renewcommand"    : {'args':3, 'defaults': {1:0}},
        "renewenviroment" : {'args':4, 'defaults': {1:0}},
        "restorecr"       : declaration,
        "rm"              : declaration,
        "rule"            : {'args':3, 'defaults': { 0: 0} },
        "savebox"         : {'args':4, 'defaults': { 0:0,2:0}},
        "sbox"            : {'args':2},
        "sc"              : declaration,
        "scriptsize"      : declaration,
        "section"         : heading(2,{1:""},level=100),
        "section*"        : {'args':1},
        "sf"              : declaration, #sans serif font
        "signature"       : {'args':1, 'element': 'component'},
        "sl"              : declaration, #slanted typeface
        "small"           : declaration,
        "subparagraph"    : {'args':2, 'defaults' : {0:""}},
        "subparagraph*"   : {'args':1},
        "subsection"      : heading(2,{0:""},level=50),
        "subsection*"     : {'args':1},
        "symbol"          : {'args':1},
        "thanks"          : {'args':1},
        "tiny"            : declaration,
        "title"           : {'args':1},
        "today"           : {'args':0},
        "tt"              : declaration,
        "twocolumn"       : tolken(1,{0:""},level=900),
        "unboldmath"      : declaration,
        "underline"       : {'args':1},
        #"verb"            :
        #"verb*"           :
        "year"            : {'args':0},
    

        "noindent"        : null(),
    
        #contribute only to formatting 
        "arraycolsep"          : null(),
        "arrayrulewidth"       : null(),
        "arraystretch"         : null(),
        "addtolength"          : {'args':2},
        "baselineskip"         : null(),
        "baselinestretch"      : null(),
        "bigskip"              : null(),
        "bigskippamount"       : null(),
        "bottomfraction"       : null(),
        "cleardoublepage"      : null(),
        "clearpage"            : null(),
        "columnsep"            : null(),
        "columnseprule"        : null(),
        "columnwidth"          : null(),
        "dblfloatpagefraction" : null(),
        "dblfloatsep"          : null(),
        "dbltextfloat"         : null(),
        "dbltopfraction"       : null(),
        "doublerulesep"        : null(),
        "evensidemargin"       : null(),
        "fboxrule"             : null(),
        "fboxsep"              : null(),
        "fill"                 : null(),
        "floatpagefraction"    : null(),
        "floatsep"             : null(),
        "flushbottom"          : null(),
        "footheight"           : null(),
        "footnotesep"          : null(),
        "footnotesize"         : null(),
        "footskip"             : null(),
        "fussy"                : null(),
        "headheight"           : null(),
        "headsep"              : null(),
        "indexspace"           : null(),
        "intextsep"            : null(),
        "itemindent"           : null(),
        "itemsep"              : null(),
        "labelwidth"           : null(),
        "labelsep"             : null(),
        "leftmargin"           : null(),
        "linewidth"            : null(),
        "listparindent"        : null(),

        "listoffigures"        : null(),
        "listofftables"        : null(),
        "makeglossary"         : null(),
        "makeindex"            : null(),
        "maketitle"            : null(),
        "marginpush"           : null(),
        "marginparsep"         : null(),
        "marginparwidth"       : null(),
        "medskip"              : null(),
        "medskipamount"        : null(),
        "newcounter"           : {'args': 2, 'defaults': {1:""}, 'element': 'null'},
        "newfont"              : {'args': 2, 'element': 'null'},
        "newlength"            : {'args': 1, 'element': 'null'},
        "newsavebox"           : {'args': 1},
        "nofiles"              : null(),
        "normalmarginpar"      : null(),
        "oddsidemargin"        : null(),
        "onecolumn"            : null(),
        "pagenumbering"        : {'args': 1},
        "pagestyle"            : null(1),
        "parindent"            : null(),
        "parsep"               : null(),
        "parskip"              : null(),
        "partosep"             : null(),
        "poptabs"              : null(),
        "protect"              : null(),
        "reversmarginpar"      : null(),
        "rightmargin"          : null(),
        "roman"                : null(),
        "setcounter"           : {'args':2},
        "setlength"            : Meta(2),
        "settowidth"           : {'args':2},
        "shortsctack"          : {'args':2,"defaults":{0:''}},    
        "sloppy"               : null(),
        "smallskip"            : null(),
        "smallskipamount"      : null(),
        "stop"                 : null(),
        "tableofcontents"      : null(),
        "texfloatsep"          : null(),
        "textfraction"         : null(),
        "textheight"           : null(),
        "textstyle"            : null(),
        "textwidth"            : null(),
        "thisgapestyle"        : {'args':1},
        "topfraction"          : null(),
        "topmargin"            : null(),
        "topsep"               : null(),
        "topskip"              : null(),
        "typein"               : {'args':2,'defaults': {0:""}},
        "typeout"              : {'args':1},
        "unitlength"           : null(),
        "usebox"               : {'args':1},
        "usecounter"           : {'args':1},
        "value"                : {'args':1},
        "vfill"                : {'args':1},
        "vspace"               : null(1),
        "vspace*"              : {'args':1},

        #for renewcommand in intro.tex, remove after renewcommand implemented correctly
        "langle" : null(),
        "rangle" : null(),
        

    
    }

    math_cmds = {

         #Table 42: Math-Mode Versions of Text Symbols
        "mathdollar"     : symbol(u"$"),
        "mathellipsis"   : symbol(u"\N{HORIZONTAL ELLIPSIS}"),
        "mathparagraph"  : symbol(u"\N{PILCROW SIGN}"),
        "mathsection"    : symbol(u"\N{SECTION SIGN}"),
        "mathsterling"   : symbol(u"\N{POUND SIGN}"),

        #Table 44: Binary Operators
        "amalg"          : symbol(u"\N{AMALGAMATION OR COPRODUCT}"),
        "ast"            : symbol(u"*"),
        "bigcirc"        : symbol(u"\N{WHITE CIRCLE}"),
        "bigtriangledown": symbol(u"\N{WHITE DOWN-POINTING TRIANGLE}"),
        "bigtriangleup"  : symbol(u"\N{WHITE UP-POINTING TRIANGLE}"),
        "bullet"         : symbol(u"\N{BULLET OPERATOR}"),
        "cap"            : symbol(u"\N{INTERSECTION}"),
        "cdot"           : symbol(u"\N{DOT OPERATOR}"),
        "circ"           : symbol(u"\N{RING OPERATOR}"),
        "cup"            : symbol(u"\N{UNION}"),
        "dagger"         : symbol(u"\N{DAGGER}"),
        "ddagger"        : symbol(u"\N{DOUBLE DAGGER}"),
        "diamond"        : symbol(u"\N{DIAMOND OPERATOR}"),
        "div"            : symbol(u"\N{DIVISION SIGN}"),
        "mp"             : symbol(u"\N{MINUS-OR-PLUS SIGN}"),
        "odot"           : symbol(u"\N{CIRCLED DOT OPERATOR}"),
        "ominus"         : symbol(u"\N{CIRCLED MINUS}"),
        "oplus"          : symbol(u"\N{CIRCLED PLUS}"),
        "oslash"         : symbol(u"\N{CIRCLED DIVISION SLASH}"),
        "otimes"         : symbol(u"\N{CIRCLED TIMES}"),
        "pm"             : symbol(u"\N{PLUS-MINUS SIGN}"),
        "setminus"       : symbol(u"\N{SET MINUS}"),
        "sqcap"          : symbol(u"\N{SQUARE CAP}"),
        "sqcup"          : symbol(u"\N{SQUARE CUP}"),
        "star"           : symbol(u"\N{STAR OPERATOR}"),
        "times"          : symbol(u"\N{MULTIPLICATION SIGN}"),
        "triangleleft"   : symbol(u"\N{WHITE LEFT-POINTING SMALL TRIANGLE}"),
        "triangleright"  : symbol(u"\N{WHITE RIGHT-POINTING SMALL TRIANGLE}"),
        "uplus"          : symbol(u"\N{MULTISET UNION}"),
        "vee"            : symbol(u"\N{LOGICAL OR}"),
        "wedge"          : symbol(u"\N{LOGICAL AND}"),
        "wr"             : symbol(u"\N{WREATH PRODUCT}"),
        
        #Table 57: Variable-sized Math Operators
        "bigcap"    : symbol(u"\N{N-ARY INTERSECTION}"),
        "bigcup"    : symbol(u"\N{N-ARY UNION}"),
        "bigodot"   : symbol(u"\N{N-ARY CIRCLED DOT OPERATOR}"),
        "bigoplus"  : symbol(u"\N{N-ARY CIRCLED PLUS OPERATOR}"),
        "bigotimes" : symbol(u"\N{N-ARY CIRCLED TIMES OPERATOR}"),
        "bigsqcup"  : symbol(u"\N{N-ARY SQUARE UNION OPERATOR}"),
        "biguplus"  : symbol(u"\N{N-ARY UNION OPERATOR WITH PLUS}"),
        "bigvee"    : symbol(u"\N{N-ARY LOGICAL OR}"),
        "bigwedge"  : symbol(u"\N{N-ARY LOGICAL AND}"),
        "coprod"    : symbol(u"\N{N-ARY COPRODUCT}"),
        "int"       : symbol(u"\N{INTEGRAL}"),
        "oint"      : symbol(u"\N{CONTOUR INTEGRAL}"),
        "prod"      : symbol(u"\N{N-ARY PRODUCT}"),
        "sum"       : symbol(u"\N{N-ARY SUMMATION}"),

        #Table 85: Subset and Superset Relations
        "sqsubseteq"   : symbol(u"\N{SQUARE IMAGE OF OR EQUAL TO}"),
        "sqsupseteq"   : symbol(u"\N{SQUARE ORIGINAL OF OR EQUAL TO}"),
        "subset"       : symbol(u"\N{SUBSET OF}"),
        "subseteq"     : symbol(u"\N{SUBSET OF OR EQUAL TO}"),
        "supset"       : symbol(u"\N{SUPERSET OF}"),
        "supseteq"     : symbol(u"\N{SUPERSET OF OR EQUAL TO}"),

        #Table 92: Inequalities
        "geq"    : symbol(u"\N{GREATER-THAN OR EQUAL TO}"),
        "gg"     : symbol(u"\N{MUCH GREATER-THAN}"),
        "leq"    : symbol(u"\N{LESS-THAN OR EQUAL TO}"),
        "ll"     : symbol(u"\N{MUCH LESS-THAN}"),
        "neq"    : symbol(u"\N{NOT EQUAL TO}"),

        #Table 102: Arrows
        "Downarrow"          : symbol(u"\N{DOWNWARDS DOUBLE ARROW}"),
        "downarrow"          : symbol(u"\N{DOWNWARDS ARROW}"),
        "hookleftarrow"      : symbol(u"\N{LEFTWARDS ARROW WITH HOOK}"),
        "hookrightarrow"     : symbol(u"\N{RIGHTWARDS ARROW WITH HOOK}"),
        "leftarrow"          : symbol(u"\N{LEFTWARDS ARROW}"),
        "Leftarrow"          : symbol(u"\N{LEFTWARDS DOUBLE ARROW}"),
        "Leftrightarrow"     : symbol(u"\N{LEFT RIGHT DOUBLE ARROW}"),
        "leftrightarrow"     : symbol(u"\N{LEFT RIGHT ARROW}"),
        "longleftarrow"      : symbol(u"\N{LONG LEFTWARDS ARROW}"),
        "Longleftarrow"      : symbol(u"\N{LONG LEFTWARDS DOUBLE ARROW}"),
        "longleftrightarrow" : symbol(u"\N{LONG LEFT RIGHT ARROW}"),
        "Longleftrightarrow" : symbol(u"\N{LONG LEFT RIGHT DOUBLE ARROW}"),
        "longmapsto"         : symbol(u"\N{LONG RIGHTWARDS ARROW FROM BAR}"),
        "Longrightarrow"     : symbol(u"\N{LONG RIGHTWARDS DOUBLE ARROW}"),
        "longrightarrow"     : symbol(u"\N{LONG RIGHTWARDS ARROW}"),
        "mapsto"             : symbol(u"\N{RIGHTWARDS ARROW FROM BAR}"),
        "nearrow"            : symbol(u"\N{NORTH EAST ARROW}"),
        "nwarrow"            : symbol(u"\N{NORTH WEST ARROW}"),
        "Rightarrow"         : symbol(u"\N{RIGHTWARDS DOUBLE ARROW}"),
        "rightarrow"         : symbol(u"\N{RIGHTWARDS ARROW}"),
        "searrow"            : symbol(u"\N{SOUTH EAST ARROW}"),
        "swarrow"            : symbol(u"\N{SOUTH WEST ARROW}"),
        "uparrow"            : symbol(u"\N{UPWARDS ARROW}"),
        "Uparrow"            : symbol(u"\N{UPWARDS DOUBLE ARROW}"),
        "updownarrow"        : symbol(u"\N{UP DOWN DOUBLE ARROW}"),
        "Updownarrow"        : symbol(u"\N{UP DOWN ARROW}"),

        #Table 103: Harpoons
        "leftharpoondown"  : symbol(u"\N{LEFTWARDS HARPOON WITH BARB DOWNWARDS}"),
        "leftharpoonup"    : symbol(u"\N{LEFTWARDS HARPOON WITH BARB UPWARDS}"),
        "rightharpoondown" : symbol(u"\N{RIGHTWARDS HARPOON WITH BARB DOWNWARDS}"),
        "rightharpoonup"   : symbol(u"\N{RIGHTWARDS HARPOON WITH BARB UPWARDS}"),
        "rightleftharpoons": symbol(u"\N{RIGHTWARDS HARPOON OVER LEFTWARDS HARPOON}"),

        #Table 128: Log-like Symbols
        "arccos" : symbol(u"arccos"),
        "arcsin" : symbol(u"arcsin"),
        "arctan" : symbol(u"arctan"),
        "arg"    : symbol(u"arg"),
        "cos"    : symbol(u"cos"),
        "cosh"   : symbol(u"cosh"),
        "cot"    : symbol(u"cot"),
        "coth"   : symbol(u"coth"),
        "csc"    : symbol(u"csc"),
        "deg"    : symbol(u"deg"),
        "det"    : symbol(u"det"),
        "dim"    : symbol(u"dim"),
        "exp"    : symbol(u"exp"),
        "gcd"    : symbol(u"gcd"),
        "hom"    : symbol(u"hom"),
        "inf"    : symbol(u"inf"),
        "ker"    : symbol(u"ker"),
        "lg"     : symbol(u"lg"),
        "lim"    : symbol(u"lim"),
        "liminf" : symbol(u"lim inf"),
        "limsup" : symbol(u"lim sup"),
        "ln"     : symbol(u"ln"),
        "log"    : symbol(u"log"),
        "max"    : symbol(u"max"),
        "min"    : symbol(u"min"),
        "Pr"     : symbol(u"Pr"),
        "sec"    : symbol(u"sec"),
        "sin"    : symbol(u"sin"),
        "sinh"   : symbol(u"sinh"),
        "sup"    : symbol(u"sup"),
        "tan"    : symbol(u"tan"),
        "tanh"   : symbol(u"tanh"),

        
        #Table 131: Greek Letters
        "alpha"      : symbol(u"\N{GREEK SMALL LETTER ALPHA}"),
        "beta"       : symbol(u"\N{GREEK SMALL LETTER BETA}"),
        "gamma"      : symbol(u"\N{GREEK SMALL LETTER GAMMA}"),
        "delta"      : symbol(u"\N{GREEK SMALL LETTER DELTA}"),
        "epsilon"    : symbol(u"\N{GREEK LUNATE EPSILON SYMBOL}"),
        "varepsilon" : symbol(u"\N{LATIN SMALL LETTER OPEN E}"),
        "zeta"       : symbol(u"\N{GREEK SMALL LETTER ZETA}"),
        "eta"        : symbol(u"\N{GREEK SMALL LETTER ETA}"),
        "theta"      : symbol(u"\N{GREEK SMALL LETTER THETA}"),
        "vartheta"   : symbol(u"\N{GREEK THETA SYMBOL}"),
        "iota"       : symbol(u"\N{GREEK SMALL LETTER IOTA}"),
        "kappa"      : symbol(u"\N{GREEK SMALL LETTER KAPPA}"),
        "lambda"     : symbol(u"\N{GREEK SMALL LETTER LAMDA}"),
        "mu"         : symbol(u"\N{GREEK SMALL LETTER MU}"),
        "nu"         : symbol(u"\N{GREEK SMALL LETTER NU}"),
        "xi"         : symbol(u"\N{GREEK SMALL LETTER XI}"),
        "pi"         : symbol(u"\N{GREEK SMALL LETTER PI}"),
        "varpi"      : symbol(u"\N{GREEK PI SYMBOL}"),
        "rho"        : symbol(u"\N{GREEK SMALL LETTER RHO}"),
        "varrho"     : symbol(u"\N{GREEK RHO SYMBOL}"),
        "sigma"      : symbol(u"\N{GREEK SMALL LETTER SIGMA}"),
        "varsigma"   : symbol(u"\N{GREEK SMALL LETTER FINAL SIGMA}"),
        "tau"        : symbol(u"\N{GREEK SMALL LETTER TAU}"),
        "upsilon"    : symbol(u"\N{GREEK SMALL LETTER UPSILON}"),
        "phi"        : symbol(u"\N{GREEK PHI SYMBOL}"),
        "varphi"     : symbol(u"\N{GREEK SMALL LETTER PHI}"),
        "chi"        : symbol(u"\N{GREEK SMALL LETTER CHI}"),
        "psi"        : symbol(u"\N{GREEK SMALL LETTER PSI}"),
        "omega"      : symbol(u"\N{GREEK SMALL LETTER OMEGA}"),
        
        "Gamma"      : symbol(u"\N{GREEK CAPITAL LETTER GAMMA}"),
        "Delta"      : symbol(u"\N{GREEK CAPITAL LETTER DELTA}"),
        "Theta"      : symbol(u"\N{GREEK CAPITAL LETTER THETA}"),
        "Lambda"     : symbol(u"\N{GREEK CAPITAL LETTER LAMDA}"),
        "Xi"         : symbol(u"\N{GREEK CAPITAL LETTER XI}"),
        "Pi"         : symbol(u"\N{GREEK CAPITAL LETTER PI}"),
        "Sigma"      : symbol(u"\N{GREEK CAPITAL LETTER SIGMA}"),
        "Upsilon"    : symbol(u"\N{GREEK CAPITAL LETTER UPSILON}"),
        "Phi"        : symbol(u"\N{GREEK CAPITAL LETTER PHI}"),
        "Psi"        : symbol(u"\N{GREEK CAPITAL LETTER PSI}"),
        "Omega"      : symbol(u"\N{GREEK CAPITAL LETTER OMEGA}"),

        
        #Table 139: Letter-like Symbols
        "bot"    : symbol(u"\N{UP TACK}"),
        "ell"    : symbol(u"\N{SCRIPT SMALL L}"),
        "exists" : symbol(u"\N{THERE EXISTS}"),
        "forall" : symbol(u"\N{FOR ALL}"),
        "hbar"   : symbol(u"\N{PLANCK CONSTANT OVER TWO PI}"),
        "Im"     : symbol(u"\N{BLACK-LETTER CAPITAL I}"),
                
        "imath"  : symbol(u"\N{LATIN SMALL LETTER DOTLESS I}"),
        "in"     : symbol(u"\N{ELEMENT OF}"),
        "jmath"  : symbol(u"\N{LATIN SMALL LETTER DOTLESS J}"),
        "ni"     : symbol(u"\N{CONTAINS AS MEMBER}"),
        "partial": symbol(u"\N{PARTIAL DIFFERENTIAL}"),
        "Re"     : symbol(u"\N{BLACK-LETTER CAPITAL R}"),
        "top"    : symbol(u"\N{DOWN TACK}"),
        "wp"     : symbol(u"\N{SCRIPT CAPITAL P}"),

        #Table 164: Math-mode Accents
        "acute"   : combining(u"\N{COMBINING ACUTE ACCENT}"),
        "bar"     : combining(u"\N{COMBINING MACRON}"),
        "breve"   : combining(u"\N{COMBINING BREVE}"),
        "check"   : combining(u"\N{COMBINING CARON}"),
        "ddot"    : combining(u"\N{COMBINING DIAERESIS}"),
        "dot"     : combining(u"\N{COMBINING DOT ABOVE}"),
        "grave"   : combining(u"\N{COMBINING GRAVE ACCENT}"),
        "hat"     : combining(u"\N{COMBINING CIRCUMFLEX ACCENT}"),
        "mathring": combining(u"\N{COMBINING RING ABOVE}"),
        "tilde"   : combining(u"\N{COMBINING TILDE}"),
        "vec"     : combining(u"\N{Combining Right Arrow Above}"),

        #Table 169: Extensible Accents
        "widetilde"     : combining(u"\N{Combining Double Tilde}"),
        "overleftarrow" : combining(),
        "overline"      : combining(),
        "overbrace"     : combining(),
        "widehat"       : combining(u"\N{Combining Double Circumflex Above}"),
        "overrightarrow": combining(),
        "underline"     : combining(),
        "sqrt"          : combining(),

        #Table 189: Dots
        "cdotp"    : symbol(u"\N{MIDDLE DOT}"),
        "cdots"    : symbol(u"\N{MIDLINE HORIZONTAL ELLIPSIS}"),
        "colon"    : symbol(u"\N{COLON}"),
        "ddots"    : symbol(u"\N{DOWN RIGHT DIAGONAL ELLIPSIS}"),
        "ldotp"    : symbol(u"\N{FULL STOP}"),


        #Table 201: Miscellaneous LATEX 2e Math Symbols
        "aleph"      : symbol(u"\N{ALEF SYMBOL}"),
        "backslash"  : symbol(u"\\"),
        "clubsuit"   : symbol(u"\N{BLACK CLUB SUIT}"),
        "diamondsuit": symbol(u"\N{WHITE DIAMOND SUIT}"),
        "emptyset"   : symbol(u"\N{EMPTY SET}"),
        "natural"    : symbol(u"\N{MUSIC NATURAL SIGN}"),
        "heartsuit"  : symbol(u"\N{WHITE HEART SUIT}"),
        "infty"      : symbol(u"\N{INFINITY}"),
        "nabla"      : symbol(u"\N{NABLA}"),
        "neg"        : symbol(u"\N{NOT SIGN}"),
        "prime"      : symbol(u"\N{PRIME}"),
        "sharp"      : symbol(u"\N{MUSIC SHARP SIGN}"),
        "spadesuit"  : symbol(u"\N{BLACK SPADE SUIT}"),
        "surd"       : symbol(u"\N{SQUARE ROOT}"),
        "triangle"   : symbol(u"\N{WHITE UP-POINTING TRIANGLE}"),
        
        #characters not documented in the comprehensive latex symbols list
        "!"               : symbol(u""),  #negative thin space, -1/6 quad
        ":"               : symbol(u" "), #medium space 2/9 quad
        ";"               : symbol(u'\u2009\u200a\u200a'), #thick space 5/18
        "|"               : symbol(u"\N{PARALLEL TO}"),

        "approx"          : symbol(u"\N{ALMOST EQUAL TO}"),
        "asymp"           : symbol(u"\N{EQUIVALENT TO}"),
        "bmod"            : symbol(u"mod"),
        "bowtie"          : symbol(u"\N{BOWTIE}"),
        "cong"            : symbol(u"\N{APPROXIMATELY EQUAL TO}"),
        "dashv"           : symbol(u"\N{LEFT TACK}"),
        "doteq"           : symbol(u"\N{APPROACHES THE LIMIT}"),
        "equiv"           : symbol(u"\N{IDENTICAL TO}"),
        "flat"            : symbol(u"\N{MUSIC FLAT SIGN}"),
        "frown"           : symbol(u"\N{FROWN}"),
        "ge"              : symbol(u"\N{GREATER-THAN OR EQUAL TO}"),
        "gets"            : symbol(u"\N{LEFTWARDS ARROW}"),
        "iff"               : symbol(u"\N{LONG LEFT RIGHT DOUBLE ARROW}"),
        "land"              : symbol(u"\N{LOGICAL AND}"),
        "langle"            : symbol(u"\N{LEFT-POINTING ANGLE BRACKET}"), #or MATHEMATICAL LEFT ANGLE BRACKET}"),
        "lbrace"            : symbol("{"),
        "lceil"             : symbol(u"\N{LEFT CEILING}"),
        "le"                : symbol(u"\N{LESS-THAN OR EQUAL TO}"),
        "lfloor"            : symbol(u"\N{LEFT FLOOR}"),
        "lnot"              : symbol(u"\N{NOT SIGN}"),
        "lor"               : symbol(u"\N{LOGICAL OR}"),
        "mid"               : symbol(u"\N{DIVIDES}"),
        "models"            : symbol(u"\N{True}"),
        "ne"                : symbol(u"\N{Not Equal To}"),
        "notin"             : symbol(u"\N{NOT AN ELEMENT OF}"),
        "owns"              : symbol(u"\N{Contains As Member}"),
        "parallel"          : symbol(u"\N{Parallel To}"),
        "perp"              : symbol(u"\N{Perpendicular}"),
        "prec"              : symbol(u"\N{Precedes}"),
        "preceq"            : symbol(u"\N{PRECEDES ABOVE SINGLE-LINE EQUALS SIGN}"), #or Precedes or Equal To}"),
        "propto"            : symbol(u"\N{Proportional To}"),
        "rangle"            : symbol(u"\N{RIGHT-POINTING ANGLE BRACKET}"), # or Mathematical Right Angle Bracket}"),
        "rbrace"            : symbol(u"}"),
        "rceil"             : symbol(u"\N{Right Ceiling}"),
        "rfloor"            : symbol(u"\N{Right Floor}"),
        "sim"               : symbol(u"\N{Tilde Operator}"),
        "simeq"             : symbol(u"\N{Asymptotically Equal To}"),
        "smallint"          : symbol(u"\N{Integral}"),
        "smile"             : symbol(u"\N{Smile}"),
        "succ"              : symbol(u"\N{Succeeds}"),
        "succeq"            : symbol(u"\N{SUCCEEDS ABOVE SINGLE-LINE EQUALS SIGN}"), #or Succeeds or Equal To}"),
        "to"                : symbol(u"\N{Rightwards Arrow}"),
        "vdash"             : symbol(u"\N{Right Tack}"),
        "vert"              : symbol(u"\N{Vertical Line}"),
        "Vert"              : symbol(u"\N{Double Vertical Line}"),
        
        "not"             : combining(u"\N{Combining Long Solidus Overlay}"), #slash through letter
        #added for intro.tex


        "mit"            : declaration, #math italics
        "scriptstyle"    : declaration,

        "cal"             : declaration, #calligraphic letters
        "overbrace"       : {'args':1,'action':'format'},
        "overline"        : {'args':1,'action':'format'},
        "underbrace"      : {'args':1,'action':'format'},
        
        "displaystyle"    : (0,{},None), #switches to displaymath or equation environment typesetting?
        "frac"            : null(2,{}), #fraction
        "left"            : (1,{},None),
        "lefteqn"         : (1,{},None),
        "pmod"            : {'args':1},#parethesized mod operator ( mod 2x -1)
        "right"           : {'args':1}, 
        "sqrt"            : null(2,{1:""}),
        "stackrel"        : {'args':2},
        

        "mathbf"          : null(),
        "limits"          : null(1),
        "bigr"            : null(),
        "bigl"            : null(),
        "text"            : null(),
        "rm"              : null(),
        "mbox"            : null(1),
        "mathop"          : null(1),
    
    }

    envs = {
        "abstract"   : (0,{}), 
        "array"      : (1,{}), #start array enviorement
        "center"     : EnvironmentParser(),
        "description": (0,{}), #labeled list
        "displaymath": (0,{}),
        "document"   : EnvironmentParser(level=1000),
        "enumerate"  : EnvironmentParser(),
        "eqnarray"   : (0,{}),
        "eqnarray*"  : (0,{}),
        "equation"   : EnvironmentParser(mode = 'math'),
        "figure"     : EnvironmentParser(1,{1:""}),
        "figure*"    : (1,{1:""}),
        "flushleft"  : (0,{}),
        "flushright" : (0,{}),
        "itemize"    : EnvironmentParser(),
        "list"       : (2,{}),
        "math"       : (0,{}),
        "minipage"   : (2,{1:""}),
        #"picture" this one uses () for options not supporting for now
        "quotation"  : (0,{}),
        "quote"      : (0,{}),
        "tabbing"    : (0,{}),
        "table"      : EnvironmentParser(1,{1:""}),
        "table*"     : (1,{1:""}),
        "tabular"    : EnvironmentParser(1,{}),
        "theorem"    : (0,{}),
        "titlepage"  : (0,{}),
        "verbatim"   : Exception("Wrong Environment"),
        "verse"      : (0,{}),



    #Not in the list but needed for intro.tex
        "align"    : EnvironmentParser(),
        "subequations"   : EnvironmentParser(),
        "cases"    : EnvironmentParser(),
        "pmatrix"    : EnvironmentParser(mode='math'),
        "thebibliography"    : EnvironmentParser(),
        

    
    
    }


    #tabbing Environments
    #\a' for an acute accent
    #\a` for a grave accent
    #\a= for a macron accent
