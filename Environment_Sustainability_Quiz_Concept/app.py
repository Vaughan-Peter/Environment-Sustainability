"""
Environment & Sustainability Quiz
Python 3.10+ recommended. Tkinter is included with standard Python on Windows.
PDF reports require reportlab: py -m pip install reportlab
"""
import json
import random
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
BANK_FILE = APP_DIR / "question_bank.json"
WINDOW_SIZE = "600x500"
BG = "#f2f7f2"
GREEN = "#246b45"
DARK = "#183c2b"
WHITE = "#ffffff"

def load_questions():
    try:
        with BANK_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list) or not data:
            raise ValueError("Question bank is empty.")
        return data
    except Exception as exc:
        messagebox.showerror("Question bank error", f"Could not load question_bank.json:\n{exc}")
        return []

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Environment & Sustainability Quiz")
        self.root.geometry(WINDOW_SIZE)
        self.root.minsize(600, 500)
        self.root.configure(bg=BG)
        self.questions = load_questions()
        self.student = {}
        self.test_questions = []
        self.responses = []
        self.current = 0
        self.topic = "Both"
        self.grade = 7
        self.length = "Small"
        self._style()
        self.show_home()

    def _style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("TFrame", background=BG)
        style.configure("TLabel", background=BG, foreground=DARK, font=("Segoe UI", 10))
        style.configure("Title.TLabel", font=("Segoe UI", 19, "bold"), foreground=GREEN)
        style.configure("Sub.TLabel", font=("Segoe UI", 11), foreground=DARK)
        style.configure("TButton", font=("Segoe UI", 10), padding=7)
        style.configure("Green.TButton", font=("Segoe UI", 10, "bold"), padding=8)
        style.map("Green.TButton", background=[("active", "#2f855a")])

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def header(self, title, subtitle=None):
        frame = ttk.Frame(self.root, padding=(20, 14, 20, 6))
        frame.pack(fill="x")
        ttk.Label(frame, text=title, style="Title.TLabel").pack(anchor="w")
        if subtitle:
            ttk.Label(frame, text=subtitle, style="Sub.TLabel", wraplength=550).pack(anchor="w", pady=(4, 0))

    def show_home(self):
        self.clear()
        self.header("EcoLearn Quiz", "Environment • Sustainability • Grades 7–12")
        body = ttk.Frame(self.root, padding=25)
        body.pack(fill="both", expand=True)
        ttk.Label(body, text="Learn today. Protect tomorrow.", font=("Segoe UI", 13, "italic")).pack(pady=(18, 25))
        ttk.Button(body, text="Start a Test", style="Green.TButton", command=self.show_setup).pack(fill="x", pady=7)
        ttk.Button(body, text="About", command=self.show_about).pack(fill="x", pady=7)
        ttk.Button(body, text="Exit", command=self.root.destroy).pack(fill="x", pady=7)
        ttk.Label(self.root, text=f"{len(self.questions)} questions in the question bank", foreground="#52705d").pack(pady=(0, 12))

    def show_about(self):
        self.clear()
        self.header("About EcoLearn Quiz")
        body = ttk.Frame(self.root, padding=24)
        body.pack(fill="both", expand=True)
        about = ("This educational quiz covers environmental science and sustainability "
                 "for students in Grades 7–12. Questions include multiple-choice and "
                 "true/false formats.\n\n"
                 "We are non-profit organization. If there are any errors on the tests, "
                 "please contact otherhalifaxprojects.com")
        ttk.Label(body, text=about, wraplength=520, justify="left").pack(anchor="w", pady=10)
        ttk.Button(body, text="Back to Main Menu", command=self.show_home).pack(anchor="w", pady=20)

    def show_setup(self):
        self.clear()
        self.header("Student & Test Setup", "Complete the details, then choose a test.")
        outer = ttk.Frame(self.root, padding=(20, 5, 20, 12))
        outer.pack(fill="both", expand=True)
        form = ttk.Frame(outer)
        form.pack(fill="x")
        self.first_var = tk.StringVar()
        self.last_var = tk.StringVar()
        self.id_var = tk.StringVar()
        self.teacher_var = tk.StringVar()
        self.grade_var = tk.StringVar(value="7")
        self.length_var = tk.StringVar(value="Small")
        self.topic_var = tk.StringVar(value="Both")
        fields = [
            ("First name", self.first_var),
            ("Last name", self.last_var),
            ("ID number (optional)", self.id_var),
            ("Teacher's name (optional)", self.teacher_var),
        ]
        for row, (label, var) in enumerate(fields):
            ttk.Label(form, text=label).grid(row=row, column=0, sticky="w", pady=3, padx=(0, 10))
            ttk.Entry(form, textvariable=var, width=34).grid(row=row, column=1, sticky="ew", pady=3)
        form.columnconfigure(1, weight=1)
        options = ttk.Frame(outer)
        options.pack(fill="x", pady=(12, 3))
        ttk.Label(options, text="Grade").grid(row=0, column=0, sticky="w", padx=(0, 8), pady=4)
        ttk.Combobox(options, textvariable=self.grade_var, values=[str(x) for x in range(7,13)], state="readonly", width=8).grid(row=0, column=1, sticky="w", pady=4)
        ttk.Label(options, text="Test length").grid(row=1, column=0, sticky="w", padx=(0, 8), pady=4)
        ttk.Combobox(options, textvariable=self.length_var, values=["Small", "Medium", "Long"], state="readonly", width=12).grid(row=1, column=1, sticky="w", pady=4)
        ttk.Label(options, text="Topic").grid(row=2, column=0, sticky="w", padx=(0, 8), pady=4)
        ttk.Combobox(options, textvariable=self.topic_var, values=["Environment", "Sustainability", "Both"], state="readonly", width=16).grid(row=2, column=1, sticky="w", pady=4)
        ttk.Label(outer, text="Small: 10 questions   •   Medium: 25   •   Long: 50", foreground="#52705d").pack(anchor="w", pady=(7, 10))
        buttons = ttk.Frame(outer)
        buttons.pack(fill="x", side="bottom")
        ttk.Button(buttons, text="Back", command=self.show_home).pack(side="left")
        ttk.Button(buttons, text="Begin Test", style="Green.TButton", command=self.begin_test).pack(side="right")

    def begin_test(self):
        first = self.first_var.get().strip()
        last = self.last_var.get().strip()
        if not first or not last:
            messagebox.showwarning("Missing details", "Please enter the student's first and last name.")
            return
        self.student = {
            "first_name": first,
            "last_name": last,
            "id_number": self.id_var.get().strip(),
            "teacher": self.teacher_var.get().strip(),
            "grade": int(self.grade_var.get()),
        }
        self.topic = self.topic_var.get()
        self.length = self.length_var.get()
        count = {"Small": 10, "Medium": 25, "Long": 50}[self.length]
        eligible = [q for q in self.questions
                    if q.get("grade_min", 7) <= self.student["grade"] <= q.get("grade_max", 12)
                    and (self.topic == "Both" or q.get("topic_group") == self.topic)]
        if len(eligible) < count:
            messagebox.showerror("Not enough questions", f"Only {len(eligible)} questions match these choices.")
            return
        self.test_questions = random.sample(eligible, count)
        self.responses = [None] * count
        self.current = 0
        self.show_question()

    def show_question(self):
        self.clear()
        total = len(self.test_questions)
        q = self.test_questions[self.current]
        self.header(f"Question {self.current + 1} of {total}", f"Grade {self.student['grade']} • {self.topic} • {self.length} test")
        outer = ttk.Frame(self.root, padding=(20, 10, 20, 12))
        outer.pack(fill="both", expand=True)
        progress = ttk.Progressbar(outer, maximum=total, value=self.current + 1, mode="determinate")
        progress.pack(fill="x", pady=(0, 14))
        ttk.Label(outer, text=q["question"], font=("Segoe UI", 12, "bold"), wraplength=540, justify="left").pack(anchor="w", pady=(0, 16))
        self.answer_var = tk.IntVar(value=-1 if self.responses[self.current] is None else self.responses[self.current])
        opts = q.get("options", ["True", "False"])
        for i, option in enumerate(opts):
            ttk.Radiobutton(outer, text=option, variable=self.answer_var, value=i).pack(anchor="w", pady=5)
        nav = ttk.Frame(outer)
        nav.pack(fill="x", side="bottom", pady=(15, 0))
        ttk.Button(nav, text="Quit Test", command=self.confirm_quit).pack(side="left")
        if self.current > 0:
            ttk.Button(nav, text="Previous", command=self.previous_question).pack(side="left", padx=6)
        if self.current < total - 1:
            ttk.Button(nav, text="Next", style="Green.TButton", command=self.next_question).pack(side="right")
        else:
            ttk.Button(nav, text="Finish Test", style="Green.TButton", command=self.finish_test).pack(side="right")

    def save_current_answer(self):
        value = self.answer_var.get()
        self.responses[self.current] = None if value < 0 else value

    def next_question(self):
        self.save_current_answer()
        self.current += 1
        self.show_question()

    def previous_question(self):
        self.save_current_answer()
        self.current -= 1
        self.show_question()

    def confirm_quit(self):
        if messagebox.askyesno("Quit test?", "Your current test will not be scored. Quit now?"):
            self.show_home()

    def finish_test(self):
        self.save_current_answer()
        unanswered = sum(x is None for x in self.responses)
        if unanswered and not messagebox.askyesno("Unanswered questions", f"You have {unanswered} unanswered question(s). Finish anyway?"):
            return
        self.show_results()

    def score_data(self):
        correct = 0
        rows = []
        category_totals = {}
        for q, response in zip(self.test_questions, self.responses):
            is_correct = response == q["answer"]
            if is_correct:
                correct += 1
            cat = q.get("category", "General")
            if cat not in category_totals:
                category_totals[cat] = [0, 0]
            category_totals[cat][1] += 1
            if is_correct:
                category_totals[cat][0] += 1
            options = q.get("options", ["True", "False"])
            chosen = "Not answered" if response is None else options[response]
            right = options[q["answer"]]
            rows.append({
                "question": q["question"], "chosen": chosen, "correct_answer": right,
                "is_correct": is_correct, "explanation": q.get("explanation", ""),
                "category": cat
            })
        return correct, rows, category_totals

    def show_results(self):
        self.clear()
        correct, rows, category_totals = self.score_data()
        total = len(rows)
        pct = round(correct / total * 100)
        self.header("Test Results", f"{self.student['first_name']} {self.student['last_name']} • Grade {self.student['grade']}")
        outer = ttk.Frame(self.root, padding=(20, 10, 20, 14))
        outer.pack(fill="both", expand=True)
        ttk.Label(outer, text=f"{correct} / {total} correct", font=("Segoe UI", 22, "bold"), foreground=GREEN).pack(pady=(8, 0))
        ttk.Label(outer, text=f"Score: {pct}%", font=("Segoe UI", 15)).pack(pady=3)
        ttk.Label(outer, text=f"Test: {self.length} • Topic: {self.topic} • Date: {datetime.now():%Y-%m-%d %H:%M}", wraplength=520).pack(pady=5)
        ttk.Label(outer, text="Topic breakdown", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(12, 3))
        for cat, (got, maxv) in sorted(category_totals.items()):
            ttk.Label(outer, text=f"{cat}: {got}/{maxv} ({round(got/maxv*100)}%)").pack(anchor="w")
        ttk.Label(outer, text="You can save a detailed PDF report with answers and explanations.", wraplength=520).pack(anchor="w", pady=(12, 8))
        buttons = ttk.Frame(outer)
        buttons.pack(fill="x", side="bottom")
        ttk.Button(buttons, text="Main Menu", command=self.show_home).pack(side="left")
        ttk.Button(buttons, text="Save Results as PDF", style="Green.TButton", command=lambda: self.export_pdf(correct, rows, category_totals)).pack(side="right")

    def export_pdf(self, correct, rows, category_totals):
        try:
            from reportlab.lib import colors
            from reportlab.lib.enums import TA_CENTER, TA_LEFT
            from reportlab.lib.pagesizes import letter
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
        except ImportError:
            messagebox.showerror("PDF library missing", "Install the PDF library with:\npy -m pip install reportlab")
            return
        default_name = f"Quiz_Results_{self.student['last_name']}_{datetime.now():%Y%m%d}.pdf"
        path = filedialog.asksaveasfilename(defaultextension=".pdf", initialfile=default_name, filetypes=[("PDF files", "*.pdf")])
        if not path:
            return
        total = len(rows)
        pct = round(correct / total * 100)
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name="ReportTitle", parent=styles["Title"], textColor=colors.HexColor("#246b45"), alignment=TA_CENTER, fontSize=20, leading=24, spaceAfter=8))
        styles.add(ParagraphStyle(name="SmallText", parent=styles["BodyText"], fontSize=8, leading=10))
        styles.add(ParagraphStyle(name="QuestionText", parent=styles["BodyText"], fontSize=9, leading=12, spaceAfter=3))
        story = []
        story.append(Paragraph("Environment &amp; Sustainability Quiz", styles["ReportTitle"]))
        story.append(Paragraph("Student Assessment Report", styles["Heading2"]))
        story.append(Spacer(1, 8))
        details = [
            ["Student", f"{self.student['first_name']} {self.student['last_name']}", "Grade", str(self.student["grade"])],
            ["ID number", self.student["id_number"] or "Not provided", "Teacher", self.student["teacher"] or "Not provided"],
            ["Topic", self.topic, "Test length", f"{self.length} ({total} questions)"],
            ["Date", datetime.now().strftime("%B %d, %Y %H:%M"), "Score", f"{correct}/{total} ({pct}%)"],
        ]
        tbl = Table(details, colWidths=[0.9*inch, 2.25*inch, 0.85*inch, 2.0*inch])
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (0,-1), colors.HexColor("#e5f0e8")),
            ("BACKGROUND", (2,0), (2,-1), colors.HexColor("#e5f0e8")),
            ("TEXTCOLOR", (0,0), (-1,-1), colors.HexColor("#183c2b")),
            ("GRID", (0,0), (-1,-1), 0.4, colors.HexColor("#b8cdbd")),
            ("FONTNAME", (0,0), (-1,-1), "Helvetica"),
            ("FONTSIZE", (0,0), (-1,-1), 8),
            ("VALIGN", (0,0), (-1,-1), "TOP"),
            ("LEFTPADDING", (0,0), (-1,-1), 6), ("RIGHTPADDING", (0,0), (-1,-1), 6),
            ("TOPPADDING", (0,0), (-1,-1), 6), ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ]))
        story.append(tbl)
        story.append(Spacer(1, 14))
        story.append(Paragraph("Topic Breakdown", styles["Heading2"]))
        breakdown = [["Topic", "Correct", "Total", "Percentage"]]
        for cat, (got, maxv) in sorted(category_totals.items()):
            breakdown.append([cat, str(got), str(maxv), f"{round(got/maxv*100)}%"])
        bt = Table(breakdown, colWidths=[3.3*inch, 0.8*inch, 0.8*inch, 1.1*inch], repeatRows=1)
        bt.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#246b45")),
            ("TEXTCOLOR", (0,0), (-1,0), colors.white),
            ("GRID", (0,0), (-1,-1), 0.35, colors.HexColor("#b8cdbd")),
            ("FONTSIZE", (0,0), (-1,-1), 8), ("VALIGN", (0,0), (-1,-1), "TOP"),
            ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#f2f7f2")]),
        ]))
        story.append(bt)
        story.append(Spacer(1, 12))
        story.append(Paragraph("Question Review", styles["Heading2"]))
        for i, row in enumerate(rows, 1):
            status = "CORRECT" if row["is_correct"] else "INCORRECT"
            color = "#246b45" if row["is_correct"] else "#a33b32"
            block = [
                Paragraph(f"<b>Question {i} — <font color='{color}'>{status}</font></b> | {row['category']}", styles["QuestionText"]),
                Paragraph(row["question"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"), styles["SmallText"]),
                Paragraph(f"<b>Your answer:</b> {row['chosen'].replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')}", styles["SmallText"]),
                Paragraph(f"<b>Correct answer:</b> {row['correct_answer'].replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')}", styles["SmallText"]),
                Paragraph(f"<b>Explanation:</b> {row['explanation'].replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')}", styles["SmallText"]),
                Spacer(1, 7),
            ]
            story.append(KeepTogether(block))
        story.append(Spacer(1, 10))
        story.append(Paragraph("We are non-profit organization. If there are any errors on the tests, please contact otherhalifaxprojects.com", styles["SmallText"]))
        def footer(canvas, doc):
            canvas.saveState()
            canvas.setStrokeColor(colors.HexColor("#b8cdbd"))
            canvas.line(0.6*inch, 0.55*inch, 7.9*inch, 0.55*inch)
            canvas.setFont("Helvetica", 8)
            canvas.setFillColor(colors.HexColor("#52705d"))
            canvas.drawString(0.65*inch, 0.35*inch, "Environment & Sustainability Quiz")
            canvas.drawRightString(7.85*inch, 0.35*inch, f"Page {doc.page}")
            canvas.restoreState()
        try:
            doc = SimpleDocTemplate(path, pagesize=letter, rightMargin=0.6*inch, leftMargin=0.6*inch, topMargin=0.6*inch, bottomMargin=0.75*inch, title="Environment & Sustainability Quiz Results")
            doc.build(story, onFirstPage=footer, onLaterPages=footer)
            messagebox.showinfo("PDF saved", f"Results report saved to:\n{path}")
        except Exception as exc:
            messagebox.showerror("PDF error", f"Could not create PDF:\n{exc}")

def main():
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
