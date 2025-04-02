<script>
  import { onMount } from "svelte";
  import ChatBot from "../../components/ChatBot.svelte";
  import PDFViewer from "../../components/PDFViewer.svelte";
  import { pdfUrl } from "../../lib/pdfStore.js";
  import { currentLanguage } from "../../lib/store.js";

  onMount(() => {
    pdfUrl.set(`http://localhost:8000/pdf_reports/latest_report.pdf?t=${Date.now()}`);
  });
</script>

<section class="auditai-container">
  <div class="chatbot-section">
    <ChatBot />

    <div class="language-selector">
      <label for="lang">🌐 Language:</label>
      <select id="lang" bind:value={$currentLanguage}>
        <option value="en">English</option>
        <option value="pt">Português</option>
        <option value="es">Español</option>
        <option value="fr">Français</option>
        <option value="de">Deutsch</option>
        <option value="it">Italiano</option>
      </select>
    </div>
  </div>

  <div class="pdf-section">
    <PDFViewer />
  </div>
</section>

<style>
.auditai-container {
  display: flex;
  width: 90%;
  max-width: 1400px;
  margin: 40px auto;
  background: white;
  padding: 25px;
  border-radius: 14px;
  box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.1);
  gap: 25px;
  justify-content: space-between;
  align-items: stretch;
}

.chatbot-section,
.pdf-section {
  flex: 1;
  min-width: 45%;
  max-width: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  background: #ffffff;
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.06);
  border-radius: 12px;
  transition: all 0.3s ease-in-out;
}

.pdf-section {
  border-left: 3px solid #e0e0e0;
}

@media screen and (max-width: 900px) {
  .auditai-container {
    flex-direction: column;
    align-items: center;
  }

  .chatbot-section,
  .pdf-section {
    width: 100%;
    min-width: unset;
    max-width: unset;
    border-left: none;
  }
}

.language-selector {
  align-self: flex-end;
  margin-top: 12px;
  font-size: 0.9rem;
}

.language-selector select {
  margin-left: 0.5rem;
  padding: 5px 10px;
  border-radius: 8px;
  border: 1px solid #ccc;
  background-color: #f1f5f9;
}
</style>
