# Bharat Stock Picks (PWA)

## यह starter क्या करता है
- मोबाइल पर install होने वाली PWA वेबसाइट
- पाँच strategy tabs
- GitHub Actions से सोमवार-शुक्रवार 4:15 PM IST पर scan
- परिणाम `data/picks.json` में प्रकाशित

## जरूरी सीमाएँ
- अभी `universe.json` में सीमित sample watchlists हैं, पूरी NSE सूची नहीं।
- Yahoo Finance/yfinance unofficial data access है; availability, accuracy, delay और redistribution rights की गारंटी नहीं। इसे execution/trading के लिए इस्तेमाल न करें।
- `Bharat Bargains` अभी वास्तविक valuation नहीं जाँचता; fundamental data जोड़ना बाकी है।
- Strategy score heuristic ranking है, AI prediction या guaranteed return नहीं।
- पहले workflow manually चलाकर logs और picks जाँचें।

## GitHub पर सेटअप (Android Chrome)
1. GitHub account बनाएँ/लॉगिन करें।
2. नया **Public** repository बनाएँ: `bharat-stock-picks`।
3. इस ZIP की सभी files और `.github/workflows/daily-scan.yml` सहित upload करें। GitHub mobile web में Add file → Upload files से कर सकते हैं; dot-folder न दिखे तो browser में Desktop site चुनें।
4. Repository → Actions → Daily NSE stock scan → Run workflow दबाएँ।
5. Settings → Pages → Build and deployment → Source में **GitHub Actions** चुनें।
6. Actions tab में `Daily NSE stock scan` workflow को Run workflow से चलाएँ। सफल होने पर साइट deploy होगी। कुछ मिनट बाद `https://YOUR-USERNAME.github.io/bharat-stock-picks/` खोलें।
7. Chrome menu → Add to Home screen / Install app चुनें।

## Free hosting / schedule
GitHub Pages public repos में उपलब्ध है; GitHub Actions public repos के standard runners free हैं। Scheduled jobs कभी-कभी delay हो सकते हैं, इसलिए exact 4:15 PM delivery की गारंटी नहीं।

## सुधारने से पहले
- universe.json में अपनी verified NSE symbol lists जोड़ें।
- Infra/sector classifications verify करें।
- Valuation strategy के लिए licensed/reliable fundamentals source जोड़ें।
- Backtest, survivorship-bias checks, transaction costs और corporate-action validation करें।
