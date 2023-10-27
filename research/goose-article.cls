% ------------------------------------------------------------------------------
%  @LaTeX-class-file{
%     filename        = "goose-article.cls",
%     version         = "0.10.1",
%     date            = "February 2023",
%     codetable       = "ISO/ASCII",
%     keywords        = "LaTeX, goose-article",
%     supported       = "https://github.com/tdegeus/goose-article",
%     docstring       = "A customized article-class."
% ------------------------------------------------------------------------------

% ==============================================================================
% Basic settings
% ==============================================================================

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{goose-article}[2022/04/06 v0.10.0 customized article class]

% ==============================================================================
% Options
% ==============================================================================

% Bibliography [namecite, twocolumnbib]
% -------------------------------------

\newif\if@namecite
\let\if@namecite\iffalse
\DeclareOption{namecite}{\let\if@namecite\iftrue}

\newif\if@twocolumnbib
\let\if@twocolumnbib\iffalse
\DeclareOption{twocolumnbib}{\let\if@twocolumnbib\iftrue}

% Layout [narrow, wide, wwide, doublespacing]
% -------------------------------------------

\newif\if@narrow
\let\if@narrow\iffalse
\DeclareOption{narrow}{\let\if@narrow\iftrue}

\newif\if@wwide
\let\if@wwide\iffalse
\DeclareOption{wwide}{\let\if@wwide\iftrue}

\newif\if@wide
\let\if@wide\iffalse
\DeclareOption{wide}{\let\if@wide\iftrue}

\newif\if@doublespacing
\let\if@doublespacing\iffalse
\DeclareOption{doublespacing}{\let\if@doublespacing\iftrue}

% Header [empty]
% --------------

\newif\if@empty
\let\if@empty\iffalse
\DeclareOption{empty}{\let\if@empty\iftrue}

% Pargraph [plainparagraph]
% -------------------------

\newif\if@plainparagraph
\let\if@plainparagraph\iffalse
\DeclareOption{plainparagraph}{\let\if@plainparagraph\iftrue}

% Math [fleqn]
% ------------

\newif\if@fleqn
\let\if@fleqn\iffalse
\DeclareOption{fleqn}{\let\if@fleqn\iftrue}

% Font [times, garamond, verdana]
% -------------------------------

\newif\if@font
\let\if@font\iffalse

\newif\if@times
\let\if@times\iffalse
\DeclareOption{times}{\let\if@times\iftrue\let\if@font\iftrue}

\newif\if@garamond
\let\if@garamond\iffalse
\DeclareOption{garamond}{\let\if@garamond\iftrue\let\if@font\iftrue}

\newif\if@verdana
\let\if@verdana\iffalse
\DeclareOption{verdana}{\let\if@verdana\iftrue\let\if@font\iftrue}

% Hyperref [showlinks, colorlinks]
% --------------------------------

\newif\if@showlinks
\let\if@showlinks\iffalse
\DeclareOption{showlinks}{\let\if@showlinks\iftrue}

\newif\if@colorlinks
\let\if@colorlinks\iffalse
\DeclareOption{colorlinks}{\let\if@colorlinks\iftrue}

% Process options
% ---------------

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}

\ProcessOptions\relax

% ==============================================================================
% Packages
% ==============================================================================

\if@fleqn
    \LoadClass[a4paper, fleqn, twoside]{article}
\else
    \LoadClass[a4paper, twoside]{article}
\fi

\if@narrow
    \RequirePackage[left=40mm, right=40mm, top=30mm, bottom=30mm]{geometry}
\else
    \if@wwide
        \RequirePackage[left=10mm, right=10mm, top=20mm, bottom=20mm]{geometry}
    \else
        \if@wide
            \RequirePackage[left=15mm, right=15mm, top=20mm, bottom=20mm]{geometry}
        \else
            \RequirePackage[left=25mm, right=25mm, top=30mm, bottom=30mm]{geometry}
        \fi
    \fi
\fi

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
% Citation style
% ==============================================================================

\if@namecite
    \RequirePackage{natbib}
    \let\oldbibliography\bibliography
    \renewcommand{\bibliography}[1]{%
        \setlength{\bibsep}{3pt plus 0.3ex}
        \def\bibfont{\scriptsize}
        \if@twocolumnbib
            \begin{multicols}{2}
                \raggedright\oldbibliography{#1}\justifying
            \end{multicols}
        \else
            \raggedright\oldbibliography{#1}\justifying
        \fi
    }
\else
    \RequirePackage[square,sort&compress,numbers,comma]{natbib}
    \let\oldbibliography\bibliography
    \renewcommand{\bibliography}[1]{%
        \setlength{\bibsep}{3pt plus 0.3ex}
        \def\bibfont{\scriptsize}
        \if@twocolumnbib
            \begin{multicols}{2}
                \raggedright\oldbibliography{#1}\justifying
            \end{multicols}
        \else
            \raggedright\oldbibliography{#1}\justifying
        \fi
    }
\fi

% escape underscopes (in DOI): https://stackoverflow.com/a/57028315/2646505
\newcommand{\replunderscores}[1]{\expandafter\@repl@underscores#1_\relax}

\def\@repl@underscores#1_#2\relax{%
    \ifx
        \relax #2\relax
        % #2 is empty => finish
        #1%
    \else
        % #2 is not empty => underscore was contained, needs to be replaced
        #1%
        \textunderscore
        % continue replacing
        % #2 ends with an extra underscore so I don't need to add another one
        \@repl@underscores#2\relax
    \fi
}

\renewcommand*{\doi}[1]{\sloppy\href{https://dx.doi.org/#1}{doi:~\replunderscores{#1}}}
\newcommand*{\arxivid}[1]{\sloppy\href{https://arxiv.org/abs/#1}{arXiv:~\replunderscores{#1}}}

% ==============================================================================
% Font
% ==============================================================================

\if@font
    \RequirePackage{mathspec}
    \RequirePackage{fontspec}
\fi

\if@garamond
    \AtBeginDocument{%
        \setmathfont(Digits)[Numbers=OldStyle]{Garamond}%
        \setromanfont[%
            BoldFont={Garamond Bold},%
            ItalicFont={Garamond Italic},%
            Mapping=tex-text%
        ]{Garamond}%
    }%
\fi

\if@verdana
    \AtBeginDocument{%
        \defaultfontfeatures{Mapping=tex-text}
        \setmainfont[Mapping=tex-text]{Verdana}
        \setsansfont{Verdana}
        \renewcommand*{\familydefault}{\sfdefault}
        \setmathfont(Greek,Digits,Latin){Verdana}
        \setmathrm{Verdana}
    }%
\fi

\if@times
    \AtBeginDocument{%
        \setmathfont(Digits)[Numbers=OldStyle]{Times New Roman}%
        \setromanfont[%
            BoldFont={Times New Roman Bold},%
            ItalicFont={Times New Roman Italic},%
            Mapping=tex-text%
        ]{Times New Roman}%
    }%
\fi

% ==============================================================================
% Spacing
% ==============================================================================

\if@doublespacing
    \AtBeginDocument{%
        \usepackage{setspace}
        \doublespacing
    }%
\fi

% ==============================================================================
% Hyperref
% ==============================================================================

\if@showlinks
    \AtBeginDocument{%
        \hypersetup{%
            pdftitle=\@title,
            citecolor=NavyBlue,
            filecolor=NavyBlue,
            linkcolor=NavyBlue,
            urlcolor=NavyBlue,
            breaklinks,
            bookmarksopen=true,
        }%
    }
\else
    \if@colorlinks
        \AtBeginDocument{%
            \hypersetup{%
                pdftitle=\@title,
                citecolor=NavyBlue,
                filecolor=NavyBlue,
                linkcolor=NavyBlue,
                urlcolor=NavyBlue,
                breaklinks,
                bookmarksopen=true,
            }%
        }
    \else
        \AtBeginDocument{%
            \hypersetup{%
                pdftitle=\@title,
                citecolor=NavyBlue,
                filecolor=NavyBlue,
                linkcolor=NavyBlue,
                urlcolor=NavyBlue,
                breaklinks,
                hidelinks,
                bookmarksopen=true,
            }%
        }
    \fi
\fi

% ==============================================================================
% Headers
% ==============================================================================

% \titleformat{command}[shape]{format}{label}{sep}{before}[after]
\titleformat{\section}{\normalfont\large\bfseries}{\thesection}{1em}{}{}
\titleformat{\subsection}{\normalfont\normalsize\bfseries}{\thesubsection}{1em}{}{}
\titleformat{\subsubsection}{\normalfont\normalsize\bfseries}{\thesubsubsection}{1em}{}{}
\if@plainparagraph
    \titleformat{\paragraph}[runin]{\normalfont\normalsize\bfseries}{}{}{}
\else
    \titleformat{\paragraph}[runin]{\normalfont\normalsize\bfseries}{}{}{}[.]
\fi

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

% add option
\newcommand{\contact}[1]{\date{{#1}}}

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
\if@empty
\else
    \fancyhead[RO,LE]{\thepage}
\fi
\newcommand{\header}[1]{\fancyhead[LO,RE]{#1}}
\newcommand{\headerOdd}[1]{\fancyhead[LO]{#1}}
\newcommand{\headerEven}[1]{\fancyhead[RE]{#1}}
