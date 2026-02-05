# TOPSIS: Technique for Order Preference by Similarity to Ideal Solution

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyPI](https://img.shields.io/badge/PyPI-Package-orange.svg)](https://pypi.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Web_App-red.svg)](https://streamlit.io/)

## 📖 Overview

TOPSIS is a multi-criteria decision-making (MCDM) method that helps rank alternatives when multiple, often conflicting criteria are involved. The core idea is simple: **the best option should be closest to the ideal solution and farthest from the worst solution**.

This project provides three implementations:
- **Command-line tool** for batch processing
- **Python package** published on PyPI
- **Web application** with email delivery

## ⚙️ How TOPSIS Works

### 1. Construct the Decision Matrix
- List all alternatives (options to choose from)
- Define evaluation criteria (e.g., cost, performance, reliability)

### 2. Normalize the Matrix
- Convert values into comparable scales using vector normalization
- Formula: `r_ij = x_ij / √(Σx²_ij)`
- Ensures criteria with different units (like dollars vs. hours) can be compared fairly

### 3. Apply Weights
- Assign importance to each criterion (e.g., performance = 0.5, cost = 0.3, reliability = 0.2)
- Multiply normalized values by their respective weights
- Formula: `v_ij = w_j × r_ij`

### 4. Determine Ideal & Negative-Ideal Solutions
- **Positive Ideal Solution (PIS)**: Best values across all criteria
  - For beneficial criteria (+): Maximum value
  - For cost criteria (-): Minimum value
- **Negative Ideal Solution (NIS)**: Worst values across all criteria
  - For beneficial criteria (+): Minimum value
  - For cost criteria (-): Maximum value

### 5. Calculate Distances
- Compute Euclidean distance of each alternative from PIS and NIS
- Distance from PIS: `S⁺ = √(Σ(v_ij - v⁺_j)²)`
- Distance from NIS: `S⁻ = √(Σ(v_ij - v⁻_j)²)`

### 6. Compute Relative Closeness
- Closeness = `S⁻ / (S⁺ + S⁻)`
- Range: 0 to 1 (higher is better)

### 7. Rank Alternatives
- Sort options based on closeness values
- The top-ranked option is the most preferred

## 📊 Example

Imagine choosing a laptop based on **Price**, **Performance**, and **Battery Life**:

| Laptop | Price ($) | Performance | Battery (hrs) |
|--------|-----------|-------------|---------------|
| A      | 800       | 85          | 6             |
| B      | 1200      | 95          | 8             |
| C      | 600       | 70          | 5             |

**Weights**: Price (0.3), Performance (0.5), Battery (0.2)  
**Impacts**: Price (-), Performance (+), Battery (+)

TOPSIS normalizes these values, applies weights, and calculates which laptop is closest to the "ideal" (low price, high performance, long battery life). The final ranking shows which laptop offers the best balance across all criteria.

**Result**: Laptop B might rank highest despite higher price due to superior performance and battery life weighted appropriately.

---

## 📦 Part I: Command-Line Implementation

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd topsis
```

### Usage

```bash
python topsis.py <InputFile> <Weights> <Impacts> <OutputFile>
```

### Example

```bash
python topsis.py data.csv "1,1,1,2" "+,+,-,+" output.csv
```

### Input Format

**data.csv:**
```csv
Model,Price,Storage,Camera,Looks
M1,250,16,12,5
M2,200,16,8,3
M3,300,32,16,4
M4,275,32,8,4
M5,225,16,16,2
```

### Output Format

**output.csv:**
```csv
Model,Price,Storage,Camera,Looks,Topsis Score,Rank
M3,300,32,16,4,0.691754,1
M4,275,32,8,4,0.535464,2
M1,250,16,12,5,0.534675,3
M5,225,16,16,2,0.401203,4
M2,200,16,8,3,0.308314,5
```

### Validation Features

✅ Correct number of parameters (4 required)  
✅ File existence check  
✅ Minimum 3 columns validation  
✅ Numeric values verification  
✅ Matching weights, impacts, and criteria count  
✅ Valid impact symbols (+ or -)  
✅ Proper error messages for all cases  

---

## 📦 Part II: PyPI Package

### Package Structure

```
topsis-package/
├── topsis_YourName_RollNo/
│   ├── __init__.py
│   └── topsis.py
├── setup.py
├── pyproject.toml
├── README.md
├── LICENSE
```

### Package Naming Convention

```
Topsis-FirstName-RollNumber
```

**Example**: `Topsis-Anshul-102303930`

### Building the Package

```bash
# Install build tools
pip install build twine

# Build package
python -m build

# Upload to PyPI
twine upload dist/*
```

### Installation from PyPI

```bash
pip install Topsis-YourName-RollNo
```

### Usage After Installation

```bash
# Command line
topsis data.csv "1,1,1,2" "+,+,-,+" output.csv

# Or in Python
from topsis_YourName_RollNo import topsis
topsis.calculate('data.csv', '1,1,1,2', '+,+,-,+', 'output.csv')
```

### setup.py Template

```python
from setuptools import setup, find_packages

setup(
    name='Topsis-YourName-RollNo',
    version='1.0.0',
    description='TOPSIS implementation for multi-criteria decision making',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    license='MIT',
    packages=find_packages(),
    install_requires=['pandas', 'numpy'],
    entry_points={
        'console_scripts': [
            'topsis=topsis_YourName_RollNo.topsis:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
```

---

## 🌐 Part III: Web Service (Streamlit)

### Features

🎨 **Modern UI Design**
- Glassmorphism aesthetic with gradient background
- Responsive layout optimized for all devices
- Interactive form validation

📧 **Email Integration**
- Automatic result delivery to user's email
- Professional email template with summary
- CSV attachment with complete results

📊 **Data Processing**
- Real-time TOPSIS calculation
- Interactive results display
- Download button for immediate access

✅ **Input Validation**
- Email format verification
- Weights and impacts count matching
- CSV structure validation
- Numeric data type checking

### Streamlit Application Setup

#### Installation

```bash
pip install streamlit pandas numpy
```

#### Configuration

Create `.streamlit/secrets.toml`:

```toml
SENDER_EMAIL = "your.email@gmail.com"
APP_PASSWORD = "your_16_digit_app_password"
```

**Getting Gmail App Password:**
1. Go to [Google Account Settings](https://myaccount.google.com/)
2. Enable 2-Step Verification
3. Go to App Passwords
4. Generate password for "Mail"
5. Copy 16-digit password to secrets.toml

#### Running Locally

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

#### Deployment Options

**Streamlit Cloud (Recommended)**
1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io/)
3. Connect repository
4. Add secrets in dashboard (Settings → Secrets)
5. Deploy

**Heroku**
```bash
# Create Procfile
web: streamlit run app.py --server.port=$PORT

# Deploy
heroku create your-app-name
git push heroku main
```

**Railway.app**
1. Connect GitHub repository
2. Add environment variables
3. Deploy automatically

### Web Interface Usage

1. **Upload CSV File**
   - Click "Upload CSV File" button
   - Select your decision matrix file
   - Must have minimum 3 columns

2. **Enter Weights**
   - Comma-separated values
   - Example: `1,1,1,2` or `0.25,0.25,0.25,0.25`
   - Count must match criteria columns

3. **Enter Impacts**
   - Use `+` for beneficial criteria (higher is better)
   - Use `-` for cost criteria (lower is better)
   - Example: `+,+,-,+`
   - Count must match criteria columns

4. **Provide Email**
   - Enter valid email address
   - Results will be sent here
   - Also available for immediate download

5. **Generate Results**
   - Click "Generate TOPSIS Results"
   - View results in interactive table
   - Download CSV or receive via email

### Email Template

The application sends a professional email with:
- Summary of analysis
- Total alternatives evaluated
- Top-ranked alternative with score
- Attached CSV file with complete results

---

## 🔗 Project Links

- **PyPI Package**: [https://pypi.org/project/Topsis-YourName-RollNo/](https://pypi.org/project/Topsis-YourName-RollNo/)
- **GitHub Repository**: [https://github.com/yourusername/topsis-project](https://github.com/yourusername/topsis-project)
- **Web Application**: [https://your-app.streamlit.app](https://your-app.streamlit.app)
- **Documentation**: [Project Wiki or Docs Link]

---

## 📚 References

### Academic Resources
- Hwang, C.L.; Yoon, K. (1981). "Multiple Attribute Decision Making: Methods and Applications"
- [TOPSIS Wikipedia](https://en.wikipedia.org/wiki/TOPSIS)
- [TOPSIS Tutorial - GeeksforGeeks](https://www.geeksforgeeks.org/topsis-method-for-multiple-criteria-decision-making/)

### Technical Resources
- [Python Packaging Guide](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [PyPI Publishing Tutorial](https://realpython.com/pypi-publish-python-package/)

---

## 📄 License

This project is licensed under the MIT License.

---

## 👤 Author

**Your Name**  
Roll Number: Your-Roll-Number  
Email: your.email@example.com  

---

<div align="center">

**Made with ❤️ for Academic Excellence**

⭐ If you find this helpful, please star the repository!

</div>
