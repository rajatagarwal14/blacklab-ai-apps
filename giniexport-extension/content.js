// GiniExport - KW CRM Opportunity Exporter
// Powered by Gini AI

(function() {
    'use strict';

    let allData = [];

    function delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    function updateProgress(msg) {
        console.log(`[GiniExport] ${msg}`);
        const statusDiv = document.getElementById('gini-export-status');
        if (statusDiv) {
            statusDiv.textContent = msg;
        }
    }

    async function setMaxPageSize() {
        const dropdown = document.querySelector('select[aria-label*="rows per page"]');
        if (dropdown) {
            dropdown.value = '100';
            dropdown.dispatchEvent(new Event('change', { bubbles: true }));
            await delay(2000);
        }
    }

    function getNextButton() {
        const buttons = Array.from(document.querySelectorAll('button'));
        return buttons.find(btn => {
            const aria = btn.getAttribute('aria-label');
            return aria && aria.toLowerCase().includes('next');
        });
    }

    function scrapeCurrentPage() {
        return new Promise((resolve) => {
            setTimeout(() => {
                const rows = document.querySelectorAll('tr[data-row-key]');
                if (!rows.length) {
                    resolve(false);
                    return;
                }

                rows.forEach(row => {
                    const cells = row.querySelectorAll('td');
                    if (cells.length > 0) {
                        const rowData = {};
                        cells.forEach((cell, idx) => {
                            const header = document.querySelectorAll('th')[idx];
                            const colName = header ? header.textContent.trim() : `Column_${idx}`;
                            rowData[colName] = cell.textContent.trim();
                        });
                        allData.push(rowData);
                    }
                });

                resolve(true);
            }, 1000);
        });
    }

    function downloadCSV(data) {
        if (!data.length) return;

        const headers = Object.keys(data[0]);
        let csv = headers.join(',') + '\\n';

        data.forEach(row => {
            const values = headers.map(header => {
                const val = row[header] || '';
                return `"${val.replace(/"/g, '""')}"`;
            });
            csv += values.join(',') + '\\n';
        });

        const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement('a');
        const url = URL.createObjectURL(blob);
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        
        link.setAttribute('href', url);
        link.setAttribute('download', `GiniExport_KW_Opportunities_${timestamp}.csv`);
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

        updateProgress(`✅ Export complete! ${data.length} records downloaded.`);
    }

    function insertExportButton() {
        const tabBarContainer = document.querySelector('div.sc-dAlyuH.kCTpGr');
        if (!tabBarContainer || document.querySelector('#gini-export-btn')) return;

        // Create button container
        const btnContainer = document.createElement('div');
        btnContainer.style.marginLeft = '15px';
        btnContainer.style.display = 'inline-block';

        // Create export button with icon
        const btn = document.createElement('button');
        btn.id = 'gini-export-btn';
        btn.title = 'Export All Opportunities (GiniExport)';
        btn.style.background = 'transparent';
        btn.style.border = 'none';
        btn.style.cursor = 'pointer';
        btn.style.display = 'inline-block';
        btn.style.verticalAlign = 'middle';
        btn.style.padding = '0';

        const img = document.createElement('img');
        img.src = 'https://dataextractor.sirv.com/Image.jpeg';
        img.alt = 'GiniExport';
        img.style.width = '26px';
        img.style.height = '26px';
        img.style.borderRadius = '6px';
        img.style.display = 'block';
        img.style.transition = 'transform 0.2s';

        btn.appendChild(img);
        btn.onmouseover = () => img.style.transform = 'scale(1.1)';
        btn.onmouseout = () => img.style.transform = 'scale(1)';
        btn.onclick = startScraping;

        // Create status display
        const statusDiv = document.createElement('div');
        statusDiv.id = 'gini-export-status';
        statusDiv.style.marginTop = '5px';
        statusDiv.style.fontSize = '12px';
        statusDiv.style.color = '#666';
        statusDiv.style.fontWeight = '500';

        btnContainer.appendChild(btn);
        btnContainer.appendChild(statusDiv);
        tabBarContainer.appendChild(btnContainer);

        console.log('[GiniExport] Export button injected successfully');
    }

    async function startScraping() {
        allData = [];
        updateProgress('⏳ Starting export...');
        
        try {
            await setMaxPageSize();
            let page = 1;
            
            while (true) {
                updateProgress(`📄 Scraping page ${page}...`);
                const ok = await scrapeCurrentPage();
                
                if (!ok) break;
                
                const nextBtn = getNextButton();
                if (!nextBtn) break;
                
                nextBtn.click();
                await delay(4000);
                page++;
            }

            if (allData.length) {
                updateProgress(`📦 Generating CSV for ${allData.length} records...`);
                await delay(500);
                downloadCSV(allData);
            } else {
                updateProgress('⚠️ No data found.');
            }
        } catch (error) {
            updateProgress(`❌ Error: ${error.message}`);
            console.error('[GiniExport] Error:', error);
        }
    }

    // Wait for page to load and inject button
    const interval = setInterval(() => {
        const container = document.querySelector('div.sc-dAlyuH.kCTpGr');
        if (container && !document.querySelector('#gini-export-btn')) {
            insertExportButton();
            clearInterval(interval);
        }
    }, 500);

    // Clear interval after 30 seconds to prevent infinite checking
    setTimeout(() => clearInterval(interval), 30000);

})();
