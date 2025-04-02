import { writable } from "svelte/store";

const isBrowser = typeof window !== "undefined";

// Função para criar um store persistente (previne erro no SSR)
function persistentStore(key, initialValue) {
    const store = writable(
        isBrowser ? JSON.parse(localStorage.getItem(key)) ?? initialValue : initialValue
    );

    if (isBrowser) {
        store.subscribe(value => localStorage.setItem(key, JSON.stringify(value)));
    }

    return store;
}

// Sidebar (aberto/fechado)
export const isSidebarOpen = persistentStore("sidebarOpen", true);

// Dark mode persistente
export const isDarkMode = persistentStore("darkMode", false);

// Estados dos menus suspensos
export const showNotificationMenu = writable(false);
export const showProfileMenu = writable(false);

// Estado do Dropzone (Arquivos carregados)
export const uploadedFiles = writable([]);

// Atualiza a classe do body automaticamente (apenas no navegador)
if (isBrowser) {
    isDarkMode.subscribe(value => document.body.classList.toggle("dark", value));
}
// src/lib/store.js

let initialLang = "en";
if (typeof window !== "undefined") {
  initialLang = window.navigator.language?.split("-")[0] || "en";
}
export const currentLanguage = writable(initialLang);
