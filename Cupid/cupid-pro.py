#!/usr/bin/env python3
"""
Cupid-Pro - Advanced Targeted Password List Generator
Author: Your Name
Description: Interactive tool to generate custom password lists based on target's information.
Disclaimer: Use only on your own systems or with explicit written permission.
"""

import itertools
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.progress import track
from rich import box
import time

console = Console()

# الأسئلة حسب القسم
QUESTIONS = {
    "Social Media": [
        "Enter target's username (social media): ",
        "Enter target's real name (First Last): ",
        "Enter target's birth year (YYYY): ",
        "Enter target's favorite number: ",
        "Enter target's pet name: ",
        "Enter target's favorite color: ",
        "Enter target's nickname: ",
        "Enter target's relationship status (single/married/complicated): ",
        "Enter target's favorite sports team: ",
        "Enter target's favorite singer/band: "
    ],
    "WiFi": [
        "Enter target's router brand (e.g., TP-Link): ",
        "Enter target's house number: ",
        "Enter target's street name: ",
        "Enter target's phone number (without country code): ",
        "Enter target's apartment number: ",
        "Enter target's WiFi name (SSID) if known: ",
        "Enter target's favorite TV show: ",
        "Enter target's car model: ",
        "Enter target's favorite food: ",
        "Enter target's favorite holiday destination: "
    ],
    "System": [
        "Enter target's computer username: ",
        "Enter target's company name: ",
        "Enter target's employee ID: ",
        "Enter target's email address: ",
        "Enter target's favorite programming language: ",
        "Enter target's favorite OS (Windows/Linux/Mac): ",
        "Enter target's favorite gaming platform: ",
        "Enter target's favorite movie: ",
        "Enter target's favorite book: ",
        "Enter target's favorite quote: "
    ]
}

# أنماط شائعة لتوليد كلمات المرور (سيتم توسيعها ديناميكياً)
BASE_PATTERNS = [
    "{username}", "{username}{year}", "{year}{username}",
    "{first}{last}", "{first}.{last}", "{first}_{last}", "{first}-{last}",
    "{first}{year}", "{year}{first}", "{last}{year}",
    "{pet}{year}", "{year}{pet}", "{pet}{username}",
    "{color}{number}", "{number}{color}", "{street}{number}",
    "{phone}", "{phone}{year}", "{wifiname}", "{wifiname}{number}",
    "{company}{year}", "{email_local}", "{email_local}{year}",
    "{username}123", "{username}123!", "{username}@{year}",
    "P@ssw0rd{year}", "Admin{year}", "root{year}",
    "{nickname}", "{nickname}{year}", "{team}{year}",
    "{singer}{year}", "{movie}{year}", "{book}{year}",
]

def collect_info(attack_type):
    """جمع المعلومات بناءً على نوع الهجوم."""
    info = {}
    questions = QUESTIONS.get(attack_type, [])
    if attack_type == "Mix All":
        # جمع جميع الأسئلة من كل الأقسام
        all_questions = []
        for qlist in QUESTIONS.values():
            all_questions.extend(qlist)
        questions = all_questions

    console.print(Panel(f"[bold cyan]{attack_type} Information Gathering[/bold cyan]", box=box.ROUNDED))
    for q in questions:
        answer = Prompt.ask(q, default="")
        if answer.strip() and answer.lower() not in ["no", "skip", ""]:
            key = q.lower().replace(" ", "_").replace("(", "").replace(")", "").replace("?", "")
            info[key] = answer.strip()
    return info

def extract_names(info):
    """استخراج الأسماء من المعلومات المجمعة."""
    names = []
    for key, value in info.items():
        if "name" in key or "username" in key or "nickname" in key:
            names.append(value)
        # استخراج الاسم الأول والأخير من "real name"
        if "real_name" in key:
            parts = value.split()
            if len(parts) >= 1:
                names.append(parts[0])
            if len(parts) >= 2:
                names.append(parts[-1])
    # إضافة كلمات من حقول أخرى قد تحتوي على أسماء
    for key in ["pet", "wife", "color", "team", "singer", "movie", "book"]:
        if key in info:
            names.append(info[key])
    return list(set(names))

def extract_years(info):
    """استخراج السنوات من المعلومات."""
    years = []
    for key, value in info.items():
        if "year" in key and value.isdigit():
            years.append(value)
        # استخراج سنة من البريد الإلكتروني (إن وجدت)
        if "email" in key and "@" in value:
            local = value.split('@')[0]
            for part in local.split('.'):
                if part.isdigit() and len(part) in [2,4]:
                    years.append(part)
    return list(set(years))

def extract_numbers(info):
    """استخراج الأرقام من المعلومات (هاتف، رقم المنزل، إلخ)."""
    numbers = []
    for key, value in info.items():
        if "number" in key or "phone" in key:
            numbers.append(value)
        # استخراج أرقام من أي حقل
        for word in value.split():
            if word.isdigit():
                numbers.append(word)
    return list(set(numbers))

def generate_passwords(info, attack_type):
    """توليد كلمات المرور بناءً على المعلومات المجمعة."""
    passwords = set()
    names = extract_names(info)
    years = extract_years(info)
    numbers = extract_numbers(info)
    
    # إضافة الكلمات المباشرة
    for name in names:
        if len(name) >= 4:
            passwords.add(name)
            passwords.add(name.lower())
            passwords.add(name.upper())
            passwords.add(name.capitalize())
    
    # توليد باستخدام الأنماط
    for pattern in BASE_PATTERNS:
        try:
            # تجربة كل اسم مع كل سنة وكل رقم
            for name in names:
                for year in years:
                    pwd = pattern.format(username=name, year=year, first=name, last=name,
                                         pet=info.get('pet_name', ''), color=info.get('favorite_color', ''),
                                         number=numbers[0] if numbers else '', street=info.get('street_name', ''),
                                         phone=info.get('phone_number', ''), wifiname=info.get('wifi_name', ''),
                                         company=info.get('company_name', ''), email_local=info.get('email_address', '').split('@')[0] if 'email_address' in info else '',
                                         nickname=info.get('nickname', ''), team=info.get('favorite_sports_team', ''),
                                         singer=info.get('favorite_singer/band', ''), movie=info.get('favorite_movie', ''),
                                         book=info.get('favorite_book', ''))
                    if len(pwd) >= 8:
                        passwords.add(pwd)
        except Exception:
            pass
    
    # توليد تركيبات إضافية (الاسم + الرقم، الرقم + الاسم)
    for name in names:
        for num in numbers:
            if len(name + num) >= 8:
                passwords.add(name + num)
                passwords.add(num + name)
                passwords.add(name + "@" + num)
                passwords.add(name + "_" + num)
                passwords.add(name + num + "!")
    
    # إضافة تواريخ الميلاد المحتملة (DDMMYYYY)
    for year in years:
        if len(year) == 4:
            for month in range(1,13):
                for day in range(1,32):
                    date = f"{day:02d}{month:02d}{year}"
                    if len(date) >= 8:
                        passwords.add(date)
    
    return sorted(passwords)

def display_passwords(passwords, limit=30):
    """عرض كلمات المرور في جدول جميل."""
    table = Table(title=f"[bold green]Generated Passwords (Total: {len(passwords)})[/bold green]", box=box.ROUNDED)
    table.add_column("#", style="cyan", no_wrap=True)
    table.add_column("Password", style="yellow")
    for i, pwd in enumerate(passwords[:limit], start=1):
        table.add_row(str(i), pwd)
    if len(passwords) > limit:
        console.print(f"\n[italic]... and {len(passwords) - limit} more.[/italic]")
    console.print(table)

def save_to_file(passwords, filename):
    """حفظ كلمات المرور في ملف."""
    with open(filename, 'w') as f:
        f.write("\n".join(passwords))
    console.print(f"[bold green]✓ Saved {len(passwords)} passwords to {filename}[/bold green]")

def main():
    console.clear()
    console.print(Panel.fit("[bold red]Cupid-Pro[/bold red]\n[italic]Advanced Targeted Password Generator[/italic]", border_style="cyan"))
    
    # اختيار نوع الهجوم
    attack_type = Prompt.ask("[bold yellow]Select attack type[/bold yellow]", choices=["Social Media", "WiFi", "System", "Mix All"], default="Social Media")
    
    # جمع المعلومات
    info = collect_info(attack_type)
    
    if not info:
        console.print("[bold red]No information provided. Exiting...[/bold red]")
        return
    
    console.print(f"\n[green]✓ Collected {len(info)} pieces of information.[/green]")
    
    # توليد كلمات المرور
    with console.status("[bold cyan]Generating passwords...[/bold cyan]"):
        time.sleep(1)
        passwords = generate_passwords(info, attack_type)
    
    if not passwords:
        console.print("[bold red]No passwords generated. Try providing more information or adjusting patterns.[/bold red]")
        return
    
    # عرض النتائج
    display_passwords(passwords)
    
    # حفظ في ملف
    if Confirm.ask("[yellow]Save passwords to file?[/yellow]"):
        filename = Prompt.ask("Enter filename", default="cupid_output.txt")
        save_to_file(passwords, filename)
    
    console.print("\n[bold green]Done. Stay ethical![/bold green]")

if __name__ == "__main__":
    main()