import os
import requests
import img2pdf

# GitHub Actions থেকে ইনপুট নেওয়া
url_template = os.environ.get("URL_TEMPLATE")
start = int(os.environ.get("START_PAGE"))
end = int(os.environ.get("END_PAGE"))
pdf_name = os.environ.get("PDF_NAME", "Output")

if not pdf_name.endswith('.pdf'):
    pdf_name += '.pdf'

os.makedirs("temp_images", exist_ok=True)
images = []

print(f"🚀 ডাউনলোড শুরু হচ্ছে: {start} থেকে {end} পর্যন্ত...")

for i in range(start, end + 1):
    url = url_template.replace("Yuki", str(i))
    filepath = f"temp_images/{i}.jpg"
    
    try:
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            with open(filepath, 'wb') as f:
                f.write(r.content)
            images.append(filepath)
            print(f"✅ Downloaded: {i}")
        else:
            print(f"⚠️ Not found: {i}")
    except Exception as e:
        print(f"❌ Error on {i}: {e}")

if images:
    print("⏳ PDF তৈরি হচ্ছে, অপেক্ষা করুন...")
    with open(pdf_name, "wb") as f:
        f.write(img2pdf.convert(images))
    print(f"🎉 কাজ শেষ! ফাইল সেভ হয়েছে: {pdf_name}")
else:
    print("❌ কোনো ছবি ডাউনলোড করা যায়নি!")
