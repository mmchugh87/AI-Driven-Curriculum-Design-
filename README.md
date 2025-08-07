# Indeed Job Scraper with Camoufox

A powerful web scraper for Indeed.com that uses Camoufox browser automation to bypass Cloudflare challenges and extract comprehensive job data.

## 🚀 Features

- **Cloudflare Bypass**: Automatic detection and solving of Cloudflare challenges
- **Cookie Consent Handling**: Automatically accepts cookie consent dialogs
- **Human-like Behavior**: Random delays and humanized browsing patterns
- **Comprehensive Data Extraction**: Title, Company, Location, Rating, Date, Salary, Description, and Links
- **Full Job Descriptions**: Optional detailed scraping from individual job pages
- **CSV Export**: Results saved in CSV format with timestamp
- **Command Line Support**: Configurable via command line arguments

## 📋 Prerequisites

### System Requirements
- Python 3.7 or higher
- Windows, macOS, or Linux
- Internet connection

### Required Libraries

The script requires several Python libraries. Install them using the following commands:

#### Core Dependencies
```bash
pip install pandas
pip install beautifulsoup4
pip install camoufox
pip install camoufox-captcha
```

#### Alternative Installation (all at once)
```bash
pip install pandas beautifulsoup4 camoufox camoufox-captcha
```

### Detailed Library Information

| Library | Purpose | Version |
|---------|---------|---------|
| `pandas` | Data manipulation and CSV export | Latest |
| `beautifulsoup4` | HTML parsing and data extraction | Latest |
| `camoufox` | Browser automation with anti-detection | Latest |
| `camoufox-captcha` | Automatic captcha solving | Latest |

## 🛠 Installation

1. **Clone or download the script:**
   ```bash
   git clone <repository-url>
   cd AI-Driven-Curriculum-Design-
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or install manually:
   ```bash
   pip install pandas beautifulsoup4 camoufox camoufox-captcha
   ```

3. **Verify installation:**
   ```bash
   python -c "import pandas, bs4, camoufox, camoufox_captcha; print('All dependencies installed successfully!')"
   ```

## 💻 Usage

### Basic Usage

Run the script with default settings:
```bash
python indeed_scraper_camoufox.py
```

**Default Configuration:**
- Position: "python analyst"
- Location: "remote"
- Max Jobs: 800
- Full Descriptions: Enabled

### Command Line Arguments

Customize the search parameters:
```bash
python indeed_scraper_camoufox.py "data scientist" "New York, NY" 500
```

**Parameters:**
1. **Position** (string): Job title or keywords
2. **Location** (string): City, state, zip code, or "remote"
3. **Max Jobs** (integer): Maximum number of jobs to scrape

### Advanced Examples

```bash
# Software engineering jobs in San Francisco (1000 jobs)
python indeed_scraper_camoufox.py "software engineer" "San Francisco, CA" 1000

# Remote marketing jobs (200 jobs)
python indeed_scraper_camoufox.py "marketing manager" "remote" 200

# Data analyst jobs in specific zip code
python indeed_scraper_camoufox.py "data analyst" "10001" 300
```

## ⚙️ Configuration

### Script Configuration

Edit the default values at the top of the script:

```python
# Configuration
DEFAULT_POSITION = "python analyst"
DEFAULT_LOCATION = "remote"
DEFAULT_MAX_JOBS = 800
DEFAULT_DELAY_MIN = 3
DEFAULT_DELAY_MAX = 8
```

### Browser Settings

Modify browser behavior:

```python
browser_options = {
    'headless': False,  # Set to True for headless mode
    'humanize': True,   # Enable human-like behavior
    'geoip': True,      # Use realistic geolocation
    'i_know_what_im_doing': True,
    'config': {'forceScopeAccess': True},
    'disable_coop': True
}
```

### Full Description Scraping

To disable full description scraping (faster execution):

```python
# In the main() function, change:
scrape_full_descriptions=False
```

## 📊 Output

### File Naming Convention
Results are saved as: `YYYY-MM-DD_HH-MM_position_location.csv`

**Example:** `2025-08-07_14-30_python analyst_remote.csv`

### Data Fields

| Column | Description | Example |
|--------|-------------|---------|
| Title | Job title | "Senior Python Developer" |
| Company | Company name | "Tech Corp Inc." |
| Location | Job location | "San Francisco, CA" |
| Rating | Company rating | "4.2" |
| Date | Posted date | "2 days ago" |
| Salary | Salary range | "$80,000 - $120,000" |
| Description | Job snippet | "We are looking for..." |
| Links | Job URL | "https://indeed.com/job/..." |

## 🔧 Troubleshooting

### Common Issues

#### 1. **ImportError: No module named 'camoufox'**
```bash
pip install camoufox camoufox-captcha
```

#### 2. **Cloudflare Challenge Not Resolving**
- The script will attempt automatic solving
- If it fails, manual intervention will be required
- Follow the on-screen prompts

#### 3. **No Jobs Found**
- Check if the search terms are valid
- Verify Indeed.com is accessible
- Try different search parameters

#### 4. **Browser Won't Start**
- Ensure Camoufox is properly installed
- Try running in headless mode by setting `headless=True`

### Performance Tips

1. **Reduce job count** for faster testing:
   ```bash
   python indeed_scraper_camoufox.py "data scientist" "remote" 50
   ```

2. **Disable full descriptions** for faster scraping:
   ```python
   scrape_full_descriptions=False
   ```

3. **Use headless mode** on servers:
   ```python
   'headless': True
   ```

## 📝 Example Output

```
================================================================================
================================================================================
||                                                                            ||
||                          INDEED JOB SCRAPER                              ||
||                                                                            ||
||                  Advanced Cloudflare Bypass System                       ||
||                                                                            ||
||               Powered by Camoufox Browser Automation                     ||
||                                                                            ||
================================================================================
================================================================================

Initializing Indeed scraping system...
Loading Cloudflare bypass modules...
Preparing data collection...

Starting Indeed scrape for: 'python analyst' in 'remote'
Target: 800 jobs
============================================================
Browser initialized with Camoufox + Captcha Solver
Starting URL: https://www.indeed.com/jobs?q=python+analyst&l=remote

Page 1 - Loading: https://www.indeed.com/jobs?q=python+analyst&l=remote&start=0
Found 15 job elements
Job number    1 added - Python Data Analyst
Job number    2 added - Senior Python Developer
...
```

## 🔒 Security & Ethics

### Responsible Scraping
- The script includes delays to avoid overwhelming Indeed's servers
- Respects robots.txt guidelines
- Uses human-like browsing patterns

### Data Privacy
- Only scrapes publicly available job postings
- No personal information is collected
- Results are stored locally

## 📄 License

This script is for educational and research purposes. Please ensure compliance with Indeed.com's Terms of Service and applicable laws in your jurisdiction.

## 🐛 Known Issues

1. **Rate Limiting**: Indeed may temporarily block requests if too many are made too quickly
2. **Page Structure Changes**: Indeed occasionally updates their HTML structure
3. **Cloudflare Updates**: New Cloudflare challenges may require script updates

## 🔄 Updates

Check for updates regularly as Indeed.com frequently changes their anti-bot measures. The script may need periodic updates to maintain functionality.

---

**Last Updated:** August 7, 2025  
**Version:** 1.0  
**Compatibility:** Indeed.com (Current)
