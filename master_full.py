import re
import subprocess, re
import build as B

def L(s):
    return s.replace("&", "\\&").replace("%", "\\%").replace("$", "\\$")

def entry(company, loc, title, dates, bullets):
    s = f"    \\resumeSubheading\n      {{{L(company)}}}{{{loc}}}\n      {{{L(title)}}}{{{dates}}}\n      \\resumeItemListStart\n"
    for x in bullets:
        s += f"        \\resumeItem{{{L(x)}}}\n"
    return s + "      \\resumeItemListEnd\n"

def section(title, entries):
    return f"\\section{{{title}}}\n  \\resumeSubHeadingListStart\n" + "".join(entries) + "  \\resumeSubHeadingListEnd\n\n"

def lines(title, rows):
    body = " \\\\\n      ".join(rows)
    return ("\\section{" + title + "}\n\\begin{itemize}[leftmargin=0.15in, label={}]\n    \\small{\\item{\n      "
            + body + "\n    }}\n\\end{itemize}\n\n")

EDU = r"""\section{Education}
  \resumeSubHeadingListStart
    \resumeSubheading
      {Montclair State University}{Montclair, NJ}
      {Master of Business Administration $|$ Feliciano School of Business $|$ GPA: 4.0}{Aug 2026 -- Expected Dec 2028}
      \resumeLine{\textbf{Coursework}: Business Essentials (MGMT 560), Business Statistics (INFO 561), Global Economy (ECON 565), Strategic Information Systems (INFO 565)}
    \resumeSubheading
      {New Jersey Institute of Technology}{Newark, NJ}
      {Bachelor of Science in Computer Science $|$ Ying Wu College of Computing $|$ GPA: 3.4}{Sep 2022 -- May 2026}
      \resumeLine{\textbf{Coursework}: Roadmap to Computing (CS 100), Introduction to Computer Science (CS 113), Introduction to Computer Science II, Data Structures and Algorithms (CS 114), Foundations of Computer Science I, Discrete Math (CS 241), Programming Language Concepts (CS 280), Intensive Programming in Linux (CS 288), Introduction to Data Science (CS 301), Database System Design and Management (CS 331), Principles of Operating Systems (CS 332), Performance Modeling in Computing (CS 337), Foundations of Computer Science II, Discrete Math (CS 341), Intro to Computer Systems (CS 350), Introduction to Cybersecurity (CS 351), Introduction to Computer Networks (CS 356), Intro to Machine Learning (CS 375), Android Application Development (CS 388), Advanced Data Structures and Algorithms (CS 435), Design in Software Engineering (CS 490), Computer Science Project, Senior Capstone (CS 491), Designing the User Experience (IS 247), Information Design Techniques (IT 201), Calculus II (MATH 112), Probability and Statistics (MATH 333)}
      \resumeLine{\textbf{Honors}: Cum Laude (May 2026), Dean's List (Fall 2022, Spring 2024, Spring 2025, Spring 2026)}
      \resumeLine{\textbf{Scholarships}: Orsted Opportunity Scholarship (Sep 2022), Highlander Persistence Scholarship and NJIT Urban Scholarship (Sep 2023), Dr. Theodore and Lois John Scholarship, General Endowed Scholarship, Guastaferro Memorial Endowed Scholarship, and Hispanic and Latinx Leadership Council Opportunity Scholarship (Sep 2024)}
      \resumeLine{\textbf{Activities}: SHPE Event Coordination Director, Fashion Club Treasurer, HACCS, ACM, ALPFA}
  \resumeSubHeadingListEnd

"""

SKILLS = lines("Skills", [
    r"\textbf{Project \& Business}{: Project Management, Project Coordination, Agile/Scrum, Jira, Event Planning, Budgeting, Microsoft Excel, Microsoft Office}",
    r"\textbf{Cloud \& IT}{: AWS (CloudWatch), Technical Support, Troubleshooting, Linux, Git, AV Systems (Crestron)}",
    r"\textbf{Programming}{: Java, Python, SQL, JavaScript, TypeScript, C/C++, Kotlin, Bash}",
    r"\textbf{Frameworks \& Data}{: React, React Native, Node.js, Express, Supabase (Postgres), MySQL, MongoDB, Pandas, Scikit-learn, Streamlit, JUnit, Playwright}",
    r"\textbf{Languages}{: English and Spanish (native or bilingual)}",
])

PROF = section("Professional Experience", [
    entry("Best Buy", "Secaucus, NJ", "Geek Squad Agent", "Nov 2026 -- Present", [
        "Serve as the first point of contact for customers' computer, phone, and device issues, handling check-in and checkout with detailed notes and repair time estimates.",
        "Set up new devices, advise customers on whether to repair or replace, and keep them updated on service-queue status.",
        "Partner with other agents on complex repairs and complete Best Buy's certified training courses."]),
    entry("Amerivents (US Open 2026)", "Flushing, NY", "Suite Runner", "Aug 2026 -- Sep 2026", [
        "Delivered food, drinks, and guest requests to premium suites during the 2026 US Open, keeping turnaround fast in a high-volume setting.",
        "Worked directly with suite guests and kitchen and service staff to fill orders accurately and resolve requests in real time."]),
    entry("Event Aces (FIFA World Cup 2026)", "East Rutherford, NJ", "Beertender & Suite Runner", "Jun 2026 -- Jul 2026", [
        "Started as a beertender, serving high volumes of guests during FIFA World Cup 2026 game days at MetLife Stadium while staying accurate and friendly under pressure.",
        "Moved into a suite runner role once MetLife's own staff covered beertending, restocking bars with regular and alcoholic beverages, ice, and garnishes whenever supplies ran low.",
        "Handled teardown and restocking after each shift, putting every item back in its original spot so drinks stayed cold and the area was left as clean as I found it.",
        "Worked with a large event staff team to keep service lines moving during peak crowds."]),
    entry("Amazon Web Services (AWS)", "Arlington, VA", "Software Development Engineer Intern", "May 2025 -- Aug 2025", [
        "Instrumented Java emitters with 13 custom CloudWatch metrics to measure how much metric data in private, air-gapped regions could be compressed, then used the dashboards to choose the approach.",
        "Designed and shipped a lossless consecutive-duplicate compression algorithm for the Amazon Dedicated Cloud BlackMirror metrics pipeline (Java, XML), cutting export payloads by an average of 38 GB a day and up to 60 GB a day across 3 air-gapped regions while meeting customers' privacy concerns.",
        "Built a matching decompressor that restores every data point exactly, and wrote 30+ JUnit tests for round-trip correctness and edge cases.",
        "Published a cross-region dashboard the wider team used to size the impact, and scoped delta encoding and sum-only compression as follow-on roadmap items.",
        "Took part in the team's daily standups."]),
    entry("Adamas Building Services", "Long Branch, NJ", "Beach Attendant & Lifeguard", "Jul 2023 -- Sep 2023", [
        "Monitored three condominium pools, enforced safety rules, ran chemical checks three times a day, and gave CPR and first aid when needed, watching over about 80 swimmers per shift and closing the season with zero accidents.",
        "Coordinated the daily setup and teardown of 150+ chairs, umbrellas, and water-sport items, and worked with facilities to keep a 95% cleanliness rating and raise guest-satisfaction feedback by 45%."]),
])

CAMPUS = section("Leadership \\& Campus Experience", [
    entry("New Jersey Institute of Technology", "Newark, NJ", "Community Assistant, Office of Residential Life", "Jun 2025 -- May 2026", [
        "Supervised a 400-resident Greek Village complex, ran regular rounds, enforced housing policy, and resolved roommate and conduct issues, with zero major violations during my term.",
        "Planned and ran all 8 to 12 community events for my building each semester, about 2 to 3 a month, from wellness workshops to study groups, on a $150 semester budget.",
        "Served as primary responder to a late-night guest-policy incident across two buildings, working with a graduate CA, a peer CA, and the on-duty Residence Coordinator to de-escalate it and enforce a building-wide no-entry directive."]),
    entry("Media and Technology Support Services (MTSS), NJIT", "Newark, NJ", "Delivery Technician & Lab Technician", "Sep 2022 -- May 2026", [
        "Worked with a team of five technicians to standardize equipment setup and pre-lecture readiness checks across 100+ lectures a year, improving estimated equipment reliability by 40%, based on daily, weekly, and monthly service-call logs.",
        "Diagnosed and fixed AV problems in classrooms and labs, including projectors, Crestron control systems, switchers, and wireless microphones.",
        "Cut the repeat-call rate on the same equipment by an estimated 30% through systematic troubleshooting."]),
    entry("New Jersey Institute of Technology", "Newark, NJ", "Office Assistant, Educational Opportunity Program (EOP)", "Sep 2024 -- Aug 2025", [
        "Ran the front desk, scheduled 15+ appointments a week through a scheduling website, and kept records accurate and confidential.",
        "Prepared documents, handled data entry, and kept the office organized with Microsoft Office, making office work at least 30% more efficient."]),
    entry("Society of Hispanic Professional Engineers (SHPE), NJIT Chapter", "Newark, NJ", "Event Coordination Director", "Mar 2024 -- May 2025", [
        "Planned and ran 12+ networking and professional development events, leading a team of about 10 student volunteers and tracking who handled each task.",
        "Grew opening-event attendance from about 60 to 70 people up to 150, and average event attendance from 30 to 50 up to 50 to 80.",
        "Pitched larger events to the e-board well ahead of time for feedback and final approval, then chose rooms and built floor plans, time-blocked agendas, and event budgets.",
        "Sent agendas and presentation materials to company guests and arranged their parking, working alongside the External VP who handled outreach to companies.",
        "Ran each event live and kept it on schedule, with backup plans ready for anything that went wrong."]),
    entry("New Jersey Institute of Technology", "Newark, NJ", "Resident Assistant, EOP Summer Program", "Jun 2024 -- Aug 2024", [
        "Supported 150 first-year students through the 10-week EOP summer program, helping them adjust to university and residence hall life.",
        "Planned program events with the RA team, including EOP alumni panels and a multicultural night.",
        "Ran elections for a floor rep on each of the program's 3 floors so residents could raise concerns and suggest additions to the program, and mediated resident conflicts, reporting them to the right administrative staff."]),
])

def proj(head, dates, bullets):
    s = f"      \\resumeProjectHeading\n          {{{head}}}{{{dates}}}\n          \\resumeItemListStart\n"
    for x in bullets:
        s += f"            \\resumeItem{{{L(x)}}}\n"
    return s + "          \\resumeItemListEnd\n"

PROJECTS = "\\section{Projects}\n    \\resumeSubHeadingListStart\n" + "".join([
    proj(r"\textbf{LinkdUp} $|$ \emph{React Native, Node.js, Express, TypeScript, Supabase} $|$ \href{https://linkdup.app}{\underline{linkdup.app}}", "Jan 2026 -- May 2026", [
        "Worked as the backend engineer on a five-person team building a group planning app where friends swipe on nearby places, vote, and lock in a time together.",
        "Placed 2nd among the NJIT CS/IT 491 Capstone 2026 teams.",
        "Integrated the Google Places and Google Calendar APIs for venue discovery and one-click event export.",
        "Built with React Native, Node/Express, TypeScript, Supabase, and the Google Maps and Calendar APIs, and live at linkdup.app."]),
    proj(r"\textbf{Personal Portfolio Website} $|$ \emph{React 19, Vite, GSAP, Vercel, Playwright}", "May 2026 -- Oct 2026", [
        "Designed and built my personal portfolio from scratch to show recruiters my work and who I am.",
        "Planned the site in phases, starting with an editorial design system (DM Serif Display headlines, purple and gold accents, and a consistent type scale) before writing any code.",
        "Built it with React 19, Vite, and GSAP, and deployed it on Vercel with serverless functions.",
        "Added a photo gallery that loads new photos automatically and strips location data from every image.",
        "Built a dark mode that follows the visitor's system setting, with a toggle that remembers their choice.",
        "Improved accessibility with contrast fixes, 44 by 44 pixel tap targets, alt text on every image, and a page lock behind the lightbox and mobile menu so keyboard and screen reader users don't get lost.",
        "Wrote 34 Playwright tests that run in Chromium, Firefox, and WebKit in both light and dark mode.",
        "Raised Lighthouse performance scores from 63 to 99 on mobile and from 74 to 100 on desktop.",
        "Live at israelalcantara.vercel.app."]),
    proj(r"\textbf{Data Analysis and Prediction App} $|$ \emph{Python, Streamlit, Scikit-learn}", "Nov 2024 -- Dec 2024", [
        "Built an interactive web app with two classmates where users upload CSV data, explore it in dynamic charts, and train a Gradient Boosting Regressor model.",
        "Built automated data preprocessing that handles missing values, scales numerical data, and encodes categories, so users can pick features and check model predictions in real time."]),
    proj(r"\textbf{Compiler for SFort95 Language} $|$ \emph{C++, Git}", "Mar 2024 -- Apr 2024", [
        "Built a full compiler for the SFort95 language with lexical analysis, parsing, and interpretation, supporting declarations, expressions, and control structures based on Fortran 95.",
        "Built a state-based lexical analyzer that detects tokens like identifiers and operators, reports how often each token appears, and flags unrecognized lexemes with error messages.",
        "Wrote a recursive-descent parser with operator precedence and syntax checks that gives clear errors for problems like missing delimiters or undefined variables.",
        "Designed an interpreter with a symbol table and runtime checks for expression accuracy, control flow, and errors like division by zero."]),
]) + "    \\resumeSubHeadingListEnd\n\n"

ORGS = lines("Organizations", [
    r"\textbf{ColorStack}, Fellow \hfill Apr 2025 -- Present",
    r"\textbf{Association of Latino Professionals For America (ALPFA)}, Member \hfill Sep 2025 -- Present",
    r"\textbf{Hispanic Association of College Computing Students (HACCS)}, Member \hfill Mar 2023 -- Present",
    r"\textbf{Association for Computing Machinery (ACM)}, Member \hfill Sep 2022 -- Present",
    r"\textbf{Society of Hispanic Professional Engineers (SHPE)}, Member \hfill Sep 2022 -- Present",
])

VOL = section("Volunteering", [
    entry("Mentor U Connect", "Newark, NJ", "STEM Mentorship Program Volunteer", "Mar 2024 -- Present", [
        "Support event logistics and help run interactive STEM workshops, handling on-the-spot needs so each session runs smoothly.",
        "Work directly with students to build their interest in STEM and help underrepresented youth see a path to higher education."]),
    entry("Queen of Peace Church", "North Arlington, NJ", "Coordination of Volunteers", "Dec 2021 -- Apr 2022", [
        "Managed inventory and organized food donations, keeping shelves stocked and making sure food items were within their expiration dates for community members in need.",
        "Coordinated volunteer schedules and tasks, and helped hand out food to individuals and families during pantry hours."]),
])

def main():
    tex = B.PRE + B.HEADER + EDU + SKILLS + PROF + CAMPUS + PROJECTS + ORGS + VOL + "\\end{document}\n"
    stem = "Israel_Alcantara_Resume_Master"
    tex = re.sub(r"(\\resumeSubheading\n(?:.*\n){2})(\s*)\\resumeLine", r"\1\2\\resumeFirstLine", tex)
    tex = re.sub(r"(\\resume(?:First)?Line\{.*\}\n)(\s*\\resumeSubheading)", r"\1    \\resumeSchoolGap\n\2", tex)
    (B.D / f"{stem}.tex").write_text(tex)
    subprocess.run(["pdflatex", "-interaction=nonstopmode", f"{stem}.tex"], cwd=B.D, capture_output=True)
    info = subprocess.run(["pdfinfo", f"{stem}.pdf"], cwd=B.D, capture_output=True, text=True).stdout
    print(stem, re.search(r"Pages:\s+(\d+)", info).group(1))

if __name__ == "__main__":
    main()
