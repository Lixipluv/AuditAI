<script>
  import { createEventDispatcher, onMount } from "svelte";
  import { slitherAnalysis } from "../lib/api.js";
  import { vulnerabilities } from "../lib/vulnerabilityStore.js";
  import { writable, get } from "svelte/store";

  const dispatch = createEventDispatcher();

  let dropzoneContainer;
  let fileInput;

  let uploadedFiles = writable([]);
  let dropMessage = writable("Arraste e solte seu contrato aqui ou clique para selecionar");
  let uploadStatus = writable("");
  let isUploading = writable(false);

  function handleFileSelect(event) {
    const files = event.target.files || event.dataTransfer.files;
    if (!files.length) return;

    const allowedExtensions = [".sol"];
    const validFiles = Array.from(files).filter(file =>
      allowedExtensions.includes(file.name.slice(file.name.lastIndexOf(".")).toLowerCase())
    );

    if (!validFiles.length) {
      uploadStatus.set("⚠️ Arquivo inválido. Apenas arquivos .sol são permitidos.");
      return;
    }

    // Permitindo apenas um arquivo por vez
    uploadedFiles.set([validFiles[0]]);
    dropMessage.set(`✅ Arquivo "${validFiles[0].name}" adicionado. Clique para substituir.`);
    dispatch("fileAdded", validFiles[0]);
  }

  async function uploadFiles() {
  const files = get(uploadedFiles);
  if (!files.length) {
    uploadStatus.set("Nenhum arquivo para enviar.");
    return;
  }

  isUploading.set(true);
  uploadStatus.set("📤 Analisando contrato com Slither...");

  const file = files[0];

  try {
    const result = await slitherAnalysis(file);
    uploadStatus.set(`✅ Análise concluída para ${file.name}.`);

    let formattedReport = [];

    if (Array.isArray(result.formatted_report)) {
      formattedReport = result.formatted_report;
    } else if (Array.isArray(result.structured_data)) {
      formattedReport = result.structured_data;
    } else {
      throw new Error("Formato do relatório inválido recebido da API");
    }

    const counts = { critical: 0, high: 0, medium: 0, low: 0, unknown: 0 };
    formattedReport.forEach(vuln => {
      const severity = vuln.impact.toLowerCase();
      counts[severity] = (counts[severity] || 0) + 1;
    });

    vulnerabilities.set([
      { title: "Critical", value: counts.critical, severity: "critical" },
      { title: "High", value: counts.high, severity: "high" },
      { title: "Medium", value: counts.medium, severity: "medium" },
      { title: "Low", value: counts.low, severity: "low" },
      { title: "Unknown", value: counts.unknown, severity: "unknown" }
    ]);

    dispatch("analysisComplete", result);

  } catch (error) {
    uploadStatus.set(`❌ Erro na análise do Slither: ${error.message}`);
    console.error(error);
  }

  isUploading.set(false);
}


  function removeFile(file) {
    uploadedFiles.set([]);
    dispatch("fileRemoved", file);
    dropMessage.set("Arraste e solte seu contrato aqui ou clique para selecionar");
  }

  function triggerFileInput() {
    fileInput.click();
  }

  onMount(() => {
    dropzoneContainer.addEventListener("dragover", (e) => {
      e.preventDefault();
      dropzoneContainer.classList.add("active");
    });

    dropzoneContainer.addEventListener("dragleave", () => {
      dropzoneContainer.classList.remove("active");
    });

    dropzoneContainer.addEventListener("drop", (e) => {
      e.preventDefault();
      dropzoneContainer.classList.remove("active");
      handleFileSelect(e);
    });
  });
</script>

<div class="dropzone-wrapper" bind:this={dropzoneContainer}>
  <div class="dropzone" role="button" tabindex="0" on:click={triggerFileInput} on:keydown={(e) => (e.key === 'Enter' || e.key === ' ') && triggerFileInput()}>

    <svg class="drop-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 15a4 4 0 004 4h10a4 4 0 004-4m-4-7l-4-4m0 0L8 8m4-4v12" />
    </svg>
    <p>{$dropMessage}</p>
    <input bind:this={fileInput} type="file" accept=".sol" on:change={handleFileSelect} hidden />
    <button class="select-btn">Selecionar Arquivo</button>
  </div>

  {#if $uploadedFiles.length > 0}
    <div class="file-preview">
      {#each $uploadedFiles as file}
        <div class="file-item">
          <span class="file-name">{file.name}</span>
          <button class="remove-btn" on:click={() => removeFile(file)}>✖</button>
        </div>
      {/each}
    </div>
  {/if}

  {#if $uploadStatus}
    <p class="upload-status">{$uploadStatus}</p>
  {/if}
</div>

<style>
.dropzone-wrapper {
  width: 100%;
  max-width: 650px;
  margin: auto;
  background: white;
  border: 2px dashed #cbd5e1;
  border-radius: 16px;
  padding: 30px;
  text-align: center;
  transition: border-color 0.3s ease;
}

.dropzone-wrapper.active {
  border-color: #2563eb;
}

.dropzone {
  cursor: pointer;
}

.drop-icon {
  width: 40px;
  height: 40px;
  margin: 0 auto 10px;
  color: #2563eb;
  opacity: 0.7;
}

.select-btn,
.upload-btn {
  margin-top: 14px;
  padding: 10px 22px;
  border: none;
  border-radius: 999px;
  font-weight: 600;
  color: white;
  background-color: #2563eb;
  cursor: pointer;
  transition: background-color 0.2s;
}

.select-btn:hover,
.upload-btn:hover {
  background-color: #1e40af;
}

.file-preview {
  margin-top: 20px;
  text-align: left;
}

.file-item {
  display: flex;
  justify-content: space-between;
  background: #f1f5f9;
  padding: 10px 14px;
  border-radius: 10px;
  margin-bottom: 8px;
}

.file-name {
  font-size: 0.95rem;
  color: #334155;
}

.remove-btn {
  background: none;
  border: none;
  color: red;
  font-size: 1.1rem;
  cursor: pointer;
}

.upload-status {
  margin-top: 18px;
  font-size: 0.95rem;
  font-weight: 500;
  color: #475569;
}
</style>
