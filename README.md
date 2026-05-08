[README.html](https://github.com/user-attachments/files/27532670/README.html)
<div align="center">
  <h1>Masroofy</h1>
  <p><b>Intelligent Budget Tracking & Financial Management</b></p>
  <p>
    <img src="https://img.shields.io/badge/Python-3.12-blue?style=flat-square&logo=python" alt="Python">
    <img src="https://img.shields.io/badge/Django-5.0-092E20?style=flat-square&logo=django" alt="Django">
    <img src="https://img.shields.io/badge/Database-SQLite3-003B57?style=flat-square&logo=sqlite" alt="SQLite">
    <img src="https://img.shields.io/badge/Code_Style-PEP_8-green?style=flat-square" alt="PEP 8">
  </p>
</div>

<hr>

<h2>About The Project</h2>
<p>
  <b>Masroofy</b> is a robust, web-based personal finance application built with the Django Web Framework. It empowers users to take control of their daily spending by tracking budget cycles, logging rapid expenses, and dynamically calculating safe daily spending limits using a custom rollover algorithm.
</p>
<p>
  <i>This project was developed as a Final Software Engineering Project, strictly adhering to PEP 8 clean code standards, comprehensive documentation, and the MVT (Model-View-Template) architectural pattern.</i>
</p>

<h2>Key Features</h2>
<ul>
  <li><b>Dynamic Dashboard:</b> Visualizes aggregate spending, remaining budget, and flags warnings when approaching 75% or 90% of the allowance.</li>
  <li><b>Rollover Algorithm:</b> Intelligently calculates unspent money from previous days and rolls it over to increase today's safe spending limit.</li>
  <li><b>Rapid Expense Logging:</b> Quickly log expenses with categories (Food, Transport, Utilities, Entertainment, Other) and automatic timestamps.</li>
  <li><b>Cycle Management:</b> Easily create new budget cycles while automatically deactivating and archiving older ones.</li>
  <li><b>Transaction History:</b> View a comprehensive, chronologically sorted list of all past expenses.</li>
</ul>

<h2>Tech Stack</h2>
<table>
  <tr>
    <td><b>Backend</b></td>
    <td>Python, Django</td>
  </tr>
  <tr>
    <td><b>Database</b></td>
    <td>SQLite3</td>
  </tr>
  <tr>
    <td><b>Frontend</b></td>
    <td>HTML5, CSS, Django Templating Engine</td>
  </tr>
  <tr>
    <td><b>Architecture</b></td>
    <td>MVT (Model-View-Template)</td>
  </tr>
</table>

<h2>Installation & Setup</h2>
<p>Follow these simple steps to run Masroofy locally on your machine:</p>

<ol>
  <li><b>Clone the repository:</b>
    <pre><code>git clone https://github.com/yourusername/masroofy_project.git
cd masroofy_project</code></pre>
  </li>
  <li><b>Create and activate a virtual environment:</b>
    <pre><code>python -m venv myenv
# On Windows:
.\myenv\Scripts ctivate
# On Mac/Linux:
source myenv/bin/activate</code></pre>
  </li>
  <li><b>Install dependencies:</b>
    <pre><code>pip install django</code></pre>
  </li>
  <li><b>Run database migrations:</b>
    <pre><code>python manage.py makemigrations
python manage.py migrate</code></pre>
  </li>
  <li><b>Start the development server:</b>
    <pre><code>python manage.py runserver</code></pre>
  </li>
</ol>
<p>Visit <code>http://127.0.0.1:8000/</code> in your web browser to start budgeting!</p>

<h2>Project Structure (Core Logic)</h2>
<pre><code>masroofy_project/
├── budget/
│   ├── models.py      # Database Schema (BudgetCycle, Expense)
│   ├── views.py       # Core Business Logic & Rollover Algorithm
│   ├── urls.py        # Application Routing
│   └── admin.py       # Django Admin Configuration
├── masroofy_project/  # Main Project Settings & Global URLs
└── templates/         # HTML Templates for the UI</code></pre>

<h2>Team & Contributors</h2>
<ul>
  <li><b>[omar mohamed hussein / ahmed mohamed ahmed / omar amgad hanafy / youssef said abdelaziz]</b> - <i>Software Engineering Final Project</i></li>
</ul>

<div align="center">
  <br>
  <p><i>Developed with using Python & Django</i></p>
