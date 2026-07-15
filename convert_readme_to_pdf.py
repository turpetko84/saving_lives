from fpdf import FPDF
import re


def clean_md(text):
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    text = re.sub(r"`(.+?)`", r"\1", text)
    return text


def main():
    with open("README.md", "r", encoding="utf-8") as f:
        md = f.read()

    pdf = FPDF()
    pdf.add_font("Arial", "", "C:/Windows/Fonts/arial.ttf")
    pdf.add_font("Arial", "B", "C:/Windows/Fonts/arialbd.ttf")
    pdf.add_font("Arial", "I", "C:/Windows/Fonts/ariali.ttf")
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    lines = md.split("\n")
    i = 0
    in_table = False
    table_rows = []

    while i < len(lines):
        line = lines[i].rstrip()

        if not line:
            if in_table and table_rows:
                render_table(pdf, table_rows)
                table_rows = []
                in_table = False
            pdf.ln(4)
            i += 1
            continue

        # Table
        if "|" in line and line.strip().startswith("|"):
            in_table = True
            if re.match(r"^\|[\s\-:|]+\|$", line.strip()):
                i += 1
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            table_rows.append(cells)
            i += 1
            continue

        if in_table and table_rows:
            render_table(pdf, table_rows)
            table_rows = []
            in_table = False

        # Code block
        if line.startswith("```"):
            i += 1
            pdf.set_font("Arial", "", 9)
            pdf.set_fill_color(240, 240, 240)
            while i < len(lines) and not lines[i].strip().startswith("```"):
                pdf.cell(0, 5, "  " + lines[i], fill=True)
                pdf.ln()
                i += 1
            i += 1
            pdf.ln(4)
            continue

        # Headings
        if line.startswith("# "):
            pdf.set_font("Arial", "B", 22)
            pdf.cell(0, 14, clean_md(line[2:]))
            pdf.ln(18)
            i += 1
            continue
        if line.startswith("## "):
            pdf.set_font("Arial", "B", 16)
            pdf.cell(0, 10, clean_md(line[3:]))
            pdf.ln(14)
            i += 1
            continue
        if line.startswith("### "):
            pdf.set_font("Arial", "B", 13)
            pdf.cell(0, 8, clean_md(line[4:]))
            pdf.ln(11)
            i += 1
            continue

        # Bullet
        if line.strip().startswith("- "):
            text = clean_md(line.strip()[2:])
            pdf.set_font("Arial", "", 11)
            pdf.cell(0, 7, "  " + chr(8226) + "  " + text)
            pdf.ln()
            i += 1
            continue

        # Normal
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 7, clean_md(line))
        i += 1

    if in_table and table_rows:
        render_table(pdf, table_rows)

    pdf.output("README.pdf")
    print("README.pdf created")


def render_table(pdf, rows):
    if not rows:
        return
    num_cols = max(len(r) for r in rows)
    col_width = (pdf.w - 20) / num_cols

    for idx, row in enumerate(rows):
        if idx == 0:
            pdf.set_font("Arial", "B", 10)
            pdf.set_fill_color(62, 39, 35)
            pdf.set_text_color(255, 248, 225)
        else:
            pdf.set_font("Arial", "", 10)
            pdf.set_text_color(62, 39, 35)
            pdf.set_fill_color(255, 248, 225) if idx % 2 == 0 else pdf.set_fill_color(255, 255, 255)

        for j in range(num_cols):
            cell_text = row[j] if j < len(row) else ""
            pdf.cell(col_width, 8, clean_md(cell_text), border=1, fill=True, align="C")
        pdf.ln()

    pdf.set_text_color(62, 39, 35)
    pdf.ln(4)


if __name__ == "__main__":
    main()
