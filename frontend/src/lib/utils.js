import { isSidebarOpen, isDarkMode, showNotificationMenu, showProfileMenu } from './store';

// Exemplo de uso:
export function toggleDarkMode() {
    isDarkMode.update(mode => !mode);
}

// Alternar menus (notificações e perfil)
export function toggleMenu(menu) {
    showNotificationMenu.set(menu === "notifications" ? !$showNotificationMenu : false);
    showProfileMenu.set(menu === "profile" ? !$showProfileMenu : false);
}

// Alternar sidebar
export function toggleSidebar() {
    isSidebarOpen.update(n => !n);
}
