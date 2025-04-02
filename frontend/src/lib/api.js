import { writable } from "svelte/store";
import { vulnerabilities } from "./vulnerabilityStore.js";
export const pdfUrl = writable(""); // URL do PDF gerado

const BASE_URL = "http://localhost:8000";

/**
 * 📤 Upload de contrato para análise com Slither
 */
export async function uploadContract(formData) {
    try {
        const response = await fetch(`${BASE_URL}/analysis/slither`, {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`Erro HTTP ${response.status}: ${errorText}`);
        }

        const data = await response.json();

        if (!data.formatted_report) {
            console.error("❌ Erro: Slither não retornou um relatório formatado válido.");
            return { error: "Erro ao processar a análise." };
        }

        return data.formatted_report;

    } catch (error) {
        console.error("❌ Erro ao enviar contrato:", error);
        return { error: error.message };
    }
}

/**
 * 🧠 Envia texto para análise pela IA Groq (chatbot ou report)
 */
export async function analyzeText(text, mode = "chatbot", language = "pt", userLevel = "médio", author = "Desconhecido") {
    try {
      const payload = {
        text: text?.trim() || "Texto vazio.",
        mode,
        language,
        user_level: userLevel,
        author
      };
  
      const response = await fetch(`${BASE_URL}/chatbot/analyze/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
  
      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Erro HTTP ${response.status}: ${errorText}`);
      }
  
      const data = await response.json();
      const rawText = data?.response || "";
  
      let extractedInstructions = null;
      let summary = rawText;
  
      // 🧠 Se IA retornou objeto direto
      if (typeof rawText === "object" && rawText !== null) {
        return {
          summary: rawText.summary || JSON.stringify(rawText),
          instructions: rawText.instructions || null
        };
      }
  
      // 🧠 Se IA retornou JSON formatado dentro de string
      try {
        const match = rawText.match(/```json([\s\S]*?)```/);
        if (match) {
          const jsonStr = match[1].trim();
          extractedInstructions = JSON.parse(jsonStr);
        }
      } catch (parseErr) {
        console.warn("⚠️ Falha ao interpretar instruções JSON da IA:", parseErr);
      }
  
      return {
        summary: summary,
        instructions: extractedInstructions
      };
  
    } catch (error) {
      console.error("⚠️ Erro ao analisar texto:", error);
      return { summary: "Erro ao processar a solicitação.", instructions: null };
    }
  }
  

/**
 * 📜 Obter o relatório mais recente gerado pelo Slither
 */
export async function getLatestSlitherReport() {
    try {
        const response = await fetch(`${BASE_URL}/reports/latest`, {
            method: "GET",
            headers: { "Content-Type": "application/json" },
        });

        if (!response.ok) {
            throw new Error(`Erro HTTP ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();
        return data || null;
    } catch (error) {
        console.error("❌ Erro ao buscar o relatório:", error);
        return null;
    }
}

/**
 * 📄 Gerar PDF com base nos dados
 */
export async function generatePDF(vulnerabilitiesData) {
    const response = await fetch(`${BASE_URL}/pdf/generate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ vulnerabilities: vulnerabilitiesData }),
    });

    if (!response.ok) {
        throw new Error(`HTTP Error ${response.status}: ${await response.text()}`);
    }

    const data = await response.json();
    pdfUrl.set(data.pdf_url);
    return data.pdf_url;
}

/**
 * 📂 Buscar o PDF mais recente gerado
 */
export async function fetchGeneratedPDF() {
    try {
        const response = await fetch(`${BASE_URL}/pdf/latest`, {
            method: "GET",
        });

        if (!response.ok) {
            throw new Error(`Erro HTTP ${response.status}: ${await response.text()}`);
        }

        const data = await response.json();
        return data.pdf_url;
    } catch (error) {
        console.error("❌ Erro ao buscar PDF gerado:", error);
        return null;
    }
}

/**
 * ✏️ Atualiza o conteúdo do relatório com instruções da IA
 */
export async function customizeReport(instructions) {
    try {
        const response = await fetch(`${BASE_URL}/chatbot/customize/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(instructions),
        });

        if (!response.ok) {
            throw new Error(`Erro HTTP ${response.status}: ${await response.text()}`);
        }

        return await response.json();
    } catch (error) {
        console.error("❌ Erro ao aplicar personalização no relatório:", error);
        throw error;
    }
}

export async function regeneratePdf() {
    try {
        const response = await fetch(`${BASE_URL}/regenerate-pdf`, {
            method: "POST",
        });

        if (!response.ok) {
            throw new Error(`Erro HTTP ${response.status}: ${await response.text()}`);
        }

        const data = await response.json();
        pdfUrl.set(data.pdf_url); // Atualiza URL global do PDF
        return data.pdf_url;
    } catch (error) {
        console.error("❌ Erro ao regenerar PDF:", error);
        throw error;
    }
}
/**
 * 💾 Exporta o relatório no formato escolhido: txt, html ou pdf
 * @param {'txt' | 'html' | 'pdf'} format
 */
export async function exportReport(format = "txt") {
    try {
        const response = await fetch(`${BASE_URL}/export?format=${format}`, {
            method: "GET",
        });

        if (!response.ok) {
            throw new Error(`Erro HTTP ${response.status}: ${await response.text()}`);
        }

        const data = await response.json();

        // Abrir o arquivo exportado em nova aba
        window.open(`${BASE_URL}${data.report_url}`, "_blank");
        return data.report_url;
    } catch (error) {
        console.error("❌ Erro ao exportar relatório:", error);
        throw error;
    }
}


export async function slitherAnalysis(file, solc_version = 'auto') {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("solc_version", solc_version);

    const res = await fetch("http://localhost:8000/slither", {
        method: "POST",
        body: formData,
    });

    if (!res.ok) throw new Error("Failed to analyze contract");

    const result = await res.json();

    // Atualizar diretamente a store com os dados do backend
    vulnerabilities.set([
        { title: "Critical", value: result.severity_counts.critical, severity: "critical" },
        { title: "High", value: result.severity_counts.high, severity: "high" },
        { title: "Medium", value: result.severity_counts.medium, severity: "medium" },
        { title: "Low", value: result.severity_counts.low, severity: "low" },
        { title: "Unknown", value: result.severity_counts.unknown, severity: "unknown" },
    ]);

    return result;
}

export async function updateReportViaChat(userMessage) {
    try {
      const response = await fetch("http://localhost:8000/chatbot/chat/update-report", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ user_message: userMessage })
      });
  
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Erro ao atualizar relatório via IA.");
      }
  
      const data = await response.json();
      return data;
    } catch (err) {
      console.error("[updateReportViaChat]", err.message);
      throw err;
    }
  }
  