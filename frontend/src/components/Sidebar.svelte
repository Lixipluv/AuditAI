<script>
    import { isSidebarOpen } from "../lib/store";
    import { toggleSidebar } from "../lib/utils";
    
    let activeMenu = "Dashboard";
    
    function setActive(menu) {
        activeMenu = menu;
    }
</script>

<aside id="sidebar" class:hide={!$isSidebarOpen}>
    <div class="brand">
        <i class='bx bxs-network-chart bx-lg'
            role="button"
            tabindex="0"
            on:click={toggleSidebar}
            on:keydown={(e) => e.key === 'Enter' && toggleSidebar()}
            aria-label="Toggle Sidebar">
        </i>

        {#if $isSidebarOpen} 
            <span class="text" role="button" tabindex="0" on:click={() => window.location.href = '/'} 
                  on:keydown={(e) => e.key === 'Enter' && (window.location.href = '/')}>
                AuditAI
            </span>
        {/if}
    </div>
    
    <ul class="side-menu">
        {#each [
            { path: "/analytics", label: "Analytics", icon: "bxs-doughnut-chart" },
            { path: "/chatbot", label: "Chatbot", icon: "bxs-message-dots" },
            { path: "/dashboard", label: "Dashboard", icon: "bxs-dashboard" },
            { path: "/documentation", label: "Documentation", icon: "bxs-book" }
        ] as item}
            <li class:active={activeMenu === item.label}>
                <a href={item.path} on:click={() => setActive(item.label)}>
                    <i class={'bx ' + item.icon}></i>
                    {#if $isSidebarOpen} <span class="text">{item.label}</span> {/if}
                </a>
            </li>
        {/each}
    </ul>
</aside>
