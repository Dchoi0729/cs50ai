from PIL import Image, ImageDraw, ImageFont
cell_size = 100
cell_border = 2
gap = 5
interior_size = cell_size - 2 * cell_border

# Create a blank canvas
img = Image.new(
    "RGBA",
    (9 * cell_size + 2 * gap, 9 * cell_size + 2 * gap),
    "black"
)
font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
draw = ImageDraw.Draw(img)

for i in range(9):
    for j in range(9):
        
        # Set offset to create borders seperating 3 by 3 squares
        x_offset = 0 if i < 3 else 2 if i > 5 else 1
        y_offset = 0 if j < 3 else 2 if j > 5 else 1

        rect = [
            (j * cell_size + cell_border + y_offset * gap,
                i * cell_size + cell_border + x_offset * gap),
            ((j + 1) * cell_size - cell_border + y_offset * gap,
                (i + 1) * cell_size - cell_border + x_offset * gap)
        ]
        
        # Draw rectangular cell for the number
        draw.rectangle(rect, fill="white")

        # Store size of number in w, h
        no, need, w, h = draw.textbbox((0,0), "9", font=font)

        # Draw number centered in cell
        draw.text(
            (rect[0][0] + ((interior_size - w) / 2),
                rect[0][1] + ((interior_size - h) / 2) - 10),
            "2", fill="black", font=font
        )

img.save("test.png")