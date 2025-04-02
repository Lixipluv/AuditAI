// src/lib/customPdfStore.js
import { writable } from "svelte/store";

export const customPdfData = writable(null); // Recebe as instruções ou edições geradas pela IA
