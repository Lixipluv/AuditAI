<script>
  import Dropzone from "../../components/Dropzone.svelte";
  import { uploadContract } from "../../lib/api.js";
  import { writable, get } from "svelte/store";
  import { updatePdfUrl } from "../../lib/pdfStore.js";
  import { vulnerabilities } from "../../lib/vulnerabilityStore.js";
  import ReportPreview from "../../components/ReportPreview.svelte";

  let uploadStatus = writable("");
  let isUploading = writable(false);
  let selectedSolcVersion = writable("0.8.23");
  let selectedFile = writable(null);
  let analysisResult = writable(null);

  function handleFileAdded(event) {
    selectedFile.set(event.detail);
    uploadStatus.set("File selected. Ready to analyze.");
    analysisResult.set(null);
  }

  async function sendFile() {
    const file = get(selectedFile);
    const solc_version = get(selectedSolcVersion);

    if (!file) {
      uploadStatus.set("No file selected.");
      return;
    }

    isUploading.set(true);
    uploadStatus.set("Uploading file and analyzing...");

    const formData = new FormData();
    formData.append("file", file);
    formData.append("solc_version", solc_version);

    try {
      const response = await uploadContract(formData);
      console.log("API Response:", response);

      let formattedReport;

      if (Array.isArray(response)) {
        formattedReport = response;
      } else if (response.formatted_report) {
        formattedReport = response.formatted_report;
      } else {
        throw new Error("Invalid response format");
      }

      analysisResult.set(formattedReport);
      uploadStatus.set("Analysis completed successfully.");

      if (response.pdf_url) {
        const filename = response.pdf_url.split("/").pop();
        updatePdfUrl(filename);
      }

      const severityCount = { critical: 0, high: 0, medium: 0, low: 0, unknown: 0 };
      formattedReport.forEach((vuln) => {
        const severity = vuln.impact?.toLowerCase() || "unknown";
        severityCount[severity] = (severityCount[severity] || 0) + 1;
      });

      vulnerabilities.set([
        { title: "Critical", value: severityCount.critical, severity: "critical" },
        { title: "High", value: severityCount.high, severity: "high" },
        { title: "Medium", value: severityCount.medium, severity: "medium" },
        { title: "Low", value: severityCount.low, severity: "low" },
        { title: "Unknown", value: severityCount.unknown, severity: "unknown" },
      ]);
    } catch (error) {
      uploadStatus.set(`Upload failed: ${error.message}`);
      analysisResult.set(null);
      console.error("Error during upload:", error);
    } finally {
      isUploading.set(false);
    }
  }

  function downloadJson() {
    const result = get(analysisResult);
    if (!result) return;

    const json = JSON.stringify(result, null, 2);
    const blob = new Blob([json], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = "auditai_analysis.json";
    anchor.click();
    URL.revokeObjectURL(url);
  }
</script>

<section class="auditai-container">
  <div class="left-section">
    <Dropzone on:fileAdded={handleFileAdded} />

    <div class="solc-version-selector">
      <label for="solc-version">Solidity Version:</label>
      <select bind:value={$selectedSolcVersion}>
        <option value="auto">Auto Detect</option>
        <option value="0.8.23">0.8.23</option>
        <option value="0.8.20">0.8.20</option>
        <option value="0.7.6">0.7.6</option>
      </select>
    </div>

    {#if $selectedFile}
      <div class="action-buttons">
        <button class="action-btn upload" on:click={sendFile} disabled={$isUploading}>
          {#if $isUploading}
            <span class="spinner"></span> Analyzing...
          {:else}
            Analyze
          {/if}
        </button>

        {#if $analysisResult}
          <button class="action-btn download" on:click={downloadJson}>
            Download JSON
          </button>
        {/if}
      </div>
    {/if}

    <p class="upload-status">{$uploadStatus}</p>
  </div>

  <div class="right-section">
    {#if $analysisResult}
      <div class="analysis-result">
        <h3 class="text-xl font-semibold text-green-700 mb-4">Analysis Report</h3>
        <ReportPreview reportData={$analysisResult} />
      </div>
    {/if}
  </div>
</section>
<style>
.auditai-container {
  display: flex;
  gap: 2rem;
  max-width: 1300px;
  margin: auto;
  background: #ffffff;
  padding: 30px;
  border-radius: 16px;
  box-shadow: 0 5px 20px rgba(0,0,0,0.06);
  flex-wrap: wrap;
  margin-top: 40px;
}

.left-section, .right-section {
  flex: 1;
  padding: 24px;
  background: #f9fafb;
  border-radius: 16px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.05);
}

.solc-version-selector {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-top: 1rem;
}

.solc-version-selector select {
  padding: 6px 12px;
  border-radius: 8px;
  border: 1px solid #ccc;
}

.action-buttons {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  margin-top: 1rem;
}

.action-btn {
  padding: 12px 24px;
  border-radius: 999px;
  color: white;
  cursor: pointer;
  border: none;
}

.upload { background: linear-gradient(to right, #3b82f6, #2563eb); }
.upload:hover { background: linear-gradient(to right, #2563eb, #1d4ed8); }

.download { background: linear-gradient(to right, #10b981, #059669); }
.download:hover { background: linear-gradient(to right, #059669, #047857); }

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid #fff;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

.upload-status {
  margin-top: 10px;
  color: #475569;
}

.analysis-result {
  background: #ffffff;
  padding: 20px;
  border-radius: 12px;
  overflow-y: auto;
  max-height: 500px;
}

.json-container {
  font-family: monospace;
  color: #1e293b;
}
</style>
