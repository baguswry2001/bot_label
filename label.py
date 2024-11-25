from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors

def generate_labels_from_input(filename, label_width=200, label_height=100):
    page_width, page_height = letter
    c = canvas.Canvas(filename, pagesize=letter)

    # Margin awal dan jarak antar-label
    x_margin, y_margin = 50, 50
    x_spacing, y_spacing = 20, 20

    # Posisi awal
    x_pos = x_margin
    y_pos = page_height - y_margin - label_height

    print("Masukkan data barang. Ketik 'selesai' untuk berhenti.")
    while True:
        nama_barang = input("Masukkan nama barang: ")
        if nama_barang.lower() == "selesai":
            break
        try:
            harga = int(input("Masukkan harga barang (angka): "))
        except ValueError:
            print("Harga harus berupa angka. Silakan coba lagi.")
            continue

        # Gambar kotak label
        c.setStrokeColor(colors.black)
        c.setLineWidth(1.5)
        c.rect(x_pos, y_pos, label_width, label_height, stroke=1, fill=0)

        # Teks bagian atas (nama toko/brand)
        c.setFillColor(colors.black)  # Atur warna teks ke hitam
        c.setFont("Helvetica", 10)
        c.drawCentredString(x_pos + label_width / 2, y_pos + label_height - 20, "7saudara 7saudara 7saudara")

        # Harga
        c.setFont("Helvetica-Bold", 24)
        c.drawCentredString(x_pos + label_width / 2, y_pos + label_height - 50, f"Rp {harga:,.0f}".replace(",", "."))

        # Nama barang dengan pembungkusan dan jarak ekstra
        font_size = 12
        max_width = label_width - 20  # Margin untuk teks
        max_lines = 2  # Maksimal 2 baris untuk nama barang
        line_spacing = 14  # Jarak antar baris
        wrapped_text, final_font_size = wrap_and_scale_text(c, nama_barang, "Helvetica", font_size, max_width, max_lines)
        draw_wrapped_text(c, wrapped_text, x_pos + label_width / 2, y_pos + 25, final_font_size, line_spacing)

        # Garis kuning
        c.setFillColor(colors.yellow)
        c.rect(x_pos, y_pos + 10, label_width, 10, fill=1, stroke=0)

        # Garis merah
        c.setFillColor(colors.red)
        c.rect(x_pos, y_pos, label_width, 10, fill=1, stroke=0)

        # Pindah ke label berikutnya
        x_pos += label_width + x_spacing
        if x_pos + label_width + x_margin > page_width:
            x_pos = x_margin
            y_pos -= label_height + y_spacing

            if y_pos < y_margin:
                c.showPage()
                x_pos = x_margin
                y_pos = page_height - y_margin - label_height

    c.save()
    print(f"Label harga berhasil disimpan ke file {filename}")

# Fungsi untuk membungkus teks dan menyesuaikan ukuran font
def wrap_and_scale_text(c, text, font_name, initial_font_size, max_width, max_lines):
    font_size = initial_font_size
    wrapped_lines = wrap_text(c, text, font_name, font_size, max_width)

    while len(wrapped_lines) > max_lines and font_size > 6:
        font_size -= 1
        wrapped_lines = wrap_text(c, text, font_name, font_size, max_width)

    return wrapped_lines, font_size

# Fungsi untuk membungkus teks
def wrap_text(c, text, font_name, font_size, max_width):
    c.setFont(font_name, font_size)
    words = text.split()
    wrapped_lines = []
    current_line = ""

    for word in words:
        test_line = f"{current_line} {word}".strip()
        if c.stringWidth(test_line) <= max_width:
            current_line = test_line
        else:
            wrapped_lines.append(current_line)
            current_line = word

    if current_line:
        wrapped_lines.append(current_line)

    return wrapped_lines

# Fungsi untuk menggambar teks
def draw_wrapped_text(c, wrapped_lines, center_x, start_y, font_size, line_spacing):
    c.setFillColor(colors.black)  # Pastikan warna teks hitam
    for i, line in enumerate(wrapped_lines):
        y = start_y - (i * line_spacing)
        c.setFont("Helvetica", font_size)
        c.drawCentredString(center_x, y, line)

# Panggil fungsi untuk membuat label
generate_labels_from_input("label_harga.pdf")
