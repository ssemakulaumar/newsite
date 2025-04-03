const express = require('express');
const bodyParser = require('body-parser');
const { exec } = require('child_process');
const app = express();
const port = 3000;

app.use(express.static('public'));
app.use(bodyParser.json());

app.post('/scrape', (req, res) => {
    const { url } = req.body;
    if (!url) {
        return res.json({ message: 'No URL provided' });
    }
    
    // Run the Python scraping script
    exec(`python3 scraper.py "${url}"`, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error: ${error.message}`);
            return res.json({ message: 'Scraping failed' });
        }
        if (stderr) {
            console.error(`Stderr: ${stderr}`);
            return res.json({ message: 'Scraping encountered issues' });
        }
        console.log(`Stdout: ${stdout}`);
        res.json({ message: 'Scraping completed successfully' });
    });
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
