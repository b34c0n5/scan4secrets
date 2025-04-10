# Report 
Report will be saved in the same folder like 
![image](https://github.com/user-attachments/assets/46506bec-26c4-4caa-810d-282a973688ab)


# How to install

```bash
git clone https://github.com/m14r41/scan4secrets.git
cd scan4secrets
pip install -r requirements.txt
```

# How to use
- Scan a directory and generate an Excel file:
```bash
python scanner.py --path /path/to/code
```

- Generate multiple output formats (Excel, CSV, PDF):
```bash
python scanner.py --path /path/to/code --formats excel pdf csv html --output scan_report
```

- Output as HTML only
```bash
python scanner.py --path /var/www/html --formats html --output web_secrets
```

# Sample Output 

![image](https://github.com/user-attachments/assets/07576fed-ae93-44c3-9427-10432fb1fcd3)
![image](https://github.com/user-attachments/assets/22d53214-9f4d-49d6-b735-308ce1daa49c)


# Feel free to add more rules


