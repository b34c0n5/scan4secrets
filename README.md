# Report 
Report will be saved in the project folder  

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
python scan4secrets.py --path /path/to/code --formats excel pdf csv html --output scan_report
```

- Output as HTML only
```bash
python scan4secrets.py --path /var/www/html --formats html --output web_secrets
```

# Sample Output On Linux

![image](https://github.com/user-attachments/assets/5e58380d-afde-42ff-95b3-785ac5ebc822)
![image](https://github.com/user-attachments/assets/6e459b0a-5844-4963-8381-0b855a626db9)


# Sample Output in Windows
![image](https://github.com/user-attachments/assets/da55c8dd-ff5b-4ab8-8fef-69b0778683aa)
![image](https://github.com/user-attachments/assets/94c39090-5abe-4e5f-bf42-381597a710ed)
![image](https://github.com/user-attachments/assets/52439c7e-ff47-49ae-a00e-6765b01d1de4)


# Feel Free to Add More Rules and Don't Miss Any Secrets :)

> **Credit:** [m14r41](https://www.linkedin.com/in/m14r41/)



