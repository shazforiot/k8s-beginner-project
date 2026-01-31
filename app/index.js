const http = require('http');
const os = require('os');

const PORT = process.env.PORT || 3000;
const APP_NAME = process.env.APP_NAME || 'K8s Demo App';
const APP_VERSION = process.env.APP_VERSION || '1.0.0';

const server = http.createServer((req, res) => {
    if (req.url === '/health') {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ status: 'healthy', timestamp: new Date().toISOString() }));
        return;
    }

    if (req.url === '/ready') {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ status: 'ready' }));
        return;
    }

    if (req.url === '/info') {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({
            app: APP_NAME,
            version: APP_VERSION,
            hostname: os.hostname(),
            platform: os.platform(),
            uptime: process.uptime(),
            memory: process.memoryUsage(),
            timestamp: new Date().toISOString()
        }));
        return;
    }

    // Main page
    res.writeHead(200, { 'Content-Type': 'text/html' });
    res.end(`
<!DOCTYPE html>
<html>
<head>
    <title>${APP_NAME}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #1a1a2e, #16213e);
            color: #fff;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container {
            text-align: center;
            padding: 40px;
            background: rgba(50, 108, 229, 0.1);
            border-radius: 20px;
            border: 2px solid #326ce5;
            max-width: 600px;
        }
        .logo { font-size: 4rem; margin-bottom: 20px; }
        h1 { color: #326ce5; margin-bottom: 10px; }
        .version { color: #7ee787; margin-bottom: 30px; }
        .info {
            background: #0d1117;
            padding: 20px;
            border-radius: 10px;
            text-align: left;
            margin-top: 20px;
        }
        .info p { margin: 10px 0; color: #a8dadc; }
        .info span { color: #54a3ff; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">☸️</div>
        <h1>${APP_NAME}</h1>
        <p class="version">Version: ${APP_VERSION}</p>
        <p>Running on Kubernetes!</p>
        <div class="info">
            <p><span>Hostname:</span> ${os.hostname()}</p>
            <p><span>Platform:</span> ${os.platform()}</p>
            <p><span>Node Version:</span> ${process.version}</p>
            <p><span>Uptime:</span> ${Math.floor(process.uptime())}s</p>
        </div>
    </div>
</body>
</html>
    `);
});

server.listen(PORT, () => {
    console.log(`🚀 ${APP_NAME} v${APP_VERSION} running on port ${PORT}`);
    console.log(`   Health check: http://localhost:${PORT}/health`);
    console.log(`   Readiness:    http://localhost:${PORT}/ready`);
    console.log(`   Info:         http://localhost:${PORT}/info`);
});

// Graceful shutdown
process.on('SIGTERM', () => {
    console.log('SIGTERM received, shutting down gracefully...');
    server.close(() => {
        console.log('Server closed');
        process.exit(0);
    });
});
