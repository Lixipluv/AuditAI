<script>
  import { pdfUrl } from "../lib/pdfStore.js";
</script>

<div class="pdf-viewer-wrapper">
  <div class="pdf-box">
    <iframe
      src={$pdfUrl}
      title="Pré-visualização do Relatório AuditAI"
      class="pdf-frame"
    ></iframe>

    <a class="download-btn" href={$pdfUrl} download="audit_report.pdf">
      Baixar Relatório
    </a>
  </div>
</div>

<style>
.pdf-viewer-wrapper {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: flex-start;
}

.pdf-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  max-height: 85vh;
  padding: 16px;
  border-radius: 16px;
  background: #ffffff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
}

.pdf-frame {
  width: 100%;
  height: 70vh;
  border: none;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  margin-bottom: 20px;
}

.download-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 18px;
  border-radius: 999px;
  background-color: #10b981;
  color: white;
  text-decoration: none;
  font-weight: 600;
  font-size: 0.95rem;
  transition: background-color 0.2s ease;
}

.download-btn:hover {
  background-color: #059669;
}
</style>
