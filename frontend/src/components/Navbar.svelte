<script>
    import { isSidebarOpen } from "../lib/store";
    import { toggleSidebar } from "../lib/utils";
    import { theme } from "../lib/themeStore.js";
    import { onMount } from "svelte";
  
    // Toggle desativado e ocultado
    /*
    let isDark = false;
  
    onMount(() => {
      if (typeof window !== "undefined") {
        isDark = localStorage.getItem("theme") === "dark";
      }
    });
  
    $: {
      if (typeof document !== "undefined") {
        document.documentElement.classList.toggle("dark", isDark);
      }
    }
  
    function toggleDarkMode() {
      theme.set(isDark ? "light" : "dark");
    }
    */
  </script>
  
  <nav id="navbar">
    <!-- Botão para abrir/fechar Sidebar -->
    <i
      class='bx bx-menu bx-sm'
      role="button"
      tabindex="0"
      on:click={toggleSidebar}
      on:keydown={(e) => e.key === 'Enter' && toggleSidebar()}
      aria-label="Abrir Sidebar"
    ></i>
  
    <!-- Toggle de tema ocultado -->
    <!--
    <div class="nav-actions">
      <input
        type="checkbox"
        class="checkbox"
        id="switch-mode"
        bind:checked={isDark}
        on:change={toggleDarkMode}
        hidden
      />
      <label class="switch-lm" for="switch-mode">
        <i class="bx bxs-moon"></i>
        <i class="bx bx-sun"></i>
        <div class="ball"></div>
      </label>
    </div>
    -->
  </nav>
  
  <style>
  #navbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 56px;
    background: var(--light);
    padding: 0 24px;
    position: sticky;
    top: 0;
    left: 0;
    z-index: 1000;
  }
  
  .nav-actions {
    display: flex;
    align-items: center;
    gap: 20px;
  }
  
  .checkbox {
    display: none;
  }
  
  .switch-lm {
    background-color: var(--grey);
    border-radius: 50px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 3px;
    height: 21px;
    width: 45px;
    position: relative;
    transform: scale(1.3);
    transition: background-color 0.3s;
  }
  
  .switch-lm .ball {
    background-color: var(--blue);
    border-radius: 50%;
    position: absolute;
    top: 2px;
    left: 2px;
    height: 17px;
    width: 17px;
    transform: translateX(0);
    transition: transform 0.25s ease;
  }
  
  .checkbox:checked + .switch-lm .ball {
    transform: translateX(22px);
  }
  
  .bxs-moon {
    color: var(--yellow);
    margin-left: 4px;
    font-size: 14px;
  }
  
  .bx-sun {
    color: var(--orange);
    margin-right: 4px;
    font-size: 14px;
  }
  
  @media screen and (max-width: 768px) {
    #navbar {
      padding: 0 16px;
    }
  
    .nav-actions {
      gap: 10px;
    }
  }
  </style>
  