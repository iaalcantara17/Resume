import re
import subprocess, pathlib, re, sys

D = pathlib.Path(__file__).parent
PRE = (D / "preamble.tex").read_text()

HEADER = r"""
\begin{document}

\begin{center}
    {\Huge \scshape Israel Alcantara} \\ \vspace{1pt}
    \small Newark, NJ\IfFileExists{phone.tex}{\input{phone.tex}\unskip}{} $|$ \href{mailto:ialcantara2003@gmail.com}{\underline{ialcantara2003@gmail.com}} $|$
    \href{https://www.linkedin.com/in/israel-alcantara}{\underline{linkedin.com/in/israel-alcantara}} \\
    \href{https://github.com/iaalcantara17}{\underline{github.com/iaalcantara17}} $|$
    \href{https://israelalcantara.vercel.app}{\underline{israelalcantara.vercel.app}}
\end{center}
\vspace{-8pt}
"""

MSU = r"""    \resumeSubheading
      {Montclair State University}{Montclair, NJ}
      {Master of Business Administration $|$ Feliciano School of Business $|$ GPA: 4.0}{Expected Dec 2028}
"""
MSU_CW = r"""      \resumeLine{\textbf{Coursework}: Business Statistics, Strategic Information Systems, Business Essentials, Global Economy}
"""
NJIT = r"""    \resumeSubheading
      {New Jersey Institute of Technology}{Newark, NJ}
      {Bachelor of Science in Computer Science $|$ Ying Wu College of Computing $|$ Cum Laude $|$ GPA: 3.4}{May 2026}
"""
NJIT_CW = r"""      \resumeLine{\textbf{Coursework}: Operating Systems, Computer Networks, Database System Design, Intensive Programming in Linux, Intro to Cybersecurity, Intro to Machine Learning}
"""
NJIT_HON = r"""      \resumeLine{\textbf{Honors}: Dean's List (4 semesters), Theodore and Lois John, Guastaferro Memorial, and Orsted Opportunity Scholarships}
      \resumeLine{\textbf{Affiliations}: ColorStack Fellow, HACCS, SHPE, ALPFA, ACM $|$ \textbf{Languages}: English and Spanish (fluent)}
"""
NJIT_LANG = r"""      \resumeLine{\textbf{Languages}: English and Spanish (fluent)}
"""


def education(cw=True, honors=True, lang_only=False, njit_cw=True):
    s = "\\section{Education}\n  \\resumeSubHeadingListStart\n" + MSU
    if cw:
        s += MSU_CW
    s += NJIT
    if cw and njit_cw:
        s += NJIT_CW
    if honors:
        s += NJIT_HON
    elif lang_only:
        s += NJIT_LANG
    return s + "  \\resumeSubHeadingListEnd\n\n"


SKILL_LINES = {
    "pm": r"\textbf{Project \& Business}{: Project Management, Project Coordination, Agile/Scrum, Jira, Event Planning, Budgeting, Excel}",
    "it": r"\textbf{Cloud \& IT}{: AWS (CloudWatch), Technical Support, Troubleshooting, Linux, Git, AV Systems (Crestron)}",
    "prog": r"\textbf{Programming}{: Java, Python, SQL, JavaScript, TypeScript, C/C++, Kotlin, Bash}",
    "fw": r"\textbf{Frameworks \& Data}{: React, React Native, Node.js, Express, Supabase (Postgres), MySQL, MongoDB, Pandas, JUnit}",
    "retail": r"\textbf{Customer \& Sales}{: Customer Service, Technical Support, Troubleshooting, Device Setup, Microsoft Office (Excel)}",
    "lang": r"\textbf{Languages}{: English and Spanish (fluent)}",
    "pm_m": r"\textbf{Project \& Business}{: Project Management, Project Coordination, Agile/Scrum, Jira, Event Planning, Budgeting, Excel}",
}


def skills(keys):
    body = " \\\\\n      ".join(SKILL_LINES[k] for k in keys)
    return ("\\section{Skills}\n\\begin{itemize}[leftmargin=0.15in, label={}]\n    \\small{\\item{\n      "
            + body + "\n    }}\n\\end{itemize}\n\n")


def summary(text):
    return ("\\section{Summary}\n\\begin{itemize}[leftmargin=0.15in, label={}, topsep=0pt, partopsep=0pt]\n    \\small{\\item{" + text
            + "}}\n\\end{itemize}\n\n")


JOBS = {
    "bestbuy": ("Best Buy", "Secaucus, NJ", "Geek Squad Agent", "Nov 2026 -- Present", {
        "a": "Serve as the first point of contact for customers' hardware issues, documenting each case and giving repair estimates.",
        "b": "Set up new devices, advise on repair or replace, update customers on queues, and partner on complex repairs.",
        "b3": "Set up new devices, advise customers on repair or replace, and keep them updated on service-queue status.",
        "c3": "Partner with other agents on complex repairs and complete Best Buy's certified training courses.",
    }),
    "amerivents": ("Amerivents (US Open 2026)", "Flushing, NY", "Suite Runner", "Aug 2026 -- Sep 2026", {
        "a": "Delivered food, drinks, and guest requests to premium suites, keeping turnaround fast in a high-volume setting.",
    }),
    "eventaces": ("Event Aces (FIFA World Cup 2026)", "East Rutherford, NJ", "Beertender \\& Suite Runner", "Jun 2026 -- Jul 2026", {
        "a": "Served high volumes of guests at MetLife Stadium on game days, staying accurate and friendly under pressure.",
        "s": "Moved into a suite runner role, restocking bars with drinks, alcohol, ice, and garnishes as they ran low.",
        "t": "Handled teardown and restocking after shifts, leaving every item in its spot and the area as clean as I found it.",
    }),
    "aws": ("Amazon Web Services (AWS)", "Arlington, VA", "Software Development Engineer Intern", "May 2025 -- Aug 2025", {
        "a": "Instrumented Java emitters with 13 CloudWatch metrics to monitor how much air-gapped data could be compressed.",
        "b": "Designed and shipped a lossless compression algorithm for the Amazon Dedicated Cloud BlackMirror metrics pipeline, cutting exports by an average of 38 GB a day across 3 air-gapped regions while meeting customers' privacy concerns.",
        "c": "Built a decompressor that restores every data point, tested it with 30+ JUnit tests, and published a dashboard.",
        "pa": "Defined 13 custom CloudWatch metrics to measure how much air-gapped metric data could be compressed.",
        "pb": "Delivered a lossless compression feature on the Amazon Dedicated Cloud BlackMirror team that cut export payloads by an average of 38 GB a day across 3 air-gapped regions while meeting customers' privacy concerns.",
        "pc": "Validated the release with 30+ automated tests and a cross-region impact dashboard for the wider team.",
        "r": "Shipped a compression feature that cut data exports by an average of 38 GB a day across 3 regions.",
    }),
    "adamas": ("Adamas Building Services", "Long Branch, NJ", "Beach Attendant \\& Lifeguard", "Jul 2023 -- Sep 2023", {
        "a": "Guarded 3 pools and about 80 swimmers a shift with zero accidents, and set up 150+ chairs and umbrellas daily.",
    }),
    "ca": ("New Jersey Institute of Technology", "Newark, NJ", "Community Assistant, Office of Residential Life", "Jun 2025 -- May 2026", {
        "a": "Supervised a 400-resident complex, enforced housing policy, and resolved conduct issues with zero major violations.",
        "b": "Planned and ran all 8 to 12 building events a semester, 2 to 3 a month, on a \\$150 semester budget.",
        "c": "Served as primary responder to a two-building guest-policy incident with two CAs and the on-duty Residence Coordinator.",
    }),
    "mtss": ("Media and Technology Support Services (MTSS), NJIT", "Newark, NJ", "Delivery Technician \\& Lab Technician", "Sep 2022 -- May 2026", {
        "a": "Diagnosed AV issues for 100+ lectures a year, cutting repeat calls on the same equipment by an estimated 30\\%.",
        "b": "Standardized setup and readiness checks with a team of 5 technicians, raising estimated equipment reliability by 40\\%.",
        "d3": "Diagnosed classroom and lab hardware problems across projectors, Crestron systems, switchers, and wireless mics.",
        "r3": "Cut the repeat-call rate on the same equipment by an estimated 30\\% through systematic troubleshooting.",
    }),
    "eop": ("New Jersey Institute of Technology", "Newark, NJ", "Office Assistant, Educational Opportunity Program (EOP)", "Sep 2024 -- Aug 2025", {
        "a": "Ran the front desk, scheduled 15+ appointments a week, and made office work at least 30\\% more efficient.",
        "e1": "Ran the front desk and scheduled 15+ appointments a week through a scheduling website.",
        "e2": "Kept student records accurate and confidential.",
        "e3": "Prepared documents and handled data entry, making office work at least 30\\% more efficient.",
    }),
    "shpe": ("Society of Hispanic Professional Engineers (SHPE), NJIT Chapter", "Newark, NJ", "Event Coordination Director", "Mar 2024 -- May 2025", {
        "a": "Planned and ran 12+ networking and professional development events, leading about 10 student volunteers.",
        "b": "Grew opening-event attendance to 150 from about 60 to 70, and average attendance to 50 to 80 from 30 to 50.",
        "c": "Pitched events to the e-board, built floor plans, agendas, and budgets, and ran each event with backup plans.",
    }),
    "ra": ("New Jersey Institute of Technology", "Newark, NJ", "Resident Assistant, EOP Summer Program", "Jun 2024 -- Aug 2024", {
        "a": "Helped 150 first-year students settle into residence hall life over 10 weeks, mediating and reporting conflicts.",
    }),
}


def job(key, bullets):
    c, loc, t, d, b = JOBS[key]
    s = f"    \\resumeSubheading\n      {{{c}}}{{{loc}}}\n      {{{t}}}{{{d}}}\n"
    if not bullets:
        return s + "      \\vspace{5pt}\n"
    s += "      \\resumeItemListStart\n"
    for k in bullets:
        s += f"        \\resumeItem{{{b[k]}}}\n"
    return s + "      \\resumeItemListEnd\n"


def exp_section(title, items):
    return f"\\section{{{title}}}\n  \\resumeSubHeadingListStart\n" + "".join(job(k, b) for k, b in items) + "  \\resumeSubHeadingListEnd\n\n"


PROJECTS = {
    "linkdup": (r"\textbf{LinkdUp} $|$ \emph{React Native, Node.js, Express, TypeScript, Supabase} $|$ \href{https://linkdup.app}{\underline{linkdup.app}}", "Jan 2026 -- May 2026", {
        "a": "Built the backend of a five-person team's group planning app, which placed 2nd in NJIT's 2026 CS/IT 491 capstone.",
        "b": "Integrated the Google Places and Google Calendar APIs for venue discovery and one-click event export.",
    }),
    "portfolio": (r"\textbf{Personal Portfolio Website} $|$ \emph{React 19, Vite, GSAP, Vercel, Playwright}", "May 2026 -- Oct 2026", {
        "a": "Raised Lighthouse scores from 63 to 99 on mobile and 74 to 100 on desktop, backed by 34 Playwright tests.",
    }),
    "data": (r"\textbf{Data Analysis and Prediction App} $|$ \emph{Python, Streamlit, Scikit-learn}", "Nov 2024 -- Dec 2024", {
        "a": "Built a web app where users upload CSV data, explore it in charts, and train a Gradient Boosting Regressor model.",
    }),
    "sfort": (r"\textbf{Compiler for SFort95 Language} $|$ \emph{C++, Git}", "Mar 2024 -- Apr 2024", {
        "a": "Built a lexical analyzer, recursive-descent parser, and interpreter with runtime checks for errors like division by zero.",
    }),
}


def projects(items):
    s = "\\section{Projects}\n    \\resumeSubHeadingListStart\n"
    for k, bl in items:
        h, d, b = PROJECTS[k]
        s += f"      \\resumeProjectHeading\n          {{{h}}}{{{d}}}\n"
        if bl:
            s += "          \\resumeItemListStart\n"
            for x in bl:
                s += f"            \\resumeItem{{{b[x]}}}\n"
            s += "          \\resumeItemListEnd\n"
        else:
            s += "          \\vspace{6pt}\n"
    return s + "    \\resumeSubHeadingListEnd\n\n"


PROF, CAMPUS = "Professional Experience", "Leadership \\& Campus Experience"

VERSIONS = {
    "PM": [
        summary("MBA student and cum laude Computer Science graduate with an AWS internship and almost 4 years in campus technology operations. Leads teams, plans events from schedule to budget, and explains technical work clearly to non-technical people. Seeking an Associate Project Manager or Project Coordinator role."),
        education(njit_cw=False),
        skills(["pm", "it", "prog"]),
        exp_section(CAMPUS, [("ca", "abc"), ("mtss", ["d3", "r3", "b"]), ("shpe", "abc")]),
        exp_section(PROF, [("bestbuy", ["a", "b3", "c3"]), ("aws", ["pa", "pb", "pc"])]),
        projects([("linkdup", "a")]),
    ],
    "IT_Analyst": [
        summary("MBA student and Computer Science graduate with an AWS internship and hands-on technical support experience at NJIT and Best Buy Geek Squad, seeking an IT Analyst or Technology Analyst role."),
        education(),
        skills(["it", "pm", "prog"]),
        exp_section(PROF, [("bestbuy", ["a", "b3", "c3"]), ("aws", "abc")]),
        exp_section(CAMPUS, [("ca", "abc"), ("mtss", ["d3", "r3", "b"])]),
        projects([("linkdup", "a"), ("data", "a")]),
    ],
    "Cloud_Support": [
        summary("Computer Science graduate and MBA student with an AWS internship on Amazon Dedicated Cloud and hands-on technical support at NJIT and Best Buy Geek Squad, seeking a Cloud Support Associate role."),
        education(),
        skills(["it", "prog", "pm"]),
        exp_section(PROF, [("bestbuy", ["a", "b3", "c3"]), ("aws", "abc")]),
        exp_section(CAMPUS, [("ca", "abc"), ("mtss", ["d3", "r3", "b"])]),
        projects([("portfolio", "a"), ("linkdup", "a")]),
    ],
    "Software_Engineer": [
        education(),
        skills(["prog", "fw", "it", "pm"]),
        exp_section(PROF, [("bestbuy", "a"), ("aws", "abc")]),
        exp_section(CAMPUS, [("ca", "a"), ("mtss", "ab"), ("shpe", "a")]),
        projects([("linkdup", "ab"), ("portfolio", "a"), ("data", "a"), ("sfort", "a")]),
    ],
    "Retail": [
        summary("Bilingual Best Buy Geek Squad Agent with customer-facing experience in tech support, residence life, and event service, seeking a retail sales role."),
        exp_section(PROF, [("bestbuy", ["a", "b3", "c3"]), ("amerivents", "a"), ("eventaces", "ast"), ("aws", "r"), ("adamas", "a")]),
        exp_section(CAMPUS, [("ca", "ab"), ("mtss", "ab"), ("eop", ["a", "e2"]), ("shpe", "b"), ("ra", "a")]),
        skills(["retail", "lang"]),
    ],
}


def build(name):
    tex = PRE + HEADER + "".join(VERSIONS[name]) + "\\end{document}\n"
    stem = f"Israel_Alcantara_Resume_{name}"
    tex = re.sub(r"(\\resumeSubheading\n(?:.*\n){2})(\s*)\\resumeLine", r"\1\2\\resumeFirstLine", tex)
    tex = re.sub(r"(\\resume(?:First)?Line\{.*\}\n)(\s*\\resumeSubheading)", r"\1    \\resumeSchoolGap\n\2", tex)
    (D / f"{stem}.tex").write_text(tex)
    subprocess.run(["pdflatex", "-interaction=nonstopmode", f"{stem}.tex"], cwd=D, capture_output=True)
    pages = subprocess.run(["pdfinfo", f"{stem}.pdf"], cwd=D, capture_output=True, text=True).stdout
    pages = re.search(r"Pages:\s+(\d+)", pages).group(1)
    return stem, pages


if __name__ == "__main__":
    for n in (sys.argv[1:] or VERSIONS):
        print(*build(n))
