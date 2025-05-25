import asyncio
import aiohttp
import aiohttp.resolver
from colorama import init, Fore, Style
import sys
import random
import ipaddress
import time
import uvloop

init()
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

async def resolve_domain(domain, session, output_file, counter, total_domains):
    try:
        resolver = aiohttp.resolver.ThreadedResolver()
        ip = await resolver.resolve(domain)
        ip_addr = ip[0]['host']
        
        sys.stdout.write(f"{Fore.BLUE}Scanning [{counter}/{total_domains}] » {Fore.LIGHTCYAN_EX}{domain}{Fore.BLUE}... ")
        sys.stdout.flush()
        print(f"{Fore.GREEN}Berhasil → {ip_addr}{Style.RESET_ALL}")
        
        with open(output_file, 'a') as f:
            f.write(ip_addr + '\n')
    except (aiohttp.client_exceptions.ClientError, ValueError, KeyError, Exception):
        sys.stdout.write(f"{Fore.BLUE}Scanning [{counter}/{total_domains}] » {Fore.LIGHTCYAN_EX}{domain}{Fore.BLUE}... ")
        sys.stdout.flush()
        print(f"{Fore.RED}Gagal: IP Tidak Ditemukan{Style.RESET_ALL}")

async def mass_domain_to_ip(input_file, max_concurrent):
    start_time = time.time()
    try:
        with open(input_file, 'r') as f:
            domains = [line.strip() for line in f if line.strip()]
        
        if not domains:
            print(f"{Fore.RED}File {input_file} kosong{Style.RESET_ALL}")
            return
        
        total_domains = len(domains)
        print(f"{Fore.CYAN}Memulai proses Mass Domain To IP...{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Total domain: {total_domains}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Max concurrent tasks: {max_concurrent}{Style.RESET_ALL}")
        print(f"{Fore.LIGHTBLACK_EX}{'═' * 60}{Style.RESET_ALL}")

        with open('ip.txt', 'w') as f:
            f.write("")

        connector = aiohttp.TCPConnector(limit=max_concurrent)
        async with aiohttp.ClientSession(connector=connector) as session:
            tasks = []
            for i, domain in enumerate(domains, 1):
                tasks.append(resolve_domain(domain, session, 'ip.txt', i, total_domains))
            await asyncio.gather(*tasks, return_exceptions=True)

        elapsed_time = time.time() - start_time
        print(f"{Fore.LIGHTBLACK_EX}{'═' * 60}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Proses selesai dalam {elapsed_time:.2f} detik! IP disimpan di ip.txt{Style.RESET_ALL}")
    except FileNotFoundError:
        print(f"{Fore.RED}File input {input_file} tidak ditemukan{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Terjadi kesalahan: {str(e)}{Style.RESET_ALL}")

def mass_ip_ranger(input_file):
    start_time = time.time()
    try:
        with open(input_file, 'r') as f:
            ips = [line.strip() for line in f if line.strip()]
        
        if not ips:
            print(f"{Fore.RED}File {input_file} kosong{Style.RESET_ALL}")
            return
        
        all_ips = []
        for ip in ips:
            try:
                ip_addr = ipaddress.IPv4Address(ip)
                base_ip = ipaddress.IPv4Address(int(ip_addr) & 0xFFFFFF00)
                for i in range(256):
                    new_ip = ipaddress.IPv4Address(int(base_ip) + i)
                    all_ips.append(str(new_ip))
            except ipaddress.AddressValueError:
                print(f"{Fore.RED}IP tidak valid: {ip}{Style.RESET_ALL}")

        random.shuffle(all_ips)

        with open('RangedIP.txt', 'w') as f:
            for ip in all_ips:
                f.write(ip + '\n')
        
        elapsed_time = time.time() - start_time
        print(f"{Fore.GREEN}Rentang IP (256 per input) telah disimpan secara acak di RangedIP.txt dalam {elapsed_time:.2f} detik{Style.RESET_ALL}")
    except FileNotFoundError:
        print(f"{Fore.RED}File input {input_file} tidak ditemukan{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Terjadi kesalahan: {str(e)}{Style.RESET_ALL}")

def main():
    ascii_art = f"""
    {Fore.LIGHTMAGENTA_EX}╭━━━╮┈┈╱╲┈┈┈╱╲{Style.RESET_ALL}
    {Fore.LIGHTMAGENTA_EX}┃╭━━╯┈┈▏{Fore.YELLOW}▔▔▔▔▔{Fore.LIGHTMAGENTA_EX}▕{Style.RESET_ALL}
    {Fore.LIGHTMAGENTA_EX}┃╰━━━━━▏{Fore.CYAN}╭▆┊╭▆{Fore.LIGHTMAGENTA_EX}▕{Style.RESET_ALL}
    {Fore.LIGHTMAGENTA_EX}╰┫╯╯╯╯╯▏{Fore.CYAN}╰╯▼╰╯{Fore.LIGHTMAGENTA_EX}▕{Style.RESET_ALL}
    {Fore.LIGHTMAGENTA_EX}┈┃╯╯╯╯╯▏{Fore.CYAN}╰━┻━╯{Fore.LIGHTMAGENTA_EX}▕{Style.RESET_ALL}
    {Fore.LIGHTMAGENTA_EX}┈╰┓┏┳━┓┏┳┳━━━╯{Style.RESET_ALL}
    {Fore.LIGHTMAGENTA_EX}┈┈┃┃┃┈┃┃┃┃┈┈┈┈{Style.RESET_ALL}
    {Fore.LIGHTMAGENTA_EX}┈┈┗┻┛┈┗┛┗┛┈┈┈┈{Style.RESET_ALL}
    """
    print(ascii_art)
    print(f"{Fore.CYAN}Mass Domain To IP & Mass IP Ranger{Style.RESET_ALL}")
    print(f"{Fore.LIGHTBLUE_EX}GitHub: {Fore.YELLOW}https://github.com/aliasakujou168{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'-'*40}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Pilih opsi:{Style.RESET_ALL}")
    print(f"{Fore.BLUE}1. Mass Domain To IP{Style.RESET_ALL}")
    print(f"{Fore.BLUE}2. Mass IP Ranger{Style.RESET_ALL}")
    
    while True:
        choice = input(f"{Fore.YELLOW}Masukkan 1 atau 2: {Style.RESET_ALL}")
        if choice in ['1', '2']:
            break
        print(f"{Fore.RED}Pilihan tidak valid, masukkan 1 atau 2{Style.RESET_ALL}")

    if choice == '1':
        input_file = input(f"{Fore.YELLOW}Masukkan nama file yang berisi daftar domain: {Style.RESET_ALL}")
        while True:
            try:
                max_concurrent = int(input(f"{Fore.YELLOW}Masukkan jumlah tugas bersamaan (disarankan 50-200): {Style.RESET_ALL}"))
                if max_concurrent > 0:
                    break
                print(f"{Fore.RED}Jumlah tugas harus lebih dari 0{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Masukkan angka yang valid{Style.RESET_ALL}")
        asyncio.run(mass_domain_to_ip(input_file, max_concurrent))
    elif choice == '2':
        input_file = input(f"{Fore.YELLOW}Masukkan nama file yang berisi daftar IP: {Style.RESET_ALL}")
        mass_ip_ranger(input_file)

if __name__ == '__main__':
    main()
