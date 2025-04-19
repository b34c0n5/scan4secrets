


# 🕵️‍♂️ `scan4secrets` : Overview


A lightweight, high-performance secret scanner built for both SAST 🔍 & DAST 🌐.


💥 **Key Features:**

- 🧠 **400+ advanced detection rules** to uncover secrets, tokens, keys, and misconfigs.
- 📂 Supports scanning across **260+ file extensions**.
- 🛠️ Tailored **wordlists** for real-world tech stacks:
  - 🧰 `CloudProvider-Service`
  - 🐳 `Docker-Compose-Kubernetes`
  - 🔐 `Keys-SSH-Certificate`
  - 🚀 `Node.js-Express.js`
  - ⚙️ `OtherConfig-CI-DevOps`
  - 🐍 `Python-Django-Flask`
  - 🎨 `React-Next.js-Vite-Frontend`
  - ⚡ `common`, `.env`, `php-laravel-symfony-drupal`, `wordpress` and more...
- 🧾 Output formats: **CSV**, **Excel**, **PDF**, **HTML**
- 🎯 Custom **output paths** supported for integration into pipelines & workflows.

---



# Report 
Report will be saved in the current working directory  

# How to install

```bash
git clone https://github.com/m14r41/scan4secrets.git
cd scan4secrets
pip install -r requirements.txt
```

# How to use
- Scan a directory and generate an Excel file:
```bash
python3 main.py --path /path/to/code
```

- Generate multiple output formats (Excel, CSV, PDF):
```bash
python main.py --path /path/to/code --formats excel pdf csv html --output scan_report
```

- Output as HTML only
```bash
python main.py --path /var/www/html --formats html --output web_secrets
```


# Sample Output for SAST ( Source Code Review)
![image](https://github.com/user-attachments/assets/d2b05f4a-eddd-42e4-bfd1-198b3a8bf395)
![image](https://github.com/user-attachments/assets/badd8bd9-0875-4a10-9a83-6c91d454b996)


---

# Sample Output for Websites
![image](https://github.com/user-attachments/assets/a0563755-36cc-450c-974d-64b114b059eb)
![image](https://github.com/user-attachments/assets/0b2e6a94-fcef-4157-b622-6f705f3076fc)
![image](https://github.com/user-attachments/assets/2e9701d6-b475-4193-a398-a17bd4641816)
![image](https://github.com/user-attachments/assets/99b545b4-65e2-4391-83b2-b12fd580e343)








# Contribution:
> Feel free to contribute, thank you :)


> **Credit:** [m14r41](https://www.linkedin.com/in/m14r41/)



