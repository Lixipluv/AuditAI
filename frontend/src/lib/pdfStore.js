import { writable } from "svelte/store";

// Holds the current PDF filename
export const currentPdfFilename = writable("latest_report.pdf");

// Full PDF URL including cache busting
export const pdfUrl = writable(`http://localhost:8000/pdf_reports/latest_report.pdf?t=${Date.now()}`);

// Update function
export function updatePdfUrl(filename) {
  currentPdfFilename.set(filename);
  pdfUrl.set(`http://localhost:8000/pdf_reports/${filename}?t=${Date.now()}`);
}
