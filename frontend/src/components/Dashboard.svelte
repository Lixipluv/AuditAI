<script>
    import { vulnerabilities } from "../lib/vulnerabilityStore.js";
    import VulnerabilityChart from "./VulnerabilityChart.svelte";
    import SeverityFilter from "./SeverityFilter.svelte";
</script>

<section class="dashboard">
    <div class="dashboard-container">
        <div class="head-title">
            <h1>Vulnerability Dashboard</h1>
        </div>

        <div class="firstRow">
            {#each $vulnerabilities as vuln}
                <div class="card {vuln.severity}">
                    <div class="description">
                        <h2>{vuln.title}</h2>
                        <h3>{vuln.value}</h3>
                    </div>
                </div>
            {/each}
        </div>

        <div class="dashboard-charts">
            <VulnerabilityChart />
            <SeverityFilter />
        </div>
    </div>
</section>
