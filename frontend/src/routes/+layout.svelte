<script>
    import "../lib/global.scss";
    import Sidebar from "../components/Sidebar.svelte";
    import Navbar from "../components/Navbar.svelte";
    import { isDarkMode } from "../lib/store";
</script>

<div class="app-container" class:dark={$isDarkMode}>
    <Sidebar />
    <section id="content">
        <Navbar />
        <slot />
    </section>
</div>