% ------------------------------------------------------------------------------
%  @LaTeX-class-file{
%     filename        = "goose-article.cls",
%     version         = "1.0.0",
%     date            = "Frebuary 2024",
%     codetable       = "ISO/ASCII",
%     keywords        = "LaTeX, goose-article",
%     supported       = "https://github.com/tdegeus/goose-article",
%     docstring       = "A customized article-class."
% ------------------------------------------------------------------------------

% ==============================================================================
% Basic settings
% ==============================================================================

\NeedsTeXFormat{LaTeX2e}[2022-06-01]
\ProvidesClass{goose-article}[2024/02/14 v1.0.0 customized article class]

% ==============================================================================
% Options
% ==============================================================================

\newif\if@twocolumnbib
\let\if@twocolumnbib\iffalse
\DeclareOption{twocolumnbib}{\let\if@twocolumnbib\iftrue}

\newif\if@doublespacing
\let\if@doublespacing\iffalse
\DeclareOption{doublespacing}{\let\if@doublespacing\iftrue}

\newif\if@linenumbers
\let\if@linenumbers\iffalse
\DeclareOption{linenumbers}{\let\if@linenumbers\iftrue}

\newif\if@fleqn
\let\if@fleqn\iffalse
\DeclareOption{fleqn}{\let\if@fleqn\iftrue}

\DeclareKeys[myopts]{
    bibpackage.store = \@myopts@bibpackage,
    bibpackage.usage = load,
    bibsize.store = \@myopts@bibsize,
    bibsize.usage = load,
    bibcols.store = \@myopts@bibcols,
    bibcols.usage = load,
    left.store = \@myopts@left,
    left.usage = load,
    right.store = \@myopts@right,
    right.usage = load,
    top.store = \@myopts@top,
    top.usage = load,
    bottom.store = \@myopts@bottom,
    bottom.usage = load,
    paragraphshape.store = \@myopts@paragraphshape,
    paragraphshape.usage = load,
    paragraphafter.store = \@myopts@paragraphafter,
    paragraphafter.usage = load,
    font.store = \@myopts@fontname,
    font.usage = load,
    pagenumbers.if = @myopts@@pagenumbers,
    pagenumbers.usage = load,
}

\SetKeys[myopts]{
    bibpackage = natbib,
    bibsize = scriptsize,
    bibcols = 1,
    left = 25mm,
    right = 25mm,
    top = 30mm,
    bottom = 30mm,
    paragraphshape = runin,
    paragraphafter = .,
    font = default,
    pagenumbers = true,
}

\ProcessKeyOptions[myopts]

\DeclareOption{openright}{\OptionNotUsed}
\DeclareOption{openany}{\OptionNotUsed}

\PassOptionsToClass{a4paper}{article}
\PassOptionsToClass{twoside}{article}
\if@fleqn
    \PassOptionsToClass{fleqn}{article}
\fi

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
\ProcessOptions\relax

\LoadClass{article}
\let\@unusedoptionlist\@empty

% ==============================================================================
% Packages
% ==============================================================================

\RequirePackage[
    left = \@myopts@left,
    right = \@myopts@right,
    top = \@myopts@top,
    bottom = \@myopts@bottom,
]{geometry}

\RequirePackage{ifthen}
\RequirePackage{fix-cm}
\RequirePackage{graphicx}
\RequirePackage{subfig}
\RequirePackage{amssymb}
\RequirePackage{amsfonts}
\RequirePackage{bm}
\RequirePackage{enumerate}
\if@fleqn
    \RequirePackage[fleqn]{amsmath}
\else
    \RequirePackage{amsmath}
\fi
\RequirePackage[font={small},labelfont=bf,labelsep=period]{caption}
\RequirePackage[bf]{titlesec}
\RequirePackage[dvipsnames]{xcolor}
\RequirePackage{authblk}
\RequirePackage{ragged2e}
\RequirePackage{multicol}
\RequirePackage{uri} % https://github.com/retorquere/zotero-better-bibtex/issues/1336
\RequirePackage{hyperref}
\RequirePackage[capitalise]{cleveref}

% ==============================================================================
% Bibliography
% ==============================================================================

\ifthenelse{\equal{\@myopts@bibpackage}{natbib}}{
    \RequirePackage[square,sort&compress,numbers,comma]{natbib}

    \let\oldbibliography\bibliography
    \renewcommand{\bibliography}[1]{%
        \setlength{\bibsep}{3pt plus 0.3ex}
        \def\bibfont{\csname \@myopts@bibsize\endcsname}
        \ifthenelse{\equal{\@myopts@bibcols}{1}}{
            \raggedright\oldbibliography{#1}\justifying
        }{
            \begin{multicols}{\@myopts@bibcols}
                \raggedright\oldbibliography{#1}\justifying
            \end{multicols}
        }
    }
}{
    \ifthenelse{\equal{\@myopts@bibpackage}{biblatex}}{
        \RequirePackage[sortcites,backend=bibtex,style=numeric-comp,sorting=none]{biblatex}
        \AtBeginBibliography{\csname \@myopts@bibsize\endcsname}
        \ifthenelse{\equal{\@myopts@bibcols}{1}}{
            % one column -> do nothing
        }{
            \ClassError{goose-article}{'bibpackage=biblatex': 'bibcols=\@myopts@bibcols' not allowed}{}
        }
    }{
        \ifthenelse{\equal{\@myopts@bibpackage}{none}}{
            % no bibliography backend -> do nothing
        }{
            \ClassError{goose-article}{Unknown option 'bibpackage=\@myopts@bibpackage'}{}
        }
    }
}

% ==============================================================================
% Font
% ==============================================================================

\ifthenelse{\equal{\@myopts@fontname}{default}}{
    % default
}
{
    \RequirePackage{mathspec}
    \RequirePackage{fontspec}

    \ifthenelse{\equal{\@myopts@fontname}{garamond}}{
        \AtBeginDocument{%
            \setmathfont(Digits)[Numbers=OldStyle]{Garamond}%
            \setromanfont[%
                BoldFont={Garamond Bold},%
                ItalicFont={Garamond Italic},%
                Mapping=tex-text%
            ]{Garamond}%
        }%
    }{
        % other font
    }

    \ifthenelse{\equal{\@myopts@fontname}{verdana}}{
        \AtBeginDocument{%
            \defaultfontfeatures{Mapping=tex-text}
            \setmainfont[Mapping=tex-text]{Verdana}
            \setsansfont{Verdana}
            \renewcommand*{\familydefault}{\sfdefault}
            \setmathfont(Greek,Digits,Latin){Verdana}
            \setmathrm{Verdana}
        }%
    }{
        % other font
    }

    \ifthenelse{\equal{\@myopts@fontname}{times}}{
        \AtBeginDocument{%
            \setmathfont(Digits)[Numbers=OldStyle]{Times New Roman}%
            \setromanfont[%
                BoldFont={Times New Roman Bold},%
                ItalicFont={Times New Roman Italic},%
                Mapping=tex-text%
            ]{Times New Roman}%
        }%
    }{
        % other font
    }
}

% ==============================================================================
% Convience development options
% ==============================================================================

\if@doublespacing
    \AtBeginDocument{%
        \RequirePackage{setspace}
        \doublespacing
    }%
\fi

\if@linenumbers
    \AtBeginDocument{%
        \RequirePackage{lineno}
        \linenumbers
    }%
\fi

% ==============================================================================
% Hyperref
% ==============================================================================

\hypersetup{
    pdftitle=\@title,
    breaklinks=true,
    colorlinks=true,
    citecolor=NavyBlue,
    filecolor=NavyBlue,
    linkcolor=NavyBlue,
    urlcolor=NavyBlue,
    bookmarksopen=true,
}

% ==============================================================================
% Headers
% ==============================================================================

% \titleformat{command}[shape]{format}{label}{sep}{before}[after]
\titleformat{\section}{\normalfont\large\bfseries}{\thesection}{1em}{}{}
\titleformat{\subsection}{\normalfont\normalsize\bfseries}{\thesubsection}{1em}{}{}
\titleformat{\subsubsection}{\normalfont\normalsize\bfseries}{\thesubsubsection}{1em}{}{}

\ifthenelse{\equal{\@myopts@paragraphafter}{none}}{
    \titleformat{\paragraph}[\@myopts@paragraphshape]{\normalfont\normalsize\bfseries}{}{}{}
}{
    \titleformat{\paragraph}[\@myopts@paragraphshape]{\normalfont\normalsize\bfseries}{}{}{}[\@myopts@paragraphafter]
}

% spacing {left}{top}{bottom}, of:
\titlespacing{\section}{0pt}{1eM}{0.8em}
\titlespacing{\subsection}{0pt}{0.8em}{0.4em}
\titlespacing{\subsubsection}{0pt}{0.8em}{0.4em}
\titlespacing{\paragraph}{0pt}{0.8em}{1em}

% no paragraph indent after header
\AtBeginDocument{%
    \makeatletter
    \let\orig@afterheading\@afterheading
    \def\@afterheading{%
        \@afterindentfalse
        \orig@afterheading
    }
    \makeatother
}

% ==============================================================================
% Title, authors, affiliation layout
% ==============================================================================

% basic settings
\newcommand{\nl}{\vspace*{-.3em}\protect\\ \fontsize{9}{10.8}\itshape}
\renewcommand\Authfont{\fontsize{11}{14.4}\selectfont}
\renewcommand\Affilfont{\fontsize{9}{10.8}\itshape}
\renewcommand*{\Authsep}{, }
\renewcommand*{\Authand}{, }
\renewcommand*{\Authands}{, }

% actual layout
\renewcommand{\maketitle}{%
    \newpage
    \null
    \vskip 2em%
    \begin{center}%
        \let \footnote \thanks
        {\Large\bfseries \@title \par}%
        \vskip 1.5em%
        {
            \normalsize
            \lineskip .5em%
            \begin{tabular}[t]{c}%
                \@author
            \end{tabular}
            \par
        }%
        \vskip 0.5em%
        {\small \@date}%
    \end{center}%
    \par
    \vskip 1.5em
    \thispagestyle{fancy}
}

% ==============================================================================
% Keywords
% ==============================================================================

\newcommand{\keywords}[1]{\vspace*{0.5eM}\noindent\textbf{Keywords: }#1}

% ==============================================================================
% Header and footer
% ==============================================================================

\RequirePackage{fancyhdr}
\setlength{\headheight}{16pt}
\pagestyle{fancy}
\fancyhead{}
\fancyfoot{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

\if@myopts@@pagenumbers
    \fancyhead[RO,LE]{\thepage}
\fi

\newcommand{\header}[1]{\fancyhead[LO,RE]{#1}}
\newcommand{\headerOdd}[1]{\fancyhead[LO]{#1}}
\newcommand{\headerEven}[1]{\fancyhead[RE]{#1}}
