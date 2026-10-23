console.log("Vite development server initialized successfully for RAG Technology Lab.");

const appElement = document.getElementById("app");
if (appElement) {
  appElement.innerHTML = `
    <div style="font-family: sans-serif; padding: 30px; max-width: 600px;">
      <h1 style="color: #2563eb;">⚡ Vite Development Environment</h1>
      <p style="color: #475569;">
        Fast HMR (Hot Module Replacement) and ESM bundler for RAG frontend applications.
      </p>
      <div style="background: #f1f5f9; padding: 15px; border-radius: 8px;">
        <strong>Features Verified:</strong>
        <ul>
          <li>Native ES Modules serving</li>
          <li>TypeScript compilation</li>
          <li>Zero-bundle dev server startup</li>
        </ul>
      </div>
    </div>
  `;
}
