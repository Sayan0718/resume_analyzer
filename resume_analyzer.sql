CREATE DATABASE resume_analyzer;

use resume_analyzer;

CREATE TABLE job_listings;

drop database resume_analyzer;

CREATE TABLE job_listings (
    job_title VARCHAR(255),
    required_skills TEXT
);
INSERT INTO job_listings (job_title, required_skills) VALUES
('Data Analyst', 'Python, SQL, Data Analysis, Data Visualization, NumPy, Pandas, Seaborn, Matplotlib, Power BI, Tableau, Excel, MySQL Workbench'),
('Machine Learning Engineer', 'Python, TensorFlow, Scikit-Learn, PyTorch, NumPy, Pandas, Data Preprocessing, Feature Engineering, Model Deployment, MLFlow'),
('Software Engineer', 'Java, Python, C++, Software Development, Git, Jenkins, Docker, Kubernetes, Spring Boot, REST APIs'),
('Backend Developer', 'Node.js, Express.js, Python, Django, Flask, MySQL, PostgreSQL, MongoDB, Redis, Docker, Kubernetes'),
('Frontend Developer', 'HTML, CSS, JavaScript, React.js, Vue.js, Angular, TypeScript, Bootstrap, Tailwind CSS, UI/UX Design, Figma'),
('Full Stack Developer', 'JavaScript, React.js, Node.js, Express.js, MongoDB, MySQL, REST APIs, Git, AWS, Firebase, Docker'),
('Cybersecurity Analyst', 'Network Security, Ethical Hacking, Penetration Testing, Kali Linux, Burp Suite, Nmap, Wireshark, SIEM, Firewalls'),
('Cloud Engineer', 'AWS, Azure, Google Cloud, Kubernetes, Docker, Terraform, CI/CD, Serverless Computing, DevOps'),
('Database Administrator', 'MySQL, PostgreSQL, MongoDB, Oracle, SQL Server, Database Optimization, Backup & Recovery, ETL, Data Warehousing'),
('AI Engineer', 'Deep Learning, Neural Networks, NLP, Computer Vision, OpenCV, PyTorch, TensorFlow, Hugging Face, MLOps, Model Optimization'),
('DevOps Engineer', 'CI/CD, Jenkins, Docker, Kubernetes, Terraform, Ansible, AWS, Linux, Git, Bash Scripting'),
('Data Scientist', 'Python, R, SQL, Data Wrangling, Machine Learning, Statistical Analysis, Tableau, Power BI, Big Data, Hadoop, Spark'),
('IoT Engineer', 'Arduino, Raspberry Pi, Embedded Systems, MQTT, Zigbee, LoRa, Edge Computing, Wireless Sensor Networks'),
('Blockchain Developer', 'Solidity, Ethereum, Hyperledger, Smart Contracts, Cryptography, Web3.js, NFT Development, DeFi'),
('Game Developer', 'Unity, Unreal Engine, C++, C#, Game Physics, OpenGL, DirectX, Blender, 3D Modeling, Game AI');


