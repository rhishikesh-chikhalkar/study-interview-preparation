from pathlib import Path

from PIL import Image

# Folder where this script is located
input_folder = Path(__file__).parent

# Create output folder inside the same folder
output_folder = input_folder / "jpg_converted"
output_folder.mkdir(exist_ok=True)

for webp_file in input_folder.glob("*.webp"):
    jpg_file = output_folder / f"{webp_file.stem}.jpg"

    try:
        with Image.open(webp_file) as img:
            # JPG does not support transparency
            if img.mode in ("RGBA", "LA"):
                background = Image.new("RGB", img.size, "white")
                background.paste(img, mask=img.getchannel("A"))
                img = background
            else:
                img = img.convert("RGB")

            img.save(jpg_file, "JPEG", quality=95)

        print(f"✓ {webp_file.name} → jpg_converted/{jpg_file.name}")

    except Exception as e:
        print(f"✗ Failed: {webp_file.name} — {e}")

print("\nConversion completed!")
input("Press Enter to exit...")
