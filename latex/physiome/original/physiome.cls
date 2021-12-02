%% Modified from olplainarticle.cls
% A plain single-column layout for articles.
%
% Created by Overleaf (writeLaTeX).
%
% Based on the SelfArx document class.
%
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{physiome}[2020/07/31, v2.1]
\RequirePackage[english]{babel}

\newif\if@reqslineno
\DeclareOption{lineno}{\@reqslinenotrue}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
\ProcessOptions*
\LoadClass{article}
\def\@journallogo{Physiome-under}

\RequirePackage{ifxetex,ifluatex}
\newif\ifxetexorluatex
\ifxetex
  \xetexorluatextrue
\else
  \ifluatex
    \xetexorluatextrue
  \else
    \xetexorluatexfalse
  \fi
\fi

\ifxetexorluatex
\else
  \RequirePackage[utf8]{inputenc}
  \RequirePackage[T1]{fontenc}
  \RequirePackage{textcomp}
\fi

\RequirePackage{xparse}
\RequirePackage{calc}
\AtEndOfClass{%
  \RequirePackage{microtype}
  \ifxetex
   \renewcommand{\lsstyle}{\addfontfeatures{LetterSpace=10}}
  \fi
}

\ifxetexorluatex
  \RequirePackage{fontspec}
  \setmainfont{TeX Gyre Pagella}
\else
  \RequirePackage{tgpagella}
\fi
% \RequirePackage{helvet}
\RequirePackage[defaultsans]{lato}
\renewcommand{\familydefault}{\sfdefault}
\RequirePackage[defaultmono]{droidsansmono}
\RequirePackage[cmintegrals,nosymbolsc]{newtxsf}
\RequirePackage{lineno}     % For numbering the lines if lineno option is given
\if@reqslineno\linenumbers\fi

\RequirePackage{amsmath,amssymb}
\RequirePackage{graphicx}
\RequirePackage[dvipsnames,RGB]{xcolor}
\RequirePackage{booktabs}
\RequirePackage{threeparttable}
\RequirePackage{authblk}
\RequirePackage{mdframed}
\RequirePackage{marginnote}
\RequirePackage{parskip}
\RequirePackage{abstract}
\RequirePackage[left=5cm,%
                right=2cm,%
                top=2.25cm,%
                bottom=2.25cm,%
                headheight=12pt,%
                letterpaper,%
                reversemarginpar,%
                marginparwidth=3.25cm,%
                marginparsep=2em%
                ]{geometry}%
                
\RequirePackage[font={rm},labelfont={bf,sf},%
                labelsep=period,%
                skip=4pt,tableposition=top,%
                singlelinecheck=false,justification=centering]{caption}
                
\RequirePackage[round]{natbib}
\RequirePackage{multibib}
\newcites{primepub}{Primary Publications}
\bibliographystyle{abbrvnat}
\bibliographystyleprimepub{abbrvnat}

%% Updated 31 July, 2020 to add curated DOI
%% as optional argument
\newcommand{\primarypubs}[3][]{%
  \nociteprimepub{#3}
    \begin{mdframed}[backgroundcolor=color2!50!white,topline=false,bottomline=false,rightline=false,leftline=false,font=\sffamily,leftmargin=-10\p@,rightmargin=-10\p@,innertopmargin=0\p@,%
        innerbottommargin=10\p@
    ]
  \if@reqslineno\internallinenumbers\fi
  \ifstrempty{#1}{}{%
    \medskip\textbf{Curated Model Implementation: }\url{http://dx.doi.org/#1}\par%
  }
  \renewcommand{\bibsection}{\subsection*{\refname}}
  \bibliographyprimepub{#2}
  \end{mdframed}\medskip
}

%
% headers and footers
%
\RequirePackage{fancyhdr}  % custom headers/footers
\RequirePackage{lastpage}  % Number of pages in the document
\pagestyle{fancy}          % Enables the custom headers/footers
% Headers
\lhead{}%
\chead{}%
\rhead{}%
% Footers
\lfoot{}%
\cfoot{}%
\rfoot{\small\sffamily\bfseries\thepage/\pageref{LastPage}}%
\renewcommand{\headrulewidth}{0pt}% % No header rule
\renewcommand{\footrulewidth}{0pt}% % No footer rule

%
% section/subsection/paragraph set-up
%
\RequirePackage[explicit]{titlesec}
\titleformat{\section}
  {\color{color1}\large\sffamily\bfseries}
  {\thesection}
  {0.5em}
  {#1}
  []
\titleformat{name=\section,numberless}
  {\color{color1}\large\sffamily\bfseries}
  {}
  {0em}
  {#1}
  []  
\titleformat{\subsection}
  {\sffamily\bfseries}
  {\thesubsection}
  {0.5em}
  {#1}
  []
\titleformat{\subsubsection}
  {\sffamily\small\bfseries\itshape}
  {\thesubsubsection}
  {0.5em}
  {#1}
  []    
\titleformat{\paragraph}[runin]
  {\sffamily\small\bfseries}
  {}
  {0em}
  {#1} 
\titlespacing*{\section}{0pc}{3ex \@plus4pt \@minus3pt}{5pt}
\titlespacing*{\subsection}{0pc}{2.5ex \@plus5pt \@minus2pt}{3pt}
\titlespacing*{\subsubsection}{0pc}{2ex \@plus4.5pt \@minus1.5pt}{2pt}
\titlespacing*{\paragraph}{0pc}{1.5ex \@plus4pt \@minus1pt}{10pt}

%
% tableofcontents set-up
%
\RequirePackage{titletoc}
\contentsmargin{0cm}
\titlecontents{section}[\tocsep]
  {\addvspace{4pt}\small\bfseries\sffamily}
  {\contentslabel[\thecontentslabel]{\tocsep}}
  {}
  {\hfill\thecontentspage}
  []
\titlecontents{subsection}[\tocsep]
  {\addvspace{2pt}\small\sffamily}
  {\contentslabel[\thecontentslabel]{\tocsep}}
  {}
  {\ \titlerule*[.5pc]{.}\ \thecontentspage}
  []
\titlecontents*{subsubsection}[\tocsep]
  {\footnotesize\sffamily}
  {}
  {}
  {}
  [\ \textbullet\ ]  
  
\RequirePackage{enumitem}
%\setlist{nolistsep} % Uncomment to remove spacing between items in lists (enumerate, itemize)


%
% article meta data
%
\newcommand{\keywords}[1]{\noindent\textcolor{color1}{\keywordname}\quad #1\par}%\vskip25\p@}
\newcommand{\articletype}[1]{\def\physiome@articletype{#1}}

%
% custom title page 
%
\newcommand{\publicationdate}[1]{\def\physiome@pubdate{#1}}
\newcommand{\curator}[1]{\def\physiome@curator{#1}}
\newcommand{\editor}[1]{\def\physiome@editor{#1}}
\newcommand{\submitteddate}[1]{\def\physiome@submitdate{#1}}
\newcommand{\accepteddate}[1]{\def\physiome@acceptdate{#1}}
\newcommand{\citethisas}[2]{\def\physiome@citethisas{#1}\def\physiome@thisdoi{#2}}
\let\authblk@author\author
\let\oldaffil\affil
\RenewDocumentCommand{\author}{ o o m }{%
  \IfValueTF{#2}{%
    \authblk@author[#1*]{#3}%
      \global\edef\physiome@corrauthor{\detokenize{#2}}%
  }{%
    \authblk@author[#1]{#3}%
  }%
}
\RequirePackage[absolute]{textpos}
\renewcommand\AB@authnote[1]{\textsuperscript{#1}}
\renewcommand\AB@affilnote[1]{\textsuperscript{#1}}
\renewcommand{\@maketitle}{%
    \def\@makefnmark{}%
    \begin{textblock*}{\marginparwidth}[1,0]%
      (\dimexpr\Gm@lmargin-\marginparsep,\Gm@tmargin)
      \raggedleft\footnotesize%
      \includegraphics[width=\hsize]{\@journallogo}%
      \ifdefvoid{\physiome@pubdate}{}{\\Published \physiome@pubdate}%
    \end{textblock*}
    %
    \begin{textblock*}{\marginparwidth}[1,1]%
      (\dimexpr\Gm@lmargin-\marginparsep,\dimexpr\paperheight-\Gm@bmargin)
      \raggedleft\footnotesize\itshape%
      {\large\rmfamily\upshape\bfseries OPEN ACCESS\strut\\\normalsize\sffamily Reproducible Model\par}%
      \ifdefvoid{\physiome@editor}{}{\textbf{Edited by}\\\physiome@editor\par}%
      \ifdefvoid{\physiome@curator}{}{\textbf{Curated by}\\\physiome@curator\par}%
      \ifdefvoid{\physiome@corrauthor}{}{\textbf{*Corresponding author}\\\physiome@corrauthor\par}%
      \ifdefvoid{\physiome@submitdate}{}{\textbf{Submitted}  \physiome@submitdate\par}%
      \ifdefvoid{\physiome@acceptdate}{}{\textbf{Accepted}  \physiome@acceptdate\par}%
      \ifdefvoid{\physiome@citethisas}{}{\textbf{Citation}\\\physiome@citethisas\\doi: \physiome@thisdoi\par}%      
    \end{textblock*}
    
    {\raggedright\sffamily\bfseries\fontsize{20}{25}\selectfont\@title\par}%
    \vskip10pt
    {\raggedright\@author\par}
    \vskip12pt%
    {\bfseries\Large\rmfamily\lsstyle\MakeUppercase{\physiome@articletype}\par}
    \vskip18pt%
}
\apptocmd{\maketitle}{\thispagestyle{empty}}{}{}
%-----------------------------------------------

\renewcommand{\abstractnamefont}{\normalfont\normalsize\bfseries}
\renewcommand{\abstracttextfont}{\normalfont\normalsize}
\renewcommand{\absnamepos}{flushleft}
\setlength{\absleftindent}{0pt}
\setlength{\absrightindent}{0pt}
\AfterEndEnvironment{abstract}{\medskip}

\definecolor{color1}{RGB}{0,0,0} % Color of section headings
\definecolor{color2}{RGB}{209,178,220} % Color of the box behind the abstract
\newcommand{\keywordname}{Keywords:} % Defines the keywords heading name

\renewcommand\Authfont{\fontsize{12}{14}\sffamily\bfseries}
\renewcommand\Affilfont{\fontsize{10}{12}\sffamily\bfseries}

\setcounter{tocdepth}{3} % Show only three levels in the table of contents section: sections, subsections and subsubsections
\flushbottom

\AtBeginDocument{%
  \RequirePackage[colorlinks,allcolors=black,linkcolor=Blue!60!black,citecolor=PineGreen!40!black,urlcolor=BrickRed!30!black,pdfpagelabels=false]{hyperref}
  \newcommand{\doi}{doi: \begingroup\Url}
  \urlstyle{sf}
}