#!/usr/bin/env python3
"""
Cupid-Pro - Advanced Targeted Password List Generator
Author: Ibrahim Mustafa
Description: Generates a wordlist containing raw input strings + optional top common passwords.
             Supports Arabic and English interface.
"""

import sys
import signal
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich import box
import time

console = Console()

ASCII_ART = """
╔═══════════════════════════════════════════════════════════════╗
║   ██████╗██╗   ██╗██████╗ ██╗██████╗      ██████╗██████╗  ██████╗ ║
║  ██╔════╝██║   ██║██╔══██╗██║██╔══██╗    ██╔════╝██╔══██╗██╔═══██╗║
║  ██║     ██║   ██║██████╔╝██║██████╔╝    ██║     ██████╔╝██║   ██║║
║  ██║     ██║   ██║██╔═══╝ ██║██╔═══╝     ██║     ██╔══██╗██║   ██║║
║  ╚██████╗╚██████╔╝██║     ██║██║         ╚██████╗██║  ██║╚██████╔╝║
║   ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝          ╚═════╝╚═╝  ╚═╝ ╚═════╝ ║
║                    Advanced Targeted Password Generator        ║
║                           Cupid-Pro v3.5                       ║
╚═══════════════════════════════════════════════════════════════╝
"""

def graceful_exit(signum, frame):
    print("\n")
    console.print("[bold yellow]👋 شكراً لاستخدامك الأداة[/bold yellow]")
    console.print("[italic]تحياتي، Ibrahim Mustafa[/italic]")
    sys.exit(0)

signal.signal(signal.SIGINT, graceful_exit)

# ========== قوائم الأسئلة (عربي / إنجليزي) ==========
QUESTIONS_AR = {
    "Social Media": [
        "أدخل اسم المستخدم: ",
        "أدخل الاسم الكامل (الأول والأخير): ",
        "أدخل سنة الميلاد (YYYY): ",
        "أدخل تاريخ الميلاد الكامل (DDMMYYYY) (اختياري): ",
        "أدخل رقم الهاتف: ",
        "أدخل اسم الحيوان الأليف: ",
        "أدخل اللقب: ",
        "أدخل اسم الزوج/الزوجة: ",
        "أدخل اسم الابن/الابنة (أو عدة أسماء مفصولة بفواصل): ",
        "أدخل الهواية المفضلة: ",
        "أدخل الفريق الرياضي المفضل: ",
        "أدخل المطرب/الفرقة الموسيقية المفضلة: "
    ],
    "WiFi": [
        "أدخل ماركة الراوتر: ",
        "أدخل رقم المنزل: ",
        "أدخل اسم الشارع: ",
        "أدخل رقم الهاتف: ",
        "أدخل اسم شبكة الواي فاي (SSID): ",
        "أدخل الكلمة المفضلة: ",
        "أدخل موديل السيارة (مثل تويوتا 2020): "
    ],
    "System": [
        "أدخل اسم مستخدم الكمبيوتر: ",
        "أدخل اسم الشركة: ",
        "أدخل البريد الإلكتروني: ",
        "أدخل رقم الموظف: ",
        "أدخل الرقم المفضل: ",
        "أدخل الكلمة المفضلة: ",
        "أدخل مدينة الميلاد: ",
        "أدخل اسم الجامعة/الكلية: ",
        "أدخل اسم المدرسة الأولى: ",
        "أدخل تاريخ مهم (مثل الزواج، أول وظيفة): ",
        "أدخل اسم الأم قبل الزواج: "
    ]
}

QUESTIONS_EN = {
    "Social Media": [
        "Enter target's username: ",
        "Enter target's real name (First Last): ",
        "Enter target's birth year (YYYY): ",
        "Enter target's full birth date (DDMMYYYY) (optional): ",
        "Enter target's phone number: ",
        "Enter target's pet name: ",
        "Enter target's nickname: ",
        "Enter partner's/spouse's name: ",
        "Enter child's name (or multiple names separated by commas): ",
        "Enter target's favorite hobby: ",
        "Enter target's favorite sports team: ",
        "Enter target's favorite singer/band: "
    ],
    "WiFi": [
        "Enter target's router brand: ",
        "Enter target's house number: ",
        "Enter target's street name: ",
        "Enter target's phone number: ",
        "Enter target's WiFi name (SSID): ",
        "Enter target's favorite word: ",
        "Enter target's car model (e.g., Toyota 2020): "
    ],
    "System": [
        "Enter target's computer username: ",
        "Enter target's company name: ",
        "Enter target's email address: ",
        "Enter target's employee ID: ",
        "Enter target's favorite number: ",
        "Enter target's favorite word: ",
        "Enter target's birthplace (city): ",
        "Enter target's university/college name: ",
        "Enter target's first school name: ",
        "Enter target's important date (e.g., wedding, first job): ",
        "Enter mother's maiden name: "
    ]
}

TEXTS_AR = {
    "title": "اختر نوع الهجوم:",
    "option_1": "  1. وسائل التواصل الاجتماعي",
    "option_2": "  2. الواي فاي",
    "option_3": "  3. النظام (كمبيوتر/عمل)",
    "option_4": "  4. مزيج الكل (جميع الأسئلة)",
    "choice_prompt": "أدخل اختيارك",
    "common_passwords_prompt": "هل تريد إضافة قائمة بأكثر 250 كلمة مرور شيوعاً إلى القائمة؟",
    "save_prompt": "هل تريد حفظ القائمة في ملف؟",
    "filename_prompt": "أدخل اسم الملف",
    "done_msg": "تم. استخدم الأداة بشكل أخلاقي!",
    "no_info_msg": "لم يتم تقديم أي معلومات. إلغاء...",
    "collect_msg": "✓ تم جمع {} معلومة.",
    "saved_msg": "✓ تم حفظ {} كلمة في {}",
    "generating": "جاري توليد الكلمات...",
    "no_words": "لم يتم توليد أي كلمات.",
    "exiting": "خروج...",
    "exit_msg": "👋 شكراً لاستخدامك الأداة",
    "thanks_msg": "تحياتي، Ibrahim Mustafa",
    "language_prompt": "اختر اللغة / Choose Language:",
    "lang_ar": "  1. العربية",
    "lang_en": "  2. English",
    "lang_choice": "Enter your choice / أدخل اختيارك",
    "attack_type_names": {
        "Social Media": "وسائل التواصل الاجتماعي",
        "WiFi": "الواي فاي",
        "System": "النظام",
        "Mix All": "مزيج الكل"
    }
}

TEXTS_EN = {
    "title": "Select attack type:",
    "option_1": "  1. Social Media",
    "option_2": "  2. WiFi",
    "option_3": "  3. System",
    "option_4": "  4. Mix All (combine all questions)",
    "choice_prompt": "Enter your choice",
    "common_passwords_prompt": "Do you want to add the top 250 most common passwords to the wordlist?",
    "save_prompt": "Save wordlist to file?",
    "filename_prompt": "Enter filename",
    "done_msg": "Done. Stay ethical!",
    "no_info_msg": "No information provided. Exiting...",
    "collect_msg": "✓ Collected {} pieces of information.",
    "saved_msg": "✓ Saved {} words to {}",
    "generating": "Generating words...",
    "no_words": "No words generated.",
    "exiting": "Exiting...",
    "exit_msg": "👋 Thank you for using the tool",
    "thanks_msg": "Regards, Ibrahim Mustafa",
    "language_prompt": "اختر اللغة / Choose Language:",
    "lang_ar": "  1. العربية",
    "lang_en": "  2. English",
    "lang_choice": "Enter your choice / أدخل اختيارك",
    "attack_type_names": {
        "Social Media": "Social Media",
        "WiFi": "WiFi",
        "System": "System",
        "Mix All": "Mix All"
    }
}

COMMON_PASSWORDS = [
    "123456", "123456789", "admin", "12345678", "Aa123456", "12345", "password",
    "123", "1234567890", "qwerty123", "qwerty", "Aa@123456", "Pass@123", "admin123",
    "12345678910", "111111", "1234567891", "Welcome1", "abc123", "Password1", "qwerty1",
    "abcd1234", "1q2w3e4r", "1qaz2wsx", "1234", "1234567", "123123", "123321", "letmein",
    "iloveyou", "monkey", "dragon", "football", "sunshine", "princess", "master", "monday",
    "freedom", "whatever", "demo", "root", "ubnt", "default", "changeme", "temp", "test",
    "testing", "dummy", "office", "user123", "sample", "welcome123", "service", "deploy",
    "admintelecom", "000000", "112233", "0987654321", "87654321", "987654321", "13579",
    "147258", "11111111", "222222", "333333", "444444", "555555", "7777777", "777777",
    "101010", "131313", "246810", "55555", "666666", "696969", "888888", "999999", "10101",
    "123098", "bmw123", "ford", "secret", "mohamed", "ahmed", "mostafa", "ali", "omar",
    "samir", "khaled", "heba", "nour", "mona", "mariam", "egypt", "cairo", "alex", "masr",
    "masry", "quran", "islam", "allah", "bismillah", "love", "king", "queen", "hero",
    "012345", "102030", "mido", "salah", "arsenal", "liverpool", "barcelona", "real madrid",
    "chelsea", "manutd", "ronaldo", "messi", "snoopy", "flower", "bigbang", "harrypoter",
    "sweetheart", "sweet", "prince", "passw0rd", "p@ssw0rd", "pass@123", "admin@123",
    "administrator", "user", "guest", "welcome", "Aa123456", "1q2w3e", "abc123456",
    "password123", "qwerty12345", "1234567q", "123456q", "12345q", "54321", "321654",
    "159753", "753951", "852456", "951753", "159357", "aaaaaa", "bbbbbb", "abcdef", "abcde",
    "abcd", "a123456", "a12345", "zaq12wsx", "qweasd", "qweasdzxc", "asdfghjk", "zxcvbnm",
    "zxcvbn", "1qazzaq1", "1qazxsw2", "qazwsxedc", "zaq1xsw2", "1qaz@WSX", "1qaz!QAZ",
    "pass123", "pass1234", "pass@1234", "Welcome@123", "Welcome1234", "admin@12345",
    "Admin123456", "Aa12345678", "Aa123456789", "P@ssw0rd", "P@ssw0rd123", "P@55w0rd",
    "p@55w0rd", "P@ssword", "password!", "Password123", "Password1234", "Password12345",
    "Password@123", "Password@1234", "Admin@12345", "Admin12345", "admin12345",
    "Admin@123456", "admin@123456", "Aa1234567", "Aa1234567890", "1qaz2wsx3edc",
    "1qaz2wsx3edc4rfv", "qwertyuiop", "qwertyuiop123", "asdfghjkl", "zxcvbnm123",
    "iloveyou123", "iloveyou1", "iloveyou!", "love123", "love1234", "loveyou", "sweet123",
    "sweet1234", "princess1", "princess123", "dragon123", "dragon1", "monkey123", "monkey1",
    "football123", "football1", "sunshine1", "sunshine123", "master1", "master123", "monday1",
    "monday123", "freedom1", "freedom123", "whatever1", "whatever123", "letmein123", "letmein1",
    "test1234", "test1", "temp123", "demo123", "changeme123", "default123", "root123",
    "ubnt123", "guest123", "user1234", "office123", "service123", "deploy123", "sample123",
    "company123", "business123", "school123", "college123", "university123", "student123",
    "teacher123", "doctor123", "engineer123", "lawyer123", "music123", "movie123", "book123",
    "game123", "gaming123", "playstation123", "xbox123", "nintendo123", "computer123",
    "laptop123", "phone123", "mobile123", "iphone123", "samsung123", "huawei123", "oppo123",
    "vivo123", "realme123", "xiaomi123", "oneplus123", "google123", "facebook123",
    "instagram123", "twitter123", "whatsapp123", "youtube123", "tiktok123", "snapchat123",
    "telegram123", "discord123", "reddit123", "linkedin123", "netflix123", "spotify123",
    "amazon123", "ebay123", "paypal123", "apple123", "microsoft123", "windows123", "linux123",
    "ubuntu123", "centos123", "debian123", "fedora123", "kali123", "parrot123", "black123",
    "white123", "red123", "blue123", "green123", "yellow123", "orange123", "purple123",
    "pink123", "brown123", "grey123", "gray123", "silver123", "gold123", "copper123",
    "bronze123", "steel123", "iron123", "metal123", "wood123", "stone123", "fire123",
    "water123", "earth123", "air123", "sky123", "star123", "moon123", "sun123", "planet123",
    "galaxy123", "universe123", "cosmos123", "space123", "rocket123", "astronaut123",
    "alien123", "robot123", "cyber123", "hacker123", "security123", "privacy123", "encrypt123",
    "decrypt123", "crypto123", "bitcoin123", "ethereum123", "blockchain123", "wallet123",
    "password1234", "password12345", "password123456", "password1234567", "password12345678",
    "password123456789", "password1234567890", "123456password", "12345678password",
    "qwertypassword", "abcdpassword", "adminpassword", "userpassword", "rootpassword", "toor",
    "toor123", "toor1234", "toor12345", "toor123456", "toor1234567", "toor12345678",
    "toor123456789", "toor1234567890"
]

def collect_info(attack_type, questions_dict, texts, lang):
    info = {}
    questions = []
    if attack_type == "Mix All":
        for qlist in questions_dict.values():
            questions.extend(qlist)
    else:
        questions = questions_dict.get(attack_type, [])
    
    attack_name = texts["attack_type_names"].get(attack_type, attack_type)
    console.print(Panel(f"[bold cyan]{attack_name} {texts.get('info_gathering', 'Information Gathering') if lang == 'en' else 'جمع المعلومات'}[/bold cyan]", box=box.ROUNDED))
    try:
        for q in questions:
            answer = Prompt.ask(q, default="")
            if answer.strip() and answer.lower() not in ["no", "skip", ""]:
                if "child's name" in q.lower() or "اسم الابن" in q.lower():
                    if "," in answer:
                        children = [c.strip() for c in answer.split(",")]
                        for i, child in enumerate(children):
                            info[f"child_{i+1}_name"] = child
                    else:
                        info["child_1_name"] = answer
                else:
                    key = q.lower().replace(" ", "_").replace("(", "").replace(")", "").replace("?", "")
                    # إزالة الكلمات العربية والإنجليزية الزائدة
                    key = key.replace("أدخل_", "").replace("enter_", "")
                    info[key] = answer.strip()
    except KeyboardInterrupt:
        graceful_exit(None, None)
    return info

def extract_raw_data(info):
    raw = set()
    for key, value in info.items():
        if len(value) >= 2:
            raw.add(value)
            raw.add(value.lower())
            raw.add(value.upper())
            raw.add(value.capitalize())
            parts = value.split()
            for part in parts:
                if len(part) >= 2:
                    raw.add(part)
                    raw.add(part.lower())
                    raw.add(part.upper())
                    raw.add(part.capitalize())
        if "email" in key and "@" in value:
            email_local = value.split('@')[0]
            if len(email_local) >= 2:
                raw.add(email_local)
                raw.add(email_local.lower())
                raw.add(email_local.upper())
                raw.add(email_local.capitalize())
    for key, val in info.items():
        if key.startswith("child_"):
            if len(val) >= 2:
                raw.add(val)
                raw.add(val.lower())
                raw.add(val.upper())
                raw.add(val.capitalize())
                parts = val.split()
                for part in parts:
                    if len(part) >= 2:
                        raw.add(part)
                        raw.add(part.lower())
                        raw.add(part.upper())
                        raw.add(part.capitalize())
    return list(raw)

def generate_wordlist(raw_words, add_common_passwords):
    wordlist = set(raw_words)
    if add_common_passwords:
        wordlist.update(COMMON_PASSWORDS)
    return sorted(wordlist)

def display_passwords(passwords, limit=40):
    table = Table(title=f"[bold green]Generated Wordlist (Total: {len(passwords)})[/bold green]", box=box.ROUNDED)
    table.add_column("#", style="cyan", no_wrap=True)
    table.add_column("Word", style="yellow")
    for i, pwd in enumerate(passwords[:limit], start=1):
        table.add_row(str(i), pwd)
    if len(passwords) > limit:
        console.print(f"\n[italic]... and {len(passwords) - limit} more.[/italic]")
    console.print(table)

def save_to_file(words, filename, texts):
    with open(filename, 'w') as f:
        f.write("\n".join(words))
    console.print(texts["saved_msg"].format(len(words), filename))

def main():
    console.clear()
    console.print(ASCII_ART, style="bold cyan")
    
    # اختيار اللغة
    console.print("[bold yellow]اختر اللغة / Choose Language:[/bold yellow]")
    console.print("  1. العربية")
    console.print("  2. English\n")
    lang_choice = Prompt.ask("[bold cyan]Enter your choice / أدخل اختيارك[/bold cyan]", choices=["1", "2"], default="1")
    
    if lang_choice == "1":
        lang = "ar"
        texts = TEXTS_AR
        questions_dict = QUESTIONS_AR
        console.print("[italic yellow]⚠️  استخدم هذه الأداة فقط لاختبار الاختراق الأخلاقي على أجهزتك الخاصة.[/italic yellow]\n")
    else:
        lang = "en"
        texts = TEXTS_EN
        questions_dict = QUESTIONS_EN
        console.print("[italic yellow]⚠️  Use only for authorized security testing on your own systems.[/italic yellow]\n")
    
    # قائمة أنواع الهجوم مترجمة
    console.print(f"[bold yellow]{texts['title']}[/bold yellow]")
    console.print(texts["option_1"])
    console.print(texts["option_2"])
    console.print(texts["option_3"])
    console.print(texts["option_4"] + "\n")
    
    try:
        choice = Prompt.ask(f"[bold cyan]{texts['choice_prompt']}[/bold cyan]", choices=["1", "2", "3", "4"], default="1")
    except KeyboardInterrupt:
        graceful_exit(None, None)
        return
    
    attack_type_map = {"1": "Social Media", "2": "WiFi", "3": "System", "4": "Mix All"}
    attack_type = attack_type_map[choice]
    
    info = collect_info(attack_type, questions_dict, texts, lang)
    if not info:
        console.print(f"[bold red]{texts['no_info_msg']}[/bold red]")
        return
    
    console.print(f"\n[green]{texts['collect_msg'].format(len(info))}[/green]")
    
    add_common = Confirm.ask(f"[yellow]{texts['common_passwords_prompt']}[/yellow]", default=False)
    
    raw_words = extract_raw_data(info)
    wordlist = generate_wordlist(raw_words, add_common)
    
    if not wordlist:
        console.print(f"[bold red]{texts['no_words']}[/bold red]")
        return
    
    display_passwords(wordlist)
    
    try:
        if Confirm.ask(f"[yellow]{texts['save_prompt']}[/yellow]"):
            filename = Prompt.ask(f"[bold cyan]{texts['filename_prompt']}[/bold cyan]", default="cupid_output.txt")
            save_to_file(wordlist, filename, texts)
    except KeyboardInterrupt:
        graceful_exit(None, None)
        return
    
    console.print(f"\n[bold green]{texts['done_msg']}[/bold green]")

if __name__ == "__main__":
    main()
