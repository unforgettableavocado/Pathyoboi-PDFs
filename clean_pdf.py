import fitz # PyMuPDF
import os

def remove_watermark_and_save_pdf(input_pdf, output_pdf, password):
    print(f"Opening: {input_pdf}")
    doc = fitz.open(input_pdf)
    
    # পাসওয়ার্ড দিয়ে আনলক করা
    if doc.is_encrypted:
        doc.authenticate(password)
    
    # নতুন পিডিএফ ডকুমেন্ট তৈরি
    out_doc = fitz.open()
    
    for page in doc:
        img_list = page.get_images(full=True)
        
        if img_list:
            # সাধারণত বইয়ের স্ক্যান করা ছবি প্রথম ইমেজ (xref) হিসেবে থাকে
            xref = img_list[0][0]
            base_image = doc.extract_image(xref)
            img_bytes = base_image["image"]
            
            # মূল পেইজের সাইজ অনুযায়ী নতুন পেইজ তৈরি
            page_rect = page.rect
            new_page = out_doc.new_page(width=page_rect.width, height=page_rect.height)
            
            # শুধু ইমেজটি ইনসার্ট করা (এতে আলাদা টেক্সট লেয়ারগুলো বাদ পড়বে)
            new_page.insert_image(page_rect, stream=img_bytes)
            
    out_doc.save(output_pdf)
    out_doc.close()
    doc.close()
    print(f"Success! Saved as: {output_pdf}")

if __name__ == "__main__":
    # আপনার ফাইলের নাম এবং পাসওয়ার্ড
    INPUT_FILE = "input.pdf" 
    OUTPUT_FILE = "cleaned_book.pdf"
    PASSWORD = "Educationblog24.com"
    
    if os.path.exists(INPUT_FILE):
        remove_watermark_and_save_pdf(INPUT_FILE, OUTPUT_FILE, PASSWORD)
    else:
        print("Input file not found!")
      
