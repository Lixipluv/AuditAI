

<script>
    let documentation = [
        { 
            title: "Introduction", 
            content: "Welcome to the AuditAI documentation. Here, you'll find everything you need to know about using the platform.",
            icon: "📘"
        },
        { 
            title: "How It Works", 
            content: "AuditAI analyzes smart contracts using Slither, providing detailed reports on vulnerabilities and security risks.",
            icon: "🛡️"
        },
        { 
            title: "Report Exporting", 
            content: "Reports can be exported in JSON or PDF format, giving users flexibility in how they manage their audit results.",
            icon: "📑"
        },
        { 
            title: "Support & Contact", 
            content: "Have questions? Visit our GitHub repository to contribute, review the code, or get support.",
            icon: "💬"
        }
    ];
</script>

<section class="documentation-container">
    <h1>📖 <span>AuditAI Documentation</span></h1>
    <div class="doc-grid">
        {#each documentation as section}
            <div class="doc-section">
                <h2>{section.icon} {section.title}</h2>
                <p>{section.content}</p>
            </div>
        {/each}
    </div>
    
    <div class="github-section">
        <p>🔗 Want to contribute or learn more?</p>
        <a href="https://github.com/Lixipluv/AuditAI" target="_blank" class="github-button">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="white" viewBox="0 0 24 24">
                <path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.302 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577v-2.256c-3.338.726-4.033-1.416-4.033-1.416-.546-1.386-1.333-1.755-1.333-1.755-1.089-.744.083-.729.083-.729 1.205.084 1.839 1.24 1.839 1.24 1.07 1.835 2.807 1.304 3.49.997.108-.776.42-1.305.763-1.605-2.665-.303-5.466-1.332-5.466-5.93 0-1.31.467-2.38 1.235-3.22-.135-.303-.54-1.524.105-3.176 0 0 1.005-.322 3.3 1.23a11.52 11.52 0 0 1 3-.403c1.02.005 2.045.137 3 .403 2.295-1.552 3.3-1.23 3.3-1.23.645 1.652.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.435.372.825 1.105.825 2.23v3.317c0 .322.21.698.825.58C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/>
            </svg>
            Visit GitHub
        </a>
    </div>
</section>

<style>
    :root {
        --primary-color: #3C91E6;
        --background-light: #f9f9f9;
        --text-dark: #1f4568;
        --text-light: #444;
        --card-bg: white;
        --card-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }

    .documentation-container {
        max-width: 950px;
        margin: 50px auto;
        padding: 20px;
        font-family: 'Inter', sans-serif;
        text-align: center;
    }

    h1 {
        color: var(--primary-color);
        font-size: 2.4rem;
        margin-bottom: 25px;
        font-weight: bold;
    }

    .doc-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 20px;
        margin-bottom: 30px;
    }

    .doc-section {
        padding: 20px;
        border-radius: 12px;
        background: var(--card-bg);
        box-shadow: var(--card-shadow);
        transition: transform 0.2s, box-shadow 0.2s;
    }

    .doc-section:hover {
        transform: translateY(-6px);
        box-shadow: 0 6px 14px rgba(0, 0, 0, 0.15);
    }

    h2 {
        margin-bottom: 10px;
        color: var(--text-dark);
        font-size: 1.5rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
    }

    p {
        color: var(--text-light);
        font-size: 1rem;
        line-height: 1.6;
    }

    .github-section {
        margin-top: 30px;
        padding: 15px;
        border-radius: 10px;
        background: var(--background-light);
        display: inline-block;
        text-align: center;
    }

    .github-button {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        padding: 12px 20px;
        background: var(--primary-color);
        color: white;
        font-weight: bold;
        text-decoration: none;
        border-radius: 8px;
        transition: background 0.2s, transform 0.2s;
        border: none;
    }

    .github-button svg {
        fill: white;
    }

    .github-button:hover {
        background: #2a7fc2;
        transform: scale(1.05);
    }
</style>
