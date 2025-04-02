<script>
  import { onMount } from "svelte";
  import { writable, get } from "svelte/store";
  import {
    analyzeText,
    generatePDF,
    getLatestSlitherReport,
    customizeReport,
    regeneratePdf,
    updateReportViaChat
  } from "../lib/api.js";
  import { pdfUrl, updatePdfUrl } from "../lib/pdfStore.js";
  import { currentLanguage } from "../lib/store.js";

  let messages = [
    {
      text: `🤖 Hello! I'm AuditAI, your smart contract auditing assistant.\n\nTry things like:\n• Translate the report to English\n• Improve the description of vulnerabilities\n• Add recommendations for each issue\n• Change the severity level to High`,
      from: "bot"
    }
  ];

  let userMessage = "";
  let botTyping = false;
  let chatContainer;

  const reportContent = writable("");
  const userLevel = "medium";
  const author = "AuditAI";

  function sanitizeText(text) {
    if (typeof text === "object") return JSON.stringify(text, null, 2);
    return text.replace(/<[^>]+>/g, "").replace(/\*\*(.*?)\*\*/g, "$1").replace(/\\n/g, "\n").trim();
  }

  async function sendMessage() {
    if (!userMessage.trim()) return;

    messages = [...messages, { text: userMessage, from: "user" }];
    const messageToSend = userMessage;
    userMessage = "";
    botTyping = true;

    try {
      const lang = get(currentLanguage);
      const response = await analyzeText(messageToSend, "report", lang, userLevel, author);

      let summary = "";
      let instructions = null;

      if (typeof response === "object") {
        summary = sanitizeText(response?.summary || JSON.stringify(response));
        instructions = response?.instructions || null;
      } else {
        summary = sanitizeText(response);
      }

      reportContent.set(summary);
      messages = [...messages, { text: summary, from: "bot" }];

      const isHTML = summary.trim().startsWith("<h") || summary.includes("<html");

      if (instructions && Array.isArray(instructions)) {
        await customizeReport(instructions);
        await regeneratePdf();
        updatePdfUrl(`latest_report.pdf?t=${Date.now()}`);

        messages = [...messages, {
          text: "✅ PDF atualizado com base nas instruções personalizadas.",
          from: "bot"
        }];
      } else if (isHTML) {
        messages = [...messages, {
          text: "📄 Visualização do conteúdo que será inserido no PDF:",
          from: "bot"
        }, {
          text: summary,
          from: "bot"
        }];

        await updateReportViaChat(messageToSend);
        updatePdfUrl(`latest_report.pdf?t=${Date.now()}`);

        messages = [...messages, {
          text: "✅ PDF atualizado com sucesso.",
          from: "bot"
        }];
      } else {
        await updateReportViaChat(`<h2>Relatório</h2><p>${summary}</p>`);
        updatePdfUrl(`latest_report.pdf?t=${Date.now()}`);

        messages = [...messages, {
          text: "✅ PDF atualizado com base no conteúdo textual fornecido.",
          from: "bot"
        }];
      }
    } catch (error) {
      console.error("Erro ao conectar com a IA:", error);
      messages = [...messages, { text: "❌ Erro ao conectar com a IA. Verifique sua conexão ou tente novamente mais tarde.", from: "bot" }];
    } finally {
      botTyping = false;
      scrollToBottom();
    }
  }

  async function updatePDF() {
    try {
      const response = await getLatestSlitherReport();
      const data = response?.report || [];

      if (!data.length) {
        alert("No report data found.");
        return;
      }

      await generatePDF(data);
      updatePdfUrl(`latest_report.pdf?t=${Date.now()}`);
    } catch (error) {
      console.error("Error generating PDF:", error);
    }
  }

  function scrollToBottom() {
    setTimeout(() => {
      chatContainer?.scrollTo({ top: chatContainer.scrollHeight, behavior: "smooth" });
    }, 100);
  }

  onMount(async () => {
    try {
      const report = await getLatestSlitherReport();
      if (report?.report?.length > 0) {
        reportContent.set("Report loaded. Ready for customization.");
        pdfUrl.set(`http://localhost:8000/pdf_reports/latest_report.pdf?t=${Date.now()}`);
      } else {
        reportContent.set("No report data found.");
      }
    } catch (e) {
      reportContent.set("Error loading report.");
      console.error("Failed to fetch report:", e);
    }
  });
</script>

<style>
.chat-wrapper {
  max-width: 700px;
  margin: 0 auto;
  padding: 1rem;
}

.chat-box {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  max-height: 700px;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  animation: fadeIn 0.25s ease-in-out;
}

.chat-message {
  display: flex;
  align-items: flex-end;
  margin-bottom: 1rem;
}

.chat-bubble {
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s ease, opacity 0.2s ease;
  animation: fadeInUp 0.25s ease-in-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(5px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.bot-bubble {
  background-color: #e2e8f0;
  color: #1e293b;
  border-bottom-left-radius: 0;
  margin-left: 10px;
  padding: 12px 16px;
  border-radius: 18px;
}

.user-bubble {
  background-color: #3b82f6;
  color: white;
  border-bottom-right-radius: 0;
  margin-right: 10px;
  padding: 12px 16px;
  border-radius: 18px;
}

.avatar {
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
  border: 2px solid white;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  margin: 0 0.5rem;
}

.input-area {
  display: flex;
  align-items: center;
  border: 1px solid #ccc;
  background: #f1f5f9;
  border-radius: 999px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
  padding: 10px 16px;
  margin-top: 12px;
}

.input-area input {
  padding: 10px;
  font-size: 1rem;
  flex: 1;
  border: none;
  background: transparent;
  outline: none;
}

.send-btn {
  background-color: #2563eb;
  border: none;
  color: white;
  border-radius: 999px;
  padding: 8px;
  width: 40px;
  height: 40px;
  display: grid;
  place-items: center;
  transition: background-color 0.2s;
}

.send-btn:hover {
  background-color: #1e40af;
}

.update-pdf-btn {
  margin-top: 16px;
  align-self: flex-start;
  background-color: #10b981;
  color: white;
  padding: 10px 18px;
  border-radius: 999px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: background-color 0.2s;
  border: none;
}

.update-pdf-btn:hover {
  background-color: #059669;
}
</style>

<div class="chat-wrapper" bind:this={chatContainer}>
  <h2 class="text-2xl font-semibold mb-4">Chatbot AuditAI</h2>

  <div class="chat-box">
    {#each messages as msg}
      <div class="chat-message" style="justify-content: {msg.from === 'user' ? 'flex-end' : 'flex-start'}">
        {#if msg.from === 'bot'}
          <img class="avatar" src="https://cdn.icon-icons.com/icons2/1371/PNG/512/robot02_90810.png" alt="Bot Avatar" />
        {/if}

        <div class="chat-bubble {msg.from === 'bot' ? 'bot-bubble' : 'user-bubble'}">
          {msg.text}
        </div>

        {#if msg.from === 'user'}
          <img class="avatar" src="https://cdn-icons-png.flaticon.com/512/847/847969.png" alt="User Avatar" />
        {/if}
      </div>
    {/each}

    {#if botTyping}
      <div class="chat-message" style="justify-content: flex-start">
        <img class="avatar" src="https://cdn.icon-icons.com/icons2/1371/PNG/512/robot02_90810.png" alt="Bot Avatar" />
        <div class="chat-bubble bot-bubble italic text-gray-500 animate-pulse">
          AuditAI está digitando...
        </div>
      </div>
    {/if}
  </div>

  <div class="input-area">
    <input
      type="text"
      placeholder="Digite sua mensagem..."
      bind:value={userMessage}
      on:keydown={(e) => e.key === "Enter" && sendMessage()}
    />
    <button class="send-btn" on:click={sendMessage}>
      <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12h14m0 0l-6-6m6 6l-6 6" />
      </svg>
    </button>
  </div>

  <button class="update-pdf-btn" on:click={updatePDF}>
    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
    </svg>
    Atualizar Preview do PDF
  </button>
</div>
