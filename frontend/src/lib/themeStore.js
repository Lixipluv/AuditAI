import { writable } from "svelte/store";

const isBrowser = typeof window !== "undefined";

const initialTheme = isBrowser && localStorage.getItem("theme") === "dark" ? "dark" : "light";
export const theme = writable(initialTheme);

if (isBrowser) {
  theme.subscribe((value) => {
    document.documentElement.classList.toggle("dark", value === "dark");
    localStorage.setItem("theme", value);
  });
}
